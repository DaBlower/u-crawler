## Usage
Just open unzip the folder for your OS and run `u-crawler`!

You might get a warning on Windows about it being malicious, you can safely ignore it. This happens because
1. It is an exe file, which some browsers treat as being suspicious
2. It is not signed (getting a signing certificate is pretty expensive!)

**Also if your browser says it couldn't download the file, use Firefox!**

## Features

- Uses requests, BeautifulSoup and Selenium with headless Chrome  
- Scrapes areas of interest (eg. Engineering and Related Technologies) and the undergraduate programs in each one  
- Respects robots.txt  
- Writes results in structured JSON files per area of interest and overall  
- Logs crawl status and errors in logs/ and debugging information if --debug or -d is passed as an argument  