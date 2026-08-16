import subprocess
import json
import os

with open("data/raw/candidates_raw.json") as f:
    data = json.load(f)

existing_ncts = [s["protocolSection"]["identificationModule"]["nctId"] for s in data["studies"]]
print(f"Total candidates to fetch in full: {len(existing_ncts)}")

api_script = "/Users/celtninja/.gemini/config/plugins/science/skills/clinical_trials_database/scripts/clinical_trials_api.py"
uv_bin = os.path.expanduser("~/.local/bin/uv")

# Fetch all 283 in one query using the baseline search term or by chunking NCT IDs
# Since the baseline search term returned these exact 283, we can search with all fields!
cmd = [
    uv_bin, "run", api_script, "search",
    "--term", '(transgender OR transsexual OR "gender diverse" OR "gender incongruence") AND (hormone OR estradiol OR estrogen OR testosterone OR antiandrogen OR spironolactone OR progesterone)',
    "--fields", "NCTId,BriefTitle,OfficialTitle,BriefSummary,DetailedDescription,ConditionsModule,ArmsInterventionsModule,EligibilityModule,PrimaryOutcome,SecondaryOutcome,DesignModule,StatusModule,LeadSponsorName,ContactsLocationsModule,hasResults",
    "--limit", "1000",
    "--output", "scratch/candidates_full.json"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode != 0:
    print("Error:", res.stderr)
else:
    with open("scratch/candidates_full.json") as f:
        full_data = json.load(f)
    print(f"Fetched {len(full_data.get('studies', []))} full candidate studies.")
