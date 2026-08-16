import json

with open("scratch/missed_studies_details.json") as f:
    studies = {s["nct_id"]: s for s in json.load(f)}

for nct in ["NCT06939257", "NCT05726903", "NCT05273112"]:
    s = studies[nct]
    print(f"=== {nct}: {s['title']} ===")
    print(f"Conditions: {s['conditions']}")
    print(f"Interventions: {s['interventions']}")
    print(f"Summary: {s['summary']}")
    print(f"Eligibility:\n{s['eligibility']}")
    print("="*60 + "\n")
