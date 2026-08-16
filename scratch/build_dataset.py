import csv
import json
import re
from collections import Counter
from pathlib import Path


REGISTRY_FILE = Path("scratch/candidates_full.json")
LEGACY_SCREENING_FILE = Path("data/candidate_studies.csv")
AI_REVIEW_FILE = Path("data/ai_boundary_case_reviews.csv")
REVIEW_FILE = Path("data/screening_review.csv")

ALLOWED_SCREENING_VALUES = {"include", "exclude", "uncertain"}
NCT_ID_PATTERN = re.compile(r"^NCT\d{8}$")


def extract_nested(value, keys, default=None):
    """Safely extract a value from nested dictionaries."""
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return default
        value = value[key]
    return value


def normalize_text(value):
    """Collapse registry whitespace without changing the words."""
    if value is None:
        return ""
    return " ".join(str(value).split())


def join_text(values):
    return "; ".join(normalize_text(value) for value in values if value)


def format_interventions(protocol):
    formatted = []
    for intervention in extract_nested(
        protocol, ["armsInterventionsModule", "interventions"], []
    ):
        parts = [
            normalize_text(intervention.get("type")),
            normalize_text(intervention.get("name")),
        ]
        label = ": ".join(part for part in parts if part)
        description = normalize_text(intervention.get("description"))
        formatted.append(f"{label} — {description}" if description else label)
    return join_text(formatted)


def format_primary_outcomes(protocol):
    formatted = []
    for outcome in extract_nested(protocol, ["outcomesModule", "primaryOutcomes"], []):
        parts = [
            normalize_text(outcome.get("measure")),
            normalize_text(outcome.get("timeFrame")),
            normalize_text(outcome.get("description")),
        ]
        formatted.append(" | ".join(part for part in parts if part))
    return join_text(formatted)


def load_csv_by_nct_id(path, required_fields):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = required_fields - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing fields: {sorted(missing)}")

        rows = {}
        for row in reader:
            nct_id = row["nct_id"].strip()
            validate_nct_id(nct_id, path)
            if nct_id in rows:
                raise ValueError(f"Duplicate NCT ID in {path}: {nct_id}")
            validate_screening_value(row["preliminary_screening"], path, nct_id)
            rows[nct_id] = row
        return rows


def validate_nct_id(nct_id, source):
    if not nct_id or not NCT_ID_PATTERN.fullmatch(nct_id):
        raise ValueError(f"Invalid NCT ID in {source}: {nct_id!r}")


def validate_screening_value(value, source, nct_id):
    if value not in ALLOWED_SCREENING_VALUES:
        raise ValueError(
            f"Invalid preliminary_screening in {source} for {nct_id}: {value!r}"
        )


def load_registry_studies():
    with REGISTRY_FILE.open(encoding="utf-8") as handle:
        studies = json.load(handle).get("studies", [])

    unique_studies = {}
    for study in studies:
        nct_id = extract_nested(
            study, ["protocolSection", "identificationModule", "nctId"]
        )
        validate_nct_id(nct_id, REGISTRY_FILE)
        if nct_id in unique_studies:
            raise ValueError(f"Duplicate NCT ID in {REGISTRY_FILE}: {nct_id}")
        unique_studies[nct_id] = study
    return studies, unique_studies


def build_review_rows(studies, legacy_screening, ai_reviews):
    rows = []
    for nct_id in sorted(studies):
        study = studies[nct_id]
        protocol = study.get("protocolSection", {})
        legacy = legacy_screening[nct_id]
        review = ai_reviews.get(nct_id)

        if review:
            preliminary_screening = review["preliminary_screening"]
            screening_reason = review["screening_reason"]
            screening_basis = "record_level_ai_review_2026-08-16"
        else:
            preliminary_screening = legacy["preliminary_screening"]
            screening_reason = (
                "Unverified legacy keyword heuristic: " + legacy["screening_reason"]
            )
            screening_basis = "legacy_keyword_heuristic_unverified"

        rows.append(
            {
                "nct_id": nct_id,
                "brief_title": normalize_text(
                    extract_nested(
                        protocol, ["identificationModule", "briefTitle"], ""
                    )
                ),
                "study_type": normalize_text(
                    extract_nested(protocol, ["designModule", "studyType"], "")
                ),
                "overall_status": normalize_text(
                    extract_nested(protocol, ["statusModule", "overallStatus"], "")
                ),
                "conditions": join_text(
                    extract_nested(protocol, ["conditionsModule", "conditions"], [])
                ),
                "brief_summary": normalize_text(
                    extract_nested(
                        protocol, ["descriptionModule", "briefSummary"], ""
                    )
                ),
                "interventions": format_interventions(protocol),
                "study_population": normalize_text(
                    extract_nested(
                        protocol, ["eligibilityModule", "studyPopulation"], ""
                    )
                ),
                "eligibility_text": normalize_text(
                    extract_nested(
                        protocol, ["eligibilityModule", "eligibilityCriteria"], ""
                    )
                ),
                "primary_outcomes": format_primary_outcomes(protocol),
                "legacy_preliminary_screening": legacy["preliminary_screening"],
                "legacy_screening_reason": legacy["screening_reason"],
                "preliminary_screening": preliminary_screening,
                "screening_reason": screening_reason,
                "preliminary_screening_basis": screening_basis,
                "human_screening": "",
                "human_screening_reason": "",
            }
        )
    return rows


def validate_review_rows(rows, expected_nct_ids):
    row_nct_ids = [row["nct_id"] for row in rows]
    if len(row_nct_ids) != len(set(row_nct_ids)):
        raise ValueError("Review rows contain duplicate NCT IDs")
    if set(row_nct_ids) != expected_nct_ids:
        raise ValueError("Review rows do not match the registry candidate universe")

    for row in rows:
        validate_screening_value(
            row["preliminary_screening"], REVIEW_FILE, row["nct_id"]
        )
        if row["human_screening"] or row["human_screening_reason"]:
            raise ValueError(f"Human-review fields must be blank for {row['nct_id']}")


def write_review_csv(rows):
    fieldnames = [
        "nct_id",
        "brief_title",
        "study_type",
        "overall_status",
        "conditions",
        "brief_summary",
        "interventions",
        "study_population",
        "eligibility_text",
        "primary_outcomes",
        "legacy_preliminary_screening",
        "legacy_screening_reason",
        "preliminary_screening",
        "screening_reason",
        "preliminary_screening_basis",
        "human_screening",
        "human_screening_reason",
    ]
    with REVIEW_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def process_data():
    raw_studies, studies = load_registry_studies()
    legacy_screening = load_csv_by_nct_id(
        LEGACY_SCREENING_FILE,
        {"nct_id", "preliminary_screening", "screening_reason"},
    )
    ai_reviews = load_csv_by_nct_id(
        AI_REVIEW_FILE,
        {"nct_id", "preliminary_screening", "screening_reason"},
    )

    if set(legacy_screening) != set(studies):
        raise ValueError("Legacy screening IDs do not match the registry candidate universe")
    unknown_review_ids = set(ai_reviews) - set(studies)
    if unknown_review_ids:
        raise ValueError(f"AI review IDs are not candidates: {sorted(unknown_review_ids)}")

    rows = build_review_rows(studies, legacy_screening, ai_reviews)
    validate_review_rows(rows, set(studies))
    write_review_csv(rows)

    counts = Counter(row["preliminary_screening"] for row in rows)
    print(f"Registry rows loaded: {len(raw_studies)}")
    print(f"Unique candidate NCT IDs: {len(studies)}")
    print(f"Record-level AI reviews merged: {len(ai_reviews)}")
    print(f"Records still carrying unverified legacy screening: {len(rows) - len(ai_reviews)}")
    print(f"Preliminary screening metadata: {dict(sorted(counts.items()))}")
    print(f"Wrote review dataset: {REVIEW_FILE}")


if __name__ == "__main__":
    process_data()
