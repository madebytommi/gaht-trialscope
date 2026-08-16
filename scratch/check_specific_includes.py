import json

with open("scratch/audit_includes.json") as f:
    includes = {s["nct_id"]: s for s in json.load(f)}

check_ncts = ["NCT06450405", "NCT07092527", "NCT06969326", "NCT06816355", "NCT05469204", "NCT05116293"]

for nct in check_ncts:
    if nct in includes:
        s = includes[nct]
        print(f"=== {nct}: {s['title']} ===")
        print(f"Conditions: {s['conditions']}")
        print(f"Interventions: {s['interventions']}")
        print(f"Summary: {s['summary']}")
        print(f"Eligibility:\n{s['eligibility']}")
        print("="*70 + "\n")
