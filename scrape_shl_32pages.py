import requests
from bs4 import BeautifulSoup
import csv

BASE = "https://www.shl.com/products/product-catalog/?start={}&type=1"

def clean(s):
    return s.strip().replace("\n", " ").replace("\r", " ").strip()

all_rows = []

for start in range(0, 32):     # 32 pages
    url = BASE.format(start)
    print(f"Scraping page {start+1}: {url}")

    r = requests.get(url, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")

    # Each product is inside tables in <a> tags
    links = soup.select("table a")
    print(" Found", len(links), "links")

    for a in links:
        href = a.get("href")
        name = clean(a.text)

        if not href:
            continue

        # absolute URL
        if not href.startswith("http"):
            href = "https://www.shl.com" + href

        all_rows.append({
            "name": name,
            "url": href
        })

# Remove duplicates
unique = {row["url"]: row for row in all_rows}.values()

print("Total unique assessments:", len(list(unique)))

# Save CSV
with open("shl_catalog_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "url"])
    writer.writeheader()
    for row in unique:
        writer.writerow(row)

print("Saved shl_catalog_raw.csv")
