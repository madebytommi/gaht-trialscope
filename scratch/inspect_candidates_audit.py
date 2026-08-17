import json
import re

with open("scratch/detailed_records.json", encoding="utf-8") as f:
    records = json.load(f)

# Let's check all 351 records for actual TGD terms vs false positive word stems
true_tgd_patterns = [
    r"\btransgender\b", r"\btranssexual\b", r"\btranssexualism\b",
    r"\btrans\s+wom[ae]n\b", r"\btrans\s+m[ae]n\b", r"\btrans\s+female\b", r"\btrans\s+male\b",
    r"\btransfemale\b", r"\btransmale\b",
    r"\btransfeminine\b", r"\btransmasculine\b", r"\bnon-?binary\b",
    r"\bgender[\s-]diverse\b", r"\bgender[\s-]diversity\b",
    r"\bgender[\s-]dysphoria\b", r"\bgender[\s-]dysphoric\b",
    r"\bgender[\s-]identity[\s-]disorder\b", r"\bgid\b",
    r"\bgender[\s-]incongruen\w*\b", r"\bgender[\s-]minority\b", r"\bgender[\s-]minorities\b",
    r"\bgender[\s-]non-?conforming\b", r"\bgender[\s-]variant\b",
    r"\bmtf\b", r"\bftm\b", r"\bmale-to-female\b", r"\bfemale-to-male\b",
    r"\btrans\s+people\b", r"\btrans\s+individuals\b", r"\btrans\s+youth\b",
    r"\btrans\s+adolescents\b", r"\btrans\s+adults\b", r"\btrans\s+patients\b",
    r"\btrans\s+population\b", r"\btrans\s+participants\b"
]
true_tgd_regex = re.compile("|".join(true_tgd_patterns), re.IGNORECASE)

records_with_true_tgd = []
records_without_true_tgd = []

for r in records:
    full_text = r["full_text"]
    matches = true_tgd_regex.findall(full_text)
    if matches:
        records_with_true_tgd.append((r["nct_id"], r["brief_title"], list(set(matches))))
    else:
        records_without_true_tgd.append((r["nct_id"], r["brief_title"]))

print(f"Records with verified TGD terms: {len(records_with_true_tgd)}")
print(f"Records without verified TGD terms: {len(records_without_true_tgd)}")
assert len(records_with_true_tgd) + len(records_without_true_tgd) == 351

# Let's inspect the records without verified TGD terms to ensure 100% that not a single one has a TGD population!
print("\nVerifying records without verified TGD terms (first 30):")
for nct, title in records_without_true_tgd[:30]:
    print(f"  {nct}: {title}")
