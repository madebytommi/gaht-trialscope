import json
from pathlib import Path

ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

with open(ENRICHED_JSON, encoding="utf-8") as f:
    data = json.load(f)

studies = data.get("studies", [])
print(f"Total studies in enriched_studies.json: {len(studies)}")

nct_ids = set()
counts = {
    "brief_summary": 0,
    "detailed_description": 0,
    "interventions": 0,
    "intervention_descriptions": 0,
    "eligibility_criteria": 0,
    "study_population": 0,
    "primary_outcomes": 0,
    "secondary_outcomes": 0,
    "official_title": 0,
    "brief_title": 0,
    "arm_groups": 0,
    "enrollment": 0,
    "lead_sponsor": 0,
    "locations": 0,
    "has_results": 0,
}

for s in studies:
    prot = s.get("protocolSection", {})
    ident = prot.get("identificationModule", {})
    nct = ident.get("nctId")
    if nct:
        nct_ids.add(nct)
    
    if ident.get("briefTitle"):
        counts["brief_title"] += 1
    if ident.get("officialTitle"):
        counts["official_title"] += 1
        
    desc = prot.get("descriptionModule", {})
    if desc.get("briefSummary"):
        counts["brief_summary"] += 1
    if desc.get("detailedDescription"):
        counts["detailed_description"] += 1
        
    arms = prot.get("armsInterventionsModule", {})
    intrs = arms.get("interventions", [])
    if intrs:
        counts["interventions"] += 1
        if any(i.get("description") for i in intrs):
            counts["intervention_descriptions"] += 1
    if arms.get("armGroups"):
        counts["arm_groups"] += 1
        
    elig = prot.get("eligibilityModule", {})
    if elig.get("eligibilityCriteria"):
        counts["eligibility_criteria"] += 1
    if elig.get("studyPopulation"):
        counts["study_population"] += 1
        
    outcomes = prot.get("outcomesModule", {})
    if outcomes.get("primaryOutcomes"):
        counts["primary_outcomes"] += 1
    if outcomes.get("secondaryOutcomes"):
        counts["secondary_outcomes"] += 1
        
    design = prot.get("designModule", {})
    if design.get("enrollmentInfo", {}).get("count") is not None:
        counts["enrollment"] += 1
        
    sponsor = prot.get("sponsorCollaboratorsModule", {})
    if sponsor.get("leadSponsor", {}).get("name"):
        counts["lead_sponsor"] += 1
        
    locs = prot.get("contactsLocationsModule", {})
    if locs.get("locations"):
        counts["locations"] += 1
        
    if s.get("hasResults"):
        counts["has_results"] += 1

print(f"Unique NCT IDs: {len(nct_ids)}")
print("\nField Coverage Summary (out of 351 records):")
for k, v in counts.items():
    print(f"  {k}: {v}/{len(studies)} ({v/len(studies):.1%})")
