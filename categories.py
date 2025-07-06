# gets a list of areas of interest on the main handbook page

import requests
import json
import logging
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
import time
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/crawl.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info(f"Catergory scrape started at {datetime.now().isoformat()}")
start_time = time.time()

# target url
url = 'https://www.handbook.unsw.edu.au/'

# set headers
headers = {'User-Agent': 'Mozilla/5.0'}

# check robots.txt
rp = RobotFileParser()
rp.set_url(url.rstrip("/") + "/robots.txt")
try:
    rp.read()
    logging.debug("Successfully read robots.txt")
except Exception as e:
    logging.error(f"Failed to read robots.txt: {e}")
    print("Unable to fetch robots.txt, check your connection")
    exit(1)

if (rp.can_fetch(headers['User-Agent'], url)):
    logging.debug("Category scraping permitted under robots.txt")
    # send request
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logging.debug(f"Successfully fetched homepage: {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch homepage: {e}")
        exit(1)

    # parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # find all areas of interest
    tiles = soup.find_all(class_='css-1tqr8qw-Tile--STileItem-Tile--STile e1mix0ja3')
    if len(tiles) == 0:
        logging.warning('Found 0 categories')
    else:
        logging.debug(f'Found {len(tiles)} categories')

    categories = []

    for tile in tiles:
        name = tile.find('h4').get_text(strip=True)
        relative_url = tile.a['href']
        encoded_relative_url = requests.utils.quote(relative_url)
        full_url = f"{url.rstrip('/')}{encoded_relative_url}"
        categories.append({'name': name, 'url': full_url})

    # make results directory if it doesn't already exist
    os.makedirs('results', exist_ok=True)

    # save output
    output_path = 'results/categories.json'

    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(categories, file, ensure_ascii=False, indent=4)
        logging.info(f"Saved {len(categories)} categories to {output_path}")
    except Exception as e:
        logging.error(f"Failed to write categories to JSON: {e}")
else:
    logging.warning('Skipping category scrape due to robots.txt restriction')
    print("Cannot parse due to robots.txt restriction")

end_time = time.time()
duration = end_time - start_time
logging.info(f"Scraping completed in {duration:.2f} seconds")
logging.info(f"Catergory scrape ended at {datetime.now().isoformat()}")