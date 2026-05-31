"""
App Store / Google Play revenue estimator.
mcp-appstore'dan gelen verilerle aylik gelir tahmini yapar.

Formul:
    revenue = rating_count × avg_subscription_price × conversion_rate
    conversion_rate default: 0.02 (%2)

Kullanim:
    python estimate_revenue.py --ratings 15678956 --price 9.99 --rate 0.02
    python estimate_revenue.py --ratings 50000 --price 4.99 --platform ios --category "Health & Fitness"
    python estimate_revenue.py --json '{"ratings": 50000, "avg_price": 4.99}'

Cikti: JSON stdout.

Not: Bu tahminidir. Gercek revenue sadece SensorTower/data.ai gibi ucretli araclardan alinabilir.
"""

import json
import sys
import argparse

DEFAULT_CONVERSION_RATE = 0.02

CATEGORY_MULTIPLIERS = {
    "Health & Fitness": 1.3,
    "Education": 1.1,
    "Finance": 1.5,
    "Business": 1.4,
    "Productivity": 1.2,
    "Social Networking": 0.8,
    "Entertainment": 0.7,
    "Games": 0.5,
    "Music": 0.9,
    "Lifestyle": 1.0,
    "Travel": 1.1,
    "Food & Drink": 0.9,
    "Shopping": 1.3,
    "Medical": 1.4,
    "Utilities": 0.9
}

PLATFORM_MULTIPLIERS = {
    "ios": 1.2,
    "android": 0.8
}


def estimate(ratings: int, avg_price: float, conversion_rate: float = DEFAULT_CONVERSION_RATE,
             category: str | None = None, platform: str | None = None) -> dict:
    base = ratings * avg_price * conversion_rate
    cat_mult = CATEGORY_MULTIPLIERS.get(category, 1.0) if category else 1.0
    plat_mult = PLATFORM_MULTIPLIERS.get(platform, 1.0) if platform else 1.0
    monthly = base * cat_mult * plat_mult

    return {
        "ratings": ratings,
        "avg_price": avg_price,
        "conversion_rate": conversion_rate,
        "category_multiplier": cat_mult,
        "platform_multiplier": plat_mult,
        "estimated_monthly_revenue": round(monthly, 2),
        "estimated_annual_revenue": round(monthly * 12, 2),
        "confidence": _confidence(ratings),
        "note": "Tahminidir. Gercek revenue sadece ucretli araclardan alinabilir."
    }


def _confidence(rating_count: int) -> str:
    if rating_count > 100000:
        return "orta-yuksek (cok sayida yorum)"
    elif rating_count > 10000:
        return "orta"
    elif rating_count > 1000:
        return "dusuk-orta"
    return "dusuk (az yorum, sapma yuksek)"


def estimate_from_mcp_data(app_data: dict, conversion_rate: float = DEFAULT_CONVERSION_RATE) -> dict:
    """mcp-appstore get_app_details + get_pricing_details ciktisindan revenue tahmini."""
    ratings = app_data.get("ratings", 0)

    avg_price = 0
    iap = app_data.get("in_app_purchases", {})
    subs = app_data.get("subscriptions", {})
    items = iap.get("items", []) + subs.get("items", [])

    prices = []
    for item in items:
        price_str = item.get("price", "$0")
        try:
            prices.append(float(price_str.replace("$", "")))
        except ValueError:
            pass

    if prices:
        avg_price = sum(prices) / len(prices)
    elif not app_data.get("base_price", {}).get("is_free", True):
        price_str = app_data.get("base_price", {}).get("formattedPrice", "$0")
        try:
            avg_price = float(price_str.replace("$", ""))
        except ValueError:
            avg_price = 0

    category = None
    if isinstance(app_data.get("categories"), list) and app_data["categories"]:
        category = app_data["categories"][0].get("name")
    elif app_data.get("genre"):
        category = app_data["genre"]

    platform = app_data.get("platform")

    return estimate(ratings, avg_price, conversion_rate, category, platform)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="App Store revenue estimator")
    parser.add_argument("--ratings", type=int, help="Toplam rating sayisi")
    parser.add_argument("--price", type=float, help="Ortalama abonelik/IAP fiyati (USD)")
    parser.add_argument("--rate", type=float, default=DEFAULT_CONVERSION_RATE, help=f"Donusum orani (default: {DEFAULT_CONVERSION_RATE})")
    parser.add_argument("--category", help="App kategorisi")
    parser.add_argument("--platform", choices=["ios", "android"], help="Platform")
    parser.add_argument("--json", help="mcp-appstore JSON verisi (dosya yolu veya ham JSON string)")
    args = parser.parse_args()

    if args.json:
        try:
            with open(args.json, "r") as f:
                app_data = json.load(f)
        except (FileNotFoundError, OSError):
            app_data = json.loads(args.json)
        result = estimate_from_mcp_data(app_data, args.rate)
    elif args.ratings and args.price:
        result = estimate(args.ratings, args.price, args.rate, args.category, args.platform)
    else:
        print(json.dumps({"error": "--ratings/--price or --json required"}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
