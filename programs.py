import json
import requests
from bs4 import BeautifulSoup
import random
import time


# load categories.json as a dictionary (which includes the urls)
with open('results/categories.json', 'r', encoding="utf-8") as file:
    categories = json.load(file)

# set headers
headers = {'User-Agent': 'Mozilla/5.0'}

# base url
base_url = "https://www.handbook.unsw.edu.au/"

all_programs = []

for category in categories:
    # set variables
    url = category["url"]
    name = category["name"]

    # send request
    print(f"Requesting URL: {url}")
    response = requests.get(url, headers=headers)
    print(f"{name}: {response.status_code}")

    # parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    program_links = soup.find_all("a", class_="cs-list-item")

    for link in program_links:
        href = link['href']
        encodedHref = requests.utils.quote(href)
        print(encodedHref)
        full_link = f'{base_url.rstrip('/')}{encodedHref}'
        print(full_link)
        container = link.find('div', class_="BrowseResultContainer")

        code = container.find('div', class_="section1 css-n5lzii-Links--StyledAILinkHeaderSection e1t6s54p6")
        credits = container.find('div', class_="section2 css-4rnfv9-Links--StyledAILinkHeaderSection e1t6s54p6")
        title = container.find('div', class_="unit-title css-1fded7k-Links--StyledAILinkHeaderSection e1t6s54p6")

        all_programs.append({
            "category": name,
            "code": code.get_text(strip=True) if code else None,
            "credits": credits.get_text(strip=True) if code else None,
            "title": title.get_text(strip=True) if code else None,
            "url": full_link
        })
    delay = random.uniform(1, 3)
    print(f"Scraped {name}, waiting {delay:.2f} seconds")
    time.sleep(delay)

# save results to json
with open('results/programs.json', 'w') as file:
    json.dump(all_programs, file, indent=4, ensure_ascii=False)