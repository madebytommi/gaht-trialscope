import json

with open("scratch/audit_excludes.json") as f:
    excludes = json.load(f)

print(f"Total excludes: {len(excludes)}\n")

for i, s in enumerate(excludes):
    nct = s["nct_id"]
    title = s["title"]
    reason = s["screening_reason"]
    cond = ", ".join(s["conditions"])
    intr = ", ".join(s["interventions"])
    summ = s["summary"]
    elig = s["eligibility"]
    
    print(f"[{i+1}] {nct} | {title}")
    print(f"    Reason: {reason}")
    print(f"    Conditions: {cond}")
    print(f"    Interventions: {intr}")
    print(f"    Summary: {summ[:180]}...")
    print("-" * 60)
