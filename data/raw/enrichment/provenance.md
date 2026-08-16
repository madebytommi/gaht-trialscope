# Screening-Context Enrichment Provenance

See [enrichment_provenance.md](file:///Volumes/Backup%20Plus/GitHub/gaht-trialscope/data/raw/enrichment/enrichment_provenance.md) for the full provenance documentation.

- **Target Candidate Universe**: 351 unique NCT IDs
- **Enrichment Retrieval Timestamp**: 2026-08-16 12:24 UTC
- **ClinicalTrials.gov API**: REST API v2 (`https://clinicaltrials.gov/api/v2/studies`) via `polite-http`
- **Method**: Batch query using `filter.ids` in chunks of 50
- **Total Requested**: 351
- **Total Retrieved**: 351
- **Failures**: 0
- **Raw Data Saved**: `data/raw/enrichment/enriched_studies.json`
