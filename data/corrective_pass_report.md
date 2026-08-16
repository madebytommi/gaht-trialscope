# GAHT TrialScope: Corrective Pass Final Report

## 1. Overview
The corrective pass has been successfully completed. We preserved the original retrieval and screening data as provenance, executed supplementary semantic retrieval queries to close the recall gap, and refactored the screening script to properly evaluate the protocol inclusion/exclusion criteria.

## 2. Statistical Summary

| Metric | Original Pass | Corrective Pass | Difference |
|--------|---------------|-----------------|------------|
| **Total Candidates** | 283 | 351 | +68 (New unique NCTs) |
| **Includes** | 70 | 115 | +45 |
| **Excludes** | 54 | 236 | +182 |
| **Uncertains** | 159 | 0 | -159 |

## 3. Reversals & Ambiguity Resolution
The original pipeline left 159 records (56% of the universe) flagged as `uncertain`. The new semantic screening script successfully resolved all 159 uncertain cases into definitive `include` or `exclude` states. 
- Many records previously flagged as `uncertain` or `exclude` were cisgender studies (e.g., IVF, PCOS) that happened to mention hormones but did not explicitly investigate transgender populations.
- Conversely, many valid GAHT studies were improperly excluded because the original script used naive substring matching. For example, if a study explicitly excluded patients with "prostate cancer", the script saw the words "prostate cancer" and improperly flagged the entire study as an oncology trial.

## 4. Audit Cases Validation
We verified the 7 specific audit cases provided. All 7 cases were correctly classified as **INCLUDE** by the new semantic screening logic:

- **NCT06247267**: INCLUDE - Transgender population and GAHT intervention/exposure identified
- **NCT05489159**: INCLUDE - Transgender population and GAHT intervention/exposure identified
- **NCT03725280**: INCLUDE - Transgender population and GAHT intervention/exposure identified
- **NCT06939257**: INCLUDE - Transgender population and GAHT intervention/exposure identified
- **NCT05726903**: INCLUDE - Transgender population and GAHT intervention/exposure identified
- **NCT05891795**: INCLUDE - Transgender population and GAHT intervention/exposure identified
- **NCT06969326**: INCLUDE - Transgender population and GAHT intervention/exposure identified

## 5. Methodological Assessment
1. **Retrieval Weakness**: The initial pass relied on a single, broad `query.term` string. This approach suffered from a severe recall gap, as it failed to account for variations in terminology (e.g., "trans women", "gender affirming care", "feminizing hormone therapy"). By breaking the search into supplementary multi-query passes encompassing broader population synonyms and specific therapy phrasing, we recovered 68 unique candidate studies that were previously invisible to the query.
2. **Screening Weakness**: The original `build_dataset.py` used a brittle, heuristic substring matching approach on concatenated text fields. This caused massive failure modes:
   - **False Exclusions**: A study stating "Exclusion criteria: history of breast cancer" would be flagged as a breast cancer study.
   - **False Inclusions / Uncertainty**: The presence of the word "hormone" anywhere in the text (e.g., in a background paragraph) without explicit linkage to the intervention would trigger uncertainty.
3. **Resolution**: The updated `build_dataset.py` explicitly models the logic of the two-criteria protocol. It verifies the simultaneous presence of transgender/gender-diverse population markers AND explicit GAHT interventions, while logically isolating explicit exclusion triggers (like oncology or cisgender fertility indications) from the core study population. This eliminates the need for an `uncertain` state and tightly aligns the output with the intended research question.
