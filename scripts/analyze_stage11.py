#!/usr/bin/env python3
"""Run Stage 11 descriptive analysis for the frozen GAHT TrialScope dataset.

This script is deterministic descriptive data plumbing. It reads only the frozen
included-study dataset created in Stage 10 and writes traceable study-level
derivations plus aggregate summaries. It does not assess clinical safety,
effectiveness, appropriateness, or treatment superiority.
"""

import csv
import json
import math
import re
import statistics
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INPUT = DATA / "frozen" / "included_studies.csv"
OUTDIR = DATA / "analysis"
STUDY_LEVEL = OUTDIR / "stage11_study_level.csv"
COUNTS_FILE = OUTDIR / "stage11_counts.csv"
SUMMARY_FILE = OUTDIR / "stage11_summary.json"
REPORT_FILE = OUTDIR / "STAGE11_REPORT.md"
EXPECTED_INCLUDED = 125


def clean(value):
    if value is None:
        return ""
    return " ".join(str(value).split())


def load_rows():
    with INPUT.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    ids = [clean(row.get("nct_id")) for row in rows]
    if len(rows) != EXPECTED_INCLUDED:
        raise ValueError(f"Expected {EXPECTED_INCLUDED} frozen includes, found {len(rows)}")
    if any(not nct_id for nct_id in ids):
        raise ValueError("Frozen included-study dataset contains missing NCT ID")
    if len(set(ids)) != len(ids):
        raise ValueError("Frozen included-study dataset contains duplicate NCT IDs")
    invalid = [row["nct_id"] for row in rows if clean(row.get("final_screening")) != "include"]
    if invalid:
        raise ValueError(f"Non-include rows found in frozen include file: {invalid[:10]}")
    return rows


def year_from_date(value):
    match = re.match(r"^(\d{4})", clean(value))
    return int(match.group(1)) if match else None


def number(value):
    text = clean(value).replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def age_to_years(value):
    text = clean(value).lower()
    if not text:
        return None
    match = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*(year|years|month|months|week|weeks|day|days)", text)
    if not match:
        return None
    n = float(match.group(1))
    unit = match.group(2)
    if unit.startswith("year"):
        return n
    if unit.startswith("month"):
        return n / 12.0
    if unit.startswith("week"):
        return n / 52.1429
    return n / 365.2425


def derive_age_group(minimum_age, maximum_age):
    lo = age_to_years(minimum_age)
    hi = age_to_years(maximum_age)
    if lo is None and hi is None:
        return "age_not_reported"
    if hi is not None and hi < 18:
        return "youth_only"
    if lo is not None and lo >= 18:
        return "adult_only"
    if lo is not None and lo < 18 and hi is not None and hi >= 18:
        return "youth_and_adult"
    if lo is not None and lo < 18 and hi is None:
        return "includes_youth_upper_unspecified"
    return "age_bounds_incomplete"


HORMONE_PATTERNS = {
    "testosterone_or_androgen": [
        r"\btestosterone\b", r"\bandrogen(?:s|ic)?\b", r"masculiniz(?:ing|ation)",
    ],
    "estradiol_or_estrogen": [
        r"\bestradiol\b", r"\bestrogen(?:s|ic)?\b", r"oestrogen", r"feminiz(?:ing|ation)",
    ],
    "progesterone_or_progestin": [
        r"\bprogesterone\b", r"\bprogestin\b", r"medroxyprogesterone",
    ],
    "antiandrogen": [
        r"anti[- ]?androgen", r"spironolactone", r"cyproterone", r"bicalutamide",
        r"finasteride", r"dutasteride", r"5[- ]alpha reductase",
    ],
    "gnrh_or_puberty_suppression": [
        r"\bgnrh\b", r"gonadotropin[- ]releasing", r"leuprolide", r"triptorelin",
        r"histrelin", r"pubert(?:y|al) suppress", r"pubert(?:y|al) block",
    ],
}


def derive_hormone_categories(row):
    text = " ".join(
        clean(row.get(field)).lower()
        for field in ["brief_title", "interventions", "adjudication_reason", "conditions"]
    )
    cats = []
    for category, patterns in HORMONE_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.I) for pattern in patterns):
            cats.append(category)
    if not cats:
        if re.search(r"\bgaht\b|gender[- ]affirming hormone|cross[- ]sex hormone|hormone therap", text, re.I):
            cats.append("gaht_unspecified")
        else:
            cats.append("hormone_role_not_normalized_from_frozen_text")
    return cats


def split_countries(value):
    text = clean(value)
    if not text:
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def percentile(values, p):
    if not values:
        return None
    values = sorted(values)
    if len(values) == 1:
        return values[0]
    k = (len(values) - 1) * p
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return values[lo]
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def pct(count, total):
    return round((count / total) * 100.0, 1) if total else 0.0


def fmt_num(value, digits=1):
    if value is None:
        return "NA"
    if abs(value - round(value)) < 1e-9:
        return f"{int(round(value)):,}"
    return f"{value:,.{digits}f}"


def sorted_counter(counter):
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def derive(rows):
    out = []
    for row in rows:
        reg_year = year_from_date(row.get("study_first_post_date"))
        start_year = year_from_date(row.get("start_date"))
        countries = split_countries(row.get("countries"))
        hormone_categories = derive_hormone_categories(row)
        enrollment = number(row.get("enrollment"))
        out.append({
            **row,
            "registration_year": "" if reg_year is None else str(reg_year),
            "start_year": "" if start_year is None else str(start_year),
            "age_group": derive_age_group(row.get("minimum_age"), row.get("maximum_age")),
            "hormone_categories": "; ".join(hormone_categories),
            "country_count": str(len(countries)),
            "is_multicountry": "true" if len(countries) > 1 else "false",
            "enrollment_numeric": "" if enrollment is None else str(int(enrollment) if enrollment.is_integer() else enrollment),
        })
    return out


def build_summary(rows):
    n = len(rows)
    registration_year = Counter()
    study_type = Counter()
    status = Counter()
    age_group = Counter()
    hormone = Counter()
    country = Counter()
    sponsor = Counter()
    results = Counter()
    enrollment_values = []
    missing = Counter()
    multicountry = 0

    for row in rows:
        year = clean(row.get("registration_year"))
        registration_year[year if year else "missing"] += 1
        study_type[clean(row.get("study_type")) or "missing"] += 1
        status[clean(row.get("overall_status")) or "missing"] += 1
        age_group[clean(row.get("age_group")) or "missing"] += 1
        for cat in [c.strip() for c in clean(row.get("hormone_categories")).split(";") if c.strip()]:
            hormone[cat] += 1
        countries = split_countries(row.get("countries"))
        if not countries:
            country["missing"] += 1
        else:
            country.update(countries)
            if len(countries) > 1:
                multicountry += 1
        sponsor[clean(row.get("lead_sponsor")) or "missing"] += 1
        has_results = clean(row.get("has_results")).lower()
        results["results_posted" if has_results == "true" else "no_results_posted"] += 1
        value = number(row.get("enrollment_numeric"))
        if value is not None:
            enrollment_values.append(value)

        for field in [
            "study_first_post_date", "study_type", "overall_status", "start_date", "enrollment",
            "lead_sponsor", "countries", "minimum_age", "maximum_age", "conditions",
        ]:
            if not clean(row.get(field)):
                missing[field] += 1

    known_years = [int(y) for y in registration_year if y != "missing"]
    enrollment_summary = {
        "reported_n": len(enrollment_values),
        "missing_n": n - len(enrollment_values),
        "total_registered_enrollment": int(sum(enrollment_values)) if enrollment_values else 0,
        "mean": round(statistics.mean(enrollment_values), 1) if enrollment_values else None,
        "median": round(statistics.median(enrollment_values), 1) if enrollment_values else None,
        "q1": round(percentile(enrollment_values, 0.25), 1) if enrollment_values else None,
        "q3": round(percentile(enrollment_values, 0.75), 1) if enrollment_values else None,
        "min": min(enrollment_values) if enrollment_values else None,
        "max": max(enrollment_values) if enrollment_values else None,
    }

    summary = {
        "included_studies": n,
        "registration_year_range": {
            "first": min(known_years) if known_years else None,
            "last": max(known_years) if known_years else None,
            "missing_n": registration_year.get("missing", 0),
        },
        "registration_year_counts": dict(sorted(registration_year.items(), key=lambda x: (x[0] == "missing", x[0]))),
        "study_type_counts": sorted_counter(study_type),
        "status_counts": sorted_counter(status),
        "age_group_counts": sorted_counter(age_group),
        "hormone_category_counts_multilabel": sorted_counter(hormone),
        "results_availability_counts": sorted_counter(results),
        "country_counts_multilabel": sorted_counter(country),
        "unique_reported_countries": len([c for c in country if c != "missing"]),
        "multicountry_studies": multicountry,
        "sponsor_counts": sorted_counter(sponsor),
        "unique_lead_sponsors": len([s for s in sponsor if s != "missing"]),
        "enrollment": enrollment_summary,
        "missingness_counts": dict(sorted(missing.items())),
    }
    return summary


def write_study_level(rows):
    fieldnames = list(rows[0].keys())
    with STUDY_LEVEL.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_counts(summary):
    records = []
    total = summary["included_studies"]
    dimensions = [
        ("registration_year", summary["registration_year_counts"]),
        ("study_type", summary["study_type_counts"]),
        ("overall_status", summary["status_counts"]),
        ("age_group", summary["age_group_counts"]),
        ("hormone_category_multilabel", summary["hormone_category_counts_multilabel"]),
        ("results_availability", summary["results_availability_counts"]),
        ("country_multilabel", summary["country_counts_multilabel"]),
        ("lead_sponsor", summary["sponsor_counts"]),
    ]
    for dimension, counts in dimensions:
        for category, count in counts.items():
            records.append({
                "dimension": dimension,
                "category": category,
                "count": count,
                "percent_of_125": pct(count, total),
            })
    with COUNTS_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["dimension", "category", "count", "percent_of_125"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(v).replace("|", "\\|") for v in row) + " |")
    return "\n".join(lines)


def top_rows(counts, total, limit=10):
    return [[name, count, f"{pct(count, total):.1f}%"] for name, count in list(counts.items())[:limit]]


def write_report(summary):
    n = summary["included_studies"]
    yr = summary["registration_year_range"]
    study_type = summary["study_type_counts"]
    statuses = summary["status_counts"]
    ages = summary["age_group_counts"]
    hormones = summary["hormone_category_counts_multilabel"]
    results = summary["results_availability_counts"]
    countries = summary["country_counts_multilabel"]
    sponsors = summary["sponsor_counts"]
    enroll = summary["enrollment"]
    missing = summary["missingness_counts"]

    year_rows = [[year, count, f"{pct(count, n):.1f}%"] for year, count in summary["registration_year_counts"].items()]
    design_rows = top_rows(study_type, n, 20)
    status_rows = top_rows(statuses, n, 20)
    age_rows = top_rows(ages, n, 20)
    hormone_rows = top_rows(hormones, n, 20)
    result_rows = top_rows(results, n, 10)
    country_rows = top_rows(countries, n, 15)
    sponsor_rows = top_rows(sponsors, n, 15)
    missing_rows = [[field, count, f"{pct(count, n):.1f}%"] for field, count in missing.items()]

    report = f"""# GAHT TrialScope — Stage 11 Descriptive Analysis

This is the first complete descriptive analysis of the **{n} studies** in `data/frozen/included_studies.csv`. It describes the ClinicalTrials.gov registration landscape defined by the project protocol; it does **not** estimate treatment safety, effectiveness, or clinical appropriateness.

## Headline snapshot

- Included registered studies: **{n}**
- Registration-year span among records with a posted date: **{yr['first']}–{yr['last']}**
- Interventional studies: **{study_type.get('INTERVENTIONAL', 0)} ({pct(study_type.get('INTERVENTIONAL', 0), n):.1f}%)**
- Observational studies: **{study_type.get('OBSERVATIONAL', 0)} ({pct(study_type.get('OBSERVATIONAL', 0), n):.1f}%)**
- Studies with ClinicalTrials.gov results posted: **{results.get('results_posted', 0)} ({pct(results.get('results_posted', 0), n):.1f}%)**
- Unique reported countries: **{summary['unique_reported_countries']}**
- Multicountry studies: **{summary['multicountry_studies']} ({pct(summary['multicountry_studies'], n):.1f}%)**
- Unique reported lead sponsors: **{summary['unique_lead_sponsors']}**
- Enrollment reported for: **{enroll['reported_n']}/{n} studies**
- Sum of registered enrollment values: **{enroll['total_registered_enrollment']:,}** participants/records (descriptive only; not a deduplicated person count across studies)
- Median registered enrollment: **{fmt_num(enroll['median'])}** (IQR **{fmt_num(enroll['q1'])}–{fmt_num(enroll['q3'])}**)

## Registration year

Registration year is derived from `study_first_post_date`, i.e. the year the record was first posted on ClinicalTrials.gov.

{md_table(['Year', 'Studies', '% of 125'], year_rows)}

## Study design

{md_table(['Study type', 'Studies', '% of 125'], design_rows)}

## Recruitment / overall status

{md_table(['Status', 'Studies', '% of 125'], status_rows)}

## Hormone intervention or exposure

These are **deterministic multi-label normalization tags**, not a new screening decision. Tags are derived from the frozen study title, intervention text, conditions, and recorded adjudication reason. A single study can contribute to multiple categories, so percentages do not sum to 100%.

{md_table(['Hormone/exposure tag', 'Studies', '% of 125'], hormone_rows)}

Any row tagged `hormone_role_not_normalized_from_frozen_text` remains an included GAHT study; the tag means the specific hormone class was not recoverable from the compact frozen text fields and should be enriched before publication-quality hormone-subtype charts.

## Participant age grouping

Age groups are derived only from registered minimum/maximum eligibility ages:

- `youth_only`: registered maximum age <18 years.
- `adult_only`: registered minimum age ≥18 years.
- `youth_and_adult`: registered minimum <18 and maximum ≥18.
- `includes_youth_upper_unspecified`: minimum <18 with no registered maximum.
- `age_bounds_incomplete` / `age_not_reported`: insufficient registered bounds for the above categories.

{md_table(['Age group', 'Studies', '% of 125'], age_rows)}

## Enrollment

- Reported: **{enroll['reported_n']}** studies
- Missing: **{enroll['missing_n']}** studies
- Total of registered enrollment fields: **{enroll['total_registered_enrollment']:,}**
- Mean: **{fmt_num(enroll['mean'])}**
- Median: **{fmt_num(enroll['median'])}**
- Q1–Q3: **{fmt_num(enroll['q1'])}–{fmt_num(enroll['q3'])}**
- Minimum–maximum: **{fmt_num(enroll['min'])}–{fmt_num(enroll['max'])}**

The sum above is a sum of registry enrollment fields, not a claim of unique individuals represented across the literature.

## Geography

Country counts are multi-label: multinational studies are counted once in each reported country.

{md_table(['Country', 'Studies', '% of 125'], country_rows)}

Unique reported countries: **{summary['unique_reported_countries']}**. Multicountry studies: **{summary['multicountry_studies']}**.

## Lead sponsors

{md_table(['Lead sponsor', 'Studies', '% of 125'], sponsor_rows)}

Unique reported lead sponsors: **{summary['unique_lead_sponsors']}**.

## Results availability

{md_table(['ClinicalTrials.gov results', 'Studies', '% of 125'], result_rows)}

`has_results` reflects posted results on the registry snapshot, not whether a study has publications elsewhere.

## Missingness relevant to interpretation

{md_table(['Field', 'Missing', '% of 125'], missing_rows)}

## Reproducibility outputs

- `stage11_study_level.csv` — all 125 included studies plus derived registration year, start year, age group, hormone-category tags, country count, multicountry flag, and numeric enrollment.
- `stage11_counts.csv` — long-form aggregate counts for downstream tables/charts.
- `stage11_summary.json` — machine-readable aggregate analysis.
- `STAGE11_REPORT.md` — this report.

## Interpretation boundary

This analysis describes **registered GAHT research captured by this protocol and ClinicalTrials.gov snapshot**. It does not represent all published GAHT research, and no distribution here should be interpreted as evidence that a treatment is safe, unsafe, effective, ineffective, preferable, or clinically appropriate.
"""
    REPORT_FILE.write_text(report, encoding="utf-8")


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    source = load_rows()
    rows = derive(source)
    summary = build_summary(rows)
    write_study_level(rows)
    write_counts(summary)
    SUMMARY_FILE.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_report(summary)

    print(
        "Stage 11 analysis complete: "
        f"{summary['included_studies']} included studies; "
        f"{summary['study_type_counts'].get('INTERVENTIONAL', 0)} interventional / "
        f"{summary['study_type_counts'].get('OBSERVATIONAL', 0)} observational; "
        f"{summary['results_availability_counts'].get('results_posted', 0)} with posted results."
    )


if __name__ == "__main__":
    main()
