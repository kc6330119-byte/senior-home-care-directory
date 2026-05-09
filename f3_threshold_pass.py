#!/usr/bin/env python3
"""
F3 Step 1 — Apply the "factually rich" 4-of-5 threshold against current Airtable.

Signal redefinition note (2026-05-09): the original five signals included
Licensing (s2) and Accreditation/Year Established (s4). Both fields are
~100% empty in the current Airtable because the Outscraper pipeline only
populates Google-Business-Profile-sourced data; licensing and accreditation
aren't published by Google. The threshold has been redefined to use only
signals that are achievable against current data, so the gate is meaningful
today and not aspirational.

Five signals, redefined:
  1. Description >= 200 chars AND not starting with a templated opening
     (the 6 patterns from enrich_descriptions.py).
  2. >= 2 services.
  3. Phone present.
  4. Website URL present.
  5. Address + Zip both present.

Pass if at least 4 of 5 signals are met. Slugs already in
config.AGENCY_NOINDEX_SLUGS (the 52 LIKELY NOT HOME CARE listings from
F5) are excluded from consideration entirely — they're already noindex.

Outputs:
  - f3_threshold_results.csv  : every record with per-signal scores
  - f3_threshold_failures.csv : the FAILS subset (these become noindex
    pre-regen; many will re-qualify after F3 Step 3 replaces their
    templated descriptions with factual ones).
  - Console: counts + per-signal failure distribution + post-regen estimate.

Re-derive whenever the Airtable data changes meaningfully.
"""
import csv
import os
import re
import sys
from dotenv import load_dotenv
from slugify import slugify

import config

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Agencies")

# Templated-opening patterns from enrich_descriptions.py:OPENINGS +
# OPENINGS_NO_LOCATION. Each pattern is a regex that, if matched against
# the first 200 chars of a description, indicates a templated origin.
TEMPLATED_OPENING_PATTERNS = [
    r"provides professional in-home care services to seniors and families",
    r"^Serving the .+ area,.+offers compassionate in-home care",
    r"is a trusted provider of home care services",
    r"^Families in .+ turn to .+ for reliable, personalized in-home care",
    r"^Based in .+ delivers quality home care services",
    r"brings experienced, compassionate caregivers",
    # No-location variants (less common but possible)
    r"^[A-Z][^.]+ offers compassionate in-home care tailored to each client",
    r"^[A-Z][^.]+ is a trusted provider of home care services, helping seniors",
    r"^Families turn to .+ for reliable, personalized in-home care",
    r"^[A-Z][^.]+ delivers quality home care services designed to help older adults",
    r"^[A-Z][^.]+ brings experienced, compassionate caregivers to seniors in need",
]
TEMPLATED_RE = re.compile("|".join(TEMPLATED_OPENING_PATTERNS), re.IGNORECASE)


def signal_1_description(desc):
    """Description >= 200 chars AND not starting with a templated opening."""
    if not desc:
        return False
    desc = desc.strip()
    if len(desc) < 200:
        return False
    head = desc[:200]
    if TEMPLATED_RE.search(head):
        return False
    return True


def signal_2_services(fields):
    """At least 2 services."""
    val = fields.get("Services", [])
    if isinstance(val, list):
        return len(val) >= 2
    if isinstance(val, str):
        return len([s for s in val.split(",") if s.strip()]) >= 2
    return False


def signal_3_phone(fields):
    """Phone present."""
    val = fields.get("Phone", "")
    return bool(val and str(val).strip())


def signal_4_website(fields):
    """Website URL present."""
    val = fields.get("Website URL", "")
    return bool(val and str(val).strip())


def signal_5_address(fields):
    """Address + Zip both present (real street address)."""
    addr = fields.get("Address", "")
    zip_code = fields.get("Zip", "")
    return bool(addr and str(addr).strip()) and bool(zip_code and str(zip_code).strip())


def score_record(fields):
    """Return (signals_dict, total_passed)."""
    desc = fields.get("Description", "")
    signals = {
        "s1_desc_quality": signal_1_description(desc),
        "s2_services": signal_2_services(fields),
        "s3_phone": signal_3_phone(fields),
        "s4_website": signal_4_website(fields),
        "s5_address": signal_5_address(fields),
    }
    return signals, sum(signals.values())


def main():
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        print("Error: AIRTABLE_API_KEY and AIRTABLE_BASE_ID required in .env")
        sys.exit(1)

    from pyairtable import Api
    import time

    print(f"\n{'='*62}")
    print(f"  F3 Step 1 — Factually-Rich 4-of-5 Threshold")
    print(f"{'='*62}\n")

    api = Api(AIRTABLE_API_KEY)
    table = api.table(AIRTABLE_BASE_ID, TABLE_NAME)

    print("Fetching records from Airtable...")
    records = []
    for page in table.iterate(page_size=100):
        records.extend(page)
        time.sleep(0.2)
    print(f"Fetched {len(records)} records.\n")

    excluded_slugs = config.AGENCY_NOINDEX_SLUGS  # The 52 from F5

    rows = []
    excluded_already = 0
    passes = 0
    fails = 0
    signal_failure_counts = {f"s{i}": 0 for i in range(1, 6)}
    signal_label = {
        "s1": "s1_desc_quality",
        "s2": "s2_licensing",
        "s3": "s3_services",
        "s4": "s4_credentials",
        "s5": "s5_address",
    }

    for r in records:
        fields = r["fields"]
        if fields.get("Status") == "Draft":
            continue

        name = fields.get("Name", "")
        city = fields.get("City", "")
        state = fields.get("State", "")
        slug = (fields.get("Slug") or slugify(f"{name}-{city}")).strip()

        if slug in excluded_slugs:
            excluded_already += 1
            continue

        signals, total = score_record(fields)
        passed = total >= 4

        if passed:
            passes += 1
        else:
            fails += 1
            for sig_key, sig_val in signals.items():
                if not sig_val:
                    short = sig_key.split("_")[0]  # s1, s2, ...
                    signal_failure_counts[short] += 1

        rows.append({
            "id": r["id"],
            "name": name,
            "slug": slug,
            "city": city,
            "state": state,
            "passed": passed,
            "total_signals": total,
            **{k: ("Y" if v else "N") for k, v in signals.items()},
        })

    # Print summary
    print(f"── Results ─────────────────────────────────────────────")
    print(f"  Already noindex (F5 LIKELY NOT HOME CARE): {excluded_already}")
    print(f"  Eligible to score:                         {len(rows)}")
    print(f"  PASS (>= 4 of 5 signals):                  {passes}")
    print(f"  FAIL (< 4 of 5 signals):                   {fails}")
    print()
    print(f"── Signal failure distribution among the {fails} fails ──")
    print(f"  s1 description quality (>=200 chars + non-templated): {signal_failure_counts['s1']} fails")
    print(f"  s2 >= 2 services:                                      {signal_failure_counts['s2']} fails")
    print(f"  s3 phone present:                                      {signal_failure_counts['s3']} fails")
    print(f"  s4 website URL present:                                {signal_failure_counts['s4']} fails")
    print(f"  s5 address + zip both present:                         {signal_failure_counts['s5']} fails")
    print()

    # Final indexable footprint (pre-regen):
    total_indexable = passes
    print(f"── Pre-regen indexable footprint ───────────────────────")
    print(f"  Indexable agencies (pass 4-of-5 today): {total_indexable}")
    print(f"  Already-noindex (F5):                   {excluded_already}")
    print(f"  Newly-noindex (F3 Step 1 fails):        {fails}")
    print(f"  Grand total:                            {total_indexable + excluded_already + fails}")
    print()

    # Estimate post-regen indexable count: simulate the s1 failures getting
    # clean descriptions (i.e., assume s1 will pass for them after F3 Step 3
    # AI regen). Anything that fails s1 only — i.e., s1=N but >=3 of {s2..s5}
    # are Y — re-qualifies post-regen.
    post_regen_addl = 0
    for row in rows:
        if row["passed"]:
            continue
        if row["s1_desc_quality"] == "Y":
            # Already passes s1, can't be helped by description regen.
            continue
        # Count how many of s2..s5 pass.
        other_passes = sum(
            1
            for k in ("s2_services", "s3_phone", "s4_website", "s5_address")
            if row[k] == "Y"
        )
        # Post-regen, s1 flips to Y, so total = other_passes + 1.
        if other_passes + 1 >= 4:
            post_regen_addl += 1

    print(f"── Post-regen estimate (after F3 Step 3 fixes s1 fails) ─")
    print(f"  Currently passing 4-of-5:                             {passes}")
    print(f"  Currently failing only because of s1 (would re-qual): {post_regen_addl}")
    print(f"  Estimated indexable post-regen:                       {passes + post_regen_addl}")
    print(f"  Permanently noindex (fail >=2 signals beyond s1):     {fails - post_regen_addl}")
    print()

    # Write output CSVs
    with open("f3_threshold_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "slug", "city", "state", "passed", "total_signals",
                        "s1_desc_quality", "s2_services", "s3_phone",
                        "s4_website", "s5_address"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in writer.fieldnames})
    print(f"Wrote f3_threshold_results.csv ({len(rows)} rows)")

    fails_rows = [r for r in rows if not r["passed"]]
    with open("f3_threshold_failures.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "slug", "city", "state", "total_signals",
                        "s1_desc_quality", "s2_services", "s3_phone",
                        "s4_website", "s5_address"],
        )
        writer.writeheader()
        for row in fails_rows:
            writer.writerow({k: row[k] for k in writer.fieldnames})
    print(f"Wrote f3_threshold_failures.csv ({len(fails_rows)} rows)")

    # Also write the s1-only-failures bucket: agencies that pass everything
    # except description quality. F3 Step 3 will regenerate descriptions
    # for this group only — smallest API spend that maximally moves the
    # indexable count.
    s1_only = []
    for row in rows:
        if row["passed"]:
            continue
        if row["s1_desc_quality"] == "Y":
            continue
        other_passes = sum(
            1
            for k in ("s2_services", "s3_phone", "s4_website", "s5_address")
            if row[k] == "Y"
        )
        if other_passes >= 3:  # post-regen, +1 for s1, hits 4-of-5
            s1_only.append(row)
    with open("f3_regen_targets.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "name", "slug", "city", "state",
                        "s1_desc_quality", "s2_services", "s3_phone",
                        "s4_website", "s5_address"],
        )
        writer.writeheader()
        for row in s1_only:
            writer.writerow({k: row[k] for k in writer.fieldnames})
    print(f"Wrote f3_regen_targets.csv ({len(s1_only)} rows — F3 Step 3 regen scope)")
    print()


if __name__ == "__main__":
    main()
