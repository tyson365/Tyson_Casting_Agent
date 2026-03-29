import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

SEARCH_QUERIES = [
    "teen male actor audition India 2026",
    "casting call boy 15 16 17 India web series 2026",
    "Netflix Amazon Prime audition teen India 2026",
    "Bollywood teen actor casting call 2026",
]

def search_auditions(query):
    results = []
    try:
        url = f"https://www.google.com/search?q={query.replace(' ','+')}&num=10"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for g in soup.find_all("div", class_="tF2Cxc")[:5]:
            title_el = g.find("h3")
            link_el = g.find("a")
            snippet_el = g.find("div", class_="VwiC3b")
            if title_el and link_el:
                title = title_el.get_text(strip=True)
                link = link_el.get("href","")
                snippet = snippet_el.get_text(strip=True) if snippet_el else ""
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
        print(f"Search error: {e}")
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
    return {"ott":1,"film":2,"ad":3,"short":4,"theatre":5}.get(item["type"],5)

def main():
    all_results = []
    seen = set()
    for q in SEARCH_QUERIES:
        for r in search_auditions(q):
            if r["title"] not in seen:
                seen.add(r["title"])
                all_results.append(r)
    all_results.sort(key=rank)
    for i, r in enumerate(all_results):
        r["rank"] = i + 1
    with open("auditions.json","w") as f:
        json.dump(all_results, f, indent=2)
    print(f"Done. Found {len(all_results)} auditions.")

if __name__ == "__main__":
    main()
