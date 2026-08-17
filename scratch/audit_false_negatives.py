import json
import csv
import re
from pathlib import Path

# Run audit on all obvious_excludes
from build_triage import records_triage, studies_by_nct

print(f"Total records in triage: {len(records_triage)}")

first_pass_excludes = [r for r in records_triage if r["ai_triage"] == "obvious_exclude"]
print(f"First-pass obvious_excludes to audit: {len(first_pass_excludes)}")

audit_results = []
moved_to_human_review = []

# Keywords to check during false negative audit
AUDIT_KEYWORDS = [
    "trans", "gender", "cross-sex", "hormon", "testosteron", "estradiol", "estrogen",
    "antiandrogen", "spironolact", "cyproteron", "progesteron", "dysphor", "incongruen",
    "sex reassign", "transition", "feminiz", "masculiniz", "ftm", "mtf", "gid"
]

for r in first_pass_excludes:
    nct_id = r["nct_id"]
    s = studies_by_nct[nct_id]
    prot = s.get("protocolSection", {})
    ident = prot.get("identificationModule", {})
    cond_mod = prot.get("conditionsModule", {})
    desc_mod = prot.get("descriptionModule", {})
    elig_mod = prot.get("eligibilityModule", {})
    arms_mod = prot.get("armsInterventionsModule", {})
    
    title = ident.get("briefTitle", "")
    official_title = ident.get("officialTitle", "")
    conds = cond_mod.get("conditions", [])
    keywords = cond_mod.get("keywords", [])
    summary = desc_mod.get("briefSummary", "")
    detailed = desc_mod.get("detailedDescription", "")
    elig = elig_mod.get("eligibilityCriteria", "")
    pop = elig_mod.get("studyPopulation", "")
    intrs = [i.get("name", "") + " (" + i.get("description", "") + ")" for i in arms_mod.get("interventions", [])]
    
    text = f"{title} {official_title} {' '.join(conds)} {' '.join(keywords)} {summary} {detailed} {' '.join(intrs)} {elig} {pop}".lower()
    
    # Check if there are any subtle hints of TGD population or GAHT
    hits = [kw for kw in AUDIT_KEYWORDS if kw in text]
    
    # Check specifically for "trans" as a substring that might mean something else (e.g. trans-fat, transcutaneous, transrectal, transvaginal, transplantation, translational)
    # vs actual transgender / transition / transsexual
    trans_words = re.findall(r"\b\w*trans\w*\b", text)
    gender_words = re.findall(r"\b\w*gender\w*\b", text)
    
    # Analyze if there's any plausible TGD/GAHT argument
    # If any true TGD or ambiguous gender minority term appears:
    plausible_tgd = False
    for tw in trans_words:
        if tw in ["transgender", "transsexual", "transsexualism", "trans", "transfemales", "transfemale", "transmales", "transmale", "transfeminine", "transmasculine", "transwomen", "transwoman", "transmen", "transman", "transition", "transitions", "transitioning"]:
            plausible_tgd = True
            break
    for gw in gender_words:
        if gw not in ["gender"]: # just gender alone often means "both genders" or "gender differences" in cis studies
            plausible_tgd = True
            break
            
    audit_results.append({
        "nct_id": nct_id,
        "title": title,
        "conditions": conds,
        "hits": hits,
        "trans_words": list(set(trans_words)),
        "gender_words": list(set(gender_words)),
        "plausible_tgd": plausible_tgd
    })
    
    if plausible_tgd:
        moved_to_human_review.append((nct_id, title, list(set(trans_words)), list(set(gender_words))))

print(f"\nAudit complete. Found {len(moved_to_human_review)} records with plausible TGD terms:")
for m in moved_to_human_review:
    print(f"  {m[0]}: {m[1]} | trans: {m[2]} | gender: {m[3]}")

with open("scratch/first_pass_audit_details.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, indent=2)

print(f"\nSaved {len(audit_results)} audit details to scratch/first_pass_audit_details.json")
