# GAHT TrialScope

GAHT TrialScope is a reproducible descriptive snapshot of registered gender-affirming hormone therapy research using public ClinicalTrials.gov data.

Please see `PROTOCOL.md` for methodology, inclusion/exclusion criteria, and limitations.

## Data and audit trail

- `data/raw/candidates_raw.json` and `data/raw/provenance.md` preserve the original 283-record retrieval.
- `data/raw/corrective_provenance.md` documents the supplementary retrieval that added 68 unique NCT IDs.
- `scratch/candidates_full.json` is the preserved combined universe of 351 unique candidates.
- `data/candidate_studies.csv` preserves the earlier forced-binary keyword screening as historical metadata.
- `data/ai_boundary_case_reviews.csv` records the seven requested record-level AI boundary-case reviews.
- `data/screening_review.csv` is the current review-oriented dataset. Its human-screening fields are blank.

*Note: Screening remains preliminary and AI-assisted. Most carried-forward classifications have not received record-level review, no human screening decisions have been entered, and the dataset is not ready for descriptive findings or clinical conclusions.*
