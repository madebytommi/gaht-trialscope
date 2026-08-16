import json

with open("scratch/audit_excludes.json") as f:
    excludes = json.load(f)

print(f"Total excludes: {len(excludes)}\n")

suspect_excludes = []
for i, s in enumerate(excludes):
    nct = s["nct_id"]
    title = s["title"]
    reason = s["screening_reason"]
    cond = " ".join(s["conditions"])
    intr = " ".join(s["interventions"])
    summ = s["summary"]
    elig = s["eligibility"]
    text = f"{title} {cond} {intr} {summ} {elig}".lower()
    
    has_trans = any(k in text for k in ['transgender', 'transsexual', 'gender diverse', 'gender-diverse', 'gender incongruen', 'gender dysphoria', 'trans woman', 'trans man', 'trans women', 'trans men'])
    
    if has_trans:
        suspect_excludes.append((i+1, s))

print(f"Found {len(suspect_excludes)} excludes mentioning transgender/gender diversity:")
for idx, s in suspect_excludes:
    print(f"[{idx}] {s['nct_id']}: {s['title']}")
    print(f"    Heuristic reason: {s['screening_reason']}")
    print(f"    Conditions: {s['conditions']}")
    print(f"    Interventions: {s['interventions']}")
    print(f"    Summary:\n{s['summary']}")
    print(f"    Eligibility:\n{s['eligibility'][:400]}")
    print("="*70)
