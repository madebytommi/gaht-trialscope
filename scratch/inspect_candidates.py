import json

with open("scratch/missed_studies_details.json") as f:
    studies = {s["nct_id"]: s for s in json.load(f)}

check_ncts = ["NCT06939257", "NCT05726903", "NCT05273112", "NCT04265885", "NCT05829928", "NCT07480590", "NCT07194226", "NCT05853120"]

for nct in check_ncts:
    if nct in studies:
        s = studies[nct]
        print(f"=== {nct}: {s['title']} ===")
        print(f"Study Type: {s['study_type']}")
        print(f"Conditions: {s['conditions']}")
        print(f"Interventions: {s['interventions']}")
        print(f"Summary: {s['summary']}")
        print(f"Eligibility: {s['eligibility']}")
        print("="*60 + "\n")
