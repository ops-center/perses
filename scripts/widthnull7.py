import os
import json

# Define the root directory to start traversal
root_dir = '.'  # change as needed

def process_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    changed = [False]

    def modify(obj):
        if isinstance(obj, dict):
            # If there is a key "width" with value None, delete it
            if 'width' in obj and obj['width'] is None:
                del obj['width']
                changed[0] = True

            # Recurse into remaining values
            for v in list(obj.values()):
                modify(v)

        elif isinstance(obj, list):
            for item in obj:
                modify(item)

    modify(data)

    if changed[0]:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Modified {filepath}")
    else:
        print(f"No changes needed for {filepath}")

# Traverse directories and process JSON files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('-migrated.json'):
            filepath = os.path.join(subdir, file)
            process_file(filepath)

print("Processing complete.")
