import asyncio
import json
from pyppeteer import connect
from utils import wait_for_elements, scrape_card_data, get_next_page_url

async def run_scraper():
    browser = await connect(browserURL='http://localhost:9222', defaultViewport=None)
    page = await browser.newPage()

    base_url = "https://www.olx.uz/nedvizhimost/kvartiry/?currency=UYE&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:from%5D=120000"
    current_url = base_url
    all_data = []

    try:
        while current_url:
            await page.goto(current_url, {'waitUntil': 'networkidle0', 'timeout': 60000})
            print(f"Scraping page: {current_url}")

            cards = await wait_for_elements(page, '[data-cy="l-card"]')
            
            for card in cards:
                card_data = await scrape_card_data(browser, page, card)
                if card_data:
                    all_data.append(card_data)
                    print(f"Scraped data: {card_data}")
                else:
                    print("Failed to scrape card data")

            current_url = await get_next_page_url(page, current_url)
            await asyncio.sleep(2)  # Add a delay between pages

        # Save data to JSON file
        with open('olx_apartments_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"Scraping completed. Data saved to olx_apartments_data.json")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        print(f"Scraping completed.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_scraper())