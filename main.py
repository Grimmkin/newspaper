import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def extract_links(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the <li> elements with the specified class name
    li_elements = soup.find_all("div", class_="search-description")

    # Extract the href links from the <li> elements
    href_links = [li.find("a")["href"] for li in li_elements]

    return href_links

def save_links_to_json(links):
    # Load existing links from JSON file if it exists
    try:
        with open("links.json", "r") as file:
            existing_links = json.load(file)
    except FileNotFoundError:
        existing_links = {}

    # Parse the main domain from the URL
    parsed_url = urlparse(url)
    main_domain = parsed_url.netloc

    # Add the extracted links to the existing links
    existing_links.setdefault(main_domain, []).extend(links)

    # Save the updated links to JSON file
    with open("links.json", "w") as file:
        json.dump(existing_links, file, indent=4)

# Main code

base_url = "https://nigeriaworld.com/cgi-bin/search/search.pl?Realm=&Match=1&Terms=relief&maxhits=10&Rank={}"
current_page = 17

while current_page >= 1:
    print(f"scraping page {current_page}")
    url = base_url.format(current_page)
    href_links = extract_links(url)
    save_links_to_json(href_links)
    current_page -= 1

print("Extraction complete. Links saved to 'links.json' file.")