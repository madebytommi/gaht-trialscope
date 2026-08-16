import csv
import json
import subprocess
from pathlib import Path

REVIEW_FILE = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")
ENRICHED_PROVENANCE = Path("data/raw/enrichment/enrichment_provenance.md")
ORIGINAL_RAW = Path("data/raw/candidates_raw.json")
CORRECTIVE_PROVENANCE = Path("data/raw/corrective_provenance.md")
ORIGINAL_PROVENANCE = Path("data/raw/provenance.md")

print("=== RUNNING FULL VALIDATION OF ENRICHMENT PASS ===")

# 1. Check raw files exist and untouched
assert ORIGINAL_RAW.exists(), "Original raw candidates file missing!"
assert ORIGINAL_PROVENANCE.exists(), "Original provenance file missing!"
assert CORRECTIVE_PROVENANCE.exists(), "Corrective provenance file missing!"
assert ENRICHED_JSON.exists(), "Enriched JSON missing!"
assert ENRICHED_PROVENANCE.exists(), "Enriched provenance missing!"

# 2. Check git status to ensure raw files from before were not modified
git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
print(f"Git status:\n{git_status}")
assert "data/raw/candidates_raw.json" not in git_status, "candidates_raw.json was modified!"
assert "data/raw/provenance.md" not in git_status, "provenance.md was modified!"
assert "data/raw/corrective_provenance.md" not in git_status, "corrective_provenance.md was modified!"

# 3. Check review dataset
with open(REVIEW_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"\nReview dataset row count: {len(rows)}")
assert len(rows) == 351, f"Expected 351 rows, got {len(rows)}"

nct_ids = [r["nct_id"].strip() for r in rows]
assert len(set(nct_ids)) == 351, f"Expected 351 unique NCT IDs, got {len(set(nct_ids))}"

# 4. Check human screening fields are blank
for r in rows:
    assert r.get("human_screening", "") == "", f"human_screening not blank for {r['nct_id']}"
    assert r.get("human_screening_reason", "") == "", f"human_screening_reason not blank for {r['nct_id']}"

print("All human-screening fields are verified blank.")

# 5. Check enriched JSON
with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

enriched_studies = enriched_data.get("studies", [])
assert len(enriched_studies) == 351, f"Expected 351 studies in enriched JSON, got {len(enriched_studies)}"
enriched_nct_ids = {s["protocolSection"]["identificationModule"]["nctId"] for s in enriched_studies}
assert enriched_nct_ids == set(nct_ids), "Enriched NCT IDs do not match review CSV NCT IDs!"

# 6. Verify context improvement statistics
brief_summaries = sum(1 for r in rows if r.get("brief_summary", "").strip() != "")
detailed_desc = sum(1 for s in enriched_studies if s.get("protocolSection", {}).get("descriptionModule", {}).get("detailedDescription"))
interventions = sum(1 for r in rows if r.get("interventions", "").strip() != "")
eligibility = sum(1 for r in rows if r.get("eligibility_text", "").strip() != "")
primary_outcomes = sum(1 for r in rows if r.get("primary_outcomes", "").strip() != "")

print("\nContext completeness:")
print(f"  brief_summary: {brief_summaries}/351 (was 68/351)")
print(f"  detailed_description (in enriched raw JSON): {detailed_desc}/351")
print(f"  interventions: {interventions}/351")
print(f"  eligibility_text: {eligibility}/351")
print(f"  primary_outcomes: {primary_outcomes}/351 (was 0/351)")

assert brief_summaries == 351, f"Expected 351 brief summaries, got {brief_summaries}"
assert eligibility == 351, f"Expected 351 eligibility texts, got {eligibility}"
assert primary_outcomes == 350, f"Expected 350 primary outcomes, got {primary_outcomes}"

print("\n=== ALL VALIDATION CHECKS PASSED SUCCESSFULLY ===")
