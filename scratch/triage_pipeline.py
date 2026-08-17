import csv
import json
import re
from pathlib import Path

REVIEW_CSV = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

studies = enriched_data.get("studies", [])

KNOWN_HUMAN_DECISIONS = {
    "NCT00023543": "exclude",
    "NCT00082082": "exclude",
    "NCT00146146": "include",
    "NCT00188708": "exclude",
    "NCT00450749": "exclude",
    "NCT00544882": "exclude",
    "NCT00608400": "exclude",
}

# Regex patterns for TGD terms
TGD_TERMS = [
    r"\btransgender\b", r"\btranssexual\b", r"\btranssexualism\b",
    r"\btrans\s+wom[ae]n\b", r"\btrans\s+m[ae]n\b", r"\btrans\s+female\b", r"\btrans\s+male\b",
    r"\btransfemale\b", r"\btransmale\b",
    r"\btransfeminine\b", r"\btransmasculine\b", r"\bnon-?binary\b",
    r"\bgender[\s-]diverse\b", r"\bgender[\s-]diversity\b",
    r"\bgender[\s-]dysphoria\b", r"\bgender[\s-]dysphoric\b",
    r"\bgender[\s-]identity[\s-]disorder\b", r"\bgid\b",
    r"\bgender[\s-]incongruen\w*\b", r"\bgender[\s-]minority\b", r"\bgender[\s-]minorities\b",
    r"\bgender[\s-]non-?conforming\b", r"\bgender[\s-]variant\b",
    r"\bmtf\b", r"\bftm\b", r"\bmale-to-female\b", r"\bfemale-to-male\b",
    r"\btrans\s+people\b", r"\btrans\s+individuals\b", r"\btrans\s+youth\b",
    r"\btrans\s+adolescents\b", r"\btrans\s+adults\b", r"\btrans\s+patients\b",
    r"\btrans\s+population\b", r"\btrans\s+participants\b"
]
TGD_REGEX = re.compile("|".join(TGD_TERMS), re.IGNORECASE)

# Distinct non-GAHT indication markers (cisgender health, oncology, etc.)
CIS_ONCOLOGY_PATTERNS = [
    r"\bprostate\s+cancer\b", r"\bprostatic\s+neoplasms\b", r"\bprostatic\s+cancer\b",
    r"\bbreast\s+cancer\b", r"\bhepatocellular\s+carcinoma\b",
    r"\bpostmenopause\b", r"\bpostmenopausal\b", r"\bmenopause\b", r"\bmenopausal\b",
    r"\bpolycystic\s+ovary\b", r"\bpcos\b", r"\bendometriosis\b", r"\badenomyosis\b",
    r"\buterine\s+fibroid\b", r"\bovulation\s+induction\b", r"\blabor\s+induction\b",
    r"\binduction\s+of\s+labor\b", r"\bpreterm\s+labor\b", r"\bpre-?eclampsia\b",
    r"\bcontraceptive\s+efficacy\b", r"\bcontraception\b"
]
CIS_ONCOLOGY_REGEX = re.compile("|".join(CIS_ONCOLOGY_PATTERNS), re.IGNORECASE)

# GAHT specific terms
GAHT_SPECIFIC_PATTERNS = [
    r"\bgender[\s-]affirming\s+hormone\b", r"\bgender[\s-]affirming\s+hormone\s+therapy\b",
    r"\bgaht\b", r"\bcsht\b", r"\bght\b",
    r"\bcross[\s-]sex\s+hormone\b", r"\bcross[\s-]sex\s+hormones\b", r"\bcross[\s-]sex\s+hormone\s+therapy\b",
    r"\bfeminizing\s+hormone\b", r"\bmasculinizing\s+hormone\b",
    r"\bfeminizing\s+hormone\s+therapy\b", r"\bmasculinizing\s+hormone\s+therapy\b",
    r"\bfeminizing\s+treatment\b", r"\bmasculinizing\s+treatment\b",
    r"\bfeminizing\s+therapy\b", r"\bmasculinizing\s+therapy\b",
    r"\bhormone\s+affirmation\b", r"\bhormonal\s+affirmation\b"
]
GAHT_SPECIFIC_REGEX = re.compile("|".join(GAHT_SPECIFIC_PATTERNS), re.IGNORECASE)

# General hormone terms
HORMONE_TERMS = [
    r"\bestradiol\b", r"\bestrogen\b", r"\bestrogens\b", r"\btestosterone\b",
    r"\bantiandrogen\b", r"\bantiandrogens\b", r"\banti-androgen\b", r"\banti-androgens\b",
    r"\bspironolactone\b", r"\bcyproterone\b", r"\bbicalutamide\b",
    r"\bfinasteride\b", r"\bdutasteride\b", r"\bprogesterone\b",
    r"\bhormone\s+therapy\b", r"\bhormone\s+replacement\b", r"\bhormonal\s+therapy\b"
]
HORMONE_REGEX = re.compile("|".join(HORMONE_TERMS), re.IGNORECASE)

evaluations = []

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
    
    # Combined texts
    title_text = f"{brief_title} {official_title}"
    cond_text = " ".join(conditions) + " " + " ".join(keywords)
    desc_text = f"{brief_summary} {detailed_description}"
    intr_names = " ".join([i.get("name", "") + " " + i.get("description", "") for i in interventions])
    arm_names = " ".join([a.get("label", "") + " " + a.get("description", "") for a in arm_groups])
    outcome_text = " ".join([o.get("measure", "") + " " + o.get("description", "") for o in primary_outcomes + secondary_outcomes])
    elig_text = f"{eligibility_criteria} {study_population}"
    
    all_text = f"{title_text} {cond_text} {desc_text} {intr_names} {arm_names} {outcome_text} {elig_text}"
    
    # Evaluate Criterion 1 (TGD Population)
    has_tgd_title = bool(TGD_REGEX.search(title_text))
    has_tgd_cond = bool(TGD_REGEX.search(cond_text))
    has_tgd_elig = bool(TGD_REGEX.search(elig_text))
    has_tgd_desc = bool(TGD_REGEX.search(desc_text))
    has_tgd_intr = bool(TGD_REGEX.search(intr_names))
    has_tgd_any = bool(TGD_REGEX.search(all_text))
    
    # Evaluate Criterion 2 (GAHT Role)
    has_gaht_specific = bool(GAHT_SPECIFIC_REGEX.search(all_text))
    has_hormone = bool(HORMONE_REGEX.search(all_text))
    
    evaluations.append({
        "nct_id": nct_id,
        "brief_title": brief_title,
        "conditions": conditions,
        "all_text": all_text,
        "title_text": title_text,
        "cond_text": cond_text,
        "desc_text": desc_text,
        "intr_names": intr_names,
        "elig_text": elig_text,
        "outcome_text": outcome_text,
        "has_tgd_any": has_tgd_any,
        "has_gaht_specific": has_gaht_specific,
        "has_hormone": has_hormone,
        "primary_outcomes": primary_outcomes,
        "interventions": interventions,
        "arm_groups": arm_groups
    })

print(f"Evaluated {len(evaluations)} records.")
print(f"Records with any TGD keyword match: {sum(1 for e in evaluations if e['has_tgd_any'])}")
print(f"Records with specific GAHT phrase match: {sum(1 for e in evaluations if e['has_gaht_specific'])}")
