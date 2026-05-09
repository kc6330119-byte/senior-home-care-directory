#!/usr/bin/env python3
"""
F3 Step 2 — Try to restore original Outscraper descriptions for the 3,179
regen targets BEFORE spending API budget on AI regen.

Source: outscraper_home_care.xlsx (the canonical pipeline export, 11,478
rows). Match by website URL. Quality gates:
  - >= 100 chars
  - <= 500 chars (sane meta-description ceiling)
  - Contains at least one home-care keyword (catches off-topic content)
  - Does NOT match any of the 6 enrich_descriptions.py template patterns
    (defensive — Outscraper data shouldn't have these but guard anyway)
  - Does NOT contain AI-refusal phrases

Description-column priority:
  1. about  (GBP human-written)
  2. company_insights.description  (Outscraper AI-extracted from website)
  3. website_description  (meta description scraped from agency website)

Output:
  - f3_outscraper_restored.json — preview file, NO Airtable write
  - Console: counts (matched / restored / unable)
  - Records that fail the quality gate fall through to F3 Step 3 (Haiku regen)
"""
import csv
import json
import re
import sys
from pathlib import Path

import pandas as pd

EXCEL_PATH = Path("outscraper_home_care.xlsx")
TARGETS_PATH = Path("f3_regen_targets.csv")
OUTPUT_JSON = Path("f3_outscraper_restored.json")
RESIDUAL_CSV = Path("f3_haiku_targets.csv")

DESC_COL_PRIORITY = ["about", "company_insights.description", "website_description"]

# HIGH-SIGNAL multi-word phrases. A description must contain at least one
# of these to pass the quality gate. Single words like "senior", "elderly",
# "medication" are too permissive — a methadone clinic's description matched
# on "medication" alone in an earlier pass and was about to get restored as
# if it were a senior home-care agency. Multi-word phrases catch the actual
# in-home-care semantic context.
HOME_CARE_KEYWORDS = [
    "home care", "homecare",
    "home health", "homehealth",
    "in-home", "in home care",
    "caregiver", "caregiving",
    "senior care", "elder care", "eldercare",
    "companion care", "personal care", "homemaker",
    "respite care", "respite services",
    "live-in", "live in care",
    "post-surgery", "post surgery",
    "veterans care", "veteran care", "va benefits",
    "private duty", "non-medical", "nonmedical",
    "alzheimer's care", "dementia care", "memory care services",
    "hospice care", "palliative care",
    "skilled nursing services",   # in-home skilled nursing, not facility
    "aging in place",
    "household tasks", "activities of daily living", "adl",
]

# enrich_descriptions.py template fragments — defensive.
TEMPLATED_FRAGMENTS = [
    "provides professional in-home care services to seniors and families",
    "offers compassionate in-home care tailored to each client",
    "is a trusted provider of home care services",
    "Families in .+ turn to .+ for reliable, personalized in-home care",
    "delivers quality home care services designed to help older adults",
    "brings experienced, compassionate caregivers",
]
TEMPLATED_RE = re.compile("|".join(TEMPLATED_FRAGMENTS), re.IGNORECASE)

REFUSAL_PATTERNS = [
    r"\bI cannot\b",
    r"\bI can't\b",
    r"\bI'm sorry\b",
    r"\bI'm unable\b",
    r"\bappears incomplete\b",
    r"\binsufficient information\b",
    r"\bdoesn't indicate\b",
    r"\bcannot accurately\b",
]
REFUSAL_RE = re.compile("|".join(REFUSAL_PATTERNS), re.IGNORECASE)


def norm_url(url):
    """Normalize a URL to a bare domain+path key for matching."""
    if not url or str(url).strip().lower() in ("", "nan", "none"):
        return ""
    u = str(url).strip().lower().rstrip("/")
    return re.sub(r"^https?://(www\.)?", "", u)


def description_quality(desc):
    """Return True if a description passes the quality gate."""
    if not desc:
        return False
    desc = str(desc).strip()
    if len(desc) < 100 or len(desc) > 500:
        return False
    lower = desc.lower()
    if not any(kw in lower for kw in HOME_CARE_KEYWORDS):
        return False
    if TEMPLATED_RE.search(desc):
        return False
    if REFUSAL_RE.search(desc):
        return False
    # Skip any obvious null markers
    if "nan" in lower.split() or lower in ("", "n/a", "none"):
        return False
    return True


def build_url_lookup():
    """Read Excel, build {normalized_url: best_description}."""
    print(f"Loading {EXCEL_PATH}...")
    df = pd.read_excel(EXCEL_PATH)
    print(f"  {len(df)} rows.")

    lookup = {}
    by_col_count = {col: 0 for col in DESC_COL_PRIORITY}
    seen_urls = 0

    for _, row in df.iterrows():
        url_key = norm_url(row.get("website", ""))
        if not url_key:
            continue
        seen_urls += 1
        if url_key in lookup:
            continue  # First-seen wins for dupe URLs

        best_desc = None
        best_col = None
        for col in DESC_COL_PRIORITY:
            if col not in df.columns:
                continue
            val = row.get(col, "")
            if pd.isna(val):
                continue
            if description_quality(val):
                best_desc = str(val).strip()
                best_col = col
                break

        if best_desc:
            lookup[url_key] = {"description": best_desc, "source_col": best_col}
            by_col_count[best_col] += 1

    print(f"  {seen_urls} rows had a website URL")
    print(f"  Quality-matched URLs: {len(lookup)}")
    for col, count in by_col_count.items():
        print(f"    via {col}: {count}")
    print()
    return lookup


def main():
    if not EXCEL_PATH.exists():
        print(f"Excel not found at {EXCEL_PATH} — skipping Outscraper restore.")
        # Pass-through: copy targets to residual without restoration
        if TARGETS_PATH.exists():
            with open(TARGETS_PATH) as f, open(RESIDUAL_CSV, "w", newline="") as out:
                out.write(f.read())
            print(f"Copied {TARGETS_PATH} → {RESIDUAL_CSV} unchanged.")
        sys.exit(0)

    if not TARGETS_PATH.exists():
        print(f"Targets file not found at {TARGETS_PATH} — run f3_threshold_pass.py first.")
        sys.exit(1)

    print(f"\n{'='*62}")
    print(f"  F3 Step 2 — Outscraper Restore")
    print(f"{'='*62}\n")

    # Load Airtable target metadata. The targets CSV has slug+name+city+state
    # but no website URL — we need that for matching. Pull it from Airtable.
    import os
    from dotenv import load_dotenv
    from pyairtable import Api
    load_dotenv()
    api = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME", "Agencies"))

    print("Fetching target records from Airtable for website URL lookup...")
    target_ids = set()
    with open(TARGETS_PATH) as f:
        for row in csv.DictReader(f):
            target_ids.add(row["id"])
    print(f"  {len(target_ids)} target IDs to fetch.")

    # Fetch all records, filter to target IDs (faster than per-record fetch).
    target_records = []
    import time
    for page in table.iterate(page_size=100):
        for r in page:
            if r["id"] in target_ids:
                target_records.append(r)
        time.sleep(0.15)
    print(f"  Fetched {len(target_records)} of {len(target_ids)} targets.\n")

    # Build the URL lookup from Excel.
    url_lookup = build_url_lookup()

    # State-name → 2-letter abbreviation for location-mismatch detection.
    STATE_ABBR = {
        "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
        "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
        "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
        "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
        "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
        "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
        "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
        "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
        "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
        "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
        "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
        "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
        "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
    }

    # Major US cities — used to catch cross-city mismatches that don't trip
    # the state filter (e.g., "Chicago's Premier" description served to a
    # Minneapolis listing — both metros, different states, but only "Chicago"
    # appears in the description and IL/Illinois is not mentioned).
    MAJOR_US_CITIES = {
        "new york", "los angeles", "chicago", "houston", "phoenix",
        "philadelphia", "san antonio", "san diego", "dallas", "san jose",
        "austin", "jacksonville", "fort worth", "columbus", "indianapolis",
        "charlotte", "san francisco", "seattle", "denver", "washington",
        "boston", "el paso", "nashville", "detroit", "oklahoma city",
        "portland", "las vegas", "memphis", "louisville", "baltimore",
        "milwaukee", "albuquerque", "tucson", "fresno", "sacramento",
        "mesa", "kansas city", "atlanta", "long beach", "colorado springs",
        "raleigh", "miami", "virginia beach", "omaha", "oakland",
        "minneapolis", "tulsa", "arlington", "tampa", "new orleans",
        "wichita", "cleveland", "bakersfield", "aurora", "anaheim",
        "honolulu", "santa ana", "riverside", "corpus christi", "lexington",
        "stockton", "henderson", "saint paul", "st. paul", "cincinnati",
        "pittsburgh", "greensboro", "anchorage", "plano", "lincoln",
        "orlando", "irvine", "newark", "durham", "chula vista",
        "toledo", "fort wayne", "st. petersburg", "laredo", "jersey city",
        "chandler", "madison", "lubbock", "scottsdale", "reno",
        "buffalo", "gilbert", "glendale", "north las vegas", "winston-salem",
        "chesapeake", "norfolk", "fremont", "garland", "irving",
        "hialeah", "richmond", "boise", "spokane", "baton rouge",
    }

    def location_compatible(desc, city, state):
        """A restored description is location-compatible if it mentions the
        agency's city OR state OR state abbreviation, OR if it doesn't mention
        any conflicting other US state or major US city. The earlier version
        only checked state names and let Chicago/Minneapolis-class within-pair
        mismatches through; this layer adds the major-cities check on top."""
        if not desc:
            return False
        d_lower = desc.lower()
        state_lower = (state or "").strip().lower()
        city_lower = (city or "").strip().lower()
        state_abbr = STATE_ABBR.get(state_lower, "")

        # If agency's state or city or state-abbr is mentioned, compatible.
        agency_state_match = (state_lower and state_lower in d_lower) or \
                             (state_abbr and re.search(r"\b" + state_abbr + r"\b", desc))
        agency_city_match = bool(city_lower and city_lower in d_lower)

        # Conflicting state? Any OTHER US state mentioned by name or abbr.
        for s_name, s_abbr in STATE_ABBR.items():
            if s_name == state_lower:
                continue
            if s_name in d_lower:
                # Conflicting state name found. If agency's own state isn't
                # also mentioned, drop. (Multi-state legitimate descriptions
                # like "serves NY and NJ" pass when agency is in either.)
                if not agency_state_match:
                    return False
            if s_abbr != state_abbr and re.search(r"\b" + s_abbr + r"\b", desc):
                if not agency_state_match:
                    return False

        # Conflicting city? Any major US city mentioned that isn't the agency's.
        for major_city in MAJOR_US_CITIES:
            if major_city == city_lower:
                continue
            if major_city in d_lower:
                # If the agency's city or state isn't also present in the
                # description, the description was written for a different
                # metropolitan area and we drop the restoration.
                if not agency_city_match and not agency_state_match:
                    return False

        return True

    # Match each target by website URL.
    restored = []
    no_url = 0
    no_match = 0
    location_drop = 0

    for r in target_records:
        fields = r["fields"]
        slug = fields.get("Slug", "")
        url = fields.get("Website URL", "")
        city = fields.get("City", "")
        state = fields.get("State", "")
        url_key = norm_url(url)

        if not url_key:
            no_url += 1
            continue

        match = url_lookup.get(url_key)
        if not match:
            no_match += 1
            continue

        if not location_compatible(match["description"], city, state):
            location_drop += 1
            continue

        restored.append({
            "id": r["id"],
            "slug": slug,
            "name": fields.get("Name", ""),
            "city": city,
            "state": state,
            "website": url,
            "old_description": fields.get("Description", ""),
            "new_description": match["description"],
            "source_col": match["source_col"],
        })

    print(f"── F3 Step 2 results ──")
    print(f"  Targets: {len(target_records)}")
    print(f"  Restored from Outscraper: {len(restored)}")
    print(f"  No website URL: {no_url}")
    print(f"  No URL match: {no_match}")
    print(f"  Dropped (location mismatch): {location_drop}")
    print(f"  Need Step 3 (Haiku regen): {len(target_records) - len(restored)}")
    print()

    # Sample 5 restored entries for spot-check.
    if restored:
        print("Sample of 5 restored descriptions:")
        for r in restored[:5]:
            print(f"\n  {r['name']} ({r['city']}, {r['state']})")
            print(f"    website: {r['website']}")
            print(f"    source_col: {r['source_col']}")
            print(f"    old: {r['old_description'][:120]}...")
            print(f"    new: {r['new_description'][:200]}")
        print()

    # Write preview JSON.
    OUTPUT_JSON.write_text(json.dumps(restored, indent=2, ensure_ascii=False))
    print(f"Wrote {OUTPUT_JSON} ({len(restored)} entries — preview only, no Airtable write yet)")

    # Write residual CSV (records that need Step 3 Haiku regen).
    restored_ids = {r["id"] for r in restored}
    with open(TARGETS_PATH) as fin, open(RESIDUAL_CSV, "w", newline="") as fout:
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
        writer.writeheader()
        residual = 0
        for row in reader:
            if row["id"] not in restored_ids:
                writer.writerow(row)
                residual += 1
    print(f"Wrote {RESIDUAL_CSV} ({residual} records → F3 Step 3 Haiku regen scope)")
    print()


if __name__ == "__main__":
    main()
