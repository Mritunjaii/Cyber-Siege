# 🛒 Product Price Scraper

This Python script uses **Selenium WebDriver** to scrape product titles and prices from various e-commerce websites such as:

- [Books to Scrape](https://books.toscrape.com/)
- [Meesho](https://meesho.com)
- [Amazon](https://amazon.in / .com)
- [Flipkart](https://flipkart.com)
- Any other site using a regex-based fallback.

It includes **headless browser support**, **anti-bot handling**, and a **regex fallback** for unknown domains.

---

## 🚀 Features

- ✅ Domain-specific scraping logic for popular sites.
- 🧠 Regex-based fallback for price extraction on unknown sites.
- 🕵️ Automatically retries with full browser if access is denied in headless mode.
- 🧾 Saves page HTML and screenshot for failed attempts.
- 📦 Easily extendable to add more site-specific logic.

---

## 📦 Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver

### Install dependencies:

```bash
pip install selenium
pip install -r requirements.txt
