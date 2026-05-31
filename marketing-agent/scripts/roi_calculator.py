"""
Bütce / ROI hesaplayici.
CAC, LTV, breakeven, payback period, kampanya ROI'si.

Kullanim:
    python roi_calculator.py --cac 150 --arpu 50 --churn 5
    python roi_calculator.py --campaign --budget 5000 --cac 150 --arpu 50 --churn 5
    python roi_calculator.py --ltv-only --arpu 50 --churn 5

Cikti: JSON stdout.
"""

import json
import argparse
import sys


def calculate_ltv(arpu: float, monthly_churn_pct: float) -> dict:
    churn_rate = monthly_churn_pct / 100
    avg_lifetime_months = 1 / churn_rate if churn_rate > 0 else 120
    ltv = arpu * avg_lifetime_months

    return {
        "arpu": arpu,
        "monthly_churn_pct": monthly_churn_pct,
        "avg_lifetime_months": round(avg_lifetime_months, 1),
        "ltv": round(ltv, 2),
        "interpretation": _ltv_interpretation(ltv, arpu)
    }


def calculate_unit_economics(cac: float, arpu: float, monthly_churn_pct: float) -> dict:
    ltv_data = calculate_ltv(arpu, monthly_churn_pct)
    ltv = ltv_data["ltv"]
    ltv_cac_ratio = ltv / cac if cac > 0 else 0
    payback_months = cac / arpu if arpu > 0 else 0
    gross_margin_per_user = ltv - cac

    return {
        **ltv_data,
        "cac": cac,
        "ltv_cac_ratio": round(ltv_cac_ratio, 2),
        "payback_months": round(payback_months, 1),
        "gross_margin_per_user": round(gross_margin_per_user, 2),
        "health": _health_status(ltv_cac_ratio, payback_months)
    }


def calculate_campaign_roi(budget: float, cac: float, arpu: float, monthly_churn_pct: float) -> dict:
    expected_users = budget / cac if cac > 0 else 0
    ltv_data = calculate_ltv(arpu, monthly_churn_pct)
    ltv = ltv_data["ltv"]
    total_ltv = expected_users * ltv
    roi_pct = ((total_ltv - budget) / budget * 100) if budget > 0 else 0
    breakeven_revenue = budget

    monthly_rev = expected_users * arpu
    breakeven_month = 0
    cumulative = 0
    for m in range(1, 37):
        churned = expected_users * ((monthly_churn_pct / 100) * (m - 1))
        active = max(expected_users - churned, 0)
        cumulative += active * arpu
        if cumulative >= budget and breakeven_month == 0:
            breakeven_month = m
            break

    if breakeven_month == 0:
        breakeven_month = breakeven_month or 37

    return {
        "budget": budget,
        "expected_users": round(expected_users),
        "arpu": arpu,
        "ltv": round(ltv, 2),
        "total_ltv": round(total_ltv, 2),
        "roi_pct": round(roi_pct, 1),
        "breakeven_month": breakeven_month,
        "monthly_revenue_estimate": round(monthly_rev, 2),
        "verdict": _campaign_verdict(roi_pct, breakeven_month)
    }


def _ltv_interpretation(ltv: float, arpu: float) -> str:
    ratio = ltv / arpu if arpu > 0 else 0
    if ratio > 24:
        return f"Güçlü: Kullanici ortalama {ratio:.0f} ay kaliyor"
    elif ratio > 12:
        return f"İyi: Kullanici ortalama {ratio:.0f} ay kaliyor"
    elif ratio > 6:
        return f"Orta: Kullanici ortalama {ratio:.0f} ay kaliyor. Churn'u düsürmeye calis."
    return f"Zayif: Kullanici ortalama {ratio:.0f} ay kaliyor. Retention'a odaklan."


def _health_status(ltv_cac: float, payback: float) -> str:
    if ltv_cac >= 3 and payback <= 12:
        return "sağlıklı — ölçeklenebilir"
    elif ltv_cac >= 1 and payback <= 18:
        return "idare eder — CAC'i düsür veya ARPU'yu artir"
    return "kritik — birim ekonomisi sürdürülemez"


def _campaign_verdict(roi_pct: float, breakeven: int) -> str:
    if roi_pct > 200:
        return f"Kesinlikle yap. %{roi_pct:.0f} ROI, {breakeven}. ayda breakeven."
    elif roi_pct > 0:
        return f"Yapilabilir. %{roi_pct:.0f} ROI, {breakeven}. ayda breakeven."
    return f"Yapma. %{roi_pct:.0f} ROI, breakeven {breakeven}+ ay."


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ROI / Bütce hesaplayici")
    parser.add_argument("--cac", type=float, default=0, help="Customer Acquisition Cost (TL)")
    parser.add_argument("--arpu", type=float, required=True, help="Aylik kullanici basi gelir (TL)")
    parser.add_argument("--churn", type=float, required=True, help="Aylik churn orani (% cinsinden, 5 = %5)")
    parser.add_argument("--campaign", action="store_true", help="Kampanya ROI modu")
    parser.add_argument("--budget", type=float, default=0, help="Kampanya bütcesi (TL)")
    parser.add_argument("--ltv-only", action="store_true", help="Sadece LTV hesapla")
    args = parser.parse_args()

    if args.ltv_only:
        result = calculate_ltv(args.arpu, args.churn)
    elif args.campaign:
        if args.budget <= 0 or args.cac <= 0:
            print(json.dumps({"error": "--campaign modunda --budget ve --cac zorunlu"}, ensure_ascii=False))
            sys.exit(1)
        result = calculate_campaign_roi(args.budget, args.cac, args.arpu, args.churn)
    else:
        if args.cac <= 0:
            print(json.dumps({"error": "--cac zorunlu (veya --ltv-only kullan)"}, ensure_ascii=False))
            sys.exit(1)
        result = calculate_unit_economics(args.cac, args.arpu, args.churn)

    print(json.dumps(result, ensure_ascii=False, indent=2))
