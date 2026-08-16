import json
import csv

with open("scratch/candidates_full.json") as f:
    full_data = json.load(f)

studies_by_nct = {s["protocolSection"]["identificationModule"]["nctId"]: s for s in full_data["studies"]}

with open("data/candidate_studies.csv", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

uncertains = [r for r in csv_rows if r["preliminary_screening"] == "uncertain"]
print(f"Total uncertains: {len(uncertains)}")

unc_includes = []
unc_excludes = []
unc_truly_uncertain = []

for r in uncertains:
    nct = r["nct_id"]
    s = studies_by_nct.get(nct, {})
    prot = s.get("protocolSection", {})
    
    title = prot.get("identificationModule", {}).get("briefTitle", "")
    summary = prot.get("descriptionModule", {}).get("briefSummary", "")
    conditions = prot.get("conditionsModule", {}).get("conditions", [])
    interventions = [i.get("name", "") + f" ({i.get('type', '')})" for i in prot.get("armsInterventionsModule", {}).get("interventions", [])]
    eligibility = prot.get("eligibilityModule", {}).get("eligibilityCriteria", "")
    
    text = f"{title} {' '.join(conditions)} {' '.join(interventions)} {summary}".lower()
    
    # Check if this study is clearly about GAHT in trans people
    # vs non-trans health studies (e.g. HIV/PrEP with no GAHT focus, cis women IVF, etc.)
    # vs purely non-hormone trans studies (voice, psychotherapy, surgery alone)
    
    is_cis_unrelated = any(k in text for k in ['polycystic ovary', 'endometriosis', 'pcos', 'postmenopausal', 'uterine fibroid', 'contraceptive efficacy', 'ovulation induction', 'assisted reproduction', 'infertility treatment']) and not any(k in text for k in ['transgender', 'gender dysphoria', 'transsexual', 'gender incongruen', 'gender diverse', 'trans woman', 'trans man'])
    
    is_trans_gaht = any(k in text for k in ['transgender', 'transsexual', 'gender diverse', 'gender-diverse', 'gender incongruen', 'gender dysphoria', 'trans woman', 'trans man', 'trans women', 'trans men', 'gender minority']) and any(k in text for k in ['gender-affirming hormone', 'gender affirming hormone', 'cross-sex hormone', 'feminizing hormone', 'masculinizing hormone', 'hormone therapy', 'estradiol', 'testosterone', 'spironolactone', 'cyproterone', 'gaht', 'csht', 'ght'])
    
    if is_cis_unrelated:
        unc_excludes.append((nct, title, "Cisgender/unrelated indication"))
    elif is_trans_gaht:
        unc_includes.append((nct, title, summary[:150]))
    else:
        unc_truly_uncertain.append((nct, title, summary[:150]))

print(f"Uncertains that are likely true GAHT INCLUDES: {len(unc_includes)}")
print(f"Uncertains that are cisgender/unrelated EXCLUDES: {len(unc_excludes)}")
print(f"Uncertains remaining: {len(unc_truly_uncertain)}")

with open("scratch/uncertain_includes.json", "w") as f:
    json.dump(unc_includes, f, indent=2)
