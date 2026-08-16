import json
import csv
import re
from pathlib import Path

# Paths
RAW_FILE = Path("scratch/candidates_full.json")
CSV_FILE = Path("data/candidate_studies.csv")

def extract_nested(d, keys, default=None):
    """Helper to safely extract nested dictionary values."""
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d

def perform_screening(study):
    """
    Perform AI-assisted preliminary screening.
    Returns: (decision, reason)
    decision in ('include', 'exclude', 'uncertain')
    """
    protocol_section = study.get("protocolSection", {})
    
    title = extract_nested(protocol_section, ["identificationModule", "briefTitle"], "").lower()
    conditions = extract_nested(protocol_section, ["conditionsModule", "conditions"], [])
    conditions_text = " ".join(conditions).lower()
    
    interventions = extract_nested(protocol_section, ["armsInterventionsModule", "interventions"], [])
    interventions_text = " ".join([i.get("name", "") for i in interventions]).lower()
    
    eligibility = extract_nested(protocol_section, ["eligibilityModule", "eligibilityCriteria"], "").lower()
    
    summary = extract_nested(protocol_section, ["descriptionModule", "briefSummary"], "").lower()
    
    text = f"{title} {conditions_text} {interventions_text} {summary} {eligibility}"
    
    # Check if this study is clearly about GAHT in trans people
    # vs non-trans health studies (e.g. HIV/PrEP with no GAHT focus, cis women IVF, etc.)
    # vs purely non-hormone trans studies (voice, psychotherapy, surgery alone)
    
    # Is it a completely unrelated condition? (Exclude)
    is_cis_unrelated = any(k in text for k in ['polycystic ovary', 'endometriosis', 'pcos', 'postmenopausal', 'uterine fibroid', 'contraceptive efficacy', 'ovulation induction', 'assisted reproduction', 'infertility treatment']) and not any(k in text for k in ['transgender', 'gender dysphoria', 'transsexual', 'gender incongruen', 'gender diverse', 'trans woman', 'trans man', 'trans women', 'trans men'])
    
    # Does it have both GAHT and a trans population mention?
    has_trans = any(k in text for k in ['transgender', 'transsexual', 'gender diverse', 'gender-diverse', 'gender incongruen', 'gender dysphoria', 'trans woman', 'trans man', 'trans women', 'trans men', 'gender minority']) 
    has_gaht = any(k in text for k in ['gender-affirming hormone', 'gender affirming hormone', 'cross-sex hormone', 'feminizing hormone', 'masculinizing hormone', 'hormone therapy', 'estradiol', 'testosterone', 'spironolactone', 'cyproterone', 'gaht', 'csht', 'ght', 'antiandrogen', 'progesterone', 'estrogen'])
    
    # Are the hormones used for something else completely like prostate cancer/breast cancer?
    has_cancer_exclude = any(k in text for k in ['prostate cancer', 'breast cancer']) and not has_trans
    
    if is_cis_unrelated:
         return "exclude", "Cisgender/unrelated indication"
    if has_cancer_exclude:
         return "exclude", "Oncology indication not related to transgender health"
    
    if has_trans and has_gaht:
         return "include", "Transgender population and GAHT intervention/exposure identified"
    else:
         return "exclude", "Does not explicitly meet both criteria (Trans population + GAHT)"


def process_data():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    studies = data.get("studies", [])
    
    # Deduplicate by NCT ID
    unique_studies = {}
    for s in studies:
        nct_id = extract_nested(s, ["protocolSection", "identificationModule", "nctId"])
        if nct_id and nct_id not in unique_studies:
            unique_studies[nct_id] = s
            
    print(f"Total raw studies: {len(studies)}")
    print(f"Unique studies after deduplication: {len(unique_studies)}")
    
    rows = []
    counts = {"include": 0, "exclude": 0, "uncertain": 0}
    
    for nct_id, study in unique_studies.items():
        protocol = study.get("protocolSection", {})
        
        brief_title = extract_nested(protocol, ["identificationModule", "briefTitle"])
        study_type = extract_nested(protocol, ["designModule", "studyType"])
        overall_status = extract_nested(protocol, ["statusModule", "overallStatus"])
        start_date = extract_nested(protocol, ["statusModule", "startDateStruct", "date"])
        first_post_date = extract_nested(protocol, ["statusModule", "studyFirstPostDateStruct", "date"])
        enrollment = extract_nested(protocol, ["designModule", "enrollmentInfo", "count"])
        lead_sponsor = extract_nested(protocol, ["sponsorCollaboratorsModule", "leadSponsor", "name"])
        
        interventions_list = extract_nested(protocol, ["armsInterventionsModule", "interventions"], [])
        interventions = "; ".join([i.get("name", "") for i in interventions_list if "name" in i])
        
        locations = extract_nested(protocol, ["contactsLocationsModule", "locations"], [])
        countries = set()
        for loc in locations:
            if "country" in loc:
                countries.add(loc["country"])
        countries_str = "; ".join(sorted(list(countries)))
        
        has_results = study.get("hasResults", False)
        
        decision, reason = perform_screening(study)
        counts[decision] += 1
        
        rows.append({
            "nct_id": nct_id,
            "brief_title": brief_title,
            "study_type": study_type,
            "overall_status": overall_status,
            "start_date": start_date,
            "study_first_post_date": first_post_date,
            "enrollment": enrollment,
            "lead_sponsor": lead_sponsor,
            "interventions": interventions,
            "countries": countries_str,
            "has_results": has_results,
            "preliminary_screening": decision,
            "screening_reason": reason
        })
        
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["nct_id", "brief_title", "study_type", "overall_status", "start_date", "study_first_post_date", 
                      "enrollment", "lead_sponsor", "interventions", "countries", "has_results", 
                      "preliminary_screening", "screening_reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            
    print("Screening breakdown:", counts)

if __name__ == "__main__":
    process_data()
