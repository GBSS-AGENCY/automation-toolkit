import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os

# Configuration
TARGET_URL = "https://example.com/products" # Replace with actual target URL
OUTPUT_DIR = "datasets"
OUTPUT_FILE = f"product_data_{datetime.datetime.now().strftime('%Y%m%d')}.csv"

def fetch_product_data(url):
    """Fetches and parses product data from the target URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"[*] Fetching data from: {url}")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[!] Error: Failed to retrieve page (Status Code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    # Modify these selectors based on the target website's HTML structure
    items = soup.find_all('div', class_='product-item')
    
    for item in items:
        name = item.find('h2', class_='product-title').text.strip() if item.find('h2', class_='product-title') else "N/A"
        price = item.find('span', class_='product-price').text.strip() if item.find('span', class_='product-price') else "N/A"
        
        products.append({"Product Name": name, "Price": price})
        
    return products

def save_to_csv(data):
    """Saves the scraped data to a CSV file."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    filepath = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Product Name", "Price"])
        writer.writeheader()
        writer.writerows(data)
        
    print(f"[*] Successfully saved {len(data)} items to {filepath}")

if __name__ == "__main__":
    print("--- GBSS Agency: Product Scraper Initialized ---")
    scraped_data = fetch_product_data(TARGET_URL)
    
    if scraped_data:
        save_to_csv(scraped_data)
    print("--- Process Complete ---")
