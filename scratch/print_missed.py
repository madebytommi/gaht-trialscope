import json

with open("scratch/missed_studies_details.json") as f:
    studies = json.load(f)

print(f"Total studies: {len(studies)}")

for idx, s in enumerate(studies):
    nct = s["nct_id"]
    title = s["title"]
    cond = s["conditions"]
    intr = s["interventions"]
    summary = s["summary"]
    elig = s["eligibility"]
    
    print(f"[{idx+1}] {nct}: {title}")
    print(f"    Conditions: {cond}")
    print(f"    Interventions: {intr}")
    print(f"    Summary snippet: {summary[:200]}...")
    print("-" * 60)
