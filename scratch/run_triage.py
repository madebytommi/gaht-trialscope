import csv
import json
import re
from pathlib import Path

REVIEW_CSV = Path("data/screening_review.csv")
ENRICHED_JSON = Path("data/raw/enrichment/enriched_studies.json")

# Load enriched full studies
with open(ENRICHED_JSON, encoding="utf-8") as f:
    enriched_data = json.load(f)

studies_by_nct = {
    s["protocolSection"]["identificationModule"]["nctId"]: s
    for s in enriched_data.get("studies", [])
}

# Load review CSV
with open(REVIEW_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    review_rows = list(reader)

print(f"Total review rows: {len(review_rows)}")
print(f"Total enriched studies: {len(studies_by_nct)}")

KNOWN_HUMAN_DECISIONS = {
    "NCT00023543": "exclude",
    "NCT00082082": "exclude",
    "NCT00146146": "include",
    "NCT00188708": "exclude",
    "NCT00450749": "exclude",
    "NCT00544882": "exclude",
    "NCT00608400": "exclude",
}

# Let's inspect each study's text content
# Keywords for TGD population
TGD_PATTERNS = [
    r"\btransgender\b", r"\btranssexual\b", r"\btranssexualism\b",
    r"\btrans\s+wom[ae]n\b", r"\btrans\s+m[ae]n\b", r"\btransfemale\b", r"\btransmale\b",
    r"\btransfeminine\b", r"\btransmasculine\b", r"\bnon-?binary\b",
    r"\bgender[\s-]diverse\b", r"\bgender[\s-]diversity\b",
    r"\bgender[\s-]dysphoria\b", r"\bgender[\s-]dysphoric\b",
    r"\bgender[\s-]identity[\s-]disorder\b", r"\bgid\b",
    r"\bgender[\s-]incongruen\w*\b", r"\bgender[\s-]minority\b",
    r"\bgender[\s-]non-?conforming\b", r"\bgender[\s-]variant\b",
    r"\bmtf\b", r"\bftm\b", r"\bmale-to-female\b", r"\bfemale-to-male\b",
    r"\btrans\s+people\b", r"\btrans\s+individuals\b", r"\btrans\s+youth\b",
    r"\btrans\s+adolescents\b", r"\btrans\s+adults\b", r"\btrans\s+patients\b",
    r"\btrans\s+population\b", r"\btrans\b"
]
TGD_RE = re.compile("|".join(TGD_PATTERNS), re.IGNORECASE)

# Keywords for GAHT
GAHT_PATTERNS = [
    r"\bgender[\s-]affirming\s+hormone\b", r"\bgender[\s-]affirming\s+hormone\s+therapy\b",
    r"\bgaht\b", r"\bcsht\b", r"\bght\b",
    r"\bcross[\s-]sex\s+hormone\b", r"\bcross[\s-]sex\s+hormones\b", r"\bcross[\s-]sex\s+hormone\s+therapy\b",
    r"\bfeminizing\s+hormone\b", r"\bmasculinizing\s+hormone\b",
    r"\bfeminizing\s+hormone\s+therapy\b", r"\bmasculinizing\s+hormone\s+therapy\b",
    r"\bfeminizing\s+treatment\b", r"\bmasculinizing\s+treatment\b",
    r"\bestradiol\b", r"\bestrogen\b", r"\bestrogens\b", r"\btestosterone\b",
    r"\bantiandrogen\b", r"\bantiandrogens\b", r"\banti-androgen\b", r"\banti-androgens\b",
    r"\bspironolactone\b", r"\bcyproterone\b", r"\bbicalutamide\b",
    r"\bfinasteride\b", r"\bdutasteride\b", r"\bprogesterone\b",
    r"\bhormone\s+therapy\b", r"\bhormone\s+replacement\b", r"\bhormonal\s+therapy\b",
    r"\bhormonal\s+treatment\b", r"\bhormone\s+treatment\b"
]
GAHT_RE = re.compile("|".join(GAHT_PATTERNS), re.IGNORECASE)

print("Setup completed successfully.")
