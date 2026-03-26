import os
import datetime
import yaml
import subprocess
import requests
from bs4 import BeautifulSoup

# Configuration
# For Browserless Add-on, the host is usually the add-on name or localhost
BROWSERLESS_ENDPOINT = "http://localhost:3000/content" 
CATEGORIES = {
    "8GB": "https://www.alza.cz/pameti-ddr5-8-gb/18897000.htm",
    "16GB": "https://www.alza.cz/pameti-ddr5-16-gb/18896987.htm",
    "32GB": "https://www.alza.cz/pameti-ram-ddr5-32-gb/18896986.htm"
}

# Absolute paths for Home Assistant environment
REPO_DIR = "/homeassistant/gitrepos/monkey265.github.io"
DATA_FILE = os.path.join(REPO_DIR, "_data/ram_prices.yml")
HISTORY_FILE = os.path.join(REPO_DIR, "_data/ram_history.yml")
PAGES_DIR = os.path.join(REPO_DIR, "_pages")

def scrape_category_via_browserless(url):
    print(f"Requesting content for {url} via Browserless...")
    try:
        # Browserless /content endpoint returns raw HTML after processing JS
        response = requests.post(
            BROWSERLESS_ENDPOINT,
            json={"url": url},
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        response.raise_for_status()
        html = response.text
        
        soup = BeautifulSoup(html, 'html.parser')
        product_boxes = soup.select(".box.browsingitem.js-box")
        items = []
        
        for box in product_boxes:
            name_el = box.select_one("a.name.browsinglink.js-box-link")
            price_el = box.select_one(".js-price-box__primary-price__value")
            
            if name_el and price_el:
                name = name_el.get_text().strip()
                price_text = price_el.get_text().strip().replace("\xa0", "").replace(" ", "").replace(",-", "")
                try:
                    price = int(price_text)
                    href = name_el.get('href')
                    items.append({
                        "name": name,
                        "price": price,
                        "link": "https://www.alza.cz" + href if href and not href.startswith("http") else href
                    })
                except ValueError:
                    continue
        
        items.sort(key=lambda x: x['price'])
        return items
    except Exception as e:
        print(f"Error scraping {url} via Browserless: {e}")
        return []

def main():
    results = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": {}
    }
    
    for cat_name, url in CATEGORIES.items():
        print(f"Scraping {cat_name}...")
        all_items = scrape_category_via_browserless(url)
        
        if all_items:
            # Top 5 for the table
            results["categories"][cat_name] = all_items[:5]
            
            # Average calculation
            avg_price = int(sum(item['price'] for item in all_items) / len(all_items))
            results["categories"][cat_name][0]["avg_price"] = avg_price
        else:
            results["categories"][cat_name] = []
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Save latest prices
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(results, f, allow_unicode=True, default_flow_style=False)
    
    # Maintain history
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = yaml.safe_load(f) or []
    
    today_entry = {"date": today}
    for cat_name, items in results["categories"].items():
        if items:
            today_entry[f"{cat_name}_min"] = items[0]["price"]
            avg_price = items[0].get("avg_price", items[0]["price"]) 
            today_entry[f"{cat_name}_avg"] = avg_price
    
    # Update or append
    updated = False
    for i, entry in enumerate(history):
        if entry.get("date") == today:
            history[i] = today_entry
            updated = True
            break
    if not updated:
        history.append(today_entry)
        
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(history, f, allow_unicode=True, default_flow_style=False)
    
    # Git Automation
    print("Staging changes...")
    try:
        subprocess.run(["git", "add", DATA_FILE, HISTORY_FILE, os.path.join(PAGES_DIR, "ram-prices.md")], cwd=REPO_DIR, check=True)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_DIR, capture_output=True, text=True).stdout
        if status:
            print("Committing and pushing...")
            subprocess.run(["git", "commit", "-m", f"Auto-update RAM prices and history: {results['last_updated']}"], cwd=REPO_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, check=True)
        else:
            print("No changes detected.")
    except Exception as e:
        print(f"Git automation failed: {e}")

    print(f"Process complete. Data saved and pushed.")

if __name__ == "__main__":
    main()
