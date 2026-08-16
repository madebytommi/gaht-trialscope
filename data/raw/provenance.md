# Retrieval Provenance

- **Source**: ClinicalTrials.gov (via APIv2 wrapper script)
- **Exact Query**: `--term "(transgender OR transsexual OR \"gender diverse\" OR \"gender incongruence\") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)"`
- **Retrieval Date and Time**: 2026-08-16 10:43 CST
- **API/Tool Used**: Google Antigravity Science ClinicalTrials.gov skill (`clinical_trials_api.py`)
- **Number of Records Returned**: 283
- **Number of Unique Records**: 283
- **Limitations**: The search relied on keyword matching across all text fields (the `query.term` parameter). Some studies may use alternate terminology for GAHT or gender diversity that were not captured in the terms list. The keyword approach also pulls in false positives where terms appear in background descriptions.

## Terms & License Notification
Data was retrieved from ClinicalTrials.gov. Please review the terms of use at [https://clinicaltrials.gov/](https://clinicaltrials.gov/).
