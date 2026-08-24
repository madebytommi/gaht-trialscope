# GAHT TrialScope — Human Include Verification Queue

This directory is the active human-verification queue for the **128 studies currently proposed for inclusion** after the Gemini 3.7 Flash triage, GPT-5.6 Sol adversarial audit, and final human adjudication of the 13 difficult boundary cases.

## Queue structure

| Batch | Review order | Studies | Notes |
|---|---:|---:|---|
| `B01.csv` | 1–20 | 20 | **Start here.** Orders 1–17 are the Sol-promoted studies that Flash originally sent to human review; orders 18–20 begin the dual-model agreements. |
| `B02.csv` | 21–40 | 20 | Flash + Sol agreement likely-includes. |
| `B03.csv` | 41–60 | 20 | Flash + Sol agreement likely-includes. |
| `B04.csv` | 61–80 | 20 | Flash + Sol agreement likely-includes. |
| `B05.csv` | 81–100 | 20 | Flash + Sol agreement likely-includes. |
| `B06.csv` | 101–120 | 20 | Flash + Sol agreement likely-includes. |
| `B07.csv` | 121–128 | 8 | Final Flash + Sol agreement likely-includes. |

Total: **128 studies** = **17 Sol-promoted from Flash `human_review` + 111 Flash/Sol agreement likely-includes**.

## Human verification rule

For every row, apply `PROTOCOL.md` and confirm both gates:

1. A transgender/gender-diverse population is explicitly part of the study population.
2. GAHT has an explicit research role as an intervention, exposure, comparison, monitoring target, pharmacologic variable, or subject of analysis.

Record:

- `human_screening = include` when both gates are clearly satisfied.
- `human_screening = exclude` when either gate fails.
- `needs_deeper_review = yes` when the preserved registry evidence is insufficient or genuinely ambiguous; do not force a decision.
- Put the concise protocol-grounded rationale in `human_screening_reason`.

## Priority

The first 17 rows deserve the most attention because Flash originally classified them as `human_review` and Sol promoted them to `likely_include`. Their `verification_focus` column preserves Sol's specific reason for promotion.

Rows 18–128 were independently classified as likely-includes by both model passes. They still require human confirmation, but most should be rapid protocol checks rather than deep investigations.

## Provenance

The queue was reconciled from:

- `data/ai_triage.csv`
- `data/ai_triage_report.md`
- `data/sol_adversarial_audit.csv`
- `data/sol_adversarial_audit_report.md`
- `data/human_screening_decisions.csv`
- the ClinicalTrials.gov registry URLs carried with each record

`scripts/build_screening_queue.py` is the richer deterministic generator for reconciling these sources with `data/raw/enrichment/enriched_studies.json`. It validates the expected project state before generating consolidated outputs.

## After the 128

Once this queue is human-verified, merge the decisions into the authoritative human-decision layer, lock the final included-study set, then perform stratified QC on the **210 proposed excludes** before downstream descriptive analysis.
