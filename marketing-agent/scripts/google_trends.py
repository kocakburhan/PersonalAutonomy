"""
Google Trends scraper — pytrends wrapper.
Ucretsiz, API key gerektirmez.

Kullanim:
    python google_trends.py --keywords "cilt bakimi,yuz yogasi" --timeframe "today 3-m" --category 0
    python google_trends.py --keywords "skincare" --timeframe "today 12-m" --geo TR

Cikti: JSON stdout. Her keyword icin:
    - zaman serisi (tarih → ilgi puani 0-100)
    - ortalama ilgi
    - trend yonu (yükselis/düsüs/duragan)
    - ilgili sorgular (rising + top)
    - ilgili konular (rising + top)

Bagimlilik: pip install pytrends
"""

import json
import sys
import argparse
from datetime import datetime

try:
    from pytrends.request import TrendReq
except ImportError:
    print(json.dumps({"error": "pytrends not installed. Run: pip install pytrends"}, ensure_ascii=False))
    sys.exit(1)

def parse_timeframe(tf: str) -> str:
    """'today 3-m' → pytrends-friendly format"""
    return tf

def analyze_trend(keywords: list[str], timeframe: str = "today 12-m", geo: str = "", category: int = 0) -> dict:
    pytrends = TrendReq(hl="tr-TR" if geo == "TR" else "en-US", tz=360)
    pytrends.build_payload(keywords, cat=category, timeframe=timeframe, geo=geo, gprop="")

    result: dict = {"keywords": keywords, "timeframe": timeframe, "geo": geo, "queried_at": datetime.now().isoformat()}

    try:
        interest_over_time = pytrends.interest_over_time()
        if interest_over_time.empty:
            result["error"] = "No data for this timeframe/geo combination"
            return result

        result["interest_time_series"] = {}
        for kw in keywords:
            if kw in interest_over_time.columns:
                series = interest_over_time[kw].dropna()
                result["interest_time_series"][kw] = {
                    "data": {str(d.date()): int(v) for d, v in series.items()},
                    "average": round(float(series.mean()), 1),
                    "max": int(series.max()),
                    "min": int(series.min()),
                    "trend": _trend_direction(series)
                }

        result["related_queries"] = {}
        result["related_topics"] = {}
        related = pytrends.related_queries()
        for kw in keywords:
            if kw in related:
                rising = related[kw].get("rising")
                top = related[kw].get("top")
                result["related_queries"][kw] = {
                    "rising": rising.to_dict("records")[:10] if rising is not None else [],
                    "top": top.to_dict("records")[:10] if top is not None else []
                }

    except Exception as e:
        result["error"] = str(e)

    return result


def _trend_direction(series) -> str:
    if len(series) < 2:
        return "yetersiz_veri"
    first_half = series.head(len(series) // 2).mean()
    second_half = series.tail(len(series) // 2).mean()
    pct_change = ((second_half - first_half) / max(first_half, 1)) * 100
    if pct_change > 15:
        return "yükseliş"
    elif pct_change < -15:
        return "düşüş"
    return "durağan"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Trends scraper via pytrends")
    parser.add_argument("--keywords", required=True, help="Virgulle ayrilmis anahtar kelimeler")
    parser.add_argument("--timeframe", default="today 12-m", help="Zaman araligi (today 3-m, today 12-m, 2024-01-01 2024-12-31)")
    parser.add_argument("--geo", default="", help="Ulke kodu (TR, US, DE... bos = worldwide)")
    parser.add_argument("--category", type=int, default=0, help="Kategori ID (0 = tum kategoriler)")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",")]
    result = analyze_trend(keywords, args.timeframe, args.geo, args.category)
    print(json.dumps(result, ensure_ascii=False, indent=2))
