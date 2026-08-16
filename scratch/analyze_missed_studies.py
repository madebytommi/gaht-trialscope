import json

with open("/tmp/all_new_studies.json") as f:
    all_new_studies = json.load(f)

print(f"Total new studies collected: {len(all_new_studies)}")

# Let's inspect each new study to see if it meets Inclusion Criteria:
# 1. Transgender/gender-diverse population
# 2. GAHT is explicit intervention, exposure, comparison, monitoring target, pharmacologic variable, or subject of analysis

relevant_missed = []
for nct, s in all_new_studies.items():
    protocol = s.get("protocolSection", {})
    title = protocol.get("identificationModule", {}).get("briefTitle", "")
    summary = protocol.get("descriptionModule", {}).get("briefSummary", "")
    conditions = protocol.get("conditionsModule", {}).get("conditions", [])
    interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
    eligibility = protocol.get("eligibilityModule", {}).get("eligibilityCriteria", "")
    study_type = protocol.get("designModule", {}).get("studyType", "")
    
    intr_names = [i.get("name", "") + " (" + i.get("type", "") + ")" for i in interventions]
    
    text = f"{title} {summary} {' '.join(conditions)} {' '.join(intr_names)} {eligibility}".lower()
    
    # Check if GAHT is explicitly studied / intervened / exposed
    # and population is trans/gender diverse
    relevant_missed.append({
        "nct_id": nct,
        "title": title,
        "study_type": study_type,
        "conditions": conditions,
        "interventions": intr_names,
        "summary": summary[:300] + "..." if len(summary) > 300 else summary,
        "text": text
    })

print(f"Total studies to analyze: {len(relevant_missed)}")

with open("/tmp/new_studies_details.json", "w") as f:
    json.dump(relevant_missed, f, indent=2)
