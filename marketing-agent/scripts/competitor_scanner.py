"""
Competitor Website Scanner
Scans competitor websites for positioning, pricing, and social proof signals.
Usage: python competitor_scanner.py <url1> <url2> ... <urlN>
Output: JSON to stdout
"""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError
from html.parser import HTMLParser

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class CompetitorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.title = ""
        self.in_title = False
        self.meta_description = ""
        self.headings = {"h1": [], "h2": [], "h3": []}
        self.current_heading = ""
        self.pricing_keywords = []
        self.trust_signals = []
        self.social_links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag in ("h1", "h2", "h3"):
            self.current_heading = tag
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            if name == "description":
                self.meta_description = attrs_dict.get("content", "")
        elif tag == "a":
            href = attrs_dict.get("href", "")
            if any(s in href for s in ("twitter.com", "facebook.com", "linkedin.com", "instagram.com")):
                self.social_links.append(href)

    def handle_endtag(self, tag):
        if tag in ("h1", "h2", "h3"):
            self.current_heading = ""
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        data = data.strip()
        if self.in_title:
            self.title += data
        if self.current_heading:
            self.headings[self.current_heading].append(data)

        # Detect pricing signals
        if any(kw in data.lower() for kw in ("ücret", "fiyat", "price", "plan", "aylık", "yıllık", "free", "pro", "enterprise", "₺", "$", "€")):
            self.pricing_keywords.append(data)

        # Detect trust signals
        if any(kw in data.lower() for kw in ("güvenli", "ssl", "şifre", "gizlilik", "garanti", "iade", "yorum", "müşteri", "500+", "1000+", "10k+", "review", "testimonial", "trusted by")):
            self.trust_signals.append(data)

        self.text_content.append(data)


def scan_competitor(url: str) -> dict:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en,tr"})
        response = urlopen(req, timeout=15)
        html = response.read().decode("utf-8", errors="replace")
    except URLError as e:
        return {"url": url, "error": str(e)}

    parser = CompetitorParser()
    parser.feed(html)

    return {
        "url": url,
        "title": parser.title.strip(),
        "meta_description": parser.meta_description,
        "headings": {
            "h1_count": len(parser.headings["h1"]),
            "h2_count": len(parser.headings["h2"]),
            "h3_count": len(parser.headings["h3"]),
        },
        "pricing_signals": parser.pricing_keywords[:15],
        "trust_signals": parser.trust_signals[:15],
        "social_links": parser.social_links,
        "word_count": len([t for t in parser.text_content if t]),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python competitor_scanner.py <url1> <url2> ..."}))
        sys.exit(1)

    results = [scan_competitor(url) for url in sys.argv[1:]]
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
