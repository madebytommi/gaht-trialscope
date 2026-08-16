import subprocess
import json
import os
from pathlib import Path

existing_raw = "data/raw/candidates_raw.json"
with open(existing_raw) as f:
    data = json.load(f)
existing_ncts = {s["protocolSection"]["identificationModule"]["nctId"] for s in data["studies"]}

test_queries = [
    # Population variations
    '("trans women" OR "trans men" OR "trans woman" OR "trans man") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    '(transfeminine OR transmasculine OR "trans-feminine" OR "trans-masculine") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    '(nonbinary OR "non-binary") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    '("gender dysphoria" OR "gender identity disorder") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    '("gender non-conforming" OR "gender nonconforming") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    # Specific therapy phrases
    '"gender-affirming hormone therapy" OR "gender affirming hormone therapy" OR "gender affirming hormone" OR "gender affirming hormones"',
    '"gender-affirming hormone" OR "gender-affirming hormones"',
    'GAHT',
    '"cross-sex hormone" OR "cross-sex hormones" OR "cross sex hormone" OR "cross sex hormones"',
    '("gender affirmation" OR "gender transition") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)'
]

api_script = "/Users/celtninja/.gemini/config/plugins/science/skills/clinical_trials_database/scripts/clinical_trials_api.py"
uv_bin = os.path.expanduser("~/.local/bin/uv")

results_by_query = {}
all_new_studies = {}

for idx, query in enumerate(test_queries):
    out_file = f"/tmp/test_query_{idx}.json"
    cmd = [
        uv_bin, "run", api_script, "search",
        "--term", query,
        "--fields", "NCTId,BriefTitle,BriefSummary,StudyType,OverallStatus,ArmsInterventionsModule,ConditionsModule,EligibilityModule",
        "--limit", "1000",
        "--count-total",
        "--output", out_file
    ]
    print(f"Running query {idx}: {query}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error on query {idx}: {res.stderr}")
        continue
    
    with open(out_file) as f:
        q_data = json.load(f)
        
    total_count = q_data.get("totalCount", len(q_data.get("studies", [])))
    studies = q_data.get("studies", [])
    new_ncts = []
    for s in studies:
        nct = s.get("protocolSection", {}).get("identificationModule", {}).get("nctId")
        if nct and nct not in existing_ncts:
            new_ncts.append(nct)
            if nct not in all_new_studies:
                all_new_studies[nct] = s
                
    results_by_query[query] = {
        "total_retrieved": len(studies),
        "total_count": total_count,
        "new_nct_count": len(new_ncts),
        "new_ncts": new_ncts
    }
    print(f"  Total: {total_count}, New NCTs not in baseline: {len(new_ncts)}")

print("\n--- Summary of New Studies Found Across All Test Queries ---")
print(f"Total unique new NCTs found: {len(all_new_studies)}")

with open("/tmp/all_new_studies.json", "w") as f:
    json.dump(all_new_studies, f, indent=2)

with open("/tmp/query_results_summary.json", "w") as f:
    json.dump(results_by_query, f, indent=2)
