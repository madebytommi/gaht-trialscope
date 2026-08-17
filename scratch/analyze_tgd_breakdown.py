import json
import re
from pathlib import Path

with open("scratch/detailed_records.json", encoding="utf-8") as f:
    records = json.load(f)

with open("scratch/inspect_candidates_audit.py") as f:
    pass

from inspect_candidates_audit import records_with_true_tgd

tgd_ncts = {nct for nct, _, _ in records_with_true_tgd}
records_by_nct = {r["nct_id"]: r for r in records}

print(f"Total verified TGD records: {len(tgd_ncts)}")

# Let's categorize the TGD records:
# 1. Clear GAHT intervention (estradiol, testosterone, antiandrogen, progesterone, etc.)
# 2. Clear GAHT exposure/comparison (trans people on GAHT vs naïve, pre vs post, IM vs SQ, dosing, PK, reference intervals, bone/cardio/brain outcomes of GAHT)
# 3. Nuanced / borderline / requiring human review:
#    - Vocal/speech therapy
#    - Surgical procedures / postoperative care
#    - Behavioral / psychosocial / mobile apps / peer support
#    - Contraception / fertility where GAHT role is subtle
#    - PrEP / HIV studies where GAHT interaction might be measured vs incidental
#    - Puberty suppression with GnRH agonists only

categories = {
    "clear_gaht_interventional": [],
    "clear_gaht_observational_exposure": [],
    "vocal_speech_therapy": [],
    "surgical_technique": [],
    "behavioral_psychosocial": [],
    "hiv_prep_testing": [],
    "contraception_reproduction": [],
    "puberty_suppression_gnrh": [],
    "other_nuanced_tgd": []
}

for nct in tgd_ncts:
    r = records_by_nct[nct]
    text = r["full_text"].lower()
    intrs_text = r["interventions_text"].lower()
    title_text = r["brief_title"].lower()
    summary_text = r["brief_summary"].lower()
    outcomes_text = r["outcomes_text"].lower()
    
    has_hormone_intr = any(h in intrs_text for h in [
        "estradiol", "estrogen", "testosterone", "spironolactone", "cyproterone",
        "progesterone", "bicalutamide", "dutasteride", "finasteride", "cross-sex", "gender affirming hormone", "feminizing hormone", "masculinizing hormone"
    ])
    
    has_gaht_phrase = any(p in text for p in [
        "gender-affirming hormone", "gender affirming hormone", "cross-sex hormone",
        "feminizing hormone", "masculinizing hormone", "gaht", "csht", "ght"
    ])
    
    # Specific subcategory checks
    is_vocal = any(k in title_text or k in intrs_text for k in ["voice", "vocal", "pitch", "speech", "communication therapy", "acoustic"]) and not has_hormone_intr
    is_surgery = any(k in title_text or k in intrs_text for k in ["vaginoplasty", "phalloplasty", "metoidioplasty", "top surgery", "mastectomy", "orchiectomy", "hysterectomy", "surgical", "anesthesia", "nerve block", "wound"]) and not has_hormone_intr and nct not in ["NCT03725280"]
    is_behavioral = any(k in intrs_text for k in ["app", "counseling", "peer", "video", "mindfulness", "navigation", "workshop", "coaching", "psychotherapy", "cognitive behavioral"]) and not has_hormone_intr and not has_gaht_phrase
    is_hiv_prep = any(k in text for k in ["hiv", "prep", "truvada", "descovy", "cabotegravir", "tenofovir", "antiretroviral"]) and not any(k in title_text for k in ["hormone", "estradiol", "testosterone"]) and not has_hormone_intr and not ("interaction" in text or "pharmacokinetic" in text or "concentration" in text)
    is_puberty = any(k in text for k in ["puberty suppression", "pubertal suppression", "puberty blocker", "triptorelin", "histrelin", "leuprolide", "gnrh"]) and not any(k in text for k in ["estradiol", "testosterone", "cross-sex", "feminizing", "masculinizing"])
    
    if is_vocal:
        categories["vocal_speech_therapy"].append((nct, r["brief_title"]))
    elif is_surgery:
        categories["surgical_technique"].append((nct, r["brief_title"]))
    elif is_behavioral:
        categories["behavioral_psychosocial"].append((nct, r["brief_title"]))
    elif is_puberty:
        categories["puberty_suppression_gnrh"].append((nct, r["brief_title"]))
    elif is_hiv_prep:
        categories["hiv_prep_testing"].append((nct, r["brief_title"]))
    elif has_hormone_intr:
        categories["clear_gaht_interventional"].append((nct, r["brief_title"]))
    elif has_gaht_phrase or any(k in title_text for k in ["hormone", "testosterone", "estradiol", "cross-sex", "antiandrogen"]):
        categories["clear_gaht_observational_exposure"].append((nct, r["brief_title"]))
    elif any(k in text for k in ["contracept", "ivf", "fertility", "oophorectomy", "ovarian"]):
        categories["contraception_reproduction"].append((nct, r["brief_title"]))
    else:
        categories["other_nuanced_tgd"].append((nct, r["brief_title"]))

print("\nBreakdown of 222 TGD records by category:")
for cat, items in categories.items():
    print(f"  {cat}: {len(items)}")

with open("scratch/tgd_categories.json", "w", encoding="utf-8") as f:
    json.dump({k: [{"nct_id": n, "title": t} for n, t in v] for k, v in categories.items()}, f, indent=2)

print("\nSaved TGD categories to scratch/tgd_categories.json")
