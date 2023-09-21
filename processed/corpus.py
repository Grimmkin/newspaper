import json
import glob

all_links = []

json_files = glob.glob("*.json")

for file_path in json_files:
    with open(file_path, "r") as file:
        data = json.load(file)

        for state in list(data.keys()):
            for i in data[state]:
                all_links.append(i["summary"])

with open("all_links.json", "w") as file:
    json.dump(all_links, file)