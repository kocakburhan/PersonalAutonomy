"""
PDF Report Generator
Generates professional marketing report PDFs using ReportLab.
Usage: python generate_pdf_report.py --input REPORT.md --output REPORT.pdf --title "Marketing Report"
"""

import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path


def parse_md_report(md_path: str) -> dict:
    """Parse marketing report markdown into structured data."""
    content = Path(md_path).read_text(encoding="utf-8")

    data = {
        "url": "",
        "date": "",
        "score": 0,
        "categories": [],
        "wins": [],
        "fixes": [],
        "actions": [],
    }

    # Extract URL
    url_match = re.search(r"# Pazarlama Raporu: (.+)", content)
    if url_match:
        data["url"] = url_match.group(1).strip()

    # Extract date
    date_match = re.search(r"\*\*Tarih:\*\* (.+)", content)
    if date_match:
        data["date"] = date_match.group(1)

    # Extract overall score
    score_match = re.search(r"\*\*Genel Pazarlama Skoru:\*\* (\d+)/100", content)
    if score_match:
        data["score"] = int(score_match.group(1))

    # Extract category scores
    cat_matches = re.findall(
        r"\|\s*(.+?)\s*\|\s*(\d+)/100\s*\|\s*(\d+)%\s*\|",
        content,
    )
    for cat_name, cat_score, cat_weight in cat_matches:
        data["categories"].append({
            "name": cat_name.strip(),
            "score": int(cat_score),
            "weight": int(cat_weight),
        })

    # Extract wins
    win_section = re.search(r"En Büyük 3 Güçlü Yön:\*\*\n(.*?)(?:\n\n|\*\*En)", content, re.DOTALL)
    if win_section:
        data["wins"] = re.findall(r"\d+\.\s*(.+)", win_section.group(1))

    # Extract fixes
    fix_section = re.search(r"En Büyük 3 Gelişim Alanı:\*\*\n(.*?)(?:\n\n|---)", content, re.DOTALL)
    if fix_section:
        data["fixes"] = re.findall(r"\d+\.\s*(.+)", fix_section.group(1))

    # Extract action items
    action_lines = re.findall(r"\d+\.\s*(.+)", content)
    data["actions"] = action_lines[-10:] if len(action_lines) > 10 else action_lines

    return data


def color_for_score(score: int) -> tuple:
    """Return (r, g, b) for score."""
    if score >= 80:
        return (0.2, 0.7, 0.3)  # green
    elif score >= 60:
        return (1.0, 0.75, 0.1)  # yellow
    else:
        return (0.9, 0.2, 0.2)  # red


def build_pdf_with_reportlab(data: dict, output_path: str, title: str):
    """Build PDF using reportlab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm, cm
        from reportlab.lib.colors import HexColor
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            PageBreak, Image
        )
        from reportlab.graphics.shapes import Drawing, Rect, String
        from reportlab.graphics.charts.barcharts import VerticalBarChart
    except ImportError:
        print("Error: reportlab not installed. Run: pip install reportlab")
        sys.exit(1)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=22, spaceAfter=12)
    heading_style = ParagraphStyle("CustomHeading", parent=styles["Heading2"], fontSize=14, spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle("CustomBody", parent=styles["Normal"], fontSize=10, leading=14)

    elements = []

    # --- Cover Page ---
    elements.append(Spacer(1, 5 * cm))
    elements.append(Paragraph(f"Marketing Report", title_style))
    elements.append(Paragraph(f"<b>{data['url']}</b>", body_style))
    elements.append(Paragraph(f"Date: {data.get('date', datetime.now().strftime('%Y-%m-%d'))}", body_style))

    score = data.get("score", 0)
    r, g, b = color_for_score(score)
    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph(
        f'<font size="48" color="#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"><b>{score}/100</b></font>',
        ParagraphStyle("ScoreStyle", alignment=1),
    ))

    elements.append(PageBreak())

    # --- Executive Summary ---
    elements.append(Paragraph("Executive Summary", heading_style))

    wins_text = "<br/>".join([f"✅ {w}" for w in data.get("wins", [])[:3]])
    fixes_text = "<br/>".join([f"🔧 {f}" for f in data.get("fixes", [])[:3]])

    elements.append(Paragraph("<b>Top 3 Strengths:</b>", body_style))
    elements.append(Paragraph(wins_text or "N/A", body_style))
    elements.append(Spacer(1, 0.5 * cm))
    elements.append(Paragraph("<b>Top 3 Areas for Improvement:</b>", body_style))
    elements.append(Paragraph(fixes_text or "N/A", body_style))

    elements.append(PageBreak())

    # --- Score Summary Table ---
    elements.append(Paragraph("Score Summary", heading_style))

    table_data = [["Category", "Score", "Weight", "Weighted"]]
    for cat in data.get("categories", []):
        w_score = cat["score"] * cat["weight"] / 100
        table_data.append([
            cat["name"],
            f"{cat['score']}/100",
            f"{cat['weight']}%",
            f"{w_score:.1f}",
        ])

    if table_data:
        col_widths = [6 * cm, 3 * cm, 3 * cm, 3 * cm]
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#333333")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(table)

    elements.append(PageBreak())

    # --- Action Items ---
    elements.append(Paragraph("Action Items", heading_style))
    for i, action in enumerate(data.get("actions", [])[:10], 1):
        elements.append(Paragraph(f"{i}. {action}", body_style))

    # Build doc
    doc.build(elements)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate PDF marketing report")
    parser.add_argument("--input", required=True, help="Input markdown file")
    parser.add_argument("--output", default="MARKETING-REPORT.pdf", help="Output PDF file")
    parser.add_argument("--title", default="Marketing Report", help="Report title")
    args = parser.parse_args()

    data = parse_md_report(args.input)
    success = build_pdf_with_reportlab(data, args.output, args.title)

    if success:
        print(f"PDF report generated: {args.output}")
    else:
        print("Failed to generate PDF.")
        sys.exit(1)


if __name__ == "__main__":
    main()
