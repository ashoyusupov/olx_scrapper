import asyncio
from pyppeteer.errors import NetworkError, PageError

async def wait_for_elements(page, selector, timeout=30000):
    try:
        await page.waitForSelector(selector, {'timeout': timeout})
        return await page.querySelectorAll(selector)
    except Exception as e:
        print(f"Error waiting for elements: {str(e)}")
        return []

async def get_text_content(page, selector):
    try:
        element = await page.querySelector(selector)
        if element:
            return await page.evaluate('(element) => element.textContent', element)
        return None
    except Exception as e:
        print(f"Error getting text content: {str(e)}")
        return None

async def get_attribute(page, selector, attribute):
    try:
        element = await page.querySelector(selector)
        if element:
            return await page.evaluate(f'(element) => element.getAttribute("{attribute}")', element)
        return None
    except Exception as e:
        print(f"Error getting attribute: {str(e)}")
        return None

async def click_button(page, selector):
    try:
        await page.waitForSelector(selector, {'visible': True, 'timeout': 30000})
        await page.click(selector)
    except Exception as e:
        print(f"Error clicking button: {str(e)}")

async def get_detailed_info(browser, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            page = await browser.newPage()
            await page.goto(url, {'waitUntil': 'networkidle0', 'timeout': 60000})
            
            price_selector = 'div[data-testid="ad-price-container"] h3'
            price = await get_text_content(page, price_selector)
            
            await click_button(page, '[data-cy="ad-contact-phone"]')
            
            phone_selector = '[data-testid="contact-phone"]'
            await page.waitForSelector(phone_selector, {'visible': True, 'timeout': 30000})
            
            phone = await get_attribute(page, phone_selector, 'href')
            if phone and phone.startswith('tel:'):
                phone = phone[4:]  # Remove 'tel:' prefix
            
            await page.close()
            return price, phone
        except (NetworkError, PageError) as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Max retries reached for URL: {url}")
                return None, None
            await asyncio.sleep(2)  # Wait before retrying
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None, None
        finally:
            if 'page' in locals() and not page.isClosed():
                await page.close()

async def scrape_card_data(browser, main_page, card):
    try:
        id = await get_attribute(main_page, '[data-cy="l-card"]', 'id')
        url = await main_page.evaluate('(element) => element.querySelector("a").href', card)
        
        await asyncio.sleep(1)  # Add a small delay between requests
        price, phone = await get_detailed_info(browser, url)
        
        return {
            'id': id,
            'url': url,
            'price': price.strip() if price else None,
            'phone': phone
        }
    except Exception as e:
        print(f"Error scraping card data: {str(e)}")
        return None

async def get_next_page_url(page, base_url):
    try:
        next_button = await page.querySelector('[data-testid="pagination-forward"]')
        if next_button:
            disabled = await page.evaluate('(element) => element.hasAttribute("aria-disabled")', next_button)
            if not disabled:
                current_page = int(base_url.split('page=')[1].split('&')[0]) if 'page=' in base_url else 1
                next_page = current_page + 1
                return base_url.replace(f'page={current_page}', f'page={next_page}') if 'page=' in base_url else f"{base_url}&page={next_page}"
        return None
    except Exception as e:
        print(f"Error getting next page URL: {str(e)}")
        return None