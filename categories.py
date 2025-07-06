# gets a list of areas of interest on the main handbook page

import requests
import json
from bs4 import BeautifulSoup
import random
import os

# target url
url = 'https://www.handbook.unsw.edu.au/'

# set headers
headers = {'User-Agent': 'Mozilla/5.0'}

# send request
response = requests.get(url, headers=headers)

# parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# find all areas of interest
tiles = soup.find_all(class_='css-1tqr8qw-Tile--STileItem-Tile--STile e1mix0ja3')

categories = []

for tile in tiles:
    name = tile.find('h4').get_text(strip="True")
    relative_url = tile.a['href']
    encoded_relative_url = requests.utils.quote(relative_url)
    full_url = f"{url.rstrip('/')}{encoded_relative_url}"
    categories.append({'name': name, 'url': full_url})
    delay = random.uniform(1,3)

# make results directory if it doesn't already exist
os.makedirs('results', exist_ok=True)

# save output
output_path = 'results/categories.json'

with open(output_path, 'w', encoding='utf-8') as file:
    json.dump(categories, file, ensure_ascii=False, indent=4)
