import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_test_links():
    print("Fetching product catalog...")
    r = requests.get(CATALOG_URL, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    links = []

    # All product cards appear under <a> tags with catalog links
    for a in soup.find_all("a", href=True):
        href = a["href"]

        # Keep only Individual Test Solutions (they contain '/product/' in URL)
        if "/product/" in href and "pack" not in href:
            full_link = BASE_URL + href if href.startswith("/") else href
            links.append(full_link)

    print(f"Found {len(links)} product pages.")
    return list(set(links))  # remove duplicates


def scrape_product_page(url):
    try:
        print("Scraping:", url)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

        name = soup.find("h1").text.strip() if soup.find("h1") else "Unknown"

        desc_tag = soup.find("div", class_="content")
        description = desc_tag.text.strip() if desc_tag else ""

        # Default values if not found
        adaptive_support = "No"
        remote_support = "Yes"
        test_type = []
        duration = 0

        # Search page text for keywords
        page_text = soup.text.lower()

        if "adaptive" in page_text:
            adaptive_support = "Yes"

        if "remote" in page_text:
            remote_support = "Yes"

        # Identify test type: K (knowledge) or P (psychological)
        if "behavior" in page_text or "personality" in page_text:
            test_type.append("P")
        if "technical" in page_text or "ability" in page_text or "skills" in page_text:
            test_type.append("K")

        if not test_type:
            test_type.append("K")  # default fallback

        return {
            "url": url,
            "name": name,
            "description": description,
            "adaptive_support": adaptive_support,
            "remote_support": remote_support,
            "test_type": test_type,
            "duration": duration
        }

    except Exception as e:
        print("Error scraping", url, e)
        return None


def main():
    links = extract_test_links()
    scraped = []

    for link in links:
        data = scrape_product_page(link)
        if data:
            scraped.append(data)
        time.sleep(1)  # avoid hammering their server

    print(f"Scraped {len(scraped)} assessments.")

    # Save to CSV
    with open("shl_catalog.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "url", "name", "description", "adaptive_support",
            "remote_support", "test_type", "duration"
        ])
        writer.writeheader()
        for row in scraped:
            writer.writerow(row)

    print("Saved shl_catalog.csv successfully.")


if __name__ == "__main__":
    main()
