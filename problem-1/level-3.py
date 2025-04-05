import random
import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException

# --- Setup Stealth Driver ---
def get_driver():
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random_user_agent()}")

    return uc.Chrome(
        options=options,
        version_main=134,  # 👈 match your Chrome version
        driver_executable_path="/home/abhishek/chromedriver-linux64/chromedriver"  # 👈 update to your local path
    )

# --- User-Agent Rotation ---
def random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]
    return random.choice(agents)

# --- Price Extractor ---
def extract_price(text):
    match = re.search(r"\$[\s]?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{2})?", text)
    return match.group(0) if match else None

# --- CAPTCHA Detector ---
def is_captcha_page(title, html):
    return any(kw in title.lower() for kw in ["robot", "captcha", "verify"]) or "are you human" in html.lower()

# --- Main Scraper Logic ---
def scrape_product_price(url, retries=2):
    for attempt in range(retries + 1):
        try:
            driver = get_driver()
            print(f"🌐 Visiting: {url}")
            driver.get(url)
            time.sleep(random.uniform(4, 7))  # simulate human delay

            title = driver.title
            html = driver.page_source

            if is_captcha_page(title, html):
                driver.save_screenshot(f"captcha_detected_{attempt}.png")
                print("🚧 CAPTCHA triggered. Retrying...\n")
                driver.quit()
                continue

            price = extract_price(html)
            print(f"✅ {title} — {price if price else 'Price not found'}")
            driver.quit()
            return

        except WebDriverException as e:
            print(f"❌ WebDriver failed: {e}")
            time.sleep(2)

    print("🛑 All retries failed.")
    return

# --- URLs to Track ---
urls = [
    "https://www.walmart.com/ip/Apple-AirPods-Pro-2nd-Generation/1045954546",
    "https://www.bestbuy.com/site/apple-airpods-pro-2nd-generation-with-usb-c-white/6507681.p"
]

for url in urls:
    scrape_product_price(url)
    print("-" * 60)
