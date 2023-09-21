import os
import json
import pprint

# initialize 3 dictionaries; Yes, Unsure, No
yes = {}
no = {}
unsure = {}

with open("all_links.json", "r") as file:
    articles = json.load(file)

articles = [article for article in articles if "subsidy" not in article]

# Check if a pointer exists
if os.path.exists("pointer.json"):
    with open("pointer.json", "r") as file:
        pointer = json.load(file)
        index = pointer["index"]
else:
    pointer = {"index": None}
    index = 0

def query(article):
    return input(f"\n ARTICLE {index} OF {len(articles)}. \n{article}\n{'-'*7}\nDoes this article have anything with distributing palliatives [y]es, [n]o, [u]nsure, [r]everse: ")

while index <= len(articles):
    article = articles[index]

    result = query(article)
    if result == "y":
        yes[index] = article

        with open("yes.json", "w") as file1:
            json.dump(yes, file1)

        index += 1

    elif result == "n":
        no[index] = article

        with open("no.json", "w") as file2:
            json.dump(no, file2)

        index += 1

    elif result == "u":
        unsure[index] = article

        with open("unsure.json", "w") as file3:
            json.dump(unsure, file3)

        index += 1

    else:
        pass

    # Update the pointer
    pointer = {"index": index}

    # Save the pointer to a JSON file
    with open("pointer.json", "w") as file:
        json.dump(pointer, file)

try:
    os.remove("pointer.json")
except FileNotFoundError:
    pass
