import requests
import csv
import time
from datetime import datetime

BASE_URL = "https://cyber.istenith.com"
PRICE_CHANGE_THRESHOLD = 5  # %
CHECK_INTERVAL = 60  # in seconds

def get_all_products():
    try:
        res = requests.get(f"{BASE_URL}/api/products")
        res.raise_for_status()
        return res.json().get("products", [])
    except Exception as e:
        print("❌ Error fetching products:", e)
        return []

def get_product_details(product_id):
    try:
        res = requests.get(f"{BASE_URL}/api/products/{product_id}")
        res.raise_for_status()
        return res.json().get("product", None)
    except Exception as e:
        print(f"❌ Error fetching product {product_id}:", e)
        return None

def load_last_price(product_id):
    try:
        with open(f"price_{product_id}.csv", "r") as f:
            rows = list(csv.reader(f))
            if len(rows) > 1:
                return float(rows[-1][1])
    except FileNotFoundError:
        return None
    return None

def record_price(product_id, name, price, change=None, significant=False):
    filename = f"price_{product_id}.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_new = False
    try:
        with open(filename, "r"):
            pass
    except FileNotFoundError:
        is_new = True

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["Timestamp", "Price", "Change", "Significant"])
        writer.writerow([timestamp, price, f"{change:.2f}%" if change else "", "Yes" if significant else ""])

def detect_change(prev_price, curr_price):
    if prev_price is None:
        return None, False
    try:
        change = ((curr_price - prev_price) / prev_price) * 100
        return change, abs(change) >= PRICE_CHANGE_THRESHOLD
    except ZeroDivisionError:
        return None, False

def track_prices():
    print("📦 Starting Price Tracker...\n")
    products = get_all_products()
    if not products:
        print("No products to track.")
        return

    while True:
        print(f"\n🔁 Checking at {datetime.now().strftime('%H:%M:%S')}...")
        for product in products:
            product_id = product.get("id")
            name = product.get("name")

            details = get_product_details(product_id)
            if not details:
                continue

            curr_price = details.get("current_price")
            if curr_price is None:
                print(f"⚠️ No price for {name}")
                continue

            prev_price = load_last_price(product_id)
            change, significant = detect_change(prev_price, curr_price)

            record_price(product_id, name, curr_price, change, significant)
            print(f"✅ {name} - ${curr_price:.2f} | Change: {f'{change:.2f}%' if change else 'N/A'} {'🚨' if significant else ''}")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    track_prices()
