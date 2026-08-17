import json
import re

with open("data/raw/enrichment/enriched_studies.json", encoding="utf-8") as f:
    enriched_data = json.load(f)

studies = enriched_data.get("studies", [])

# Let's inspect each study's details
results = []

for s in studies:
    prot = s.get("protocolSection", {})
    ident = prot.get("identificationModule", {})
    nct_id = ident.get("nctId")
    brief_title = ident.get("briefTitle", "")
    official_title = ident.get("officialTitle", "")
    
    cond_mod = prot.get("conditionsModule", {})
    conditions = cond_mod.get("conditions", [])
    keywords = cond_mod.get("keywords", [])
    
    desc_mod = prot.get("descriptionModule", {})
    brief_summary = desc_mod.get("briefSummary", "")
    detailed_description = desc_mod.get("detailedDescription", "")
    
    arms_mod = prot.get("armsInterventionsModule", {})
    interventions = arms_mod.get("interventions", [])
    arm_groups = arms_mod.get("armGroups", [])
    
    outcomes_mod = prot.get("outcomesModule", {})
    primary_outcomes = outcomes_mod.get("primaryOutcomes", [])
    secondary_outcomes = outcomes_mod.get("secondaryOutcomes", [])
    
    elig_mod = prot.get("eligibilityModule", {})
    eligibility_criteria = elig_mod.get("eligibilityCriteria", "")
    study_population = elig_mod.get("studyPopulation", "")
    
    intrs_text = "; ".join([f"{i.get('type')}: {i.get('name')} ({i.get('description', '')})" for i in interventions])
    arms_text = "; ".join([f"{a.get('label')}: {a.get('description', '')}" for a in arm_groups])
    outcomes_text = "; ".join([f"{o.get('measure')} (Time: {o.get('timeFrame', '')}) - {o.get('description', '')}" for o in primary_outcomes])
    
    full_text = f"{brief_title} {official_title} {' '.join(conditions)} {' '.join(keywords)} {brief_summary} {detailed_description} {intrs_text} {arms_text} {outcomes_text} {eligibility_criteria} {study_population}".lower()
    
    results.append({
        "nct_id": nct_id,
        "brief_title": brief_title,
        "conditions": conditions,
        "interventions_text": intrs_text,
        "arms_text": arms_text,
        "outcomes_text": outcomes_text,
        "brief_summary": brief_summary,
        "eligibility_criteria": eligibility_criteria,
        "full_text": full_text
    })

# Save for detailed rule evaluation
with open("scratch/detailed_records.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} detailed records to scratch/detailed_records.json")
