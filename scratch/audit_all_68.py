import json

with open("scratch/missed_studies_details.json") as f:
    studies = json.load(f)

print(f"Total new studies to audit: {len(studies)}\n")

# Let's inspect each study's title, conditions, interventions, summary, and eligibility
for i, s in enumerate(studies):
    nct = s["nct_id"]
    title = s["title"]
    cond = ", ".join(s["conditions"])
    intr = ", ".join(s["interventions"])
    summ = s["summary"]
    elig = s["eligibility"]
    
    print(f"=== STUDY {i+1}: {nct} ===")
    print(f"TITLE: {title}")
    print(f"CONDITIONS: {cond}")
    print(f"INTERVENTIONS: {intr}")
    print(f"SUMMARY: {summ[:300]}...")
    print(f"ELIGIBILITY: {elig[:300]}...")
    print()
