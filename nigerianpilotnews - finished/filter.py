import json
import os
from newspaper import Article
from newspaper import Config

def read_article(url):
    # Configure Newspaper3k
    config = Config()
    config.keep_article_html = True

    # Initialize Article object
    article = Article(url, config=config)

    # Download and parse the article
    article.download()
    article.parse()

    # Perform NLP tasks
    article.nlp()

    return article

def filter_keywords(article):
    keywords = article.keywords
    palliative_keywords = [
        "receive", "disburse", "distribute", "subsidy", "palliative",
        "beneficiary", "beneficiaries", "relief"
    ]

    # Check if any keyword matches the palliative keywords
    for keyword in keywords:
        if keyword.lower() in palliative_keywords:
            return True
    
    return False

# Read JSON file
with open("links.json", "r") as file:
    json_data = json.load(file)

filtered_links = {}
filtered_articles = []

# Check if a pointer exists
if os.path.exists("pointer.json"):
    with open("pointer.json", "r") as file:
        pointer = json.load(file)
else:
    pointer = {"domain": None, "index": None}

print(pointer)

domain = list(json_data.keys())[0]

urls = list(json_data.values())[0]
print(urls)

filtered_links.setdefault(domain, [])

# Check if the pointer matches the current domain
if pointer["domain"] == domain:
    start_index = pointer["index"] + 1
else:
    start_index = 0

# Iterate over each URL and read the article
for i in range(start_index, len(urls)):
    url = urls[i]
    article = read_article(url)
    if filter_keywords(article):
        filtered_links[domain].append(url)
        filtered_articles.append({
            "url": url,
            "summary": article.summary
        })

    # Save filtered links to JSON file
    with open("filtered_links.json", "w") as file:
        json.dump(filtered_links, file, indent=4)

    # Save filtered articles with links and summaries to JSON file
    with open("filtered_articles_with_links.json", "w") as file:
        json.dump(filtered_articles, file, indent=4)

    # Update the pointer
    pointer = {"domain": domain, "index": i}

    # Save the pointer to a JSON file
    with open("pointer.json", "w") as file:
        json.dump(pointer, file)

# Remove the pointer file once all articles are processed
try:
    os.remove("pointer.json")
except FileNotFoundError:
    pass

print("Filtered links saved to 'filtered_links.json' file.")
print("Filtered articles with links and summaries saved to 'filtered_articles_with_links.json' file.")