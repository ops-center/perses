import os
import json

# Define the root directory to start traversal
root_dir = '.'  # Change as needed

# Function to process and modify JSON files
def process_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Extract the content of the "dashboard" key
    if "dashboard" in data:
        modified_data = data["dashboard"]
    else:
        print(f"Skipping {filepath}: No 'dashboard' key found")
        return

    # Save with -ready.json suffix in the same directory
    new_filename = filepath.replace('-grafana12.json', '-ready.json')
    with open(new_filename, 'w') as f:
        json.dump(modified_data, f, indent=2)

    print(f"Processed and saved {filepath} as {new_filename}")

# Traverse directories and process JSON files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('-grafana12.json'):
            filepath = os.path.join(subdir, file)
            process_file(filepath)

print("Processing complete.")