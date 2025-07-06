import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import random
import time

# selenium options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
options.add_argument("--window-size=1920,1080")


# load categories.json as a dictionary (which includes the urls)
with open('results/categories.json', 'r', encoding="utf-8") as file:
    categories = json.load(file)

# set headers
headers = {'User-Agent': 'Mozilla/5.0'}

# base url
base_url = "https://www.handbook.unsw.edu.au/"

all_programs = {}

for category in categories:
    # set variables
    url = category["url"]
    name = category["name"]

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # wait until one element with class "cs-list-item" is loaded    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cs-list-item"))
    )
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    category_programs = []

    program_links = soup.find_all("a", class_="cs-list-item")

    for link in program_links:
        href = link['href']
        encodedHref = requests.utils.quote(href)
        full_link = f'{base_url.rstrip('/')}{encodedHref}'
        container = link.find('div', class_="BrowseResultContainer")

        code = container.find('div', class_="section1 css-n5lzii-Links--StyledAILinkHeaderSection e1t6s54p6")
        credits = container.find('div', class_="section2 css-4rnfv9-Links--StyledAILinkHeaderSection e1t6s54p6")
        title = container.find('div', class_="unit-title css-1fded7k-Links--StyledAILinkHeaderSection e1t6s54p6")

        category_programs.append({
            "category": name,
            "code": code.get_text(strip=True) if code else None,
            "credits": credits.get_text(strip=True) if code else None,
            "title": title.get_text(strip=True) if code else None,
            "url": full_link
        })
    all_programs[name] = category_programs
    delay = random.uniform(1, 2)
    print(f"Scraped {name}, waiting {delay:.2f} seconds")
    time.sleep(delay)

output_dir = Path("results/programs/2025")
output_dir.mkdir(parents=True, exist_ok=True)

# save results to json
with open(output_dir / 'programs.json', 'w') as file:
    json.dump(all_programs, file, indent=4, ensure_ascii=False)

# save each category as its own json
for category, programs in all_programs.items():
    # sanitise filenames
    safe_filename = "".join(c for c in category if c.isalnum)
    file_path = output_dir / f"{safe_filename}.json"
    
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(programs, file, ensure_ascii=False, indent=4)