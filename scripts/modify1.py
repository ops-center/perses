import os
import json

# Define the root directory to start traversal
root_dir = '.'  # Change as needed

# Function to process and modify JSON files
# Wrap the content into "dashboard" key and add "overwrite" and "folderId"
def process_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    modified_data = {
        "dashboard": data,
        "overwrite": True,
        "folderId": 0
    }

    # Save with -hi.json suffix in the same directory
    new_filename = filepath.replace('.json', '-hi.json')
    with open(new_filename, 'w') as f:
        json.dump(modified_data, f, indent=2)


# Traverse directories and process JSON files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.json') and not file.endswith('-hi.json') and not file.endswith('-grafana12.json'):
            filepath = os.path.join(subdir, file)
            process_file(filepath)
            print(f"Processed and saved {filepath}")

print("Processing complete.")
