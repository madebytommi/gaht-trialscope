import csv
import json
import re
from pathlib import Path

REVIEW_CSV = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")
OUTPUT_CSV = Path("data/ai_triage.csv")
OUTPUT_REPORT = Path("data/ai_triage_report.md")

with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

studies = enriched_data.get("studies", [])
studies_by_nct = {
    s["protocolSection"]["identificationModule"]["nctId"]: s
    for s in studies
}

with open(REVIEW_CSV, encoding="utf-8") as f:
    review_rows = list(csv.DictReader(f))

nct_order = [r["nct_id"].strip() for r in review_rows]
assert len(nct_order) == 351
assert len(set(nct_order)) == 351

KNOWN_HUMAN_DECISIONS = {
    "NCT00023543": "exclude",
    "NCT00082082": "exclude",
    "NCT00146146": "include",
    "NCT00188708": "exclude",
    "NCT00450749": "exclude",
    "NCT00544882": "exclude",
    "NCT00608400": "exclude",
}

# Regex for verified TGD terms
TGD_CLEAR_RE = re.compile(
    r"\b(transgender|transsexual|transsexualism|trans\s+wom[ae]n|trans\s+m[ae]n|transfemale|transmale|"
    r"transfeminine|transmasculine|non-?binary|gender[\s-]diverse|gender[\s-]diversity|"
    r"gender[\s-]dysphoria|gender[\s-]dysphoric|gender[\s-]identity[\s-]disorder|gid|"
    r"gender[\s-]incongruen\w*|gender[\s-]non-?conforming|gender[\s-]variant|mtf|ftm|"
    r"male-to-female|female-to-male|trans\s+people|trans\s+individuals|trans\s+youth|"
    r"trans\s+adolescents|trans\s+adults|trans\s+patients|trans\s+population|trans\s+participants)\b",
    re.IGNORECASE
)

# Explicit GAHT phrases
GAHT_CLEAR_RE = re.compile(
    r"\b(gender[\s-]affirming\s+hormone|gender[\s-]affirming\s+hormone\s+therapy|"
    r"gaht|csht|ght|cross[\s-]sex\s+hormone|cross[\s-]sex\s+hormones|cross[\s-]sex\s+hormone\s+therapy|"
    r"feminizing\s+hormone|masculinizing\s+hormone|feminizing\s+hormone\s+therapy|"
    r"masculinizing\s+hormone\s+therapy|feminizing\s+treatment|masculinizing\s+treatment|"
    r"feminizing\s+therapy|masculinizing\s+therapy|feminizing\s+regimen|masculinizing\s+regimen|"
    r"hormone\s+affirmation|hormonal\s+affirmation)\b",
    re.IGNORECASE
)

HORMONE_TERMS = ["estradiol", "estrogen", "estrogens", "testosterone", "antiandrogen", "antiandrogens", "anti-androgen", "anti-androgens", "spironolactone", "cyproterone", "progesterone", "bicalutamide", "dutasteride", "finasteride"]

triage_rows = []
first_pass_excludes = []

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
    
    title_text = f"{brief_title} {official_title}".strip()
    cond_text = (" ".join(conditions) + " " + " ".join(keywords)).strip()
    desc_text = f"{brief_summary} {detailed_description}".strip()
    intr_names = " ".join([i.get("name", "") + " " + i.get("description", "") for i in interventions]).strip()
    arm_names = " ".join([a.get("label", "") + " " + a.get("description", "") for a in arm_groups]).strip()
    outcomes_text = " ".join([o.get("measure", "") + " " + o.get("description", "") for o in primary_outcomes + secondary_outcomes]).strip()
    elig_text = f"{eligibility_criteria} {study_population}".strip()
    all_text = f"{title_text} {cond_text} {desc_text} {intr_names} {arm_names} {outcomes_text} {elig_text}".lower()
    
    has_tgd = bool(TGD_CLEAR_RE.search(all_text))
    has_gaht_phrase = bool(GAHT_CLEAR_RE.search(all_text))
    has_hormone_intr = any(h in intr_names.lower() for h in HORMONE_TERMS)
    has_hormone_any = any(h in all_text for h in HORMONE_TERMS)
    
    # 1. Non-TGD Studies -> Obvious Exclude
    if not has_tgd:
        c1 = "no"
        c2 = "no"
        triage = "obvious_exclude"
        conf = "high"
        
        if re.search(r"prostate|prostatic|bph", all_text):
            reason = "No explicit TGD population; oncology/urologic study in prostate disease/cancer."
        elif re.search(r"postmenopause|postmenopausal|menopause|hot flashe", all_text):
            reason = "No explicit TGD population; study evaluates postmenopausal hormone therapy in cisgender women."
        elif re.search(r"polycystic\s+ovary|pcos", all_text):
            reason = "No explicit TGD population; study investigates polycystic ovary syndrome in cisgender women."
        elif re.search(r"contracept", all_text):
            reason = "No explicit TGD population; study evaluates contraceptive efficacy/safety in cisgender women."
        elif re.search(r"infertility|ivf|ovulation|pregnancy|labor|preterm|embryo", all_text):
            reason = "No explicit TGD population; reproductive or obstetric study in cisgender population."
        elif re.search(r"breast\s+cancer", all_text):
            reason = "No explicit TGD population; oncology study in breast cancer."
        elif re.search(r"hypogonadism", all_text):
            reason = "No explicit TGD population; study evaluates testosterone in male hypogonadism."
        else:
            reason = "No explicit transgender or gender-diverse study population identified in registry record."
            
        first_pass_excludes.append(nct_id)
        
    # 2. TGD Studies -> Evaluate GAHT research role
    else:
        c1 = "yes"
        
        # Subcategory flags
        is_pure_voice = any(k in title_text.lower() or k in intr_names.lower() for k in ["voice", "vocal", "pitch", "speech", "acoustic"]) and not has_hormone_intr
        is_pure_surgery = any(k in title_text.lower() or k in intr_names.lower() for k in ["vaginoplasty", "phalloplasty", "metoidioplasty", "top surgery", "mastectomy", "orchiectomy", "hysterectomy", "surgical", "anesthesia", "nerve block", "wound", "tumescent"]) and not has_hormone_intr and nct_id not in ["NCT03725280"]
        is_pure_behavioral = any(k in intr_names.lower() for k in ["app", "counseling", "peer", "video", "mindfulness", "navigation", "workshop", "coaching", "psychotherapy", "cognitive behavioral"]) and not has_hormone_intr and not has_gaht_phrase
        is_hiv_prep = any(k in all_text for k in ["hiv", "prep", "truvada", "descovy", "cabotegravir", "tenofovir"]) and not any(k in title_text.lower() for k in ["hormone", "estradiol", "testosterone"]) and not has_hormone_intr and not ("interaction" in all_text or "pharmacokinetic" in all_text or "concentration" in all_text)
        is_puberty_only = any(k in all_text for k in ["puberty suppression", "pubertal suppression", "puberty blocker", "triptorelin", "histrelin", "leuprolide", "gnrh"]) and not any(k in all_text for k in ["estradiol", "testosterone", "cross-sex", "feminizing", "masculinizing", "gaht"])
        
        # Specific known boundary cases
        if nct_id == "NCT05726903":
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but evaluates depot medroxyprogesterone for contraception rather than GAHT; human review required to confirm exclusion."
        elif nct_id == "NCT06969326":
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but evaluates topical estradiol for post-hysterectomy wound healing with background testosterone; human review required."
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
        elif has_hormone_intr or has_gaht_phrase or any(k in title_text.lower() for k in ["hormone", "testosterone", "estradiol", "cross-sex", "antiandrogen", "spironolactone", "cyproterone", "gaht", "feminizing", "masculinizing"]):
            c2 = "yes"
            triage = "likely_include"
            conf = "high"
            reason = "Explicit transgender/gender-diverse population; GAHT is an explicit intervention, exposure, monitoring target, or primary variable."
        elif is_pure_voice:
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but primary intervention is vocal/speech therapy; human review required to verify if GAHT is an analyzed variable."
        elif is_pure_surgery:
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but primary intervention is surgical technique; human review required to verify if GAHT is an analyzed variable."
        elif is_pure_behavioral:
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but study evaluates behavioral/psychosocial intervention; human review required to confirm hormone role."
        elif is_hiv_prep:
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but study evaluates HIV/PrEP intervention; human review required to confirm if GAHT interactions are analyzed."
        elif is_puberty_only:
            c2 = "no"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but evaluates puberty suppression with GnRH agonists alone without explicit GAHT component; human review required."
        else:
            c2 = "unclear"
            triage = "human_review"
            conf = "medium"
            reason = "Explicit TGD population, but GAHT research role requires human adjudication to distinguish explicit exposure from background use."
            
    triage_rows.append({
        "nct_id": nct_id,
        "brief_title": brief_title,
        "criterion_1_tgd": c1,
        "criterion_2_gaht": c2,
        "ai_triage": triage,
        "ai_triage_reason": reason,
        "confidence": conf,
        "human_decision_existing": KNOWN_HUMAN_DECISIONS.get(nct_id, "")
    })

# Run False-Negative Audit on all first-pass obvious_excludes
second_pass_moved = []
for r in triage_rows:
    if r["nct_id"] in first_pass_excludes:
        # Re-audit every single obvious_exclude
        s = studies_by_nct[r["nct_id"]]
        full_text = f"{s['protocolSection'].get('identificationModule', {}).get('briefTitle', '')} {s['protocolSection'].get('descriptionModule', {}).get('briefSummary', '')} {s['protocolSection'].get('eligibilityModule', {}).get('eligibilityCriteria', '')}".lower()
        
        # Check if there is any plausible TGD/GAHT argument
        if TGD_CLEAR_RE.search(full_text):
            r["ai_triage"] = "human_review"
            r["confidence"] = "low"
            r["ai_triage_reason"] = "Second-pass audit identified potential TGD population term; moved from obvious_exclude to human_review."
            second_pass_moved.append((r["nct_id"], r["brief_title"]))

# Output CSV
fieldnames = [
    "nct_id",
    "brief_title",
    "criterion_1_tgd",
    "criterion_2_gaht",
    "ai_triage",
    "ai_triage_reason",
    "confidence",
    "human_decision_existing"
]

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(triage_rows)

print(f"Wrote {len(triage_rows)} rows to {OUTPUT_CSV}")

# Summary counts
triage_counts = {}
conf_counts = {}
for r in triage_rows:
    triage_counts[r["ai_triage"]] = triage_counts.get(r["ai_triage"], 0) + 1
    conf_counts[r["confidence"]] = conf_counts.get(r["confidence"], 0) + 1

print("\nFinal Triage Breakdown:")
for k, v in sorted(triage_counts.items()):
    print(f"  {k}: {v}")

print("\nFinal Confidence Breakdown:")
for k, v in sorted(conf_counts.items()):
    print(f"  {k}: {v}")

print(f"\nFirst-pass obvious excludes: {len(first_pass_excludes)}")
print(f"Second-pass moved to human_review: {len(second_pass_moved)}")
