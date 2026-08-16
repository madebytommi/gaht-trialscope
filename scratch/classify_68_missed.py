import json

with open("scratch/missed_studies_details.json") as f:
    studies = json.load(f)

print(f"Total studies: {len(studies)}")

includes = []
excludes = []
uncertain = []

for s in studies:
    nct = s["nct_id"]
    title = s["title"]
    cond = s["conditions"]
    intr = s["interventions"]
    summary = s["summary"]
    elig = s["eligibility"]
    text = f"{title} {' '.join(cond)} {' '.join(intr)} {summary} {elig}".lower()
    
    # Check if GAHT is an explicit intervention/exposure/target
    # Look for specific GAHT interventions
    has_gaht_intr = any(k in " ".join(intr).lower() for k in [
        'estradiol', 'estrogen', 'testosterone', 'spironolactone', 'cyproterone', 'bicalutamide', 
        'progesterone', 'hormone', 'cross-sex', 'feminizing', 'masculinizing', 'gaht', 'finasteride', 'dutasteride'
    ])
    
    has_gaht_title = any(k in title.lower() for k in [
        'estradiol', 'estrogen', 'testosterone', 'spironolactone', 'cyproterone', 'bicalutamide', 
        'progesterone', 'hormone', 'cross-sex', 'feminizing', 'masculinizing', 'gaht', 'finasteride', 'dutasteride',
        'gender-affirming hormone', 'gender affirming hormone'
    ])
    
    has_gaht_summary = any(k in summary.lower() for k in [
        'gender-affirming hormone', 'gender affirming hormone', 'cross-sex hormone', 'feminizing hormone', 'masculinizing hormone',
        'estradiol', 'testosterone therapy', 'hormone therapy', 'hormone replacement', 'estrogen therapy', 'cyproterone', 'bicalutamide'
    ])
    
    # Non-hormone interventions
    purely_non_hormone = any(k in title.lower() for k in [
        'phalloplasty', 'surgery', 'vaginoplasty', 'intonation', 'voice training', 'app', 'stigma',
        'erection prosthesis', 'epithesis', 'psychosocial', 'psychological', 'parents\' perspectives',
        'competency program', 'quantum ai', 'kjønnsdysfori'
    ])
    
    if (has_gaht_intr or has_gaht_title) and not purely_non_hormone:
        includes.append(s)
    elif purely_non_hormone:
        excludes.append(s)
    elif has_gaht_summary:
        uncertain.append(s)
    else:
        excludes.append(s)

print(f"Candidate Includes: {len(includes)}")
for inc in includes:
    print(f"[INC] {inc['nct_id']} | Title: {inc['title']} | Intr: {inc['interventions']}")

print(f"\nCandidate Uncertain: {len(uncertain)}")
for unc in uncertain:
    print(f"[UNC] {unc['nct_id']} | Title: {unc['title']} | Intr: {unc['interventions']}")

print(f"\nCandidate Excludes: {len(excludes)}")
for exc in excludes:
    print(f"[EXC] {exc['nct_id']} | Title: {exc['title']}")
