import json

with open("scratch/detailed_records.json", encoding="utf-8") as f:
    records = {r["nct_id"]: r for r in json.load(f)}

s = records.get("NCT03528135", {})
print("=== NCT03528135 ===")
print("Title:", s.get("brief_title"))
print("Summary:", s.get("brief_summary"))
print("Eligibility:\n", s.get("eligibility_criteria"))
