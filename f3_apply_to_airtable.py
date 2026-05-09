#!/usr/bin/env python3
"""
F3 apply — write the combined preview's new descriptions back to Airtable.

Source: f3_combined_preview.json (Outscraper restored + Haiku regenerated)
Destination: Airtable Agencies table, "Description" field.

Pre-write filters:
  - Drop any record whose slug is now in config.AGENCY_NOINDEX_SLUGS
    (defensive — should already be filtered by build steps).
  - Strip "_x000D_" carriage-return artifacts from any restored description.

Writes in batches of 10. Reports progress + total errors.
"""
import json
import os
import sys
import time
from dotenv import load_dotenv
from pyairtable import Api

import config

load_dotenv()

PREVIEW_PATH = "f3_combined_preview.json"
BATCH_SIZE = 10


def clean_description(desc):
    """Strip Excel artifacts and normalize whitespace."""
    if not desc:
        return desc
    # _x000D_ is a literal sequence Excel emits for embedded carriage returns
    desc = desc.replace("_x000D_", "").replace("_X000D_", "")
    # Collapse runs of 3+ newlines/spaces
    import re
    desc = re.sub(r"\s+", " ", desc).strip()
    return desc


def main():
    if not os.getenv("AIRTABLE_API_KEY") or not os.getenv("AIRTABLE_BASE_ID"):
        print("Error: AIRTABLE_API_KEY and AIRTABLE_BASE_ID required in .env")
        sys.exit(1)

    print(f"\n{'='*62}")
    print(f"  F3 Apply — write descriptions to Airtable")
    print(f"{'='*62}\n")

    with open(PREVIEW_PATH) as f:
        records = json.load(f)
    print(f"Loaded {len(records)} records from {PREVIEW_PATH}")

    # Drop now-noindexed records (defensive)
    before = len(records)
    records = [r for r in records if r["slug"] not in config.AGENCY_NOINDEX_SLUGS]
    dropped = before - len(records)
    if dropped:
        print(f"  Dropped {dropped} records now in AGENCY_NOINDEX_SLUGS")
    print(f"  Final apply-set: {len(records)}")
    print()

    # Build update batches.
    updates = []
    artifact_cleaned = 0
    for r in records:
        new_desc = r.get("new_description", "")
        cleaned = clean_description(new_desc)
        if cleaned != new_desc:
            artifact_cleaned += 1
        if not cleaned:
            continue  # skip empty
        updates.append({"id": r["id"], "fields": {"Description": cleaned}})

    if artifact_cleaned:
        print(f"  Stripped Excel/whitespace artifacts from {artifact_cleaned} descriptions")
    print(f"  Ready to write: {len(updates)} updates")
    print()

    api = Api(os.getenv("AIRTABLE_API_KEY"))
    table = api.table(os.getenv("AIRTABLE_BASE_ID"),
                      os.getenv("AIRTABLE_TABLE_NAME", "Agencies"))

    written = 0
    errors = []
    print("Writing to Airtable...")
    for i in range(0, len(updates), BATCH_SIZE):
        batch = updates[i:i + BATCH_SIZE]
        try:
            table.batch_update(batch)
            written += len(batch)
        except Exception as e:
            errors.append((i, str(e)))
            print(f"  [{i}] ERROR: {e}")
        if (i // BATCH_SIZE) % 20 == 0:  # progress every 200 records
            print(f"  ... {min(i + BATCH_SIZE, len(updates))}/{len(updates)}")
        time.sleep(0.05)  # gentle throttle

    print()
    print(f"{'='*62}")
    print(f"  F3 APPLY COMPLETE")
    print(f"{'='*62}")
    print(f"  Records written:    {written}")
    print(f"  Batch errors:       {len(errors)}")
    print(f"  Final agencies w/ updated descriptions: {written}")
    if errors:
        print(f"\nFirst 5 batch errors:")
        for idx, err in errors[:5]:
            print(f"  batch starting at {idx}: {err}")


if __name__ == "__main__":
    main()
