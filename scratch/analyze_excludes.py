import json

with open("scratch/audit_excludes.json") as f:
    excludes = json.load(f)

with open("scratch/audit_includes.json") as f:
    includes = json.load(f)

print("="*80)
print(f"AUDITING {len(excludes)} EXCLUDES FOR POTENTIAL FALSE NEGATIVES")
print("="*80)

# Let's inspect each exclude
false_negatives = []
true_excludes = []

for idx, item in enumerate(excludes):
    nct = item["nct_id"]
    title = item["title"]
    reason = item["screening_reason"]
    cond = item["conditions"]
    intr = item["interventions"]
    summ = item["summary"]
    elig = item["eligibility"]
    
    # Let's see if this study actually investigated GAHT in trans people despite matching an exclusion trigger!
    print(f"[{idx+1}] {nct}: {title}")
    print(f"    Heuristic Reason: {reason}")
    print(f"    Conditions: {cond}")
    print(f"    Interventions: {intr}")
    print(f"    Summary: {summ[:200]}...")
    print("-" * 60)
