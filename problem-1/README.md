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

