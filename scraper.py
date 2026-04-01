import requests
import json
from datetime import datetime
import os

API_KEY = os.environ.get("SERP_API_KEY")

QUERIES = [
    "teen boy actor casting call India 2026",
    "male actor age 16 17 casting India web series 2026",
    "young male actor audition India Netflix Amazon 2026",
    "casting call boy 15 16 17 18 India film 2026",
    "teen male casting Bollywood OTT 2026",
]

EXCLUDE_KEYWORDS = [
    "female","girl","woman","lady","actress","dance competition",
    "model female","singer","bhabhi","didi","sister",
    "age 20 to 28","age 21 to","age 22 to","age 23 to","age 24 to",
    "age 25","age 26","age 27","age 28","age 29","age 30","age 35","age 40",
    "20 to 28","25 to 35","21 to 30","22 to 30","20-28","25-35","20 to 30",
    "18 to 25","19 to 25","19 to 27","18 to 30"
]

INCLUDE_KEYWORDS = ["boy","male","teen","young","youth","kid","child","actor","16","17","15","14","18"]

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
            if any(k in text for k in EXCLUDE_KEYWORDS):
                continue
            if not any(k in text for k in ["audition","casting","actor","role","call"]):
                continue
            if not any(k in text for k in INCLUDE_KEYWORDS):
                continue
            results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "source": "Google",
                "type": detect_type(text),
                "platform": detect_platform(text),
                "date": datetime.now().strftime("%Y-%m-%d")
            })
    except Exception as e:
        print(f"Error: {e}")
    return results

def detect_type(text):
    if any(k in text for k in ["netflix","prime","hotstar","jio","ott","web series","webseries","streaming"]):
        return "ott"
    elif any(k in text for k in ["film","movie","feature","bollywood","cinema"]):
        return "film"
    elif any(k in text for k in ["ad","commercial","brand","campaign","advertisement"]):
        return "ad"
    elif any(k in text for k in ["theatre","theater","play","stage"]):
        return "theatre"
    else:
        return "short"

def detect_platform(text):
    if "netflix" in text: return "Netflix"
    if "amazon" in text or "prime" in text: return "Amazon Prime"
    if "hotstar" in text or "jio" in text: return "JioHotstar"
    if "sony" in text: return "Sony LIV"
    if "zee" in text: return "Zee5"
    return ""

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
