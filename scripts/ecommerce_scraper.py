import requests
from bs4 import BeautifulSoup
import csv
import os

# Configuration for a single, always-updating live data file
TARGET_URL = "http://books.toscrape.com/" 
OUTPUT_DIR = "datasets"
OUTPUT_FILE = "live_products.csv"  # Always updates this single live file

def fetch_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"[*] Fetching live data from: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[!] Error: Failed to retrieve page (Status Code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    items = soup.find_all('article', class_='product_pod')
    for item in items:
        name = item.find('h3').find('a')['title'] if item.find('h3') else "N/A"
        price = item.find('p', class_='price_color').text.strip() if item.find('p', class_='price_color') else "N/A"
        products.append({"Product Name": name, "Price": price})
        
    return products

def save_to_csv(data):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    
    # Overwrites with fresh live content on every run
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Product Name", "Price"])
        writer.writeheader()
        writer.writerows(data)
        
    print(f"[*] Successfully updated live file with {len(data)} items at {filepath}")

if __name__ == "__main__":
    print("--- GBSS Agency: Live Scraper Initialized ---")
    scraped_data = fetch_product_data(TARGET_URL)
    if scraped_data:
        save_to_csv(scraped_data)
    print("--- Process Complete ---")
