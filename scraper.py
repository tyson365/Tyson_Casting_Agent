import requests
import json
from datetime import datetime
import os

API_KEY = os.environ.get("SERP_API_KEY")

QUERIES = [
    "teen male actor audition India 2026",
    "casting call boy 15 16 17 India web series 2026",
    "Netflix Amazon Prime casting teen India 2026",
]

def search(query):
    results = []
    try:
        r = requests.get("https://serpapi.com/search", params={
            "q": query,
            "api_key": API_KEY,
            "num": 10,
            "gl": "in",
            "hl": "en"
        }, timeout=15)
        data = r.json()
        for item in data.get("organic_results", []):
            title = item.get("title","")
            link = item.get("link","")
            snippet = item.get("snippet","")
            text = (title + " " + snippet).lower()
            if any(k in text for k in ["audition","casting","actor","role"]):
                results.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "source": "Google",
                    "type": detect_type(text),
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
    except Exception as e:
        print(f"Error: {e}")
    return results

def detect_type(text):
    if any(k in text for k in ["netflix","prime","hotstar","ott","web series"]):
        return "ott"
    elif any(k in text for k in ["film","movie","feature","bollywood"]):
        return "film"
    elif any(k in text for k in ["ad","commercial","brand","campaign"]):
        return "ad"
    elif any(k in text for k in ["theatre","theater","play","stage"]):
        return "theatre"
    else:
        return "short"

def main():
    all_results = []
    seen = set()
    for q in QUERIES:
        for r in search(q):
            if r["title"] not in seen:
                seen.add(r["title"])
                all_results.append(r)
    all_results.sort(key=lambda x: {"ott":1,"film":2,"ad":3,"short":4,"theatre":5}.get(x["type"],5))
    for i, r in enumerate(all_results):
        r["rank"] = i + 1
    with open("auditions.json","w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Done. Found {len(all_results)} auditions.")

if __name__ == "__main__":
    main()
