import os
import json
import requests
import time  # ✅ Add this import

GRAFANA_URL = "http://localhost:3002"
USERNAME = "admin"
PASSWORD = "admin"

def import_dashboard(filepath):
    with open(filepath, "r") as f:
        dashboard_json = json.load(f)
    url = f"{GRAFANA_URL}/api/dashboards/import"
    response = requests.post(
        url,
        json=dashboard_json,
        auth=(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"}
    )
    print(response.text)
    response.raise_for_status()
    result = response.json()
    return result.get("uid")

def fetch_and_save_dashboard(uid, original_filepath):
    url = f"{GRAFANA_URL}/api/dashboards/uid/{uid}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    response.raise_for_status()
    dashboard_data = response.json()
    new_filename = original_filepath.replace("-hi.json", "-grafana12.json")
    with open(new_filename, "w") as f:
        json.dump(dashboard_data, f, indent=2)

def main():
    for subdir, _, files in os.walk("."):
        for file in files:
            if file.endswith("-hi.json"):
                hi_path = os.path.join(subdir, file)
                print(f"Importing: {hi_path}")
                uid = import_dashboard(hi_path)
                print(f"Imported UID: {uid}")
                # time.sleep(2)  # ✅ Sleep for 2 seconds after importing
                if uid:
                    fetch_and_save_dashboard(uid, hi_path)
                    print(f"Saved as: {hi_path.replace('-hi.json', '-grafana12.json')}")

if __name__ == "__main__":
    main()
