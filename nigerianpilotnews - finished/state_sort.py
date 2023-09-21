import json
import re

# Load the data from the JSON file
with open("filtered_articles_with_links.json", "r") as file:
    data = json.load(file)

state_sorted = {}  # Dictionary to store URLs and summaries by state
state_sorted["NO LOCATION"] = []  # List to store summaries without state mentioned

# List of states to search for in the summaries
states = [
    "Abia",
    "Abuja"
    "Adamawa",
    "Akwa Ibom",
    "Anambra",
    "Bauchi",
    "Bayelsa",
    "Benue",
    "Borno",
    "Cross River",
    "Delta",
    "Ebonyi",
    "Edo",
    "Ekiti",
    "Enugu",
    "Federal Capital Territory",
    "FCT",
    "Gombe",
    "Imo",
    "Jigawa",
    "Kaduna",
    "Kano",
    "Katsina",
    "Kebbi",
    "Kogi",
    "Kwara",
    "Lagos",
    "Nasarawa",
    "Niger",
    "Ogun",
    "Ondo",
    "Osun",
    "Oyo",
    "Plateau",
    "Rivers",
    "Sokoto",
    "Taraba",
    "Yobe",
    "Zamfara"
]

# Iterate over each article
for article in data:
    url = article["url"]
    summary = article["summary"]
    found_states = []

    # Search for states in the summary
    for state in states:
        if re.search(r"\b" + state + r"\b", summary, re.IGNORECASE):
            found_states.append(state)

    if found_states:
        # Add the URL and summary to each found state in the dictionary
        for state in found_states:
            if state not in state_sorted:
                state_sorted[state] = []
            state_sorted[state].append({"url": url, "summary": summary})
    else:
        # Add the URL and summary to the "NO LOCATION" list
        state_sorted["NO LOCATION"].append({"url": url, "summary": summary})

# Save the dictionary in a JSON file
with open("state_sorted.json", "w") as file:
    json.dump(state_sorted, file, indent=4)