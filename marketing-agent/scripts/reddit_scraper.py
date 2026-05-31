"""
Reddit scraper — subreddit ve keyword bazli icerik cekme.
Reddit JSON API kullanir (OAuth gerektirmez, rate-limited).

Kullanim:
    python reddit_scraper.py --subreddits "startups,sideproject,SaaS" --keywords "problem,need,app" --limit 50
    python reddit_scraper.py --subreddits "iosprogramming" --keywords "review,alternative" --sort top --limit 100

Cikti: JSON stdout. Her post icin:
    - subreddit, baslik, metin, skor, yorum sayisi, url, tarih
    - keyword match'leri (hangi keyword'ler eslesti)
    - pain_point_score (sikayet/istek belirtme olasiligi 0-1)

Bagimlilik: stdlib only (urllib)
"""

import json
import sys
import argparse
import urllib.request
import urllib.parse
import time
from datetime import datetime

REDDIT_BASE = "https://www.reddit.com"

PAIN_KEYWORDS = [
    "looking for", "is there an app", "any app", "recommend",
    "need", "wish there was", "i want", "does anyone",
    "frustrated", "hate", "terrible", "worst", "ugly",
    "bug", "crash", "doesn't work", "broken",
    "too expensive", "overpriced", "not worth",
    "alternative to", "replacement for", "better than",
    "missing", "lacking", "should have", "why doesn't"
]

def search_subreddits(subreddits: list[str], keywords: list[str], sort: str = "relevance", limit: int = 50) -> list[dict]:
    results = []
    seen_urls = set()

    for subreddit in subreddits:
        for keyword in keywords:
            query = f'subreddit:{subreddit} {keyword}'
            url = f"{REDDIT_BASE}/search.json?q={urllib.parse.quote(query)}&sort={sort}&limit={min(limit, 100)}&t=year"

            try:
                req = urllib.request.Request(url, headers={"User-Agent": "marketing-agent/1.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode())

                for post in data.get("data", {}).get("children", []):
                    pdata = post["data"]
                    permalink = pdata.get("permalink", "")
                    if permalink in seen_urls:
                        continue
                    seen_urls.add(permalink)

                    title = pdata.get("title", "")
                    selftext = pdata.get("selftext", "")
                    full_text = f"{title} {selftext}".lower()

                    matched = [kw for kw in keywords if kw.lower() in full_text]

                    pain_score = _pain_score(full_text)

                    results.append({
                        "subreddit": pdata.get("subreddit"),
                        "title": title,
                        "selftext": selftext[:500],
                        "score": pdata.get("score"),
                        "num_comments": pdata.get("num_comments"),
                        "url": f"{REDDIT_BASE}{permalink}",
                        "created_utc": datetime.utcfromtimestamp(pdata.get("created_utc", 0)).isoformat(),
                        "matched_keywords": matched,
                        "pain_point_score": round(pain_score, 2)
                    })
            except urllib.error.HTTPError as e:
                results.append({"error": f"HTTP {e.code} on r/{subreddit} + '{keyword}'"})
            except Exception as e:
                results.append({"error": str(e)})

            time.sleep(2)

    results.sort(key=lambda x: x.get("pain_point_score", 0), reverse=True)
    return results[:limit]


def search_keywords_across_reddit(keywords: list[str], limit: int = 50) -> list[dict]:
    """Tum Reddit'te keyword ara (subreddit filtresiz)."""
    results = []
    seen_urls = set()

    for keyword in keywords:
        url = f"{REDDIT_BASE}/search.json?q={urllib.parse.quote(keyword)}&sort=relevance&limit={min(limit, 100)}&t=year"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "marketing-agent/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())

            for post in data.get("data", {}).get("children", []):
                pdata = post["data"]
                permalink = pdata.get("permalink", "")
                if permalink in seen_urls:
                    continue
                seen_urls.add(permalink)

                title = pdata.get("title", "")
                selftext = pdata.get("selftext", "")
                full_text = f"{title} {selftext}".lower()

                results.append({
                    "subreddit": pdata.get("subreddit"),
                    "title": title,
                    "selftext": selftext[:500],
                    "score": pdata.get("score"),
                    "num_comments": pdata.get("num_comments"),
                    "url": f"{REDDIT_BASE}{permalink}",
                    "created_utc": datetime.utcfromtimestamp(pdata.get("created_utc", 0)).isoformat(),
                    "pain_point_score": round(_pain_score(full_text), 2)
                })
        except urllib.error.HTTPError as e:
            results.append({"error": f"HTTP {e.code} on keyword '{keyword}'"})
        except Exception as e:
            results.append({"error": str(e)})

        time.sleep(2)

    results.sort(key=lambda x: x.get("pain_point_score", 0), reverse=True)
    return results[:limit]


def _pain_score(text: str) -> float:
    score = 0
    for kw in PAIN_KEYWORDS:
        if kw in text:
            score += 1 / len(PAIN_KEYWORDS)
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit subreddit/keyword scraper")
    parser.add_argument("--subreddits", default="", help="Virgulle ayrilmis subreddit'ler (opsiyonel)")
    parser.add_argument("--keywords", required=True, help="Virgulle ayrilmis anahtar kelimeler")
    parser.add_argument("--sort", default="relevance", choices=["relevance", "top", "new", "comments"])
    parser.add_argument("--limit", type=int, default=50, help="Max sonuc sayisi")
    parser.add_argument("--all-reddit", action="store_true", help="Tum Reddit'te ara (subreddit filtresiz)")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",")]

    if args.all_reddit:
        results = search_keywords_across_reddit(keywords, args.limit)
    else:
        subreddits = [s.strip() for s in args.subreddits.split(",")] if args.subreddits else []
        if not subreddits:
            print(json.dumps({"error": "--subreddits required (or use --all-reddit)"}, ensure_ascii=False))
            sys.exit(1)
        results = search_subreddits(subreddits, keywords, args.sort, args.limit)

    output = {
        "queried_at": datetime.now().isoformat(),
        "subreddits": subreddits if not args.all_reddit else "all",
        "keywords": keywords,
        "sort": args.sort,
        "result_count": len(results),
        "results": results
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
