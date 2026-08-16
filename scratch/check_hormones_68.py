import json

with open("scratch/missed_studies_details.json") as f:
    studies = json.load(f)

print(f"Total: {len(studies)}")

for i, s in enumerate(studies):
    text = (s['title'] + " " + s['summary'] + " " + " ".join(s['conditions']) + " " + " ".join(s['interventions']) + " " + s['eligibility']).lower()
    
    # Let's check for any mention of hormone terms
    hormone_mentions = [w for w in ['hormon', 'estrogen', 'estradiol', 'testosterone', 'spironolactone', 'cyproterone', 'bicalutamide', 'finasteride', 'dutasteride', 'progest', 'blocker', 'antiandrogen', 'endocrine', 'cross-sex', 'ght', 'gaht', 'hrt'] if w in text]
    
    print(f"[{i+1}] {s['nct_id']} | {s['title']}")
    print(f"    Hormone mentions: {hormone_mentions}")
    if hormone_mentions:
        print(f"    Interventions: {s['interventions']}")
        print(f"    Summary snippet: {s['summary'][:250]}")
    print("-" * 50)
