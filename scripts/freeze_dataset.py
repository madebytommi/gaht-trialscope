#!/usr/bin/env python3
"""Freeze the GAHT TrialScope screened candidate universe.

This script performs deterministic data plumbing only. It does not create new
scientific screening judgments. Current recorded adjudications take precedence;
legacy record-level decisions preserved in the Flash triage layer are retained
explicitly; remaining records may be finalized only from the validated
obvious-exclude stratum.
"""

import csv
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FROZEN = DATA / "frozen"

CANDIDATE_FILE = DATA / "candidate_studies.csv"
FLASH_FILE = DATA / "ai_triage.csv"
SOL_FILE = DATA / "sol_adversarial_audit.csv"
ADJUDICATION_FILE = DATA / "human_screening_decisions.csv"
ENRICHED_FILE = DATA / "raw" / "enrichment" / "enriched_studies.json"

SCREENED_FILE = FROZEN / "screened_studies.csv"
INCLUDED_FILE = FROZEN / "included_studies.csv"
MANIFEST_FILE = FROZEN / "manifest.json"
REPORT_FILE = FROZEN / "README.md"

EXPECTED_CANDIDATES = 351
EXPECTED_CURRENT_ADJUDICATIONS = 248
EXPECTED_LEGACY_ADJUDICATIONS = 6
EXPECTED_STRATIFIED_OBVIOUS_EXCLUDES = 97
EXPECTED_OBVIOUS_EXCLUDE_SOL_AUDIT = 31

LOW_PRIORITY_QC_SAMPLE = {
    "NCT00962637", "NCT01662466", "NCT02060474", "NCT02381821",
    "NCT02551367", "NCT02741154", "NCT02766803", "NCT03230084",
    "NCT03516747", "NCT03528135", "NCT03593317", "NCT04107480",
    "NCT04586348", "NCT05019417", "NCT05244694", "NCT05369247",
    "NCT05587296", "NCT05649943", "NCT05829018", "NCT05853120",
    "NCT06391034", "NCT06405243", "NCT06418347", "NCT06747624",
    "NCT06779331",
}


def clean(value):
    if value is None:
        return ""
    return " ".join(str(value).split())


def load_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    by_id = {}
    for row in rows:
        nct_id = clean(row.get("nct_id"))
        if not nct_id:
            raise ValueError(f"Missing nct_id in {path}")
        if nct_id in by_id:
            raise ValueError(f"Duplicate {nct_id} in {path}")
        by_id[nct_id] = row
    return by_id


def load_registry():
    with ENRICHED_FILE.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    studies = payload.get("studies", []) if isinstance(payload, dict) else payload
    by_id = {}
    for study in studies:
        protocol = study.get("protocolSection", {})
        nct_id = clean(protocol.get("identificationModule", {}).get("nctId"))
        if not nct_id:
            raise ValueError("Enriched registry record missing NCT ID")
        if nct_id in by_id:
            raise ValueError(f"Duplicate {nct_id} in enriched registry data")
        by_id[nct_id] = study
    return by_id


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def registry_fields(study):
    protocol = study.get("protocolSection", {})
    eligibility = protocol.get("eligibilityModule", {}) or {}
    conditions = protocol.get("conditionsModule", {}).get("conditions", []) or []
    status = protocol.get("statusModule", {}) or {}
    last_update = status.get("lastUpdatePostDateStruct", {}) or {}
    return {
        "minimum_age": clean(eligibility.get("minimumAge")),
        "maximum_age": clean(eligibility.get("maximumAge")),
        "sex": clean(eligibility.get("sex")),
        "conditions": "; ".join(clean(v) for v in conditions if clean(v)),
        "registry_last_update_post_date": clean(last_update.get("date")),
    }


def validate_inputs(candidates, flash, sol, adjudications, registry):
    candidate_ids = set(candidates)
    if len(candidate_ids) != EXPECTED_CANDIDATES:
        raise ValueError(
            f"Expected {EXPECTED_CANDIDATES} candidate studies, found {len(candidate_ids)}"
        )
    if set(flash) != candidate_ids:
        raise ValueError("Flash triage does not exactly match the candidate universe")
    if set(registry) != candidate_ids:
        missing = sorted(candidate_ids - set(registry))
        extra = sorted(set(registry) - candidate_ids)
        raise ValueError(
            "Enriched registry data does not exactly match candidate universe: "
            f"missing={missing[:10]}, extra={extra[:10]}"
        )
    if not set(sol).issubset(candidate_ids):
        raise ValueError("Sol audit contains IDs outside the candidate universe")
    if not set(adjudications).issubset(candidate_ids):
        raise ValueError("Recorded adjudications contain IDs outside candidate universe")
    if len(adjudications) != EXPECTED_CURRENT_ADJUDICATIONS:
        raise ValueError(
            f"Expected {EXPECTED_CURRENT_ADJUDICATIONS} current adjudications, "
            f"found {len(adjudications)}"
        )

    invalid = {
        nct_id: clean(row.get("human_screening")).lower()
        for nct_id, row in adjudications.items()
        if clean(row.get("human_screening")).lower() not in {"include", "exclude"}
    }
    if invalid:
        raise ValueError(f"Invalid adjudication values: {invalid}")

    legacy = {}
    for nct_id in candidate_ids - set(adjudications):
        decision = clean(flash[nct_id].get("human_decision_existing")).lower()
        if decision in {"include", "exclude"}:
            legacy[nct_id] = decision

    if len(legacy) != EXPECTED_LEGACY_ADJUDICATIONS:
        raise ValueError(
            f"Expected {EXPECTED_LEGACY_ADJUDICATIONS} legacy decisions, found "
            f"{len(legacy)}: {sorted(legacy)}"
        )
    bad_legacy = {
        nct_id: decision
        for nct_id, decision in legacy.items()
        if decision != "exclude" or clean(flash[nct_id].get("ai_triage")) != "obvious_exclude"
    }
    if bad_legacy:
        raise ValueError(f"Unexpected legacy decision(s): {bad_legacy}")

    stratified = candidate_ids - set(adjudications) - set(legacy)
    if len(stratified) != EXPECTED_STRATIFIED_OBVIOUS_EXCLUDES:
        raise ValueError(
            f"Expected {EXPECTED_STRATIFIED_OBVIOUS_EXCLUDES} stratified obvious "
            f"excludes, found {len(stratified)}"
        )
    non_obvious = sorted(
        nct_id
        for nct_id in stratified
        if clean(flash[nct_id].get("ai_triage")) != "obvious_exclude"
    )
    if non_obvious:
        raise ValueError(
            "Unadjudicated candidates exist outside the obvious-exclude stratum: "
            + ", ".join(non_obvious)
        )

    if len(LOW_PRIORITY_QC_SAMPLE) != 25:
        raise ValueError("Low-priority QC sample must contain 25 unique IDs")
    for nct_id in sorted(LOW_PRIORITY_QC_SAMPLE):
        if nct_id not in candidate_ids:
            raise ValueError(f"QC sample ID missing from candidate universe: {nct_id}")
        if clean(flash[nct_id].get("ai_triage")) != "obvious_exclude":
            raise ValueError(f"QC sample {nct_id} is not Flash obvious_exclude")
        decision = clean(adjudications.get(nct_id, {}).get("human_screening")).lower()
        if decision != "exclude":
            raise ValueError(f"QC sample {nct_id} is not recorded as exclude")

    sol_obvious = [
        row for row in sol.values() if clean(row.get("flash_triage")) == "obvious_exclude"
    ]
    if len(sol_obvious) != EXPECTED_OBVIOUS_EXCLUDE_SOL_AUDIT:
        raise ValueError(
            f"Expected {EXPECTED_OBVIOUS_EXCLUDE_SOL_AUDIT} Sol-audited obvious "
            f"excludes, found {len(sol_obvious)}"
        )
    disagreements = [
        clean(row.get("nct_id"))
        for row in sol_obvious
        if clean(row.get("sol_audit")) != "agree_obvious_exclude"
    ]
    if disagreements:
        raise ValueError(
            "Sol obvious-exclude audit contains disagreement(s): "
            + ", ".join(sorted(disagreements))
        )

    return legacy, stratified, sol_obvious


FIELDNAMES = [
    "nct_id", "final_screening", "decision_basis", "adjudication_reason",
    "brief_title", "study_type", "overall_status", "start_date",
    "study_first_post_date", "registry_last_update_post_date", "enrollment",
    "lead_sponsor", "interventions", "countries", "has_results",
    "minimum_age", "maximum_age", "sex", "conditions", "flash_triage",
    "flash_confidence", "sol_audit",
]


def build_rows(candidates, flash, sol, adjudications, registry, legacy):
    rows = []
    for nct_id in sorted(candidates):
        candidate = candidates[nct_id]
        flash_row = flash[nct_id]
        sol_row = sol.get(nct_id, {})
        reg = registry_fields(registry[nct_id])

        if nct_id in adjudications:
            adjudication = adjudications[nct_id]
            final = clean(adjudication.get("human_screening")).lower()
            basis = "recorded_adjudication"
            reason = clean(adjudication.get("human_screening_reason"))
        elif nct_id in legacy:
            final = legacy[nct_id]
            basis = "legacy_recorded_adjudication"
            reason = (
                "Legacy record-level exclusion preserved in ai_triage.csv "
                "human_decision_existing; retained explicitly during freeze reconciliation."
            )
        else:
            final = "exclude"
            basis = "validated_obvious_exclude_stratum"
            reason = (
                "No individual adjudication recorded; retained as an obvious exclude "
                "after the predefined Sol audit and 25-study low-priority QC sample "
                "showed no obvious-exclude reversals."
            )

        rows.append({
            "nct_id": nct_id,
            "final_screening": final,
            "decision_basis": basis,
            "adjudication_reason": reason,
            "brief_title": clean(candidate.get("brief_title")),
            "study_type": clean(candidate.get("study_type")),
            "overall_status": clean(candidate.get("overall_status")),
            "start_date": clean(candidate.get("start_date")),
            "study_first_post_date": clean(candidate.get("study_first_post_date")),
            "registry_last_update_post_date": reg["registry_last_update_post_date"],
            "enrollment": clean(candidate.get("enrollment")),
            "lead_sponsor": clean(candidate.get("lead_sponsor")),
            "interventions": clean(candidate.get("interventions")),
            "countries": clean(candidate.get("countries")),
            "has_results": clean(candidate.get("has_results")),
            "minimum_age": reg["minimum_age"],
            "maximum_age": reg["maximum_age"],
            "sex": reg["sex"],
            "conditions": reg["conditions"],
            "flash_triage": clean(flash_row.get("ai_triage")),
            "flash_confidence": clean(flash_row.get("confidence")),
            "sol_audit": clean(sol_row.get("sol_audit")),
        })
    return rows


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    candidates = load_csv(CANDIDATE_FILE)
    flash = load_csv(FLASH_FILE)
    sol = load_csv(SOL_FILE)
    adjudications = load_csv(ADJUDICATION_FILE)
    registry = load_registry()

    legacy, stratified, sol_obvious = validate_inputs(
        candidates, flash, sol, adjudications, registry
    )
    rows = build_rows(candidates, flash, sol, adjudications, registry, legacy)

    if len(rows) != EXPECTED_CANDIDATES:
        raise ValueError("Frozen row count does not equal candidate universe")
    final_counts = Counter(row["final_screening"] for row in rows)
    basis_counts = Counter(row["decision_basis"] for row in rows)
    if sum(final_counts.values()) != EXPECTED_CANDIDATES:
        raise ValueError("Final decision counts do not sum to candidate universe")
    if set(final_counts) - {"include", "exclude"}:
        raise ValueError(f"Unexpected final decision(s): {sorted(final_counts)}")
    if basis_counts["recorded_adjudication"] != EXPECTED_CURRENT_ADJUDICATIONS:
        raise ValueError("Unexpected current adjudication count in frozen rows")
    if basis_counts["legacy_recorded_adjudication"] != EXPECTED_LEGACY_ADJUDICATIONS:
        raise ValueError("Unexpected legacy adjudication count in frozen rows")
    if basis_counts["validated_obvious_exclude_stratum"] != EXPECTED_STRATIFIED_OBVIOUS_EXCLUDES:
        raise ValueError("Unexpected stratified obvious-exclude count in frozen rows")

    FROZEN.mkdir(parents=True, exist_ok=True)
    write_csv(SCREENED_FILE, rows)
    included = [row for row in rows if row["final_screening"] == "include"]
    write_csv(INCLUDED_FILE, included)

    source_commit = clean(os.environ.get("FREEZE_SOURCE_COMMIT") or os.environ.get("GITHUB_SHA"))
    input_hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in [CANDIDATE_FILE, FLASH_FILE, SOL_FILE, ADJUDICATION_FILE, ENRICHED_FILE]
    }
    output_hashes = {
        str(SCREENED_FILE.relative_to(ROOT)): sha256(SCREENED_FILE),
        str(INCLUDED_FILE.relative_to(ROOT)): sha256(INCLUDED_FILE),
    }

    manifest = {
        "project": "GAHT TrialScope",
        "freeze_stage": 10,
        "source_commit": source_commit,
        "candidate_universe": EXPECTED_CANDIDATES,
        "final_counts": dict(sorted(final_counts.items())),
        "decision_basis_counts": dict(sorted(basis_counts.items())),
        "current_adjudications": len(adjudications),
        "legacy_recorded_adjudications": len(legacy),
        "legacy_recorded_adjudication_ids": sorted(legacy),
        "stratified_obvious_excludes": len(stratified),
        "low_priority_qc_sample_size": len(LOW_PRIORITY_QC_SAMPLE),
        "low_priority_qc_sample_exclude_confirmations": len(LOW_PRIORITY_QC_SAMPLE),
        "sol_audited_obvious_excludes": len(sol_obvious),
        "sol_obvious_exclude_agreements": len(sol_obvious),
        "input_sha256": input_hashes,
        "output_sha256": output_hashes,
    }
    MANIFEST_FILE.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    report = f"""# GAHT TrialScope — Frozen Screened Dataset

Stage 10 freezes the screened candidate universe used for downstream descriptive analysis. The build is deterministic and generated by `scripts/freeze_dataset.py`.

## Freeze result

- Candidate universe: **{EXPECTED_CANDIDATES} unique NCT IDs**
- Final included studies: **{final_counts['include']}**
- Final excluded studies: **{final_counts['exclude']}**
- Current adjudication-file records applied: **{len(adjudications)}**
- Legacy record-level exclusions reconciled from `ai_triage.csv`: **{len(legacy)}**
- Total record-level decisions represented: **{len(adjudications) + len(legacy)}**
- Obvious excludes finalized through the validated stratified-QC rule: **{len(stratified)}**
- Low-priority obvious-exclude QC sample: **25/25 confirmed exclude; 0 reversals**
- Sol obvious-exclude audit: **{len(sol_obvious)}/{len(sol_obvious)} agreed obvious exclude**
- Unresolved non-obvious records: **0**
- Duplicate candidate IDs: **0**
- Candidate / Flash / enriched-registry universe mismatch: **0**

## Authoritative files

- `screened_studies.csv` — all {EXPECTED_CANDIDATES} candidates with one final screening state and decision provenance.
- `included_studies.csv` — the {final_counts['include']} final included studies for Stage 11 descriptive analysis.
- `manifest.json` — source commit, counts, legacy reconciliation IDs, and SHA-256 hashes for reproducibility.

## Decision precedence

1. A current recorded adjudication in `data/human_screening_decisions.csv` determines the final state when present.
2. Six older record-level exclusions preserved in `data/ai_triage.csv` as `human_decision_existing` are retained explicitly as `legacy_recorded_adjudication` rather than silently discarded.
3. A candidate with neither source of record-level adjudication may only be finalized as excluded if Flash classified it `obvious_exclude`.
4. That lower-risk stratum is retained under the predefined validation design: 31 Sol-audited obvious excludes all agreed, and the 25-study low-priority QC sample produced 25 exclusions, 0 reversals, and 0 unresolved cases.
5. Any unadjudicated record outside `obvious_exclude` causes the freeze build to fail.

## Provenance language

The frozen dataset uses neutral provenance labels. It does **not** label the {len(stratified)} stratified-QC exclusions as individually human-verified. This preserves the protocol distinction between record-level adjudication and validated exclusion-stratum handling.

## Source snapshot

Source commit: `{source_commit or 'not supplied'}`

Exact input and output SHA-256 hashes are recorded in `manifest.json`.
"""
    REPORT_FILE.write_text(report, encoding="utf-8")

    print(
        f"Freeze passed: {EXPECTED_CANDIDATES} candidates -> "
        f"{final_counts['include']} include / {final_counts['exclude']} exclude; "
        f"{len(adjudications)} current adjudications + {len(legacy)} legacy; "
        f"{len(stratified)} stratified obvious excludes."
    )
    print("Legacy reconciled IDs: " + ", ".join(sorted(legacy)))


if __name__ == "__main__":
    main()
