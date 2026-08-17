# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "polite-http",
# ]
# ///

import urllib.parse
import json
import sys
import time
from polite_http import http_client

BASE_URL = "https://clinicaltrials.gov/api/v2"
client = http_client.HttpClient(BASE_URL + "/", qps=1.0)

# Test 1: Single study with all protocol modules / full study
test_nct = "NCT00023543"
url_single = f"{BASE_URL}/studies/{test_nct}"
print(f"Fetching single study: {url_single}")
data_single = client.fetch_json(url_single)
print(f"Keys in single study response: {list(data_single.keys())}")
if "protocolSection" in data_single:
    print(f"Modules in protocolSection: {list(data_single['protocolSection'].keys())}")

# Test 2: Multi-study query with filter.ids
test_ncts = ["NCT00023543", "NCT00082082", "NCT00146146"]
ids_param = "|".join(test_ncts)
url_multi = f"{BASE_URL}/studies?filter.ids={urllib.parse.quote(ids_param)}&pageSize=10"
print(f"\nFetching multi-study query: {url_multi}")
try:
    data_multi = client.fetch_json(url_multi)
    print(f"Multi-study totalCount: {data_multi.get('totalCount')}")
    print(f"Studies returned: {len(data_multi.get('studies', []))}")
    retrieved_ncts = [s['protocolSection']['identificationModule']['nctId'] for s in data_multi.get('studies', [])]
    print(f"Retrieved NCTs: {retrieved_ncts}")
except Exception as e:
    print(f"Multi-study error: {e}")
