import json
import newspaper
from newspaper import Article
from tqdm import tqdm  # For the progress bar

# Define the states
states = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
    "Ebonyi", "Edo", "Ekiti", "Enugu", "Federal Capital Territory", "FCT", "Gombe", "Imo", "Jigawa", "Kaduna",
    "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo",
    "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara", "NO LOCATION"
]

# Open the text file containing article links
with open('article_urls.txt', 'r') as file:
    article_links = file.read().splitlines()

# Create a dictionary to store articles by state
articles_by_state = {state: [] for state in states}

# Process each article link
progress_bar = tqdm(total=len(article_links), desc="Processing articles", unit="article")
for link in article_links:
    try:
        # Create an Article object
        article = Article(link)
        article.download()
        article.parse()

        # Apply NLP and check for state mentions
        state_mentioned = False
        for state in states:
            if state.lower() in article.text.lower():
                articles_by_state[state].append(article.url)
                state_mentioned = True
                break

        # If no state mentioned, put it under "NO LOCATION" key
        if not state_mentioned:
            articles_by_state["NO LOCATION"].append(article.url)

    except newspaper.article.ArticleException:
        print(f"Error processing article: {link}")

    # Update the progress bar
    progress_bar.update(1)

    # Save the articles by state to the JSON file
    with open('articles_by_state.json', 'w') as json_file:
        json.dump(articles_by_state, json_file, indent=4)

# Close the progress bar
progress_bar.close()

print("Articles processed successfully!")