"""
Marketing Page Analyzer
HTML parser that extracts SEO, content, conversion, trust, and tracking signals from a webpage.
Usage: python analyze_page.py <url>
Output: JSON to stdout
"""

import sys
import re
import json
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import URLError


class MarketingPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.h1 = []
        self.h2 = []
        self.h3 = []
        self.images = []
        self.links = []
        self.buttons = []
        self.forms = 0
        self.scripts = []
        self.in_title = False
        self.in_h1 = False
        self.in_h2 = False
        self.in_h3 = False
        self.in_button = False
        self.current_tag = ""
        self.current_attrs = {}
        self.schema_types = []
        self.has_ssl = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            self.in_title = True
        elif tag in ("h1", "h2", "h3"):
            self.current_tag = tag
            setattr(self, f"in_{tag}", True)
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            if name == "description" or prop == "og:description":
                self.meta_description = attrs_dict.get("content", "")
        elif tag == "img":
            alt = attrs_dict.get("alt", "")
            src = attrs_dict.get("src", "")
            if src:
                self.images.append({"src": src, "alt": alt, "missing_alt": not bool(alt)})
        elif tag == "a":
            href = attrs_dict.get("href", "")
            text = attrs_dict.get("aria-label", "")
            cls = attrs_dict.get("class", "")
            self.links.append({"href": href, "text": text, "class": cls})
        elif tag == "button":
            self.in_button = True
            self.current_attrs = attrs_dict
        elif tag == "form":
            self.forms += 1
        elif tag == "script":
            script_type = attrs_dict.get("type", "")
            if "application/ld+json" in script_type:
                self.schema_types.append("json-ld")
            src = attrs_dict.get("src", "")
            if src:
                self.scripts.append(src)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in ("h1", "h2", "h3"):
            setattr(self, f"in_{tag}", False)
            self.current_tag = ""
        elif self.in_button and tag == "button":
            self.buttons.append({
                "text": self._current_data.strip() if hasattr(self, '_current_data') else "",
                "attrs": self.current_attrs
            })
            self.in_button = False
            self.current_attrs = {}

    def handle_data(self, data):
        self._current_data = data
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1.append(data.strip())
        elif self.in_h2:
            self.h2.append(data.strip())
        elif self.in_h3:
            self.h3.append(data.strip())


def fetch_page(url: str) -> str:
    """Fetch page content with basic browser-like headers."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
    }
    req = Request(url, headers=headers)
    response = urlopen(req, timeout=15)
    return response.read().decode("utf-8", errors="replace")


def analyze_page(url: str) -> dict:
    try:
        html = fetch_page(url)
    except URLError as e:
        return {"error": f"Failed to fetch {url}: {e}"}

    parser = MarketingPageParser()
    parser.feed(html)
    parser.has_ssl = url.startswith("https://")

    word_count = len(re.findall(r"\b\w+\b", " ".join(parser.h1 + parser.h2)))

    return {
        "url": url,
        "ssl": parser.has_ssl,
        "title": parser.title.strip(),
        "title_length": len(parser.title.strip()),
        "title_ok": 30 <= len(parser.title.strip()) <= 70,
        "meta_description": parser.meta_description.strip(),
        "meta_length": len(parser.meta_description.strip()),
        "meta_ok": 120 <= len(parser.meta_description.strip()) <= 160,
        "headings": {
            "h1_count": len(parser.h1),
            "h1": parser.h1,
            "h2_count": len(parser.h2),
            "h2": parser.h2,
            "h3_count": len(parser.h3),
            "h3": parser.h3,
        },
        "images": {
            "total": len(parser.images),
            "missing_alt": sum(1 for img in parser.images if img["missing_alt"]),
            "items": parser.images[:20],  # first 20
        },
        "links": {
            "total": len(parser.links),
            "internal": sum(1 for l in parser.links if url in l.get("href", "") or l.get("href", "").startswith("/")),
            "external": sum(1 for l in parser.links if l.get("href", "").startswith(("http://", "https://")) and url not in l.get("href", "")),
        },
        "conversion": {
            "forms": parser.forms,
            "buttons": parser.buttons,
        },
        "content": {
            "word_count_estimate": word_count,
        },
        "technical": {
            "schema_types": parser.schema_types,
            "script_count": len(parser.scripts),
        },
        "score": _calculate_score(parser),
    }


def _calculate_score(parser) -> dict:
    scores = {}

    # Title score
    title_len = len(parser.title.strip())
    scores["title"] = 80 if 30 <= title_len <= 70 else (40 if 10 <= title_len <= 100 else 10)

    # Meta score
    meta_len = len(parser.meta_description.strip())
    scores["meta"] = 80 if 120 <= meta_len <= 160 else (40 if meta_len > 0 else 0)

    # Heading score
    scores["headings"] = 100 if len(parser.h1) == 1 else (50 if len(parser.h1) > 0 else 0)

    # Image alt score
    total_imgs = len(parser.images)
    missing = sum(1 for img in parser.images if img["missing_alt"])
    scores["images"] = 100 if total_imgs == 0 else max(0, 100 - (missing / total_imgs * 100))

    # Form / CTA score
    scores["cta"] = 80 if parser.forms > 0 or len(parser.buttons) > 0 else 20

    # SSL score
    scores["ssl"] = 100 if parser.has_ssl else 0

    weights = {"title": 20, "meta": 15, "headings": 15, "images": 10, "cta": 20, "ssl": 20}
    overall = sum(scores[k] * weights[k] / 100 for k in weights)
    scores["overall"] = round(overall, 1)

    return scores


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python analyze_page.py <url>"}))
        sys.exit(1)

    url = sys.argv[1]
    result = analyze_page(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
