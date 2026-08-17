import csv
import json
import re
from pathlib import Path

REVIEW_CSV = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

studies = enriched_data.get("studies", [])

with open(REVIEW_CSV, encoding="utf-8") as f:
    review_rows = list(csv.DictReader(f))

# Verify matching 351 NCT IDs
nct_order = [r["nct_id"].strip() for r in review_rows]
assert len(nct_order) == 351
assert len(set(nct_order)) == 351

studies_by_nct = {
    s["protocolSection"]["identificationModule"]["nctId"]: s
    for s in studies
}
assert set(nct_order) == set(studies_by_nct.keys())

KNOWN_HUMAN_DECISIONS = {
    "NCT00023543": "exclude",
    "NCT00082082": "exclude",
    "NCT00146146": "include",
    "NCT00188708": "exclude",
    "NCT00450749": "exclude",
    "NCT00544882": "exclude",
    "NCT00608400": "exclude",
}

# Regex for clear TGD terms
TGD_CLEAR_RE = re.compile(
    r"\b(transgender|transsexual|transsexualism|trans\s+wom[ae]n|trans\s+m[ae]n|transfemale|transmale|"
    r"transfeminine|transmasculine|non-?binary|gender[\s-]diverse|gender[\s-]diversity|"
    r"gender[\s-]dysphoria|gender[\s-]dysphoric|gender[\s-]identity[\s-]disorder|gid|"
    r"gender[\s-]incongruen\w*|gender[\s-]non-?conforming|gender[\s-]variant|mtf|ftm|"
    r"male-to-female|female-to-male|trans\s+people|trans\s+individuals|trans\s+youth|"
    r"trans\s+adolescents|trans\s+adults|trans\s+patients|trans\s+population|trans\s+participants)\b",
    re.IGNORECASE
)

TGD_AMBIGUOUS_RE = re.compile(
    r"\b(gender\s+minority|gender\s+minorities|gender\s+affirmation|gender-affirming|gender\s+transition)\b",
    re.IGNORECASE
)

# Regex for clear GAHT interventions / exposures / variables
GAHT_CLEAR_RE = re.compile(
    r"\b(gender[\s-]affirming\s+hormone\b|gender[\s-]affirming\s+hormone\s+therapy\b|"
    r"gaht\b|csht\b|ght\b|cross[\s-]sex\s+hormone\b|cross[\s-]sex\s+hormones\b|cross[\s-]sex\s+hormone\s+therapy\b|"
    r"feminizing\s+hormone\b|masculinizing\s+hormone\b|feminizing\s+hormone\s+therapy\b|"
    r"masculinizing\s+hormone\s+therapy\b|feminizing\s+treatment\b|masculinizing\s+treatment\b|"
    r"feminizing\s+therapy\b|masculinizing\s+therapy\b|feminizing\s+regimen\b|masculinizing\s+regimen\b)\b",
    re.IGNORECASE
)

# Specific hormone mentions in TGD context
HORMONE_SPECIFIC_RE = re.compile(
    r"\b(estradiol|estrogen|estrogens|testosterone|antiandrogen|antiandrogens|anti-androgen|anti-androgens|"
    r"spironolactone|cyproterone|bicalutamide|finasteride|dutasteride|progesterone)\b",
    re.IGNORECASE
)

# Excluded indications (when unrelated to TGD)
CIS_INDICATIONS_RE = re.compile(
    r"\b(prostate\s+cancer|prostatic\s+neoplasms|breast\s+cancer|hepatocellular\s+carcinoma|"
    r"postmenopause|postmenopausal|menopause|menopausal|polycystic\s+ovary|pcos|endometriosis|"
    r"adenomyosis|uterine\s+fibroid|ovulation\s+induction|labor\s+induction|induction\s+of\s+labor|"
    r"preterm\s+labor|pre-?eclampsia|hypogonadism|male\s+hypogonadism|male\s+infertility|female\s+infertility|"
    r"contraceptive\s+efficacy|contraception)\b",
    re.IGNORECASE
)

records_triage = []

for nct_id in nct_order:
    s = studies_by_nct[nct_id]
    prot = s.get("protocolSection", {})
    ident = prot.get("identificationModule", {})
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
    
    design_mod = prot.get("designModule", {})
    study_type = design_mod.get("studyType", "")
    
    # Text representations
    title_text = f"{brief_title} {official_title}"
    cond_text = " ".join(conditions) + " " + " ".join(keywords)
    desc_text = f"{brief_summary} {detailed_description}"
    intr_names = " ".join([i.get("name", "") + " " + i.get("description", "") for i in interventions])
    arm_names = " ".join([a.get("label", "") + " " + a.get("description", "") for a in arm_groups])
    outcomes_text = " ".join([o.get("measure", "") + " " + o.get("description", "") for o in primary_outcomes + secondary_outcomes])
    elig_text = f"{eligibility_criteria} {study_population}"
    all_text = f"{title_text} {cond_text} {desc_text} {intr_names} {arm_names} {outcomes_text} {elig_text}"
    
    # Assessment of Criterion 1 (TGD Population)
    has_tgd_clear = bool(TGD_CLEAR_RE.search(all_text))
    has_tgd_ambig = bool(TGD_AMBIGUOUS_RE.search(all_text))
    
    # Assessment of Criterion 2 (GAHT Role)
    has_gaht_clear = bool(GAHT_CLEAR_RE.search(all_text))
    has_hormone = bool(HORMONE_SPECIFIC_RE.search(all_text))
    
    # Let's check indication context
    has_cis_ind = bool(CIS_INDICATIONS_RE.search(cond_text + " " + title_text))
    
    # Individual record evaluation
    c1 = "unclear"
    c2 = "unclear"
    triage = "human_review"
    reason = ""
    conf = "medium"
    
    # 1. Clear non-TGD studies (e.g. cisgender conditions with NO TGD mention)
    if not has_tgd_clear and not has_tgd_ambig:
        c1 = "no"
        c2 = "no"
        triage = "obvious_exclude"
        conf = "high"
        # Determine specific reason
        if re.search(r"prostate|prostatic", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; oncology study in prostate cancer."
        elif re.search(r"postmenopause|postmenopausal|menopause", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; study evaluates postmenopausal hormone therapy in cisgender women."
        elif re.search(r"polycystic\s+ovary|pcos", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; study investigates polycystic ovary syndrome in cisgender women."
        elif re.search(r"contracept", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; study evaluates contraceptive efficacy/safety in cisgender women."
        elif re.search(r"infertility|ivf|ovulation|pregnancy|labor", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; reproductive/obstetric study in cisgender population."
        elif re.search(r"breast\s+cancer", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; oncology study in breast cancer."
        elif re.search(r"hypogonadism", all_text, re.IGNORECASE):
            reason = "No explicit TGD population; study evaluates testosterone in male hypogonadism."
        else:
            reason = "No explicit transgender or gender-diverse study population identified in registry record."
            
    # 2. Studies with TGD population
    elif has_tgd_clear:
        c1 = "yes"
        
        # Check GAHT role
        # Does the study explicitly investigate GAHT?
        # A: Direct GAHT intervention or comparison
        if has_gaht_clear or (has_hormone and any(term in all_text.lower() for term in [
            "start", "initiat", "taking", "naïve", "naive", "cross-sex", "feminizing", "masculinizing",
            "estradiol", "testosterone", "spironolactone", "cyproterone", "progesterone", "hormone therapy",
            "hormone concentration", "pharmacokinetic", "reference interval", "bone mineral", "cardiovascular"
        ])):
            # Let's check if GAHT is just background vs research component
            # Specific exclusion / borderline patterns:
            is_pure_voice = "voice" in all_text.lower() and "pitch" in all_text.lower() and not any(h in intr_names.lower() for h in ["testosterone", "estradiol", "hormone"])
            is_pure_behavioral = any(k in intr_names.lower() for k in ["app", "counseling", "peer navigation", "video", "survey", "questionnaire"]) and not any(k in intr_names.lower() for k in ["estradiol", "testosterone", "spironolactone", "cyproterone", "progesterone"]) and not has_gaht_clear
            is_pure_surgery = any(k in all_text.lower() for k in ["vaginoplasty", "phalloplasty", "metoidioplasty", "top surgery", "mastectomy"]) and not any(k in intr_names.lower() for k in ["estradiol", "testosterone", "spironolactone", "cyproterone", "progesterone"]) and not has_gaht_clear
            is_gnrh_only = "gnrh" in all_text.lower() or "pubert" in all_text.lower() or "triptorelin" in all_text.lower() or "leuprolide" in all_text.lower() or "histrelin" in all_text.lower()
            
            # Check for known boundary cases
            if nct_id == "NCT05726903":
                c2 = "unclear"
                triage = "human_review"
                conf = "medium"
                reason = "Explicit TGD population, but investigates depot medroxyprogesterone for contraception rather than GAHT; human review required."
            elif nct_id == "NCT06969326":
                c2 = "unclear"
                triage = "human_review"
                conf = "medium"
                reason = "Explicit TGD population, but evaluates topical estradiol for post-hysterectomy healing with testosterone as background; human review required."
            elif nct_id == "NCT03725280":
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender male population; compares ovarian tissue before vs after testosterone GAHT exposure in IVF setting."
            elif nct_id == "NCT05891795":
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender/gender-diverse population; investigates acne arising as an adverse effect of masculinizing hormone therapy."
            elif nct_id == "NCT06939257":
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit gender-diverse adult population; explicitly compares pain outcomes in individuals initiating GAHT vs not using GAHT."
            elif nct_id == "NCT05489159":
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender/nonbinary adolescent population; longitudinally evaluates effects of initiating masculinizing or feminizing GAHT."
            elif nct_id == "NCT06247267":
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender population; evaluates cardiovascular changes during transition with estradiol/spironolactone or testosterone GAHT."
            elif has_gaht_clear:
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender/gender-diverse population; GAHT is explicitly investigated as an intervention, exposure, or primary variable."
            elif any(k in intr_names.lower() for k in ["estradiol", "estrogen", "testosterone", "spironolactone", "cyproterone", "progesterone", "bicalutamide", "dutasteride", "finasteride"]):
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender/gender-diverse population; hormone therapy is an explicit study intervention."
            elif any(k in title_text.lower() for k in ["hormone therapy", "testosterone", "estradiol", "cross-sex", "gaht", "feminizing", "masculinizing"]):
                c2 = "yes"
                triage = "likely_include"
                conf = "high"
                reason = "Explicit transgender/gender-diverse population; hormone therapy is explicitly evaluated in relation to study outcomes."
            elif is_pure_voice:
                c2 = "no"
                triage = "human_review"  # biased toward human review
                conf = "medium"
                reason = "Explicit TGD population, but primary intervention is vocal/speech therapy; human review required to confirm if GAHT is an analyzed variable."
            elif is_pure_behavioral:
                c2 = "no"
                triage = "human_review"
                conf = "medium"
                reason = "Explicit TGD population, but study evaluates behavioral/psychosocial intervention; human review required to confirm hormone role."
            elif is_pure_surgery:
                c2 = "no"
                triage = "human_review"
                conf = "medium"
                reason = "Explicit TGD population, but study evaluates surgical technique; human review required to verify if GAHT is an analyzed variable."
            elif is_gnrh_only and not any(h in all_text.lower() for h in ["estradiol", "testosterone"]):
                c2 = "no"
                triage = "human_review"
                conf = "medium"
                reason = "Explicit TGD population, but evaluates puberty suppression with GnRH agonists alone without explicit GAHT component; human review required."
            else:
                # Nuanced case
                c2 = "unclear"
                triage = "human_review"
                conf = "medium"
                reason = "Explicit TGD population, but GAHT research role requires human adjudication to distinguish explicit exposure from background use."
        else:
            # TGD clear, but no explicit GAHT terms found
            c2 = "no"
            triage = "human_review"  # Bias toward human review when TGD is present
            conf = "medium"
            reason = "Explicit TGD population, but no explicit GAHT intervention/exposure identified; human review required to confirm exclusion."
            
    else:
        # Ambiguous TGD terms (e.g. gender minority, gender affirmation)
        c1 = "unclear"
        c2 = "yes" if has_hormone or has_gaht_clear else "unclear"
        triage = "human_review"
        conf = "low"
        reason = "Terminology regarding transgender/gender-diverse population or GAHT role is ambiguous; human review required."
        
    records_triage.append({
        "nct_id": nct_id,
        "brief_title": brief_title,
        "criterion_1_tgd": c1,
        "criterion_2_gaht": c2,
        "ai_triage": triage,
        "ai_triage_reason": reason,
        "confidence": conf,
        "human_decision_existing": KNOWN_HUMAN_DECISIONS.get(nct_id, ""),
        "full_text": all_text
    })

print(f"Completed initial triage for {len(records_triage)} records.")
triage_counts = {}
for r in records_triage:
    triage_counts[r["ai_triage"]] = triage_counts.get(r["ai_triage"], 0) + 1
print(f"Triage counts: {triage_counts}")
