# Corrective Retrieval Provenance

## Scope and evidence

This file permanently documents the supplementary ClinicalTrials.gov retrieval that expanded the original 283-record candidate retrieval to 351 unique NCT IDs. It is reconstructed from the retained `scratch/query_results_summary.json`, `scratch/all_new_studies.json`, `scratch/candidates_full.json`, the 17 committed `scratch/test_query_*.json` result artifacts, and `scratch/find_missed_studies.py`.

- **Original retrieval preserved at**: `data/raw/candidates_raw.json` (283 records; 283 unique NCT IDs)
- **Supplementary result artifacts**: 17 query-result JSON files, numbered 0 through 16
- **Supplementary retrieval date/time**: unavailable in the result JSON and scripts. The artifacts were committed on 2026-08-16 at 10:55:07 -05:00, but a Git commit time is not an exact retrieval timestamp.
- **API/tool**: ClinicalTrials.gov API v2 through the Google Antigravity Science ClinicalTrials.gov wrapper script `clinical_trials_api.py`, invoked with `uv run ... search --term <QUERY> --fields NCTId,BriefTitle,BriefSummary,StudyType,OverallStatus,ArmsInterventionsModule,ConditionsModule,EligibilityModule,DesignModule --limit 1000 --count-total --output <FILE>`.
- **Comparison rule**: each query result was compared by NCT ID with the 283 IDs in the original raw retrieval. “New IDs” below means absent from the original 283, not necessarily first discovered by that particular supplementary query; the same new ID can therefore appear under more than one query.
- **Searches rerun for this reconstruction**: none.

## Supplementary queries

### Query 0

- **Exact query text**: `("trans women" OR "trans men" OR "trans woman" OR "trans man") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)`
- **Records returned**: 31 (reported total count: 31)
- **Overlap with original 283**: 31
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 1

- **Exact query text**: `(transfeminine OR transmasculine OR "trans-feminine" OR "trans-masculine") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)`
- **Records returned**: 11 (reported total count: 11)
- **Overlap with original 283**: 11
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 2

- **Exact query text**: `(nonbinary OR "non-binary") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)`
- **Records returned**: 20 (reported total count: 20)
- **Overlap with original 283**: 20
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 3

- **Exact query text**: `("gender dysphoria" OR "gender identity disorder") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)`
- **Records returned**: 61 (reported total count: 61)
- **Overlap with original 283**: 61
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 4

- **Exact query text**: `("gender non-conforming" OR "gender nonconforming") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)`
- **Records returned**: 7 (reported total count: 7)
- **Overlap with original 283**: 6
- **IDs absent from original 283**: 1
- **New NCT IDs**: `NCT03528135`

### Query 5

- **Exact query text**: `"gender-affirming hormone therapy" OR "gender affirming hormone therapy" OR "gender affirming hormone" OR "gender affirming hormones"`
- **Records returned**: 50 (reported total count: 50)
- **Overlap with original 283**: 48
- **IDs absent from original 283**: 2
- **New NCT IDs**: `NCT05853120`, `NCT06939257`

### Query 6

- **Exact query text**: `"gender-affirming hormone" OR "gender-affirming hormones"`
- **Records returned**: 50 (reported total count: 50)
- **Overlap with original 283**: 48
- **IDs absent from original 283**: 2
- **New NCT IDs**: `NCT05853120`, `NCT06939257`

### Query 7

- **Exact query text**: `GAHT`
- **Records returned**: 30 (reported total count: 30)
- **Overlap with original 283**: 30
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 8

- **Exact query text**: `"cross-sex hormone" OR "cross-sex hormones" OR "cross sex hormone" OR "cross sex hormones"`
- **Records returned**: 14 (reported total count: 14)
- **Overlap with original 283**: 14
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 9

- **Exact query text**: `("gender affirmation" OR "gender transition") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)`
- **Records returned**: 14 (reported total count: 14)
- **Overlap with original 283**: 14
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 10

- **Exact query text**: `(transgender OR transsexual OR "gender diverse" OR "gender incongruence" OR "gender dysphoria" OR "trans women" OR "trans men" OR transfeminine OR transmasculine OR nonbinary) AND (cyproterone OR bicalutamide OR finasteride OR dutasteride OR feminizing OR masculinizing OR "gender-affirming" OR "gender affirming" OR "cross-sex" OR "cross sex")`
- **Records returned**: 147 (reported total count: 147)
- **Overlap with original 283**: 105
- **IDs absent from original 283**: 42
- **New NCT IDs**: `NCT07181551`, `NCT07286123`, `NCT07480590`, `NCT06639763`, `NCT06443164`, `NCT06565663`, `NCT04378439`, `NCT06502353`, `NCT07075731`, `NCT04820088`, `NCT05016232`, `NCT06001307`, `NCT07681908`, `NCT06094257`, `NCT07194226`, `NCT05292820`, `NCT06428669`, `NCT07412509`, `NCT06880705`, `NCT01534351`, `NCT06844097`, `NCT05175170`, `NCT05534763`, `NCT04818580`, `NCT06390332`, `NCT06316102`, `NCT04217707`, `NCT05829928`, `NCT04096053`, `NCT04993469`, `NCT07147166`, `NCT07324967`, `NCT05897086`, `NCT05726903`, `NCT04491422`, `NCT04979338`, `NCT06070324`, `NCT05925361`, `NCT00985738`, `NCT06098781`, `NCT07017595`, `NCT07512856`

### Query 11

- **Exact query text**: `"gender affirming care" OR "gender-affirming care"`
- **Records returned**: 20 (reported total count: 20)
- **Overlap with original 283**: 10
- **IDs absent from original 283**: 10
- **New NCT IDs**: `NCT07480590`, `NCT04378439`, `NCT07681908`, `NCT06939257`, `NCT06316102`, `NCT04096053`, `NCT07147166`, `NCT05726903`, `NCT07729644`, `NCT07512856`

### Query 12

- **Exact query text**: `"gender affirmation treatment" OR "gender-affirming treatment" OR "gender affirmation therapy" OR "gender-affirming therapy"`
- **Records returned**: 10 (reported total count: 10)
- **Overlap with original 283**: 8
- **IDs absent from original 283**: 2
- **New NCT IDs**: `NCT07194226`, `NCT05829928`

### Query 13

- **Exact query text**: `"feminizing hormone therapy" OR "masculinizing hormone therapy" OR "feminizing hormone" OR "masculinizing hormone" OR "feminizing hormones" OR "masculinizing hormones"`
- **Records returned**: 15 (reported total count: 15)
- **Overlap with original 283**: 15
- **IDs absent from original 283**: 0
- **New NCT IDs**: None

### Query 14

- **Exact query text**: `AREA[ConditionSearch]"Gender Dysphoria"`
- **Records returned**: 91 (reported total count: 91)
- **Overlap with original 283**: 51
- **IDs absent from original 283**: 40
- **New NCT IDs**: `NCT07286123`, `NCT07480590`, `NCT06639763`, `NCT06565663`, `NCT04478214`, `NCT03899896`, `NCT04290286`, `NCT05292820`, `NCT05097820`, `NCT06428669`, `NCT05273112`, `NCT04474366`, `NCT07412509`, `NCT04064671`, `NCT04573127`, `NCT05534763`, `NCT04265885`, `NCT04554849`, `NCT04217707`, `NCT05829928`, `NCT04993469`, `NCT03872648`, `NCT07147166`, `NCT03293771`, `NCT04160364`, `NCT05897086`, `NCT03643120`, `NCT06639776`, `NCT05726903`, `NCT05883553`, `NCT04979338`, `NCT05204732`, `NCT05126134`, `NCT05903911`, `NCT07661823`, `NCT05884307`, `NCT05925361`, `NCT03602222`, `NCT06098781`, `NCT07017595`

### Query 15

- **Exact query text**: `AREA[ConditionSearch]"Gender Incongruence"`
- **Records returned**: 91 (reported total count: 91)
- **Overlap with original 283**: 51
- **IDs absent from original 283**: 40
- **New NCT IDs**: `NCT07286123`, `NCT07480590`, `NCT06639763`, `NCT06565663`, `NCT04478214`, `NCT03899896`, `NCT04290286`, `NCT05292820`, `NCT05097820`, `NCT06428669`, `NCT05273112`, `NCT04474366`, `NCT07412509`, `NCT04064671`, `NCT04573127`, `NCT05534763`, `NCT04265885`, `NCT04554849`, `NCT04217707`, `NCT05829928`, `NCT04993469`, `NCT03872648`, `NCT07147166`, `NCT03293771`, `NCT04160364`, `NCT05897086`, `NCT03643120`, `NCT06639776`, `NCT05726903`, `NCT05883553`, `NCT04979338`, `NCT05204732`, `NCT05126134`, `NCT05903911`, `NCT07661823`, `NCT05884307`, `NCT05925361`, `NCT03602222`, `NCT06098781`, `NCT07017595`

### Query 16

- **Exact query text**: `transgender AND (bicalutamide OR cyproterone OR dutasteride OR finasteride)`
- **Records returned**: 21 (reported total count: 21)
- **Overlap with original 283**: 18
- **IDs absent from original 283**: 3
- **New NCT IDs**: `NCT01534351`, `NCT05175170`, `NCT00985738`

## Deduplicated supplementary addition

The per-query new-ID lists above deduplicate to **68 unique NCT IDs**:

`NCT00985738`, `NCT01534351`, `NCT03293771`, `NCT03528135`, `NCT03602222`, `NCT03643120`, `NCT03872648`, `NCT03899896`, `NCT04064671`, `NCT04096053`, `NCT04160364`, `NCT04217707`, `NCT04265885`, `NCT04290286`, `NCT04378439`, `NCT04474366`, `NCT04478214`, `NCT04491422`, `NCT04554849`, `NCT04573127`, `NCT04818580`, `NCT04820088`, `NCT04979338`, `NCT04993469`, `NCT05016232`, `NCT05097820`, `NCT05126134`, `NCT05175170`, `NCT05204732`, `NCT05273112`, `NCT05292820`, `NCT05534763`, `NCT05726903`, `NCT05829928`, `NCT05853120`, `NCT05883553`, `NCT05884307`, `NCT05897086`, `NCT05903911`, `NCT05925361`, `NCT06001307`, `NCT06070324`, `NCT06094257`, `NCT06098781`, `NCT06316102`, `NCT06390332`, `NCT06428669`, `NCT06443164`, `NCT06502353`, `NCT06565663`, `NCT06639763`, `NCT06639776`, `NCT06844097`, `NCT06880705`, `NCT06939257`, `NCT07017595`, `NCT07075731`, `NCT07147166`, `NCT07181551`, `NCT07194226`, `NCT07286123`, `NCT07324967`, `NCT07412509`, `NCT07480590`, `NCT07512856`, `NCT07661823`, `NCT07681908`, `NCT07729644`

Merging those 68 IDs with the original 283 produced `scratch/candidates_full.json` with **351 records and 351 unique NCT IDs**. The original 283 IDs are all present in the combined artifact, and the 68-ID set difference exactly matches `scratch/all_new_studies.json`.

## Limitations

- Exact supplementary retrieval date/time is not recoverable from the retained artifacts; only the later Git commit time is available.
- The saved scripts identify the wrapper and command arguments, but the retained result JSON does not record the ClinicalTrials.gov API response timestamp, wrapper version, API version string, request URL, or pagination/request logs.
- The 17 queries overlap substantially. Per-query “new” counts are relative to the original 283 and must not be added together.
- Supplementary searches broaden candidate retrieval only. Query matches do not establish scientific eligibility under `PROTOCOL.md`.
- The combined registry artifact retains brief summaries for 68 records and does not retain a primary-outcomes module for the 351 records. The review dataset therefore exposes all context available in the preserved combined artifact but cannot reconstruct fields that were not saved.
