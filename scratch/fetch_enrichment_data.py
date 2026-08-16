# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "polite-http",
# ]
# ///

import csv
import json
import os
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from polite_http import http_client

BASE_URL = "https://clinicaltrials.gov/api/v2"
client = http_client.HttpClient(BASE_URL + "/", qps=1.0)

REVIEW_CSV = Path("data/screening_review.csv")
RAW_ENRICHMENT_DIR = Path("data/raw/enrichment")
RAW_ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_JSON = RAW_ENRICHMENT_DIR / "enriched_studies.json"

# 1. Load exact 351 NCT IDs from data/screening_review.csv
with open(REVIEW_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

nct_ids = [r["nct_id"].strip() for r in rows]
unique_nct_ids = sorted(list(set(nct_ids)))
print(f"Target candidate universe: {len(unique_nct_ids)} unique NCT IDs")
if len(unique_nct_ids) != 351:
    raise ValueError(f"Expected 351 NCT IDs, got {len(unique_nct_ids)}")

# 2. Batch fetch via filter.ids in chunks of 50
chunk_size = 50
chunks = [unique_nct_ids[i:i + chunk_size] for i in range(0, len(unique_nct_ids), chunk_size)]

fetched_studies = {}
failures = []
start_time = datetime.now(timezone.utc)

print(f"Fetching in {len(chunks)} chunks of up to {chunk_size}...")

for idx, chunk in enumerate(chunks):
    ids_param = "|".join(chunk)
    url = f"{BASE_URL}/studies?filter.ids={urllib.parse.quote(ids_param)}&pageSize=1000"
    print(f"Chunk {idx+1}/{len(chunks)}: fetching {len(chunk)} IDs...")
    try:
        data = client.fetch_json(url)
        studies = data.get("studies", [])
        for s in studies:
            nct = s.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
            if nct:
                fetched_studies[nct] = s
        print(f"  Received {len(studies)} studies (cumulative: {len(fetched_studies)})")
    except Exception as e:
        print(f"  Error fetching chunk {idx+1}: {e}")

# 3. Check for any missing NCT IDs and fetch individually as fallback
missing = set(unique_nct_ids) - set(fetched_studies.keys())
if missing:
    print(f"Attempting individual fetch for {len(missing)} missing NCT IDs: {sorted(missing)}")
    for nct in sorted(missing):
        url = f"{BASE_URL}/studies/{nct}"
        try:
            study_data = client.fetch_json(url)
            if study_data and "protocolSection" in study_data:
                fetched_studies[nct] = study_data
                print(f"  Successfully fetched individual {nct}")
            else:
                failures.append((nct, "No protocolSection in response"))
        except Exception as e:
            print(f"  Failed to fetch individual {nct}: {e}")
            failures.append((nct, str(e)))

end_time = datetime.now(timezone.utc)

print("\n--- Retrieval Summary ---")
print(f"Requested: {len(unique_nct_ids)}")
print(f"Successfully fetched: {len(fetched_studies)}")
print(f"Failures: {len(failures)}")
print(f"Universe integrity preserved: {set(fetched_studies.keys()) == set(unique_nct_ids)}")

# 4. Save raw enrichment JSON
enrichment_payload = {
    "metadata": {
        "retrieval_start_utc": start_time.isoformat(),
        "retrieval_end_utc": end_time.isoformat(),
        "api_base_url": BASE_URL,
        "method": "ClinicalTrials.gov REST API v2 batch query via filter.ids and individual /studies/{nctId} fallback",
        "total_requested": len(unique_nct_ids),
        "total_fetched": len(fetched_studies),
        "failures": failures
    },
    "studies": [fetched_studies[nct] for nct in unique_nct_ids if nct in fetched_studies]
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(enrichment_payload, f, indent=2)

print(f"Saved raw enrichment data to: {OUTPUT_JSON} ({os.path.getsize(OUTPUT_JSON):,} bytes)")
