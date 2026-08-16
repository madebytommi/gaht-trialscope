# Screening-Context Enrichment Provenance

## Scope and Purpose

This document records the registry-context enrichment pass conducted on the authoritative 351-record candidate universe for the GAHT TrialScope project. The purpose of this pass was to retrieve complete, structured ClinicalTrials.gov protocol modules and registry context for the 351 fixed NCT IDs without searching for new studies or altering the candidate universe.

## Retrieval Details

- **Target Candidate Universe**: Exactly 351 unique NCT IDs (derived from `data/screening_review.csv` / `scratch/candidates_full.json`).
- **Enrichment Retrieval Timestamp**: 2026-08-16 12:24 UTC (2026-08-16 12:24:26 - 12:24:33 UTC).
- **ClinicalTrials.gov API & Tooling**:
  - Endpoint: ClinicalTrials.gov REST API v2 (`https://clinicaltrials.gov/api/v2/studies`)
  - Client Tooling: Polite HTTP client (`polite-http` v0.1.1) adhering to a 1.0 query-per-second (QPS) rate limit.
- **Exact Retrieval Method**:
  - The 351 unique NCT IDs were partitioned into 8 batches of up to 50 NCT IDs.
  - Each batch was queried via the `/studies` endpoint using the exact identifier filter `filter.ids=<NCT_ID_1>|<NCT_ID_2>|...&pageSize=1000`.
  - Fallback mechanism: Single-study endpoint `/studies/{nctId}` configured for any records missed in batch responses (0 fallbacks required).
- **Records Requested**: 351
- **Records Successfully Retrieved**: 351 (100.0% retrieval success rate).
- **Failures / Missing Records**: 0 failures, 0 missing records.
- **Candidate Universe Integrity**: Verified before and after retrieval. The set of retrieved NCT IDs strictly equals the pre-existing 351 candidate NCT IDs.

## Data Saved

- **Raw Enriched Dataset**: `data/raw/enrichment/enriched_studies.json` (8,484,444 bytes, 351 complete study objects).
- **Enriched Modules Preserved**:
  - `identificationModule`: NCTId, briefTitle, officialTitle, organization.
  - `statusModule`: overallStatus, startDateStruct, primaryCompletionDateStruct, completionDateStruct, lastUpdatePostDateStruct.
  - `sponsorCollaboratorsModule`: leadSponsor, collaborators, responsibleParty.
  - `descriptionModule`: briefSummary, detailedDescription.
  - `conditionsModule`: conditions, keywords.
  - `designModule`: studyType, phases, designInfo, enrollmentInfo.
  - `armsInterventionsModule`: armGroups, interventions (type, name, description).
  - `outcomesModule`: primaryOutcomes (measure, timeFrame, description), secondaryOutcomes.
  - `eligibilityModule`: eligibilityCriteria, studyPopulation, sex, minimumAge, maximumAge, stdAges, healthyVolunteers.
  - `contactsLocationsModule`: locations (facility, city, state, zip, country, status).
  - `derivedSection` & `hasResults`: results indicator and derived index terms.

## Field Coverage Improvements

Across the 351 candidate records:
- **Brief Summary**: 351 / 351 records (100.0%) — increased from 68 records (+283 records).
- **Detailed Description**: 244 / 351 records (69.5%) — previously 0 records in review CSV.
- **Intervention Information**: 305 / 351 records (86.9% — with 294 containing intervention descriptions; remaining 46 are non-interventional observational studies).
- **Eligibility Criteria**: 351 / 351 records (100.0%).
- **Study Population**: 130 / 351 records (37.0% — present across observational study designs).
- **Primary Outcomes**: 350 / 351 records (99.7%) — increased from 0 records (+350 records).
- **Secondary Outcomes**: 256 / 351 records (72.9%).
- **Official Title**: 351 / 351 records (100.0%).
- **Arms / Arm Groups**: 313 / 351 records (89.2%).
- **Enrollment Count**: 350 / 351 records (99.7%).
- **Lead Sponsor**: 351 / 351 records (100.0%).
- **Study Locations / Countries**: 330 / 351 records (94.0%).
- **Results Availability**: 31 / 351 records (8.8%).

## Limitations

- Data reflects study registrations and updates as published on ClinicalTrials.gov up to the retrieval date (2026-08-16).
- Completeness of optional registry fields (such as `detailedDescription` or `studyPopulation` in non-observational studies) depends on original sponsor/investigator submission.
- Registry context enrichment provides source documentation for human review; it does not constitute human review or alter historical AI-assisted screening classifications.
