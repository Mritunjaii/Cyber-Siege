# 🛒 Product Price Tracker & Scraper

This Python project helps in analyzing pricing strategies across various e-commerce platforms.

It consists of two levels:

- **Level 1**: Scrapes product prices and titles using **Selenium** from live websites.
- **Level 2**: Tracks real-time price fluctuations using a **mock API**, saves historical data, and detects significant price changes.

---

## 🧭 Table of Contents

- [Level 1: Web Scraper](#level-1-web-scraper)
- [Level 2: Mock API Price Tracker](#level-2-mock-api-price-tracker)
- [Requirements](#requirements)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

---

## 🔍 Level 1: Web Scraper

This script uses **Selenium WebDriver** to scrape product titles and prices from various e-commerce websites such as:

- [Books to Scrape](https://books.toscrape.com/)
- [Meesho](https://meesho.com)
- [Amazon](https://amazon.in / .com)
- [Flipkart](https://flipkart.com)
- ✅ Any other site using a **regex-based fallback**

### 🚀 Features

- Domain-specific scraping logic for popular sites.
- Regex-based fallback for unknown websites.
- Handles headless mode and retries if blocked.
- Saves page HTML and screenshot for failed scrapes.
- Modular and easily extendable.

---

## 📈 Level 2: Mock API Price Tracker

This script fetches live product price data from a **mock e-commerce API**:

> https://cyber.istenith.com

It records prices periodically and stores them in individual CSV files with full timestamp logs.

### 🔧 Endpoints Used

- `/api/products`: List all products  
- `/api/products/<product_id>`: Get specific product details  
- `/api/product-page/<product_id>`: HTML product page

### 💡 Features

- Tracks multiple products in real-time.
- Saves price history in CSV format.
- Detects significant price changes (5%+).
- Handles edge cases:
  - Duplicate entries with no change
  - Missing/unavailable products
  - Inconsistent data handling

### 📁 Example Output CSV

Each product creates a CSV like `price_1.csv`:

```csv
Timestamp,Price,Change,Significant
2025-04-05 18:22:00,575.13,, 
2025-04-05 18:23:00,590.00,2.58%,No
2025-04-05 18:24:00,620.00,5.08%,Yes

```bash 
    pip install -R Requirements.txt



# 🕵️ Level 3: CAPTCHA Bypass & Dynamic Price Tracker

## 🚨 Problem Statement
You are a **data hunter** chasing real-time price fluctuations across major e-commerce platforms like **Walmart** and **Best Buy**. However, automated scraping is guarded by CAPTCHAs, anti-bot protection, and dynamic pages.

Your task is to build a **stealthy scraper** using `Selenium` and `undetected-chromedriver` that can:
- Bypass CAPTCHA challenges
- Rotate User Agents
- Mimic human behavior with dynamic delays
- Auto-retry on CAPTCHA or system failure
- Extract product prices reliably

---

## 🔧 Tech Stack
- Python 3.10+
- selenium
- undetected-chromedriver
- re (for regex based price extraction)

---

## 📦 Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd modulusn/problem-1
```

### 2. Setup Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install ChromeDriver v134
Make sure your local Chrome is version 134. Download the matching ChromeDriver:
```bash
wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.117/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
```

> If needed, you can update the script to use a custom path like:
```python
driver_executable_path="/absolute/path/to/chromedriver"
```

### 4. Fix Python Build Errors (if using Python 3.12+)
```bash
sudo apt install python3-distutils
pip install setuptools
```

---

## ▶️ Run the Script
```bash
python level-3.py
```

---

## 🔍 Features

- ✅ **Undetected Chrome Driver**: Avoids detection from anti-bot mechanisms.
- 🔁 **Auto Retry on CAPTCHA**: Detects and retries if CAPTCHA appears.
- 👤 **Rotating User Agents**: Simulates different browsers.
- ⏱️ **Human-like delays**: Adds randomized sleep between actions.
- 💸 **Regex-based Price Extraction**: Captures dollar-formatted prices.

---

## 📎 Target Links
- [Walmart Product Page](https://www.walmart.com/ip/Apple-AirPods-Pro-2nd-Generation/1045954546)
- [Best Buy Product Page](https://www.bestbuy.com/site/apple-airpods-pro-2nd-generation-with-usb-c-white/6507681.p)

---

## 🛠 Troubleshooting

### ❌ `WebDriver failed: session not created`
- Make sure your local Chrome matches the version of ChromeDriver (134).
- Use the `version_main=134` flag in the driver if needed.

### ❌ `ModuleNotFoundError: No module named 'distutils'`
- Install it via `sudo apt install python3-distutils`

### ❌ CAPTCHA Loop
- Try increasing the random sleep duration.
- Improve user-agent randomness.
- Optionally add proxy rotation.

---

## 📈 Example Output
```
🌐 Visiting: https://www.walmart.com/ip/Apple-AirPods-Pro-2nd-Generation/1045954546
✅ Apple AirPods Pro (2nd Generation) — $199.99
--------------------------------------------------
🌐 Visiting: https://www.bestbuy.com/site/apple-airpods-pro-2nd-generation-with-usb-c-white/6507681.p
✅ Best Buy — $189.00
--------------------------------------------------
```

---

Happy Scraping! 🕸️

