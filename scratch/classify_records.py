import csv
import json
import re
from pathlib import Path

REVIEW_CSV = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

studies = enriched_data.get("studies", [])

# Let's inspect the 7 known human decisions first
KNOWN_HUMAN_DECISIONS = {
    "NCT00023543": "exclude",
    "NCT00082082": "exclude",
    "NCT00146146": "include",
    "NCT00188708": "exclude",
    "NCT00450749": "exclude",
    "NCT00544882": "exclude",
    "NCT00608400": "exclude",
}

# Detailed analysis per study
study_data = []

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
    sex = elig_mod.get("sex", "")
    std_ages = elig_mod.get("stdAges", [])
    
    study_data.append({
        "nct_id": nct_id,
        "brief_title": brief_title,
        "official_title": official_title,
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
        "std_ages": std_ages,
        "study_type": prot.get("designModule", {}).get("studyType", "")
    })

print(f"Total parsed studies: {len(study_data)}")

# Let's inspect non-TGD studies to ensure none have subtle TGD populations
non_tgd_candidates = []
tgd_candidates = []

tgd_regex = re.compile(
    r"\b(transgender|transsexual|transsexualism|trans\s+wom[ae]n|trans\s+m[ae]n|transfemale|transmale|"
    r"transfeminine|transmasculine|non-?binary|gender[\s-]diverse|gender[\s-]diversity|"
    r"gender[\s-]dysphoria|gender[\s-]dysphoric|gender[\s-]identity[\s-]disorder|gid|"
    r"gender[\s-]incongruen\w*|gender[\s-]minority|gender[\s-]minorities|gender[\s-]non-?conforming|"
    r"gender[\s-]variant|mtf|ftm|male-to-female|female-to-male|gender[\s-]affirming|gender[\s-]affirmation|"
    r"gender\s+transition|cross-sex)\b",
    re.IGNORECASE
)

for s in study_data:
    full_text = f"{s['brief_title']} {s['official_title']} {' '.join(s['conditions'])} {' '.join(s['keywords'])} {s['brief_summary']} {s['detailed_description']} {' '.join(i.get('name', '') + ' ' + i.get('description', '') for i in s['interventions'])} {s['eligibility_criteria']} {s['study_population']}"
    if tgd_regex.search(full_text):
        tgd_candidates.append((s, full_text))
    else:
        non_tgd_candidates.append((s, full_text))

print(f"TGD candidates: {len(tgd_candidates)}")
print(f"Non-TGD candidates: {len(non_tgd_candidates)}")

with open("scratch/non_tgd_candidates.json", "w", encoding="utf-8") as f:
    json.dump([{
        "nct_id": s["nct_id"],
        "brief_title": s["brief_title"],
        "conditions": s["conditions"],
        "interventions": [i.get("name") for i in s["interventions"]],
        "eligibility_sample": s["eligibility_criteria"][:300]
    } for s, _ in non_tgd_candidates], f, indent=2)

print("Saved non-TGD candidates to scratch/non_tgd_candidates.json")
