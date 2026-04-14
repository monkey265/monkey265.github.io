import os
import datetime
import yaml
import subprocess
import requests
import re
import json

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

import cloudscraper

def scrape_alza(scraper, url):
    """Scrapes Alza using cloudscraper and hydration-marker JSON parsing."""
    print(f"Requesting Alza content for {url}...")
    try:
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        html = response.text
        
        items = []
        # Strategy: Alza Hydration Markers
        # These markers contain a 'categoryJsonLd' component with 'items'
        marker_match = re.search(r'data-component="categoryJsonLd"[^>]+data-initialdata="({.*?})"', html)
        if marker_match:
            try:
                # Decode HTML entities and parse JSON
                json_str = marker_match.group(1).replace("&quot;", "\"")
                data = json.loads(json_str)
                for item in data.get("items", []):
                    name = item.get("name")
                    price = item.get("price")
                    link = item.get("url", "")
                    if name and price:
                        items.append({
                            "name": name,
                            "price": int(price),
                            "link": link if link.startswith("http") else f"https://www.alza.cz{link}",
                            "source": "alza"
                        })
            except Exception as e:
                print(f"Failed to parse Alza marker: {e}")

        if not items:
            # Fallback Grid parsing (more robust)
            matches = re.findall(r'class="name browsinglink js-box-link"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>.*?class="price-box">.*?class="actual">([^<]+)</span>', html, re.DOTALL)
            for href, name, price_str in matches:
                try:
                    price = int(re.sub(r'[^\d]', '', price_str))
                    if price > 100:
                        items.append({
                            "name": name.strip(),
                            "price": price,
                            "link": href if href.startswith("http") else f"https://www.alza.cz{href}",
                            "source": "alza"
                        })
                except: continue
                
        print(f"Found {len(items)} items from Alza.")
        return items
    except Exception as e:
        print(f"Alza scrape failed: {e}")
        return []

def scrape_datart(scraper, url):
  """Scrapes Datart using cloudscraper and GTM data attribute parsing."""
  print(f"Requesting Datart content for {url}...")
  try:
      response = scraper.get(url, timeout=30)
      response.raise_for_status()
      html = response.text
      
      items = []
      # Strategy: data-gtm-data-product attributes
      matches = re.findall(r'data-gtm-data-product=["\']({.*?})["\']', html)
      for match in matches:
          try:
              # HTML entities decode manually for simple cases
              decoded = match.replace("&quot;", "\"").replace("&amp;", "&")
              data = json.loads(decoded)
              name = data.get("item_name")
              price = data.get("price")
              # Try to find a link nearby in the HTML if possible, or just use the category URL
              if name and price:
                  items.append({
                      "name": name,
                      "price": int(price),
                      "link": url, # Fallback to category URL
                      "source": "datart"
                  })
          except: continue
          
      if not items:
          # Fallback HTML split regex
          blocks = html.split('class="product-box"')
          for block in blocks[1:]:
              name_match = re.search(r'class="item-title".*?href="([^"]+)".*?>([^<]+)</a>', block, re.DOTALL)
              price_match = re.search(r'class="actual".*?>([^<]+)</span>', block, re.DOTALL)
              if name_match and price_match:
                  try:
                      price = int(re.sub(r'[^\d]', '', price_match.group(1)))
                      items.append({
                          "name": name_match.group(2).strip(),
                          "price": price,
                          "link": f"https://www.datart.cz{name_match.group(1)}" if not name_match.group(1).startswith("http") else name_match.group(1),
                          "source": "datart"
                      })
                  except: continue

      # Inject source if missing
      for item in items:
          if "source" not in item:
              item["source"] = "datart"
              
      return items
  except Exception as e:
      print(f"Datart scrape failed: {e}")
      return []

def main():
    # Verify/Update Git remote if token is provided
    ensure_authenticated_remote()
    
    results = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": {}
    }
    
    # Initialize robust scraper
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
            print(f"Inter-category delay (2s)...")
            time.sleep(2)
            
        print(f"Updating {cat_name} from {len(urls)} sources...")
        merged_items = []
        
        for url in urls:
            items = []
            if "alza.cz" in url:
                items = scrape_alza(scraper, url)
            elif "datart.cz" in url:
                items = scrape_datart(scraper, url)
                
            if items:
                merged_items.extend(items)
            
            # Politeness delay
            import time
            time.sleep(1)
            
        if merged_items:
            # Sort by price ascending
            merged_items.sort(key=lambda x: x['price'])
            
            # Top 10 overall
            results["categories"][cat_name] = merged_items[:10]
            
            # Average calculation for all items found in this category
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
            # Overall min and avg (legacy)
            today_entry[f"{cat_name}_min"] = items[0]["price"]
            avg_price = items[0].get("avg_price", items[0]["price"]) 
            today_entry[f"{cat_name}_avg"] = avg_price
            
            # Shop specific minimums
            alza_items = [i for i in items if i.get("source") == "alza"]
            datart_items = [i for i in items if i.get("source") == "datart"]
            
            if alza_items:
                today_entry[f"{cat_name}_alza"] = min(i["price"] for i in alza_items)
            if datart_items:
                today_entry[f"{cat_name}_datart"] = min(i["price"] for i in datart_items)
    
    # Update or append
    updated = False
    for i, entry in enumerate(history):
        if entry.get("date") == today:
            # Merge keys to preserve old data if partial update
            history[i].update(today_entry)
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
