import json
import csv
import re
from pathlib import Path

# Paths
RAW_FILE = Path("data/raw/candidates_raw.json")
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
    
    # Extract text fields
    title = extract_nested(protocol_section, ["identificationModule", "briefTitle"], "").lower()
    conditions = extract_nested(protocol_section, ["conditionsModule", "conditions"], [])
    conditions_text = " ".join(conditions).lower()
    
    interventions = extract_nested(protocol_section, ["armsInterventionsModule", "interventions"], [])
    interventions_text = " ".join([i.get("name", "") for i in interventions]).lower()
    
    eligibility = extract_nested(protocol_section, ["eligibilityModule", "eligibilityCriteria"], "").lower()
    
    all_text = " ".join([title, conditions_text, interventions_text, eligibility])
    
    # Exclusion triggers
    exclusion_keywords = ["prostate cancer", "breast cancer", "menopause", "hypogonadism", "contraception", "fertility treatment", "ivf"]
    for ex in exclusion_keywords:
        if ex in title or ex in conditions_text:
            return "exclude", f"Explicit non-GAHT indication found: {ex}"
            
    if "gnrh" in all_text and "estradiol" not in all_text and "testosterone" not in all_text:
        return "exclude", "Only GnRH mentioned, no explicit GAHT"
        
    # Inclusion triggers
    trans_keywords = ["transgender", "transsexual", "nonbinary", "gender-diverse", "gender diverse", "gender incongruen", "gender dysphoria"]
    hormone_keywords = ["hormone", "estradiol", "estrogen", "testosterone", "antiandrogen", "spironolactone", "progesterone"]
    
    has_trans = any(t in all_text for t in trans_keywords)
    has_hormone = any(h in all_text for h in hormone_keywords)
    
    if has_trans and has_hormone:
        # Check if intervention is specifically hormone
        if any(h in interventions_text for h in hormone_keywords):
             return "include", "Transgender population and GAHT intervention explicitly matched"
        elif any(h in title for h in hormone_keywords):
             return "include", "Transgender population and GAHT mentioned in title"
        
    return "uncertain", "Ambiguous: Requires manual review to confirm both criteria"

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
