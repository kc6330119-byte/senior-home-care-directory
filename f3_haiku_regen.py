#!/usr/bin/env python3
"""
F3 Step 3 — AI-regenerate descriptions for the residual targets that didn't
get an Outscraper restore.

Inputs: f3_haiku_targets.csv (residual from Step 2)
Output: f3_haiku_responses.json (preview only, no Airtable write)

Design:
  - 4 prompt structures, hash(slug) % 4 picks one:
      bucket 0: lead with services
      bucket 1: lead with location/coverage
      bucket 2: lead with year established / accreditations
      bucket 3: lead with payment options / accessibility
  - Shared blacklist of 9 marketing-template phrases (the enrich_descriptions.py
    fragments + a few near-misses).
  - Defensive: never mention or imply ratings/reviews; never invent.
  - Output target: 100-150 words, 2-3 sentences.

Two structural-variation checks run after generation:
  Check A — first-30-char duplicate rate
    First 30 chars of every description (case-normalized), counted across
    the whole 1,096 set. If any first-30 string appears in >5% of records,
    flag that bucket for regeneration.

  Check B — 5-random-100-char-window collision rate
    For each description, pick 5 deterministic 100-char windows (seed per
    slug). For each prompt bucket, count distinct slugs sharing each
    window-hash. If any window-hash collides on >2% of records in that
    bucket, regenerate that bucket.

Both checks iterate up to 3 times; if still failing, abort and report.

Cost ceiling: $20 hard cap. Re-verify at $15. Haiku 4.5 only.
"""
import csv
import hashlib
import json
import os
import random
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from pyairtable import Api

load_dotenv()

TARGETS_PATH = Path("f3_haiku_targets.csv")
OUTPUT_JSON = Path("f3_haiku_responses.json")
COMBINED_PREVIEW = Path("f3_combined_preview.json")

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 320
TEMPERATURE = 0.85  # More variation than 0.6 — pushes against the closer-template trap
WORKERS = 10

# Cost ceiling
COST_PAUSE_AT = 15.00
COST_HARD_CAP = 20.00

# Pricing (Haiku 4.5)
PRICE_INPUT_PER_MTOK = 1.00
PRICE_OUTPUT_PER_MTOK = 5.00

# Structural-variation thresholds
CHECK_A_THRESHOLD = 0.05  # first-30-char dup rate
CHECK_B_THRESHOLD = 0.02  # 100-char window collision rate per bucket

# Phrases the model is told NEVER to write. Lifted from enrich_descriptions.py
# templates plus a few near-misses, plus closer phrases that emerged in the
# 5-record smoke test (Haiku tends to end with a generic "contact directly"
# closer; we forbid that to break structural similarity in the last ~100
# chars of every description, which is what the window-collision check
# would otherwise flag).
BLACKLISTED_PHRASES = [
    "brings experienced",
    "compassionate caregivers",
    "helps seniors live safely",
    "reach out to",
    "well-regarded",
    "trusted provider",
    "tailored to each",
    "personalized care",
    "professional in-home care",
    "designed to help older adults",
    "thrive in familiar surroundings",
    "supports independence and dignity",
    # Closer-template forbidden phrases — HVD-pattern in the ending
    "contact the agency directly",
    "contact the center directly",
    "for more information",
    "for additional information",
    "should contact",
    "interested individuals",
    "prospective clients",
    "learn more about",
    "feel free to",
    "get in touch",
]

# 4 prompt opening directives
OPENING_DIRECTIVES = [
    "Open the description by stating WHAT SERVICES they provide first.",  # bucket 0
    "Open the description by establishing the GEOGRAPHIC AREA they serve first.",  # bucket 1
    "Open the description with their YEAR ESTABLISHED or ACCREDITATIONS or licensing first; if those aren't provided, lead with the agency's distinguishing fact.",  # bucket 2
    "Open the description with PAYMENT OPTIONS or ACCESSIBILITY (Medicaid, Medicare, VA benefits, private pay).",  # bucket 3
]


def slug_hash(slug):
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest(), 16)


def assign_bucket(slug):
    return slug_hash(slug) % 4


def build_prompt(record, bucket):
    """Build the Haiku user prompt for one record."""
    services = ", ".join(record.get("services", [])[:6]) or "(not specified)"
    care_types = ", ".join(record.get("care_types", [])[:6]) or "(not specified)"
    payment = ", ".join(record.get("payment_options", [])[:6]) or "(not specified)"
    languages = ", ".join(record.get("languages", [])[:5]) or "English"
    year = record.get("year_established", "") or "(not specified)"
    accred = ", ".join(record.get("accreditation", [])[:5]) or "(not specified)"

    blacklist_str = "; ".join(f'"{p}"' for p in BLACKLISTED_PHRASES)

    return f"""Write a 2-3 sentence factual description (100-150 words) for a home care agency directory listing.

{OPENING_DIRECTIVES[bucket]}

AGENCY FACTS:
- Name: {record['name']}
- Location: {record['city']}, {record['state']}
- Services offered: {services}
- Care types: {care_types}
- Payment options accepted: {payment}
- Languages: {languages}
- Year established: {year}
- Accreditation: {accred}

RULES (non-negotiable):
- Output ONLY the description text. No headers, no labels, no quotes, no preamble.
- Length: 100-150 words. Three or four short sentences. NEVER end with a "contact us" / "reach out" / "learn more" closer — end on a substantive factual sentence.
- Be factual. NEVER invent details not in the agency facts above.
- Do NOT mention or imply ratings, reviews, or star scores anywhere.
- Do NOT use any of these phrases (exact or paraphrased): {blacklist_str}.
- If the agency name suggests a non-home-care entity (treatment center, hospital, medical center, clinic, rehab facility), keep the description brief and factual — do NOT claim they provide in-home care unless the services or care-types listed above explicitly say so.
- Use varied sentence structure. Avoid the "Name + verb + city + state" formula in sentence 1.
- Vary your sentence length — mix short and long. Vary which fact you cite first across the description.
- No marketing fluff. No promises. No emotional language. No "your loved one" address.
- If you genuinely have fewer than ~100 words of factual content, write 80-100 instead. NEVER invent filler.
"""


def fetch_target_records():
    """Pull full Airtable records for the residual target IDs."""
    api = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(os.getenv("AIRTABLE_BASE_ID"), os.getenv("AIRTABLE_TABLE_NAME", "Agencies"))

    target_ids = set()
    with open(TARGETS_PATH) as f:
        for row in csv.DictReader(f):
            target_ids.add(row["id"])
    print(f"  {len(target_ids)} target IDs from {TARGETS_PATH}")

    records = []
    for page in table.iterate(page_size=100):
        for r in page:
            if r["id"] not in target_ids:
                continue
            f = r["fields"]
            records.append({
                "id": r["id"],
                "slug": f.get("Slug", ""),
                "name": f.get("Name", ""),
                "city": f.get("City", ""),
                "state": f.get("State", ""),
                "services": _to_list(f.get("Services", [])),
                "care_types": _to_list(f.get("Care Types", [])),
                "payment_options": _to_list(f.get("Payment Options", [])),
                "languages": _to_list(f.get("Languages", [])),
                "year_established": f.get("Year Established", ""),
                "accreditation": _to_list(f.get("Accreditation", [])),
                "old_description": f.get("Description", ""),
                "_bucket": assign_bucket(f.get("Slug", "")),
            })
        time.sleep(0.15)
    print(f"  Fetched {len(records)} of {len(target_ids)} targets.")
    return records


def _to_list(val):
    if isinstance(val, list):
        return val
    if isinstance(val, str) and val.strip():
        return [s.strip() for s in val.split(",") if s.strip()]
    return []


def call_haiku(client, record):
    """One Haiku call. Returns (text, input_tokens, output_tokens)."""
    prompt = build_prompt(record, record["_bucket"])
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        return text, msg.usage.input_tokens, msg.usage.output_tokens
    except anthropic.RateLimitError:
        time.sleep(2)
        msg = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        return text, msg.usage.input_tokens, msg.usage.output_tokens


def regenerate_records(client, records, regen_indices, label):
    """Regenerate descriptions for the listed indices in `records`. Mutates
    in place. Returns (added_input_tokens, added_output_tokens)."""
    print(f"\n  Regenerating {len(regen_indices)} records [{label}]...")
    in_tok = 0
    out_tok = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(call_haiku, client, records[i]): i for i in regen_indices}
        done = 0
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                text, it, ot = fut.result()
                records[i]["new_description"] = text
                in_tok += it
                out_tok += ot
            except Exception as e:
                records[i]["new_description"] = ""
                records[i]["error"] = str(e)
            done += 1
            if done % 100 == 0:
                print(f"    ... {done}/{len(regen_indices)}")
    return in_tok, out_tok


def first_30_check(records):
    """Returns dict of {first_30: count} for all non-empty descriptions."""
    counts = Counter()
    for r in records:
        desc = (r.get("new_description") or "").strip().lower()
        if not desc:
            continue
        first_30 = re.sub(r"\s+", " ", desc[:30])
        counts[first_30] += 1
    return counts


def window_collision_check(records, bucket):
    """For records in the given prompt bucket, collect 5 random 100-char windows
    per record and return Counter of windows → distinct-slug count."""
    bucket_recs = [r for r in records if r["_bucket"] == bucket]
    counts = Counter()
    for r in bucket_recs:
        desc = (r.get("new_description") or "").strip()
        if len(desc) < 100:
            continue
        # Deterministic 5 random windows per slug.
        rng = random.Random(r["slug"])
        max_start = len(desc) - 100
        starts = sorted(set(rng.randint(0, max_start) for _ in range(5)))
        for start in starts:
            window = desc[start:start + 100]
            window_norm = re.sub(r"\s+", " ", window).lower()
            counts[window_norm] += 1
    return counts, bucket_recs


def total_cost(in_tok, out_tok):
    return in_tok / 1_000_000 * PRICE_INPUT_PER_MTOK + out_tok / 1_000_000 * PRICE_OUTPUT_PER_MTOK


def main():
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set in .env")
        sys.exit(1)
    if not TARGETS_PATH.exists():
        print(f"Error: {TARGETS_PATH} not found — run F3 Step 2 first.")
        sys.exit(1)

    print(f"\n{'='*62}")
    print(f"  F3 Step 3 — Haiku Regen ({MODEL})")
    print(f"{'='*62}\n")

    print("Fetching target records from Airtable...")
    records = fetch_target_records()
    # --limit N : truncate for smoke testing
    if "--limit" in sys.argv:
        n = int(sys.argv[sys.argv.index("--limit") + 1])
        records = records[:n]
        print(f"  --limit applied: {len(records)} records")
    print()

    # Bucket distribution
    bucket_counts = Counter(r["_bucket"] for r in records)
    print("Prompt-bucket distribution:")
    for b in range(4):
        print(f"  bucket {b}: {bucket_counts[b]} records")
    print()

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Initial generation pass.
    in_tok, out_tok = regenerate_records(client, records, list(range(len(records))), "initial pass")
    cost = total_cost(in_tok, out_tok)
    print(f"\n  Initial pass complete. Tokens: in={in_tok} out={out_tok}. Cost so far: ${cost:.3f}")

    if cost > COST_PAUSE_AT:
        print(f"\n  COST PAUSE at ${COST_PAUSE_AT}. Re-verify before continuing.")
        OUTPUT_JSON.write_text(json.dumps(records, indent=2, ensure_ascii=False))
        sys.exit(0)

    # Structural-variation iteration
    for iteration in range(1, 4):
        print(f"\n── Structural-variation pass {iteration} ──")

        # Check A: first-30-char duplicate rate (across all records).
        a_counts = first_30_check(records)
        n_records = sum(a_counts.values())
        a_max = max(a_counts.values()) if a_counts else 0
        a_rate = a_max / n_records if n_records else 0
        print(f"  Check A (first-30-char dup rate): max={a_max}/{n_records} = {a_rate:.3%}")
        a_fail = a_rate > CHECK_A_THRESHOLD

        if a_fail:
            top_first_30 = sorted(a_counts.items(), key=lambda kv: -kv[1])[:5]
            for s, c in top_first_30:
                print(f"    [{c}] first-30: {s!r}")

        # Check B: per-bucket 100-char window collision rate.
        bucket_fails = []
        for b in range(4):
            counts, bucket_recs = window_collision_check(records, b)
            if not bucket_recs:
                continue
            max_collision = max(counts.values()) if counts else 0
            rate = max_collision / len(bucket_recs)
            print(f"  Check B (bucket {b}): max collision={max_collision}/{len(bucket_recs)} = {rate:.3%}")
            if rate > CHECK_B_THRESHOLD:
                top_windows = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
                for w, c in top_windows[:1]:
                    print(f"    bucket {b} top window [{c}]: {w[:80]}...")
                bucket_fails.append(b)

        if not a_fail and not bucket_fails:
            print(f"\n  ALL STRUCTURAL CHECKS PASSED at iteration {iteration}.")
            break

        # Identify records to regenerate.
        to_regen = set()

        if a_fail:
            # Regenerate every record sharing a top-N first-30.
            top_keys = {k for k, c in a_counts.items() if c >= max(2, int(CHECK_A_THRESHOLD * n_records))}
            for i, r in enumerate(records):
                desc = (r.get("new_description") or "").strip().lower()
                first_30 = re.sub(r"\s+", " ", desc[:30])
                if first_30 in top_keys:
                    to_regen.add(i)
            print(f"  Check A fail → {len(to_regen)} records flagged for regen")

        for b in bucket_fails:
            counts, bucket_recs = window_collision_check(records, b)
            top_windows = {w for w, c in counts.items() if c >= max(2, int(CHECK_B_THRESHOLD * len(bucket_recs)))}
            bucket_regen = set()
            for r in bucket_recs:
                desc = (r.get("new_description") or "").strip()
                if len(desc) < 100:
                    continue
                rng = random.Random(r["slug"])
                max_start = len(desc) - 100
                starts = sorted(set(rng.randint(0, max_start) for _ in range(5)))
                for start in starts:
                    w = re.sub(r"\s+", " ", desc[start:start + 100]).lower()
                    if w in top_windows:
                        bucket_regen.add(records.index(r))
                        break
            print(f"  Check B bucket {b} fail → {len(bucket_regen)} records flagged for regen")
            to_regen |= bucket_regen

        if not to_regen:
            print(f"  No records to regenerate; aborting.")
            break

        # Reassign buckets for to_regen records: rotate to a different prompt
        # to break the structural pattern. (slug + iteration) % 4.
        for i in to_regen:
            new_b = (slug_hash(records[i]["slug"]) + iteration) % 4
            records[i]["_bucket"] = new_b

        i2, o2 = regenerate_records(client, records, sorted(to_regen), f"variation pass {iteration}")
        in_tok += i2
        out_tok += o2
        cost = total_cost(in_tok, out_tok)
        print(f"  Cost so far: ${cost:.3f}")

        if cost > COST_HARD_CAP:
            print(f"\n  HARD CAP HIT at ${cost:.2f}. Stopping iteration.")
            break
        if cost > COST_PAUSE_AT:
            print(f"\n  COST PAUSE at ${COST_PAUSE_AT}. Stopping iteration.")
            break

    cost = total_cost(in_tok, out_tok)
    print(f"\n── Final stats ──")
    print(f"  Records: {len(records)}")
    print(f"  Successful: {sum(1 for r in records if r.get('new_description'))}")
    print(f"  Errors: {sum(1 for r in records if r.get('error'))}")
    print(f"  Tokens: in={in_tok}  out={out_tok}")
    print(f"  Cost: ${cost:.4f}")

    OUTPUT_JSON.write_text(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"\nWrote {OUTPUT_JSON} — preview only, no Airtable write.")


if __name__ == "__main__":
    main()
