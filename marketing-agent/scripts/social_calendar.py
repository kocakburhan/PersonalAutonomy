"""
Social Media Content Calendar Generator
Generates a structured 30-day content calendar with pillar rotation.
Usage: python social_calendar.py --topic "AI Marketing" --platforms instagram,linkedin --brand "MyBrand"
Output: JSON to stdout
"""

import sys
import json
import argparse
from datetime import datetime, timedelta

PILLARS = [
    {"name": "Değer/Eğitim", "rate": 0.40, "formats": ["Carousel", "Guide", "How-to", "İstatistik"]},
    {"name": "Sosyal Kanıt", "rate": 0.20, "formats": ["Vaka Çalışması", "Müşteri Yorumu", "UGC Repost", "Sonuçlar"]},
    {"name": "Ürün/Tanıtım", "rate": 0.15, "formats": ["Özellik Tanıtımı", "Demo", "Karşılaştırma", "Güncelleme"]},
    {"name": "Topluluk/Etkileşim", "rate": 0.15, "formats": ["Anket", "Soru-Cevap", "Challenge", "Tartışma"]},
    {"name": "Marka/Kültür", "rate": 0.10, "formats": ["Behind-the-scenes", "Ekip", "Değerler", "Etkinlik"]},
]

PLATFORM_HOOKS = {
    "instagram": [
        "{sayi} şeyi yanlış yapıyorsun 👇",
        "Bunu bilmiyordun...",
        "Kaydet, sonra teşekkür edersin 📌",
        "Yeni başlayanlar için rehber 🧵",
    ],
    "linkedin": [
        "{konu} hakkında acı bir gerçek:",
        "Geçen ay {sayi} kişiyle konuştum. Şunu fark ettim:",
        "3 ayda {sonuc} — işte nasıl yaptım:",
    ],
    "twitter": [
        "Unpopular opinion: {konu}",
        "{sayi} dakikada {sonuc} 🧵",
        "Stop doing {hata}. Do this instead:",
    ],
    "tiktok": [
        "POV: {senaryo}",
        "{sayi} things that changed my life",
        "Wait for it... 🤯",
    ],
}

HASHTAGS = {
    "instagram": ["marketing", "büyüme", "strateji", "içerik", "dijitalpazarlama"],
    "linkedin": ["marketing", "growth", "strategy", "leadership"],
    "twitter": ["marketing", "growth", "startup"],
    "tiktok": ["marketing", "growthhack", "learnontiktok"],
}


def generate_calendar(topic: str, platforms: list, brand: str, days: int = 30) -> dict:
    today = datetime.now()
    calendar = []
    pillar_counts = {p["name"]: 0 for p in PILLARS}

    for day in range(days):
        date = today + timedelta(days=day)

        # Rotate pillars to maintain ratio
        total_assigned = sum(pillar_counts.values())
        pillar = _pick_pillar(pillar_counts, total_assigned, days)
        pillar_counts[pillar["name"]] += 1

        entry = {
            "day": day + 1,
            "date": date.strftime("%Y-%m-%d"),
            "weekday": date.strftime("%A"),
            "pillar": pillar["name"],
            "format": pillar["formats"][day % len(pillar["formats"])],
            "platforms": platforms,
        }

        # Generate platform-specific content ideas
        entry["content"] = {}
        for plat in platforms:
            hooks = PLATFORM_HOOKS.get(plat, PLATFORM_HOOKS["instagram"])
            hook = hooks[day % len(hooks)].replace("{konu}", topic).replace("{sayi}", str(day + 1))
            tags = HASHTAGS.get(plat, []) + [brand.lower().replace(" ", "")]
            entry["content"][plat] = {
                "hook": hook,
                "idea": f"{pillar['name']} içeriği: {topic} — {pillar['formats'][day % len(pillar['formats'])]}",
                "hashtags": [f"#{t}" for t in tags[:7]],
            }

        calendar.append(entry)

    return {
        "topic": topic,
        "brand": brand,
        "platforms": platforms,
        "days": days,
        "pillar_distribution": pillar_counts,
        "calendar": calendar,
    }


def _pick_pillar(counts: dict, total: int, total_days: int) -> dict:
    """Pick pillar that is most under target ratio."""
    best_pillar = PILLARS[0]
    best_deficit = -999

    for pillar in PILLARS:
        current_ratio = counts[pillar["name"]] / max(total, 1)
        target = pillar["rate"] * total_days / (total + 1) if total > 0 else pillar["rate"]
        current_count = counts[pillar["name"]]
        target_count = pillar["rate"] * (total + 1)
        deficit = target_count - current_count

        if deficit > best_deficit:
            best_deficit = deficit
            best_pillar = pillar

    return best_pillar


def main():
    parser = argparse.ArgumentParser(description="Social Media Content Calendar Generator")
    parser.add_argument("--topic", required=True, help="Main topic for content")
    parser.add_argument("--platforms", default="instagram,linkedin", help="Comma-separated platforms")
    parser.add_argument("--brand", default="Brand", help="Brand name")
    parser.add_argument("--days", type=int, default=30, help="Number of days")
    args = parser.parse_args()

    platforms = [p.strip().lower() for p in args.platforms.split(",")]
    result = generate_calendar(args.topic, platforms, args.brand, args.days)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
