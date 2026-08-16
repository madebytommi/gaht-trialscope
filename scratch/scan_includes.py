import json

with open("scratch/audit_includes.json") as f:
    includes = json.load(f)

print(f"Auditing all {len(includes)} includes:")
for idx, s in enumerate(includes):
    prot = s
    nct = prot["nct_id"]
    title = prot["title"]
    cond = " ".join(prot["conditions"])
    intr = " ".join(prot["interventions"])
    summ = prot["summary"]
    
    # Check if there is any study that might be a false positive
    print(f"{idx+1}. {nct} | {title[:60]} | Cond: {cond[:40]} | Intr: {intr[:40]}")
