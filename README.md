# U-crawler
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)![Hackatime Badge](https://hackatime-badge.hackclub.com/U092DB4LGMP/u-crawler)<br/>
A python-based web scraper that collects and categorises UNSW (University of New South Wales) undergraduate programs by their areas of interest and outputs it into structured JSON files

## Objective
The objective of this crawler is to scrape every area of interest and find all of the undergraduate programs offered at the University of New South Wales.

## Directory Structure
```
├── categories.py
├── main.py
├── programs.py
└── results
    ├── categories.json - Contains the areas of interest which programs.py then uses
    └── programs
        └── 2025 - Each area of interest has its own JSON file with every program inside of it
            ├── Architecture and Building.json
            ├── Business and Management.json
            ├── Creative Arts.json
            ├── Education.json
            ├── Engineering and Related Technologies.json
            ├── Environmental and Related Studies.json
            ├── Health.json
            ├── Humanities and Law.json
            ├── Information Technology.json
            ├── Natural and Physical Sciences.json
            └── programs.json - This contains all of the separate area of interest files together
```

## Setup instructions
### Prebuilt executables
Just download the [latest release](https://github.com/DaBlower/u-crawler/releases/latest), unzip and run!

### Manual
1. Clone this repository
2. Create a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate # or venv\Scripts\activate on Windows
    ```
3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
## Usage
Run the scraper using
`python main.py`
Note: You can only run the scraper using main.py, you cannot run categories.py or programs.py separately
## Features
* Uses `requests`, `BeautifulSoup` and `Selenium` with headless Chrome
* Scrapes areas of interest (eg. Engineering and Related Technologies) and the undergraduate programs in each one
* Respects `robots.txt`
* Writes results in structured JSON files per area of interest and overall
* Logs crawl status and errors in `logs/` and debugging information if `--debug` or `-d` is passed as an argument
