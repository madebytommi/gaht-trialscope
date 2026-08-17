import json

with open("scratch/detailed_records.json", encoding="utf-8") as f:
    records = json.load(f)

with open("scratch/inspect_candidates_audit.py") as f:
    pass

from inspect_candidates_audit import records_without_true_tgd, records_with_true_tgd

print(f"Total non-TGD: {len(records_without_true_tgd)}")

records_by_nct = {r["nct_id"]: r for r in records}

categorized = {
    "prostate_cancer_bph": [],
    "menopause_hrt": [],
    "pcos_ovarian": [],
    "contraception_pregnancy_infertility": [],
    "general_oncology_endocrine_other": []
}

for nct, title in records_without_true_tgd:
    r = records_by_nct[nct]
    text = r["full_text"].lower()
    
    if any(k in text for k in ["prostate", "prostatic", "bph"]):
        categorized["prostate_cancer_bph"].append((nct, title))
    elif any(k in text for k in ["postmenopausal", "postmenopause", "menopause", "menopausal", "hot flashes"]):
        categorized["menopause_hrt"].append((nct, title))
    elif any(k in text for k in ["pcos", "polycystic ovary", "polycystic ovarian"]):
        categorized["pcos_ovarian"].append((nct, title))
    elif any(k in text for k in ["contraception", "contraceptive", "pregnancy", "infertility", "labor", "preterm", "ovulation", "icsi"]):
        categorized["contraception_pregnancy_infertility"].append((nct, title))
    else:
        categorized["general_oncology_endocrine_other"].append((nct, title))

print("\nBreakdown of 129 non-TGD obvious excludes:")
for cat, items in categorized.items():
    print(f"  {cat}: {len(items)}")

print("\nListing all general_oncology_endocrine_other items:")
for nct, title in categorized["general_oncology_endocrine_other"]:
    r = records_by_nct[nct]
    print(f"  {nct}: {title} | Conds: {r['conditions']}")
