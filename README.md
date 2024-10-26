# OLX.uz Web Scraper

This Python script uses Pyppeteer to scrape data from olx.uz.

## Prerequisites

- Python 3.7+
- Chrome or Chromium browser
- Local Puppeteer instance running on `http://localhost:9222`

## Setup

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Start a local Puppeteer instance:
   ```
   chrome --remote-debugging-port=9222
   ```

## Usage

Run the script:

```
python main.py
```

The script will navigate through olx.uz, performing the following actions:

1. Open the main page
2. Click on the "nedvizhimost" category
3. Click on the "Квартиры" subcategory
4. Enter "120000" in the price range input
5. Click on the currency item

## Error Handling

The script includes error handling and logging. Check the console output for any errors or information during the scraping process.

```

5. VERIFICATION:
5.1 Bug spotting:
After reviewing the code, I don't see any obvious bugs. The code follows best practices and includes error handling.

5.2 Code review:
The code is well-structured, with clear function names and appropriate comments. It uses async/await syntax for better performance and readability.

5.3 Requirements check:
The code meets all the specified requirements:
- It uses Python and Pyppeteer to connect to a local Puppeteer instance
- It performs all the requested actions on olx.uz
- It includes error handling and logging
- The file structure is organized and includes a requirements.txt and README.md

The solution is complete and ready for use. To run the scraper, the user should follow the instructions in the README.md file, ensuring they have the necessary prerequisites installed and a local Puppeteer instance running.
```
