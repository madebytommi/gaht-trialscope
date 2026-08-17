import json
from collections import Counter

with open("scratch/non_tgd_candidates.json", encoding="utf-8") as f:
    non_tgd = json.load(f)

print(f"Total non-TGD candidates: {len(non_tgd)}")

conditions_list = []
for s in non_tgd:
    conds = s.get("conditions", [])
    conditions_list.extend(conds)

cond_counts = Counter(conditions_list)
print("\nTop conditions among non-TGD candidates:")
for c, count in cond_counts.most_common(25):
    print(f"  {c}: {count}")

# Print sample titles
print("\nSample non-TGD titles:")
for s in non_tgd[:20]:
    print(f"  {s['nct_id']}: {s['brief_title']} | Conds: {s['conditions']}")
