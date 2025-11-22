import requests
from bs4 import BeautifulSoup
import csv
import time
import re

INPUT_CSV = "shl_catalog.csv"
OUTPUT_CSV = "shl_catalog.csv"

def clean(s):
    return (s or "").replace("\n", " ").replace("\r", " ").strip()

def extract_details(url):
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            print("Failed:", url)
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        # Name
        name_tag = soup.find(["h1", "h2"])
        name = clean(name_tag.text) if name_tag else ""

        # Description
        desc_tag = soup.find("div", class_="content") \
                or soup.find("section", class_="product__content") \
                or soup.find("div", class_="product-description")
        description = clean(desc_tag.text) if desc_tag else ""

        page_text = soup.get_text(" ").lower()

        # Flags
        adaptive_support = "Yes" if "adaptive" in page_text else "No"
        remote_support = "Yes" if ("remote" in page_text or "online" in page_text) else "No"

        # Test type
        t = []
        if any(k in page_text for k in ["personality","behaviour","behavior"]):
            t.append("P")
        if any(k in page_text for k in ["ability","cognitive","skills","technical","aptitude"]):
            t.append("K")
        if not t:
            t.append("K")

        # Duration
        duration = 0
        m = re.search(r"(\d{1,3})\s*(minutes|min)", page_text)
        if m:
            duration = int(m.group(1))

        return {
            "url": url,
            "name": name,
            "description": description,
            "adaptive_support": adaptive_support,
            "remote_support": remote_support,
            "test_type": str(t),
            "duration": duration
        }

    except Exception as e:
        print("Error:", url, e)
        return None

# Read the 55 URLs
urls = []
with open(INPUT_CSV, "r") as f:
    next(f)
    for line in f:
        name, url = line.strip().split(",", 1)
        urls.append(url)

rows = []

print(f"Extracting details for {len(urls)} products...")

for i, url in enumerate(urls):
    print(f"[{i+1}/{len(urls)}] {url}")
    data = extract_details(url)
    if data:
        rows.append(data)
    time.sleep(0.7)

# Write final CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "url","name","description","adaptive_support",
        "remote_support","test_type","duration"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"\nDONE! Saved full dataset to {OUTPUT_CSV}")
