import os
import json

# Root directory to start traversal
root_dir = '.'   # change if needed

def clean_panel(panel):
    # Remove unsupported keys
    for key in ["pluginVersion", "iteration", "links", "transformations"]:
        panel.pop(key, None)
    # Remove row panels
    if panel.get("type") == "row":
        return None
    # Clean fieldConfig mappings
    if "fieldConfig" in panel and "defaults" in panel["fieldConfig"]:
        panel["fieldConfig"]["defaults"].pop("mappings", None)
    return panel

def process_file(filepath):
    try:
        with open(filepath) as f:
            data = json.load(f)

        if "panels" in data:
            data["panels"] = [p for p in (clean_panel(p) for p in data["panels"]) if p]

        # Construct output filename (optional: overwrite or save separately)
#         new_filename = filepath.replace('-ready.json', '-cleaned.json')
        new_filename = filepath

        with open(new_filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Cleaned {filepath} → {new_filename}")

    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")

# Traverse directories and process JSON files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('-ready.json'):
            filepath = os.path.join(subdir, file)
            process_file(filepath)

print("Cleaning complete.")
