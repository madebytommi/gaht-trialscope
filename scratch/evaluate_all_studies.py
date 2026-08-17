import csv
import json
import re
from pathlib import Path

REVIEW_CSV = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

studies = enriched_data.get("studies", [])
print(f"Loaded {len(studies)} studies from enriched JSON.")

records = []
for s in studies:
    prot = s.get("protocolSection", {})
    ident = prot.get("identificationModule", {})
    nct_id = ident.get("nctId")
    brief_title = ident.get("briefTitle", "")
    official_title = ident.get("officialTitle", "")
    
    status = prot.get("statusModule", {}).get("overallStatus", "")
    design = prot.get("designModule", {})
    study_type = design.get("studyType", "")
    phases = design.get("phases", [])
    
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
    sex = elig_mod.get("sex", "")
    gender_based = elig_mod.get("genderBased", False)
    gender_description = elig_mod.get("genderDescription", "")
    std_ages = elig_mod.get("stdAges", [])
    
    records.append({
        "nct_id": nct_id,
        "brief_title": brief_title,
        "official_title": official_title,
        "study_type": study_type,
        "overall_status": status,
        "conditions": conditions,
        "keywords": keywords,
        "brief_summary": brief_summary,
        "detailed_description": detailed_description,
        "interventions": interventions,
        "arm_groups": arm_groups,
        "primary_outcomes": primary_outcomes,
        "secondary_outcomes": secondary_outcomes,
        "eligibility_criteria": eligibility_criteria,
        "study_population": study_population,
        "sex": sex,
        "gender_based": gender_based,
        "gender_description": gender_description,
        "std_ages": std_ages,
        "has_results": s.get("hasResults", False)
    })

print(f"Parsed {len(records)} study records.")

# Save a quick overview to inspect
with open("scratch/parsed_records_summary.json", "w", encoding="utf-8") as f:
    json.dump([{
        "nct_id": r["nct_id"],
        "brief_title": r["brief_title"],
        "conditions": r["conditions"],
        "interventions": [i.get("name") for i in r["interventions"]],
        "study_type": r["study_type"]
    } for r in records], f, indent=2)

print("Saved summary to scratch/parsed_records_summary.json")
