from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time
import re

# Initialize and configure the Chrome WebDriver
def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    # Create the WebDriver
    return webdriver.Chrome(options=options)

# Extract the price text from a given URL based on domain logic or regex fallback
def extract_price_text(driver, url):
    domain = urlparse(url).netloc

    try:
        # Case: Books to Scrape (Static test site)
        if "books.toscrape.com" in domain:
            return driver.find_element(By.CLASS_NAME, "price_color").text

        # Case: Meesho
        elif "meesho.com" in domain:
            price_elements = driver.find_elements(By.CSS_SELECTOR, "h4")
            for el in price_elements:
                if "₹" in el.text:
                    return el.text.strip()
            return "Price not found"

        # Case: Amazon
        elif "amazon." in domain:
            try:
                return driver.find_element(By.ID, "priceblock_ourprice").text
            except:
                try:
                    return driver.find_element(By.ID, "priceblock_dealprice").text
                except:
                    try:
                        return driver.find_element(By.CLASS_NAME, "a-price-whole").text
                    except:
                        return "Price not found"

        # Case: Flipkart
        elif "flipkart.com" in domain:
            try:
                return driver.find_element(By.CSS_SELECTOR, "div._30jeq3._16Jk6d").text
            except:
                return "Price not found"

        # 🔄 Fallback using regex for unknown or unsupported domains
        else:
            html = driver.page_source
            prices = re.findall(r'₹\s?[\d,]+(?:\.\d{1,2})?', html)
            if prices:
                return prices[0]  # Return the first match
            else:
                return "Price not found (regex fallback failed)"

    except NoSuchElementException:
        return "Price not found"

# Fetches product information (title and price) from a product page
def fetch_product_info(url):
    driver = setup_driver(headless=True)

    try:
        driver.get(url)
        time.sleep(5)  # Let the page load

        # Handle anti-bot blocks or access denied pages
        if "access denied" in driver.page_source.lower() or "blocked" in driver.page_source.lower():
            print("Access denied in headless mode. Retrying with full browser...")
            driver.quit()

            # Retry with full browser mode
            driver = setup_driver(headless=False)
            driver.get(url)
            time.sleep(5)

        # Get product title (with fallback)
        title = driver.title.strip() if driver.title else "No Title Found"

        # Extract price using domain-specific logic or regex
        price = extract_price_text(driver, url)

        # Save page for debugging if price isn't found
        if "Price not found" in price:
            with open("backup_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.save_screenshot("backup_debug.png")

        return {
            "name": title,
            "price": price or "Price not found"
        }

    except TimeoutException:
        return {"error": "Timeout while loading the page."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
    finally:
        driver.quit()

# Prompt the user for a URL to fetch the product info
if __name__ == "__main__":
    url = input("Enter Product URL: ").strip()
    
    if not url.startswith("http"):
        print("Invalid URL. Please include http or https.")
    else:
        print(f"\nFetching from: {url}")
        info = fetch_product_info(url)

        if 'error' in info:
            print("❌ Error:", info['error'])
        else:
            print("✅ Product Name:", info['name'])
            print("💰 Price:", info['price'])
