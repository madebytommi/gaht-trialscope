# GAHT TrialScope: Corrective Pass Report and Repair Clarification

## 1. What the corrective pass changed

The earlier corrective pass preserved the original 283-record raw retrieval, ran 17 supplementary ClinicalTrials.gov queries, and added 68 NCT IDs that were absent from the original retrieval. The resulting candidate universe contains 351 unique NCT IDs.

The supplementary retrieval is now documented in `data/raw/corrective_provenance.md`. That provenance record separates the original retrieval, per-query supplementary results, the 68-ID deduplicated addition, and the final combined universe.

## 2. Historical screening output

The following table records what the earlier corrective pass produced. It is retained as history, not presented as a validated screening result.

| Metric | Original pass | Earlier corrective heuristic | Difference |
|---|---:|---:|---:|
| Total candidates | 283 | 351 | +68 |
| Includes | 70 | 115 | +45 |
| Excludes | 54 | 236 | +182 |
| Uncertains | 159 | 0 | -159 |

The 115/236/0 distribution came from keyword rules in the former `scratch/build_dataset.py`. That script assigned `include` when transgender/gender-diverse and hormone keywords co-occurred, and otherwise forced a record to `exclude` after a small set of additional keyword checks. It did not perform semantic or record-level scientific screening. Zero uncertain records therefore reflects the forced binary implementation; it does not demonstrate that ambiguity was resolved or that the method succeeded.

`data/candidate_studies.csv` preserves that historical heuristic output unchanged.

## 3. Narrow repair

The repaired `scratch/build_dataset.py` performs deterministic data work only: loading the preserved 351-record registry artifact, validating and deduplicating NCT IDs, extracting registry context, validating the three allowed preliminary screening values (`include`, `exclude`, and `uncertain`), merging screening metadata from data files, and writing `data/screening_review.csv`.

It no longer searches study text for population or hormone keywords and no longer makes inclusion or exclusion decisions. The new review dataset labels 344 carried-forward decisions as `legacy_keyword_heuristic_unverified`. Those values are preliminary metadata only and still require record-level and human review. Human-screening fields are intentionally blank.

## 4. Requested boundary-case review

The seven requested records were reviewed against the actual registry context preserved in `scratch/candidates_full.json` and the two criteria in `PROTOCOL.md`. These remain AI-assisted preliminary decisions, not human-verified decisions.

- **NCT06247267 — include**: transgender patients are an explicit population, and estradiol/spironolactone or testosterone is explicitly studied during hormonal transition.
- **NCT05489159 — include**: transgender and nonbinary adolescents are followed as they initiate masculinizing or feminizing GAHT.
- **NCT03725280 — include**: transgender men before versus after testosterone therapy are explicit study groups, so GAHT is an exposure/comparison despite the IVF setting.
- **NCT06939257 — include**: gender-minority adults initiating GAHT are explicitly compared with gender-minority adults not using GAHT for pain outcomes.
- **NCT05726903 — exclude**: the population criterion is met, but depot medroxyprogesterone is studied for contraception and contraceptive counseling, not as GAHT.
- **NCT05891795 — include**: transgender male and gender-diverse patients on masculinizing hormone therapy are studied for acne arising after that therapy, making GAHT an explicit exposure.
- **NCT06969326 — exclude**: topical estradiol is a postoperative treatment after hysterectomy rather than GAHT, while testosterone use is background eligibility information rather than the study variable.

These decisions are stored separately in `data/ai_boundary_case_reviews.csv` so Python merges, but does not generate, the scientific judgments. The two exclusions reverse the earlier heuristic classifications while preserving those earlier values in the review dataset's `legacy_preliminary_screening` fields.

## 5. Current readiness and limitations

`data/screening_review.csv` contains all 351 candidates with title, study type, status, conditions, available brief summary, intervention details, available study-population text, full retained eligibility text, preliminary screening provenance, and blank human-review fields. The combined scratch artifact did not retain primary-outcomes modules and retained brief summaries for only 68 records, so those fields cannot be reconstructed without another registry retrieval; this limitation is exposed rather than concealed.

The dataset is ready for record-level human screening, with minor source-context limitations noted above. It is **not ready for downstream descriptive analysis** because 344 classifications remain unverified legacy heuristic metadata and none of the 351 records has a human screening decision.
