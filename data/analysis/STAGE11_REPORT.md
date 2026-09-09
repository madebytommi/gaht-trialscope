# GAHT TrialScope — Stage 11 Descriptive Analysis

This is the first complete descriptive analysis of the **125 studies** in `data/frozen/included_studies.csv`. It describes the ClinicalTrials.gov registration landscape defined by the project protocol; it does **not** estimate treatment safety, effectiveness, or clinical appropriateness.

## Headline snapshot

- Included registered studies: **125**
- Registration-year span among records with a posted date: **2005–2026**
- Interventional studies: **48 (38.4%)**
- Observational studies: **77 (61.6%)**
- Studies with ClinicalTrials.gov results posted: **10 (8.0%)**
- Unique reported countries: **24**
- Multicountry studies: **4 (3.2%)**
- Unique reported lead sponsors: **80**
- Enrollment reported for: **125/125 studies**
- Sum of registered enrollment values: **30,955** participants/records (descriptive only; not a deduplicated person count across studies)
- Median registered enrollment: **70** (IQR **26–160**)

## Registration year

Registration year is derived from `study_first_post_date`, i.e. the year the record was first posted on ClinicalTrials.gov.

| Year | Studies | % of 125 |
| --- | --- | --- |
| 2005 | 1 | 0.8% |
| 2010 | 2 | 1.6% |
| 2011 | 1 | 0.8% |
| 2014 | 3 | 2.4% |
| 2015 | 2 | 1.6% |
| 2016 | 2 | 1.6% |
| 2017 | 4 | 3.2% |
| 2018 | 9 | 7.2% |
| 2019 | 6 | 4.8% |
| 2020 | 20 | 16.0% |
| 2021 | 13 | 10.4% |
| 2022 | 14 | 11.2% |
| 2023 | 10 | 8.0% |
| 2024 | 15 | 12.0% |
| 2025 | 11 | 8.8% |
| 2026 | 7 | 5.6% |
| missing | 5 | 4.0% |

## Study design

| Study type | Studies | % of 125 |
| --- | --- | --- |
| OBSERVATIONAL | 77 | 61.6% |
| INTERVENTIONAL | 48 | 38.4% |

## Recruitment / overall status

| Status | Studies | % of 125 |
| --- | --- | --- |
| COMPLETED | 50 | 40.0% |
| RECRUITING | 31 | 24.8% |
| UNKNOWN | 12 | 9.6% |
| ACTIVE_NOT_RECRUITING | 10 | 8.0% |
| TERMINATED | 8 | 6.4% |
| NOT_YET_RECRUITING | 6 | 4.8% |
| WITHDRAWN | 4 | 3.2% |
| ENROLLING_BY_INVITATION | 3 | 2.4% |
| SUSPENDED | 1 | 0.8% |

## Hormone intervention or exposure

These are **deterministic multi-label normalization tags**, not a new screening decision. Tags are derived from the frozen study title, intervention text, conditions, and recorded adjudication reason. A single study can contribute to multiple categories, so percentages do not sum to 100%.

| Hormone/exposure tag | Studies | % of 125 |
| --- | --- | --- |
| testosterone_or_androgen | 50 | 40.0% |
| estradiol_or_estrogen | 46 | 36.8% |
| gaht_unspecified | 39 | 31.2% |
| hormone_role_not_normalized_from_frozen_text | 11 | 8.8% |
| antiandrogen | 9 | 7.2% |
| gnrh_or_puberty_suppression | 5 | 4.0% |
| progesterone_or_progestin | 4 | 3.2% |

Any row tagged `hormone_role_not_normalized_from_frozen_text` remains an included GAHT study; the tag means the specific hormone class was not recoverable from the compact frozen text fields and should be enriched before publication-quality hormone-subtype charts.

## Participant age grouping

Age groups are derived only from registered minimum/maximum eligibility ages:

- `youth_only`: registered maximum age <18 years.
- `adult_only`: registered minimum age ≥18 years.
- `youth_and_adult`: registered minimum <18 and maximum ≥18.
- `includes_youth_upper_unspecified`: minimum <18 with no registered maximum.
- `age_bounds_incomplete` / `age_not_reported`: insufficient registered bounds for the above categories.

| Age group | Studies | % of 125 |
| --- | --- | --- |
| adult_only | 98 | 78.4% |
| includes_youth_upper_unspecified | 12 | 9.6% |
| youth_and_adult | 9 | 7.2% |
| youth_only | 3 | 2.4% |
| age_not_reported | 2 | 1.6% |
| age_bounds_incomplete | 1 | 0.8% |

## Enrollment

- Reported: **125** studies
- Missing: **0** studies
- Total of registered enrollment fields: **30,955**
- Mean: **247.6**
- Median: **70**
- Q1–Q3: **26–160**
- Minimum–maximum: **0–7,348**

The sum above is a sum of registry enrollment fields, not a claim of unique individuals represented across the literature.

## Geography

Country counts are multi-label: multinational studies are counted once in each reported country.

| Country | Studies | % of 125 |
| --- | --- | --- |
| United States | 55 | 44.0% |
| missing | 11 | 8.8% |
| Austria | 8 | 6.4% |
| France | 7 | 5.6% |
| Thailand | 7 | 5.6% |
| Denmark | 5 | 4.0% |
| Germany | 5 | 4.0% |
| Italy | 5 | 4.0% |
| Brazil | 4 | 3.2% |
| Canada | 3 | 2.4% |
| China | 2 | 1.6% |
| Israel | 2 | 1.6% |
| Netherlands | 2 | 1.6% |
| Norway | 2 | 1.6% |
| Peru | 2 | 1.6% |

Unique reported countries: **24**. Multicountry studies: **4**.

## Lead sponsors

| Lead sponsor | Studies | % of 125 |
| --- | --- | --- |
| University of Colorado, Denver | 9 | 7.2% |
| Medical University of Vienna | 6 | 4.8% |
| University of California, San Diego | 6 | 4.8% |
| missing | 5 | 4.0% |
| Medical College of Wisconsin | 4 | 3.2% |
| Central Hospital, Nancy, France | 3 | 2.4% |
| Tel-Aviv Sourasky Medical Center | 3 | 2.4% |
| Thai Red Cross AIDS Research Centre | 3 | 2.4% |
| Chulalongkorn University | 2 | 1.6% |
| Emory University | 2 | 1.6% |
| IRCCS Azienda Ospedaliero-Universitaria di Bologna | 2 | 1.6% |
| Johns Hopkins University | 2 | 1.6% |
| Massachusetts General Hospital | 2 | 1.6% |
| Mayo Clinic | 2 | 1.6% |
| Odense University Hospital | 2 | 1.6% |

Unique reported lead sponsors: **80**.

## Results availability

| ClinicalTrials.gov results | Studies | % of 125 |
| --- | --- | --- |
| no_results_posted | 115 | 92.0% |
| results_posted | 10 | 8.0% |

`has_results` reflects posted results on the registry snapshot, not whether a study has publications elsewhere.

## Missingness relevant to interpretation

| Field | Missing | % of 125 |
| --- | --- | --- |
| countries | 11 | 8.8% |
| lead_sponsor | 5 | 4.0% |
| maximum_age | 56 | 44.8% |
| minimum_age | 3 | 2.4% |
| start_date | 5 | 4.0% |
| study_first_post_date | 5 | 4.0% |

## Reproducibility outputs

- `stage11_study_level.csv` — all 125 included studies plus derived registration year, start year, age group, hormone-category tags, country count, multicountry flag, and numeric enrollment.
- `stage11_counts.csv` — long-form aggregate counts for downstream tables/charts.
- `stage11_summary.json` — machine-readable aggregate analysis.
- `STAGE11_REPORT.md` — this report.

## Interpretation boundary

This analysis describes **registered GAHT research captured by this protocol and ClinicalTrials.gov snapshot**. It does not represent all published GAHT research, and no distribution here should be interpreted as evidence that a treatment is safe, unsafe, effective, ineffective, preferable, or clinically appropriate.
