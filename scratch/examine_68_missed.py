import json

with open("scratch/all_new_studies.json") as f:
    new_studies = json.load(f)

print(f"Total new studies loaded: {len(new_studies)}")

analyzed = []
for nct, s in new_studies.items():
    protocol = s.get("protocolSection", {})
    title = protocol.get("identificationModule", {}).get("briefTitle", "")
    summary = protocol.get("descriptionModule", {}).get("briefSummary", "")
    conditions = protocol.get("conditionsModule", {}).get("conditions", [])
    interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
    eligibility = protocol.get("eligibilityModule", {}).get("eligibilityCriteria", "")
    study_type = protocol.get("designModule", {}).get("studyType", "")
    
    intr_names = [i.get("name", "") + " (" + i.get("type", "") + ")" for i in interventions]
    
    analyzed.append({
        "nct_id": nct,
        "title": title,
        "study_type": study_type,
        "conditions": conditions,
        "interventions": intr_names,
        "summary": summary,
        "eligibility": eligibility[:500]
    })

with open("scratch/missed_studies_details.json", "w") as f:
    json.dump(analyzed, f, indent=2)

print("Saved missed_studies_details.json")
