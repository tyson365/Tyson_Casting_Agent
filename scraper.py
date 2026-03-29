import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def scrape_castingindia():
    results = []
    try:
        url = "https://www.castingindia.com/casting-calls"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.find_all("div", class_="casting-card") or soup.find_all("article")
        for card in cards[:20]:
            title = card.find("h2") or card.find("h3") or card.find("h1")
            if title:
                text = title.get_text(strip=True).lower()
                if any(k in text for k in ["teen","young","16","17","15","youth","boy","student"]):
                    results.append({
                        "title": title.get_text(strip=True),
                        "source": "CastingIndia",
                        "type": detect_type(text),
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
    except Exception as e:
        print(f"CastingIndia error: {e}")
    return results

def scrape_alh():
    results = []
    try:
        url = "https://alh.in/auditions"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("div", class_="post") or soup.find_all("article")
        for item in items[:20]:
            title = item.find("h2") or item.find("h3")
            if title:
                text = title.get_text(strip=True).lower()
                if any(k in text for k in ["teen","young","16","17","15","youth","boy","male","student"]):
                    results.append({
                        "title": title.get_text(strip=True),
                        "source": "ALH",
                        "type": detect_type(text),
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
    except Exception as e:
        print(f"ALH error: {e}")
    return results

def detect_type(text):
    if any(k in text for k in ["netflix","prime","hotstar","ott","web series","webseries"]):
        return "ott"
    elif any(k in text for k in ["film","movie","feature","bollywood"]):
        return "film"
    elif any(k in text for k in ["ad","commercial","brand","campaign"]):
        return "ad"
    elif any(k in text for k in ["theatre","theater","play","stage"]):
        return "theatre"
    else:
        return "short"

def rank(item):
    order = {"ott":1,"film":2,"ad":3,"short":4,"theatre":5}
    return order.get(item["type"], 5)

def main():
    all_results = scrape_castingindia() + scrape_alh()
    all_results.sort(key=rank)
    for i, r in enumerate(all_results):
        r["rank"] = i + 1
    with open("auditions.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Done. Found {len(all_results)} auditions.")

if __name__ == "__main__":
    main()
