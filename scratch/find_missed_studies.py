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
    '("gender affirmation" OR "gender transition") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    # Specific antiandrogens & terminology
    '(transgender OR transsexual OR "gender diverse" OR "gender incongruence" OR "gender dysphoria" OR "trans women" OR "trans men" OR transfeminine OR transmasculine OR nonbinary) AND (cyproterone OR bicalutamide OR finasteride OR dutasteride OR feminizing OR masculinizing OR "gender-affirming" OR "gender affirming" OR "cross-sex" OR "cross sex")',
    '"gender affirming care" OR "gender-affirming care"',
    '"gender affirmation treatment" OR "gender-affirming treatment" OR "gender affirmation therapy" OR "gender-affirming therapy"',
    '"feminizing hormone therapy" OR "masculinizing hormone therapy" OR "feminizing hormone" OR "masculinizing hormone" OR "feminizing hormones" OR "masculinizing hormones"',
    'AREA[ConditionSearch]"Gender Dysphoria"',
    'AREA[ConditionSearch]"Gender Incongruence"',
    'transgender AND (bicalutamide OR cyproterone OR dutasteride OR finasteride)'
]

api_script = "/Users/celtninja/.gemini/config/plugins/science/skills/clinical_trials_database/scripts/clinical_trials_api.py"
uv_bin = os.path.expanduser("~/.local/bin/uv")

results_by_query = {}
all_new_studies = {}

for idx, query in enumerate(test_queries):
    out_file = f"scratch/test_query_{idx}.json"
    cmd = [
        uv_bin, "run", api_script, "search",
        "--term", query,
        "--fields", "NCTId,BriefTitle,BriefSummary,StudyType,OverallStatus,ArmsInterventionsModule,ConditionsModule,EligibilityModule,DesignModule",
        "--limit", "1000",
        "--count-total",
        "--output", out_file
    ]
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
                all_new_studies[nct] = (query, s)
                
    results_by_query[query] = {
        "total_retrieved": len(studies),
        "total_count": total_count,
        "new_nct_count": len(new_ncts),
        "new_ncts": new_ncts
    }
    print(f"Query {idx} ({query[:50]}...): Total={total_count}, New={len(new_ncts)}")

print(f"\nTotal unique new NCTs found: {len(all_new_studies)}")

# Save all new studies to scratch
new_studies_dict = {nct: s for nct, (q, s) in all_new_studies.items()}
with open("scratch/all_new_studies.json", "w") as f:
    json.dump(new_studies_dict, f, indent=2)

with open("scratch/query_results_summary.json", "w") as f:
    json.dump(results_by_query, f, indent=2)
