#!/usr/bin/env python3
"""Build the consolidated GAHT TrialScope human-screening queue.

This is deterministic data plumbing only. It does not make new scientific
screening judgments. It reconciles existing Flash triage, Sol adversarial audit,
ClinicalTrials.gov enrichment, and explicit human adjudications into a single
review queue.
"""

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

FLASH_FILE = DATA / "ai_triage.csv"
SOL_FILE = DATA / "sol_adversarial_audit.csv"
HUMAN_FILE = DATA / "human_screening_decisions.csv"
ENRICHED_FILE = DATA / "raw" / "enrichment" / "enriched_studies.json"
FULL_QUEUE_FILE = DATA / "consolidated_screening_queue.csv"
INCLUDE_QUEUE_FILE = DATA / "likely_include_review_queue.csv"
REPORT_FILE = DATA / "consolidated_screening_queue_report.md"

BATCH_SIZE = 20


def clean(value):
    if value is None:
        return ""
    return " ".join(str(value).split())


def nested(obj, *keys, default=None):
    for key in keys:
        if not isinstance(obj, dict):
            return default
        obj = obj.get(key)
        if obj is None:
            return default
    return obj


def join_values(values):
    return "; ".join(clean(v) for v in (values or []) if clean(v))


def format_interventions(protocol):
    out = []
    for intervention in nested(
        protocol, "armsInterventionsModule", "interventions", default=[]
    ) or []:
        label = ": ".join(
            p for p in [clean(intervention.get("type")), clean(intervention.get("name"))] if p
        )
        description = clean(intervention.get("description"))
        out.append(f"{label} — {description}" if description else label)
    return "; ".join(v for v in out if v)


def format_primary_outcomes(protocol):
    out = []
    for outcome in nested(protocol, "outcomesModule", "primaryOutcomes", default=[]) or []:
        parts = [
            clean(outcome.get("measure")),
            clean(outcome.get("timeFrame")),
            clean(outcome.get("description")),
        ]
        out.append(" | ".join(p for p in parts if p))
    return "; ".join(v for v in out if v)


def load_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
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
        nct_id = clean(nested(protocol, "identificationModule", "nctId", default=""))
        if not nct_id:
            raise ValueError("Enriched registry record missing NCT ID")
        if nct_id in by_id:
            raise ValueError(f"Duplicate {nct_id} in enriched registry data")
        by_id[nct_id] = study
    return by_id


def registry_fields(study):
    protocol = study.get("protocolSection", {})
    return {
        "brief_title": clean(nested(protocol, "identificationModule", "briefTitle", default="")),
        "study_type": clean(nested(protocol, "designModule", "studyType", default="")),
        "overall_status": clean(nested(protocol, "statusModule", "overallStatus", default="")),
        "conditions": join_values(nested(protocol, "conditionsModule", "conditions", default=[])),
        "brief_summary": clean(nested(protocol, "descriptionModule", "briefSummary", default="")),
        "interventions": format_interventions(protocol),
        "study_population": clean(nested(protocol, "eligibilityModule", "studyPopulation", default="")),
        "eligibility_text": clean(nested(protocol, "eligibilityModule", "eligibilityCriteria", default="")),
        "primary_outcomes": format_primary_outcomes(protocol),
    }


def classify(flash, sol, human):
    if human:
        decision = clean(human.get("human_screening")).lower()
        if decision not in {"include", "exclude"}:
            raise ValueError(f"Invalid human decision: {decision!r}")
        return f"final_{decision}", "0_human_final"

    flash_decision = clean(flash.get("ai_triage"))
    sol_decision = clean(sol.get("sol_decision")) if sol else ""

    if flash_decision == "human_review" and sol_decision == "likely_include":
        return "proposed_include", "1_sol_promoted"

    if flash_decision == "likely_include" and sol_decision == "agree_likely_include":
        return "proposed_include", "2_dual_model_agreement"

    # All remaining non-human records are held for exclusion QC. Under the
    # current audit, the model disagreements and genuine ambiguities have all
    # received explicit human adjudication, so nothing unresolved should fall
    # through here from the likely-include/human-review strata.
    if flash_decision in {"likely_include", "human_review"} and not sol_decision:
        raise ValueError(
            f"Expected Sol audit for Flash {flash_decision}, but none was found"
        )

    return "proposed_exclude", "3_exclude_qc"


def build_rows():
    flash = load_csv(FLASH_FILE)
    sol = load_csv(SOL_FILE)
    human = load_csv(HUMAN_FILE)
    registry = load_registry()

    candidate_ids = set(flash)
    if len(candidate_ids) != 351:
        raise ValueError(f"Expected 351 Flash candidates, found {len(candidate_ids)}")
    if set(registry) != candidate_ids:
        missing_registry = sorted(candidate_ids - set(registry))
        extra_registry = sorted(set(registry) - candidate_ids)
        raise ValueError(
            "Registry/Flash candidate universe mismatch: "
            f"missing_registry={missing_registry[:5]}, extra_registry={extra_registry[:5]}"
        )
    if not set(sol).issubset(candidate_ids):
        raise ValueError("Sol audit contains an NCT ID outside the candidate universe")
    if not set(human).issubset(candidate_ids):
        raise ValueError("Human decisions contain an NCT ID outside the candidate universe")

    rows = []
    for nct_id in sorted(candidate_ids):
        f = flash[nct_id]
        s = sol.get(nct_id, {})
        h = human.get(nct_id, {})
        current_status, priority_tier = classify(f, s, h)
        reg = registry_fields(registry[nct_id])

        rows.append(
            {
                "review_order": "",
                "review_batch": "",
                "priority_tier": priority_tier,
                "current_status": current_status,
                "nct_id": nct_id,
                "brief_title": reg["brief_title"] or clean(f.get("brief_title")),
                "registry_url": clean(f.get("registry_url")) or f"https://clinicaltrials.gov/study/{nct_id}",
                "study_type": reg["study_type"],
                "overall_status": reg["overall_status"],
                "conditions": reg["conditions"],
                "flash_triage": clean(f.get("ai_triage")),
                "flash_confidence": clean(f.get("ai_confidence")),
                "flash_reason": clean(f.get("ai_triage_reason")),
                "flash_evidence": clean(f.get("evidence_snippet")),
                "sol_decision": clean(s.get("sol_decision")),
                "sol_criterion_1_tgd_population": clean(s.get("criterion_1_tgd_population")),
                "sol_criterion_2_gaht_research_role": clean(s.get("criterion_2_gaht_research_role")),
                "sol_boundary_reason": clean(s.get("boundary_reason")),
                "sol_evidence": clean(s.get("evidence_summary")),
                "brief_summary": reg["brief_summary"],
                "interventions": reg["interventions"],
                "study_population": reg["study_population"],
                "eligibility_text": reg["eligibility_text"],
                "primary_outcomes": reg["primary_outcomes"],
                "human_screening": clean(h.get("human_screening")),
                "human_screening_reason": clean(h.get("human_screening_reason")),
                "human_verification_notes": "",
                "needs_deeper_review": "",
            }
        )

    # Put the active include-verification work first: 17 Sol-promoted records,
    # then the 111 dual-model agreements. Number only those 128 active rows.
    rows.sort(key=lambda r: (r["priority_tier"], r["nct_id"]))
    include_order = 0
    for row in rows:
        if row["current_status"] == "proposed_include":
            include_order += 1
            row["review_order"] = str(include_order)
            row["review_batch"] = f"B{((include_order - 1) // BATCH_SIZE) + 1:02d}"

    counts = Counter(row["current_status"] for row in rows)
    tiers = Counter(row["priority_tier"] for row in rows)

    expected = {
        "final_exclude": 13,
        "proposed_include": 128,
        "proposed_exclude": 210,
    }
    for key, value in expected.items():
        if counts[key] != value:
            raise ValueError(f"Expected {value} {key} rows, found {counts[key]}")
    if tiers["1_sol_promoted"] != 17:
        raise ValueError(
            f"Expected 17 Sol-promoted includes, found {tiers['1_sol_promoted']}"
        )
    if tiers["2_dual_model_agreement"] != 111:
        raise ValueError(
            "Expected 111 dual-model likely-includes, "
            f"found {tiers['2_dual_model_agreement']}"
        )

    return rows, counts, tiers


FIELDNAMES = [
    "review_order",
    "review_batch",
    "priority_tier",
    "current_status",
    "nct_id",
    "brief_title",
    "registry_url",
    "study_type",
    "overall_status",
    "conditions",
    "flash_triage",
    "flash_confidence",
    "flash_reason",
    "flash_evidence",
    "sol_decision",
    "sol_criterion_1_tgd_population",
    "sol_criterion_2_gaht_research_role",
    "sol_boundary_reason",
    "sol_evidence",
    "brief_summary",
    "interventions",
    "study_population",
    "eligibility_text",
    "primary_outcomes",
    "human_screening",
    "human_screening_reason",
    "human_verification_notes",
    "needs_deeper_review",
]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows, counts, tiers):
    includes = [r for r in rows if r["current_status"] == "proposed_include"]
    batch_counts = Counter(r["review_batch"] for r in includes)
    batch_lines = "\n".join(
        f"- **{batch}**: {batch_counts[batch]} studies"
        for batch in sorted(batch_counts)
    )

    report = f"""# Consolidated Human Screening Queue\n\nThis queue is generated deterministically from:\n\n- `data/ai_triage.csv` — Gemini 3.7 Flash first-pass triage\n- `data/sol_adversarial_audit.csv` — GPT-5.6 Sol independent adversarial audit\n- `data/raw/enrichment/enriched_studies.json` — preserved ClinicalTrials.gov registry evidence\n- `data/human_screening_decisions.csv` — explicit final human adjudications\n\nThe generator does **not** make new scientific screening decisions. It only reconciles existing evidence and decisions.\n\n## Current screening state\n\n- Candidate universe: **{len(rows)}**\n- Final human adjudications: **{counts['final_exclude']} excludes**\n- Active proposed includes requiring human verification: **{counts['proposed_include']}**\n  - Sol-promoted from Flash `human_review`: **{tiers['1_sol_promoted']}**\n  - Flash/Sol agreement likely-includes: **{tiers['2_dual_model_agreement']}**\n- Proposed excludes reserved for exclusion QC: **{counts['proposed_exclude']}**\n\n## Include verification order\n\nReview `data/likely_include_review_queue.csv` from top to bottom. The 17 Sol-promoted records come first because Flash originally expressed uncertainty; the 111 dual-model agreements follow.\n\nFor each study, confirm both protocol gates:\n\n1. A transgender/gender-diverse population is explicitly part of the study population.\n2. GAHT has an explicit research role as an intervention, exposure, comparison, monitoring target, pharmacologic variable, or subject of analysis.\n\nIf both are clearly met, record the human decision as `include`. If either fails, record `exclude`. If the preserved registry evidence is insufficient, set `needs_deeper_review` rather than forcing a decision.\n\n## Batches\n\n{batch_lines}\n\nAfter all 128 proposed includes are human-verified, perform stratified QC on the 210 proposed excludes before locking the final included-study set.\n"""
    REPORT_FILE.write_text(report, encoding="utf-8")


def main():
    rows, counts, tiers = build_rows()
    write_csv(FULL_QUEUE_FILE, rows)
    write_csv(
        INCLUDE_QUEUE_FILE,
        [row for row in rows if row["current_status"] == "proposed_include"],
    )
    write_report(rows, counts, tiers)
    print(
        "Built screening queue: "
        f"{counts['proposed_include']} proposed includes, "
        f"{counts['final_exclude']} final human excludes, "
        f"{counts['proposed_exclude']} proposed excludes/QC."
    )


if __name__ == "__main__":
    main()
