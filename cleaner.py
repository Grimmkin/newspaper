import json

def remove_duplicates(links):
    # Remove duplicates while preserving the order
    return list(dict.fromkeys(links))

def deduplicate_links_in_json_file(file_path):
    # Load links from JSON file
    with open(file_path, "r") as file:
        existing_links = json.load(file)

    # Deduplicate the links for each key
    deduplicated_links = {}
    for key, links in existing_links.items():
        deduplicated_links[key] = remove_duplicates(links)

    # Write the deduplicated links back to JSON file
    with open(file_path, "w") as file:
        json.dump(deduplicated_links, file, indent=4)

# Usage example
json_file_path = "links.json"
deduplicate_links_in_json_file(json_file_path)
print("Duplicates removed. Changes saved to 'links.json' file.")