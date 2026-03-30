import os
import datetime
import yaml
import subprocess
import requests
import cloudscraper
import re
from bs4 import BeautifulSoup

# Configuration
# No longer using Browserless. Cloudscraper handles anti-bot measures.
CATEGORIES = {
    "8GB": [
        "https://www.alza.cz/pameti-ddr5-8-gb/18897000.htm",
        "https://www.datart.cz/pameti-ram-ddr5-8-gb.html"
    ],
    "16GB": [
        "https://www.alza.cz/pameti-ddr5-16-gb/18896987.htm",
        "https://www.datart.cz/pameti-ram-ddr5-16-gb.html"
    ],
    "32GB": [
        "https://www.alza.cz/pameti-ram-ddr5-32-gb/18896986.htm",
        "https://www.datart.cz/pameti-ram-ddr5-32-gb.html"
    ]
}

# Absolute paths for environment (auto-detecting repo root)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DATA_FILE = os.path.join(REPO_DIR, "_data/ram_prices.yml")
HISTORY_FILE = os.path.join(REPO_DIR, "_data/ram_history.yml")
PAGES_DIR = os.path.join(REPO_DIR, "_pages")

def ensure_authenticated_remote():
    """Checks if the remote URL includes a token, updates it if GITHUB_TOKEN is available."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Note: GITHUB_TOKEN not found in environment. Skipping remote URL update.")
        return

    try:
        # Get current remote URL
        current_url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=REPO_DIR, capture_output=True, text=True, check=True
        ).stdout.strip()

        # If token is already in any part of the URL, do nothing
        if token in current_url:
            return

        # Prepare new URL (assumes github.com)
        if "github.com" in current_url:
            # Extract path like 'user/repo'
            path = current_url.split("github.com/")[-1].replace(".git", "")
            new_url = f"https://{token}@github.com/{path}.git"
            
            print(f"Updating git remote to include security token...")
            subprocess.run(["git", "remote", "set-url", "origin", new_url], cwd=REPO_DIR, check=True)
            
    except Exception as e:
        print(f"Failed to check/update git remote: {e}")

def scrape_category_via_cloudscraper_alza(scraper, url, max_retries=3):
    print(f"Requesting content for {url} via Cloudscraper...")
    
    for attempt in range(max_retries):
        try:
            response = scraper.get(url, timeout=30)
            
            if response.status_code == 403:
                print(f"Attempt {attempt + 1}: Received 403 Forbidden. Retrying in {5 * (attempt + 1)}s...")
                import time
                time.sleep(5 * (attempt + 1))
                continue
                
            response.raise_for_status()
            html = response.text
            break # Success
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error scraping {url} after {max_retries} attempts: {e}")
                return []
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            import time
            time.sleep(2)
    else:
        return []

    try:
        # Strategy 1: Look for JSON-LD embedded data (very reliable)
        import json
        try:
            # Look for hydration-marker with categoryJsonLd component
            pattern = r'data-component="categoryJsonLd"\s+data-initialdata="([^"]+)"'
            match = re.search(pattern, html)
            if match:
                # Unescape HTML entities in the JSON string
                import html as html_lib
                json_raw = html_lib.unescape(match.group(1))
                data = json.loads(json_raw)
                json_items = data.get("items", [])
                
                if json_items:
                    print(f"Found {len(json_items)} items via JSON-LD.")
                    items = []
                    for item in json_items:
                        items.append({
                            "name": item.get("name"),
                            "price": item.get("price"),
                            "link": item.get("url") if item.get("url").startswith("http") else "https://www.alza.cz" + item.get("url")
                        })
                    items.sort(key=lambda x: x['price'])
                    return items
        except Exception as je:
            print(f"JSON-LD extraction failed, falling back to HTML: {je}")

        # Strategy 2: HTML Parsing (fallback)
        soup = BeautifulSoup(html, 'html.parser')
        product_boxes = soup.select(".box.browsingitem, .item.browsingitem, [data-testid='product-card']")
        
        if not product_boxes:
            product_boxes = soup.find_all("div", class_=lambda c: c and ("product" in c or "item" in c))
            
        print(f"Found {len(product_boxes)} potential product boxes via HTML.")
        
        items = []
        for box in product_boxes:
            name_el = box.select_one("a.name, .name-container a, .spec-name, [data-testid='product-name']")
            # Narrowed price selectors to avoid containers that include discounts/original prices
            price_el = box.select_one(".js-price-box__primary-price__value, .price-box__primary-price__value, .price_withVat, .price-value")
            
            if name_el and price_el:
                name = name_el.get_text().strip()
                price_text = price_el.get_text().strip().replace("\xa0", "").replace(" ", "").replace(",-", "").replace("Kč", "")
                
                # Extract digits only
                match = re.search(r'(\d[\d\s]*)', price_text)
                if match:
                    price_text = match.group(1).replace(" ", "")
                
                try:
                    price = int(price_text)
                    # Ignore ridiculously low prices (unlikely for RAM)
                    if price < 100:
                        continue
                        
                    href = name_el.get('href')
                    items.append({
                        "name": name,
                        "price": price,
                        "link": "https://www.alza.cz" + href if href and not href.startswith("http") else href
                    })
                except (ValueError, TypeError):
                    continue
        
        items.sort(key=lambda x: x['price'])
        return items
    except Exception as e:
        print(f"Error scraping {url} via Cloudscraper: {e}")
        return []

def scrape_category_via_cloudscraper_datart(scraper, url, max_retries=3):
    print(f"Requesting content for {url} via Cloudscraper (Datart)...")
    
    for attempt in range(max_retries):
        try:
            response = scraper.get(url, timeout=30)
            if response.status_code == 403:
                print(f"Attempt {attempt + 1}: Received 403 Forbidden for Datart. Retrying in {5 * (attempt + 1)}s...")
                import time
                time.sleep(5 * (attempt + 1))
                continue
            response.raise_for_status()
            html = response.text
            break
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error scraping Datart {url} after {max_retries} attempts: {e}")
                return []
            import time
            time.sleep(2)
    else:
        return []

    try:
        soup = BeautifulSoup(html, 'html.parser')
        product_boxes = soup.select(".product-box")
        print(f"Found {len(product_boxes)} potential product boxes via HTML (Datart).")
        
        items = []
        for box in product_boxes:
            name_el = box.select_one(".item-title-holder h3 a")
            price_el = box.select_one("[data-qa='actual-price'], .actual")
            
            if name_el and price_el:
                name = name_el.get_text().strip()
                price_text = price_el.get_text().strip().replace("\xa0", "").replace(" ", "").replace(",-", "").replace("Kč", "")
                
                # Extract digits
                match = re.search(r'(\d[\d\s]*)', price_text)
                if match:
                    price_text = match.group(1).replace(" ", "")
                
                try:
                    price = int(price_text)
                    if price < 100: continue
                    
                    href = name_el.get('href')
                    items.append({
                        "name": name,
                        "price": price,
                        "link": "https://www.datart.cz" + href if href and not href.startswith("http") else href
                    })
                except:
                    continue
        
        return items
    except Exception as e:
        print(f"Error parsing Datart {url}: {e}")
        return []

def scrape_url(scraper, url):
    if "alza.cz" in url:
        return scrape_category_via_cloudscraper_alza(scraper, url)
    elif "datart.cz" in url:
        return scrape_category_via_cloudscraper_datart(scraper, url)
    return []

def main():
    # Verify/Update Git remote if token is provided
    ensure_authenticated_remote()
    
    results = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": {}
    }
    
    # Use a single scraper session for all categories with a specific browser fingerprint
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'linux',
            'desktop': True
        }
    )
    
    for i, (cat_name, urls) in enumerate(CATEGORIES.items()):
        if i > 0:
            import time
            print(f"Inter-category delay (3s)...")
            time.sleep(3)
            
        print(f"Scraping {cat_name} from {len(urls)} sources...")
        merged_items = []
        for url in urls:
            items = scrape_url(scraper, url)
            if items:
                merged_items.extend(items)
            # Small delay between same-category sources
            import time
            time.sleep(1)
            
        if merged_items:
            # Sort by price ascending
            merged_items.sort(key=lambda x: x['price'])
            
            # Top 5 overall
            results["categories"][cat_name] = merged_items[:5]
            
            # Average calculation across ALL found items
            avg_price = int(sum(item['price'] for item in merged_items) / len(merged_items))
            results["categories"][cat_name][0]["avg_price"] = avg_price
        else:
            results["categories"][cat_name] = []
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Check if we found ANY data at all
    has_data = any(len(items) > 0 for items in results["categories"].values())
    if not has_data:
        print("CRITICAL: Scraping returned NO results for any category. Skipping file update and Git push to prevent overwriting with empty data.")
        return
    
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
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"  # Prevent git from asking for password/username
    
    try:
        # Add files
        subprocess.run(["git", "add", DATA_FILE, HISTORY_FILE, os.path.join(PAGES_DIR, "ram-prices.md")], 
                       cwd=REPO_DIR, env=env, check=True)
        
        # Check for changes
        status = subprocess.run(["git", "status", "--porcelain"], 
                                cwd=REPO_DIR, env=env, capture_output=True, text=True).stdout
        
        if status:
            print("Committing and pushing...")
            subprocess.run(["git", "commit", "-m", f"Auto-update RAM prices and history: {results['last_updated']}"], 
                           cwd=REPO_DIR, env=env, check=True)
            
            # Push with verbose error output
            result = subprocess.run(["git", "push", "origin", "main"], 
                                   cwd=REPO_DIR, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Git push failed:\n{result.stderr}")
            else:
                print("Push successful.")
        else:
            print("No changes detected.")
    except Exception as e:
        print(f"Git automation failed: {e}")

    print(f"Process complete. Data saved and pushed.")

if __name__ == "__main__":
    main()
