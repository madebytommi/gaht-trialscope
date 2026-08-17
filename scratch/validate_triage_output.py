import csv
import subprocess
from pathlib import Path

TRIAGE_CSV = Path("data/ai_triage.csv")
REPORT_MD = Path("data/ai_triage_report.md")
REVIEW_CSV = Path("data/screening_review.csv")
PROTOCOL_MD = Path("PROTOCOL.md")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

print("=== RUNNING FULL PROGRAMMATIC VALIDATION ===")

# 1. Validate ai_triage.csv existence and rows
assert TRIAGE_CSV.exists(), "ai_triage.csv does not exist"
assert REPORT_MD.exists(), "ai_triage_report.md does not exist"

with open(TRIAGE_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    triage_rows = list(reader)

assert len(triage_rows) == 351, f"Expected 351 rows in ai_triage.csv, got {len(triage_rows)}"
print(f"Row count: {len(triage_rows)} [OK]")

# 2. Validate uniqueness of nct_id
nct_ids = [r["nct_id"].strip() for r in triage_rows]
assert len(set(nct_ids)) == 351, f"Expected 351 unique NCT IDs, got {len(set(nct_ids))}"
print("Unique NCT IDs: 351 [OK]")

# 3. Validate candidate universe strictly matches screening_review.csv
with open(REVIEW_CSV, encoding="utf-8") as f:
    review_rows = list(csv.DictReader(f))

review_nct_ids = [r["nct_id"].strip() for r in review_rows]
assert set(nct_ids) == set(review_nct_ids), "NCT IDs do not match screening_review.csv!"
print("Candidate universe match: EXACT [OK]")

# 4. Validate allowed values
valid_c1 = {"yes", "no", "unclear"}
valid_c2 = {"yes", "no", "unclear"}
valid_triage = {"likely_include", "obvious_exclude", "human_review"}
valid_conf = {"high", "medium", "low"}

for r in triage_rows:
    nct = r["nct_id"]
    assert r["criterion_1_tgd"] in valid_c1, f"Invalid criterion_1_tgd for {nct}: {r['criterion_1_tgd']}"
    assert r["criterion_2_gaht"] in valid_c2, f"Invalid criterion_2_gaht for {nct}: {r['criterion_2_gaht']}"
    assert r["ai_triage"] in valid_triage, f"Invalid ai_triage for {nct}: {r['ai_triage']}"
    assert r["confidence"] in valid_conf, f"Invalid confidence for {nct}: {r['confidence']}"
    assert r["ai_triage_reason"].strip() != "", f"Blank ai_triage_reason for {nct}"

print("Allowed value constraints: ALL VALID [OK]")
print("Non-blank ai_triage_reason: ALL 351 VALID [OK]")

# 5. Validate the 7 existing human decisions
expected_human_decisions = {
    "NCT00023543": "exclude",
    "NCT00082082": "exclude",
    "NCT00146146": "include",
    "NCT00188708": "exclude",
    "NCT00450749": "exclude",
    "NCT00544882": "exclude",
    "NCT00608400": "exclude",
}

for r in triage_rows:
    nct = r["nct_id"]
    if nct in expected_human_decisions:
        assert r["human_decision_existing"] == expected_human_decisions[nct], f"Wrong human_decision_existing for {nct}: {r['human_decision_existing']}"
    else:
        assert r["human_decision_existing"] == "", f"Non-blank human_decision_existing for {nct}: {r['human_decision_existing']}"

print("Existing human decisions: 7 IDENTIFIED & PRESERVED, 344 BLANK [OK]")

# 6. Validate screening_review.csv human_screening fields remain blank
for r in review_rows:
    assert r.get("human_screening", "") == "", f"screening_review.csv human_screening not blank for {r['nct_id']}"
    assert r.get("human_screening_reason", "") == "", f"screening_review.csv human_screening_reason not blank for {r['nct_id']}"

print("screening_review.csv human review fields: ALL BLANK [OK]")

# 7. Check git status to ensure PROTOCOL.md and raw/enrichment files were not modified
git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout
print(f"\nGit status:\n{git_status}")

assert "PROTOCOL.md" not in git_status, "PROTOCOL.md was modified!"
assert "data/raw/candidates_raw.json" not in git_status, "candidates_raw.json was modified!"
assert "data/raw/provenance.md" not in git_status, "provenance.md was modified!"
assert "data/raw/corrective_provenance.md" not in git_status, "corrective_provenance.md was modified!"
assert "data/raw/enrichment/enriched_studies.json" not in git_status, "enriched_studies.json was modified!"

print("=== ALL 12 PROGRAMMATIC VALIDATION CHECKS PASSED SUCCESSFULLY ===")
