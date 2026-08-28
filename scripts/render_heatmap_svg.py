#!/usr/bin/env python3
"""Render contribution heatmap SVG - static version that GitHub will display."""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL_SIZE = 13
CELL_GAP = 3
CELL_ROUND = 2
WEEKS = 53
DAYS = 7
MARGIN_LEFT = 40
MARGIN_TOP = 30

SVG_WIDTH = MARGIN_LEFT + WEEKS * (CELL_SIZE + CELL_GAP) + 20
SVG_HEIGHT = MARGIN_TOP + DAYS * (CELL_SIZE + CELL_GAP) + 70


def generate_heatmap_svg(data: dict) -> str:
    contributions = data.get("contributions", [])
    stats = data.get("stats", {})
    contrib_map = {c["date"]: c for c in contributions}

    if contributions:
        dates = [c["date"] for c in contributions]
        start_date = datetime.strptime(min(dates), "%Y-%m-%d")
    else:
        start_date = datetime.now() - timedelta(weeks=52)

    lines = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" width="{SVG_WIDTH}" height="{SVG_HEIGHT}">')
    lines.append(f'<rect width="100%" height="100%" fill="#0d1117"/>')

    # Day labels
    for i, label in enumerate(["", "Mon", "", "Wed", "", "Fri", ""]):
        if label:
            y = MARGIN_TOP + i * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
            lines.append(f'<text font-family="monospace" font-size="10" fill="#8b949e" x="0" y="{y}">{label}</text>')

    # Month labels
    current_month = None
    for week in range(WEEKS):
        week_start = start_date + timedelta(weeks=week)
        month = week_start.strftime("%b")
        if month != current_month:
            current_month = month
            x = MARGIN_LEFT + week * (CELL_SIZE + CELL_GAP)
            lines.append(f'<text font-family="monospace" font-size="10" fill="#8b949e" x="{x}" y="{MARGIN_TOP - 8}">{month}</text>')

    # Cells - NO animation, just static
    for week in range(WEEKS):
        for day in range(DAYS):
            cell_date = start_date + timedelta(weeks=week, days=day)
            date_str = cell_date.strftime("%Y-%m-%d")
            contrib = contrib_map.get(date_str, {"count": 0, "level": 0})
            level = contrib.get("level", 0)
            x = MARGIN_LEFT + week * (CELL_SIZE + CELL_GAP)
            y = MARGIN_TOP + day * (CELL_SIZE + CELL_GAP)
            color = PALETTE[min(level, len(PALETTE) - 1)]
            lines.append(f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}" rx="{CELL_ROUND}"/>')

    # Legend
    legend_y = MARGIN_TOP + DAYS * (CELL_SIZE + CELL_GAP) + 15
    lines.append(f'<text font-family="monospace" font-size="10" fill="#8b949e" x="{MARGIN_LEFT}" y="{legend_y}">Less</text>')
    for i, color in enumerate(PALETTE):
        box_x = MARGIN_LEFT + 40 + i * (CELL_SIZE + CELL_GAP)
        lines.append(f'<rect x="{box_x}" y="{legend_y - 10}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}" rx="{CELL_ROUND}"/>')
    lines.append(f'<text font-family="monospace" font-size="10" fill="#8b949e" x="{MARGIN_LEFT + 40 + len(PALETTE) * (CELL_SIZE + CELL_GAP) + 8}" y="{legend_y}">More</text>')

    # Stats
    stats_y = legend_y + 30
    total = stats.get("total", 0)
    lines.append(f'<text font-family="monospace" font-size="12" fill="#c9d1d9" x="{MARGIN_LEFT}" y="{stats_y}">{total:,} contributions in the last year</text>')

    lines.append('</svg>')
    return '\n'.join(lines)


def main():
    data_path = "data/contributions.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    svg_content = generate_heatmap_svg(data)
    with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Saved contrib-heatmap.svg")


if __name__ == "__main__":
    main()
