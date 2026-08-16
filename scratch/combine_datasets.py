import json

with open("data/raw/candidates_raw.json") as f:
    orig_data = json.load(f)
orig_studies = orig_data["studies"]
orig_ncts = {s["protocolSection"]["identificationModule"]["nctId"]: s for s in orig_studies}

with open("scratch/all_new_studies.json") as f:
    new_data = json.load(f)

for nct, val in new_data.items():
    if isinstance(val, list) and len(val) == 2:
        orig_ncts[nct] = val[1]
    else:
        orig_ncts[nct] = val

print(f"Original studies: {len(orig_studies)}")
print(f"Total unique combined studies: {len(orig_ncts)}")

combined_studies = list(orig_ncts.values())

with open("scratch/candidates_full.json", "w") as f:
    json.dump({"studies": combined_studies}, f, indent=2)

print("Saved combined dataset to scratch/candidates_full.json")
