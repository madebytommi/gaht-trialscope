import json
import csv

with open("scratch/candidates_full.json") as f:
    full_data = json.load(f)

studies_by_nct = {s["protocolSection"]["identificationModule"]["nctId"]: s for s in full_data["studies"]}

with open("data/candidate_studies.csv", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

print(f"Total CSV rows: {len(csv_rows)}")

# Separate by preliminary screening
excludes = [r for r in csv_rows if r["preliminary_screening"] == "exclude"]
includes = [r for r in csv_rows if r["preliminary_screening"] == "include"]
uncertains = [r for r in csv_rows if r["preliminary_screening"] == "uncertain"]

print(f"Excludes: {len(excludes)}")
print(f"Includes: {len(includes)}")
print(f"Uncertains: {len(uncertains)}")

# Let's inspect all 54 EXCLUDE records
print("\n" + "="*80)
print("AUDITING ALL 54 PRELIMINARY EXCLUDE RECORDS")
print("="*80)

audit_excludes = []
for r in excludes:
    nct = r["nct_id"]
    s = studies_by_nct.get(nct, {})
    prot = s.get("protocolSection", {})
    
    title = prot.get("identificationModule", {}).get("briefTitle", "")
    summary = prot.get("descriptionModule", {}).get("briefSummary", "")
    conditions = prot.get("conditionsModule", {}).get("conditions", [])
    interventions = [i.get("name", "") + f" ({i.get('type', '')})" for i in prot.get("armsInterventionsModule", {}).get("interventions", [])]
    eligibility = prot.get("eligibilityModule", {}).get("eligibilityCriteria", "")
    
    audit_excludes.append({
        "nct_id": nct,
        "title": title,
        "screening_reason": r["screening_reason"],
        "conditions": conditions,
        "interventions": interventions,
        "summary": summary,
        "eligibility": eligibility
    })

with open("scratch/audit_excludes.json", "w") as f:
    json.dump(audit_excludes, f, indent=2)

# Let's inspect all 70 INCLUDE records
print("\n" + "="*80)
print("AUDITING ALL 70 PRELIMINARY INCLUDE RECORDS")
print("="*80)

audit_includes = []
for r in includes:
    nct = r["nct_id"]
    s = studies_by_nct.get(nct, {})
    prot = s.get("protocolSection", {})
    
    title = prot.get("identificationModule", {}).get("briefTitle", "")
    summary = prot.get("descriptionModule", {}).get("briefSummary", "")
    conditions = prot.get("conditionsModule", {}).get("conditions", [])
    interventions = [i.get("name", "") + f" ({i.get('type', '')})" for i in prot.get("armsInterventionsModule", {}).get("interventions", [])]
    eligibility = prot.get("eligibilityModule", {}).get("eligibilityCriteria", "")
    
    audit_includes.append({
        "nct_id": nct,
        "title": title,
        "screening_reason": r["screening_reason"],
        "conditions": conditions,
        "interventions": interventions,
        "summary": summary,
        "eligibility": eligibility
    })

with open("scratch/audit_includes.json", "w") as f:
    json.dump(audit_includes, f, indent=2)

print("Saved audit_excludes.json and audit_includes.json")
