# GAHT TrialScope

GAHT TrialScope is a reproducible descriptive snapshot of registered gender-affirming hormone therapy research using public ClinicalTrials.gov data.

Please see `PROTOCOL.md` for methodology, inclusion/exclusion criteria, and limitations.

## Data and audit trail

- `data/raw/candidates_raw.json` and `data/raw/provenance.md` preserve the original 283-record retrieval.
- `data/raw/corrective_provenance.md` documents the supplementary retrieval that added 68 unique NCT IDs.
- `scratch/candidates_full.json` is the preserved combined universe of 351 unique candidates.
- `data/candidate_studies.csv` preserves the earlier forced-binary keyword screening as historical metadata.
- `data/ai_boundary_case_reviews.csv` records the seven requested record-level AI boundary-case reviews.
- `data/screening_review.csv` is the current 351-record review-oriented dataset; its embedded human-screening fields have not yet been regenerated from the current adjudication layer.
- `data/human_screening_decisions.csv` is the authoritative machine-readable layer for final human screening decisions. It currently records 13 adjudicated boundary cases, all excluded under `PROTOCOL.md`.

*Note: Screening is still in progress. Thirteen boundary cases now have final human decisions; the remaining candidate classifications are preliminary/AI-assisted until human verification or quality-control review is completed. The dataset is not yet ready for descriptive findings or clinical conclusions.*
