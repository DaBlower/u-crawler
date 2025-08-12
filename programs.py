import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from urllib.robotparser import RobotFileParser
import random
from datetime import datetime
import sys
import logging
import time
import os

def run(debug):
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        filename=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-categories.log",
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.basicConfig(
        filename=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-programs.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info(f"Catergory scrape started at {datetime.now().isoformat()}")
    start_time = time.time()
    # selenium options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1920,1080")

    # load categories.json as a dictionary (which includes the urls)
    try:
        with open('results/categories.json', 'r', encoding="utf-8") as file:
            categories = json.load(file)
        logging.debug("Successfully loaded categories.json")
    except Exception as e:
        logging.error(f"Failed to load categories.json - have you ran categories.py yet? {e}")
        print(f"ERROR: Failed to load categories.json - have you ran categories.py yet? (also if you are a SOM reviewer, please show the logs){e}")
        sys.exit(1)

    # check if categories is empty
    if not categories:
        logging.error("No categories found in categories.json")
        print("ERROR: No categories found in categories.json (also if you are a SOM reviewer, please show the logs)")
        sys.exit(1)

    # set headers
    headers = {'User-Agent': 'Mozilla/5.0'}

    # base url
    base_url = "https://www.handbook.unsw.edu.au/"

    all_programs = {}

    # check robots.txt
    rp = RobotFileParser()

    for category in categories:
        # set variables
        url = category["url"]
        name = category["name"]
        rp.set_url(url.rstrip("/") + "/robots.txt")
        try:
            rp.read()
            logging.debug("Successfully read robots.txt")
        except Exception as e:
            logging.error(f"Failed to read robots.txt: {e}")
            print(f"ERROR: Unable to fetch robots.txt, check your connection (also if you are a SOM reviewer, please show the logs){e}")
            sys.exit(1)

        if (rp.can_fetch(headers['User-Agent'], url)):
            logging.debug(f"Scraping of {url} permitted under Robots.txt")

            try:
                driver = webdriver.Chrome(options=options)
                driver.get(url)

                # wait until one element with class "cs-list-item" is loaded    
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cs-list-item"))
                )
                html = driver.page_source
                logging.debug(f"Headless browser for {url} loaded successfully")
            except Exception as e:
                logging.error(f"Failed to load headless browser for {url}: {e}")
                print(f"ERROR: Failed to load headless browser for {url} (also if you are a SOM reviewer, please show the logs){e}")
                continue # skip to next loop iteration
            finally:
                try:
                    driver.quit()
                except NameError:
                    pass
            soup = BeautifulSoup(html, 'html.parser')

            category_programs = []

            program_links = soup.find_all("a", class_="cs-list-item")

            for link in program_links:
                try:
                    href = link['href']
                    encodedHref = requests.utils.quote(href)
                    full_link = f'{base_url.rstrip("/")}{encodedHref}'
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
                except Exception as e:
                    logging.warning(f"Skipped program link in {name}: {e}")
            all_programs[name] = category_programs
            delay = random.uniform(1, 2)
            print(f"Scraped {name}, waiting {delay:.2f} seconds")
            time.sleep(delay)
        else:
            logging.WARN(f"Skipped {url} due to robots.txt restrictions")
            print(f"WARNING: Skipped {name} due to robots.txt restrictions")

    output_dir = Path("results/programs/2025")
    output_dir.mkdir(parents=True, exist_ok=True)

    # save all results in a singular json
    try:
        # save results to json
        with open(output_dir / 'programs.json', 'w') as file:
            json.dump(all_programs, file, indent=4, ensure_ascii=False)
            logging.debug(f"Wrote all programs to programs.json successfully")
    except Exception as e:
        logging.error(f"Failed to write all programs to programs.json (also if you are a SOM reviewer, please show the logs)")


    # save each category as its own json
    try:
        for category, programs in all_programs.items():
            # sanitise filenames
            safe_filename = "".join(c for c in category if c.isalnum)
            file_path = output_dir / f"{safe_filename}.json"
            
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(programs, file, ensure_ascii=False, indent=4)
        logging.debug(f'Successfully saved {safe_filename}.json')
    except Exception as e:
        logging.error(f"Failed to write file for {category}: (also if you are a SOM reviewer, please show the logs) {e}")

    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Scraping completed in {duration:.2f} seconds")
    logging.info(f"Programs scrape ended at {datetime.now().isoformat()}")
    print("Programs.py finished")