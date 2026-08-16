import json
import csv

with open("data/candidate_studies.csv", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

includes = [r for r in csv_rows if r["preliminary_screening"] == "include"]
excludes = [r for r in csv_rows if r["preliminary_screening"] == "exclude"]
uncertains = [r for r in csv_rows if r["preliminary_screening"] == "uncertain"]

print("=== GAHT TrialScope Final Corrective Pass Report ===")
print(f"Total Candidate Records: {len(csv_rows)}")
print(f"Includes: {len(includes)}")
print(f"Excludes: {len(excludes)}")
print(f"Uncertains: {len(uncertains)}")

audit_cases = ["NCT06247267", "NCT05489159", "NCT03725280", "NCT06939257", "NCT05726903", "NCT05891795", "NCT06969326"]
print("\n=== Audit Cases ===")
for r in csv_rows:
    if r["nct_id"] in audit_cases:
        print(f"{r['nct_id']}: {r['preliminary_screening'].upper()} - {r['screening_reason']}")
