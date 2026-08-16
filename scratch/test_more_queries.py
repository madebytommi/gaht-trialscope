import subprocess
import json
import os

existing_raw = "data/raw/candidates_raw.json"
with open(existing_raw) as f:
    data = json.load(f)
existing_ncts = {s["protocolSection"]["identificationModule"]["nctId"] for s in data["studies"]}

# Load new studies from previous run if any
try:
    with open("/tmp/all_new_studies.json") as f:
        all_new_studies = json.load(f)
except Exception:
    all_new_studies = {}

more_queries = [
    # Specific antiandrogens / hormone terms omitted from baseline
    '(transgender OR transsexual OR "gender diverse" OR "gender incongruence" OR "gender dysphoria" OR "trans women" OR "trans men" OR transfeminine OR transmasculine OR nonbinary) AND (cyproterone OR bicalutamide OR finasteride OR dutasteride OR feminizing OR masculinizing OR "gender-affirming" OR "gender affirming" OR "cross-sex" OR "cross sex")',
    
    # Standalone gender-affirming care / hormone phrases
    '"gender affirming care" OR "gender-affirming care"',
    '"gender affirmation treatment" OR "gender-affirming treatment" OR "gender affirmation therapy" OR "gender-affirming therapy"',
    '"feminizing hormone therapy" OR "masculinizing hormone therapy" OR "feminizing hormone" OR "masculinizing hormone" OR "feminizing hormones" OR "masculinizing hormones"',
    '"cross-sex hormone therapy" OR "cross sex hormone therapy"',
    
    # Condition searches
    'AREA[ConditionSearch]"Gender Dysphoria"',
    'AREA[ConditionSearch]"Gender Incongruence"',
    'AREA[ConditionSearch]"Gender Identity Disorder"',
    'AREA[ConditionSearch]"Transgender"',
    
    # Specific drug names + transgender without condition filter
    'transgender AND (bicalutamide OR cyproterone OR dutasteride OR finasteride)',
    'transgender AND (estradiol OR testosterone OR spironolactone OR progesterone)' # Note: baseline had (transgender OR ...) AND (...)
]

api_script = "/Users/celtninja/.gemini/config/plugins/science/skills/clinical_trials_database/scripts/clinical_trials_api.py"
uv_bin = os.path.expanduser("~/.local/bin/uv")

results_by_query = {}

for idx, query in enumerate(more_queries):
    out_file = f"/tmp/test_more_query_{idx}.json"
    cmd = [
        uv_bin, "run", api_script, "search",
        "--term", query,
        "--fields", "NCTId,BriefTitle,BriefSummary,StudyType,OverallStatus,ArmsInterventionsModule,ConditionsModule,EligibilityModule",
        "--limit", "1000",
        "--count-total",
        "--output", out_file
    ]
    print(f"Running more query {idx}: {query}")
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

with open("/tmp/query_more_results_summary.json", "w") as f:
    json.dump(results_by_query, f, indent=2)
