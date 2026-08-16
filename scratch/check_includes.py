import json

with open("scratch/audit_includes.json") as f:
    includes = json.load(f)

print(f"Total includes: {len(includes)}\n")

suspect_includes = []
verified_includes = []

for idx, s in enumerate(includes):
    nct = s["nct_id"]
    title = s["title"]
    reason = s["screening_reason"]
    cond = ", ".join(s["conditions"])
    intr = ", ".join(s["interventions"])
    summ = s["summary"]
    elig = s["eligibility"]
    text = f"{title} {cond} {intr} {summ}".lower()
    
    # Check if trans population is actually the STUDY POPULATION (not in exclusion criteria)
    # Check if hormone is actually GAHT (not PCOS, heart failure, cis hypogonadism, etc.)
    print(f"[{idx+1}] {nct}: {title}")
    print(f"    Conditions: {cond}")
    print(f"    Interventions: {intr}")
    print(f"    Summary snippet: {summ[:200]}...")
    print("-" * 60)
