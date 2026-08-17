import csv

with open("data/screening_review.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in data/screening_review.csv: {len(rows)}")
fieldnames = reader.fieldnames
print(f"Fieldnames: {fieldnames}")

ncts = [r["nct_id"] for r in rows]
unique_ncts = set(ncts)
print(f"Unique NCTs: {len(unique_ncts)}")

# Check human screening fields
human_screenings = [r["human_screening"] for r in rows if r.get("human_screening")]
human_reasons = [r["human_screening_reason"] for r in rows if r.get("human_screening_reason")]
print(f"Non-empty human_screening: {len(human_screenings)}")
print(f"Non-empty human_screening_reason: {len(human_reasons)}")

# Check completeness of other fields in current CSV
for fn in fieldnames:
    non_empty = sum(1 for r in rows if r.get(fn, "").strip() != "")
    print(f"  {fn}: {non_empty} non-empty / {len(rows)}")
