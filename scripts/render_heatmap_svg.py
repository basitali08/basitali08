#!/usr/bin/env python3
"""Render contribution heatmap SVG from contribution data.

Features:
- 53-week × 7-day calendar grid
- GitHub-style green color ramp
- Diagonal reveal animation
- Stats footer
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
USERNAME = "basitali08"

# Color palette (none -> brightest)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

# SVG dimensions
CELL_SIZE = 13
CELL_GAP = 3
CELL_ROUND = 2
WEEKS = 53
DAYS = 7
MARGIN_LEFT = 40
MARGIN_TOP = 30
LEGEND_HEIGHT = 20
STATS_HEIGHT = 30

SVG_WIDTH = MARGIN_LEFT + WEEKS * (CELL_SIZE + CELL_GAP) + 20
SVG_HEIGHT = MARGIN_TOP + DAYS * (CELL_SIZE + CELL_GAP) + LEGEND_HEIGHT + STATS_HEIGHT + 20


def get_day_of_week(date_str: str) -> int:
    """Get day of week (0=Sunday, 6=Saturday)."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.weekday()


def generate_heatmap_svg(data: dict) -> str:
    """Generate the heatmap SVG."""
    contributions = data.get("contributions", [])
    stats = data.get("stats", {})

    # Create date-to-contribution mapping
    contrib_map = {c["date"]: c for c in contributions}

    # Find the date range
    if contributions:
        dates = [c["date"] for c in contributions]
        start_date = datetime.strptime(min(dates), "%Y-%m-%d")
        end_date = datetime.strptime(max(dates), "%Y-%m-%d")
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=52)

    lines = []

    # SVG header
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" width="{SVG_WIDTH}" height="{SVG_HEIGHT}">
  <style>
    @keyframes slideIn {{
      from {{
        opacity: 0;
        transform: translateY(-10px) translateX(-10px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0) translateX(0);
      }}
    }}
    .cell {{
      opacity: 0;
      animation: slideIn 0.1s ease forwards;
      animation-delay: var(--delay);
    }}
    .cell.revealed {{
      opacity: 1;
    }}
    .day-label {{
      font-family: 'Courier New', monospace;
      font-size: 10px;
      fill: #8b949e;
    }}
    .month-label {{
      font-family: 'Courier New', monospace;
      font-size: 10px;
      fill: #8b949e;
    }}
    .legend-text {{
      font-family: 'Courier New', monospace;
      font-size: 10px;
      fill: #8b949e;
    }}
    .stats-text {{
      font-family: 'Courier New', monospace;
      font-size: 12px;
      fill: #c9d1d9;
    }}
  </style>
  <rect width="100%" height="100%" fill="#0d1117"/>
''')

    # Day labels (Mon, Wed, Fri)
    day_labels = ["", "Mon", "", "Wed", "", "Fri", ""]
    for i, label in enumerate(day_labels):
        if label:
            y = MARGIN_TOP + i * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
            lines.append(f'  <text class="day-label" x="0" y="{y}">{label}</text>')

    # Month labels
    current_month = None
    for week in range(WEEKS):
        # Calculate the date for this week position
        week_start = start_date + timedelta(weeks=week)
        month = week_start.strftime("%b")

        if month != current_month:
            current_month = month
            x = MARGIN_LEFT + week * (CELL_SIZE + CELL_GAP)
            lines.append(f'  <text class="month-label" x="{x}" y="{MARGIN_TOP - 8}">{month}</text>')

    # Contribution cells
    for week in range(WEEKS):
        for day in range(DAYS):
            # Calculate the actual date
            cell_date = start_date + timedelta(weeks=week, days=day)
            date_str = cell_date.strftime("%Y-%m-%d")

            # Get contribution data
            contrib = contrib_map.get(date_str, {"count": 0, "level": 0})
            level = contrib.get("level", 0)

            # Calculate position
            x = MARGIN_LEFT + week * (CELL_SIZE + CELL_GAP)
            y = MARGIN_TOP + day * (CELL_SIZE + CELL_GAP)

            # Calculate animation delay (diagonal reveal)
            delay = (week + day) * 0.01

            # Get color from palette
            color = PALETTE[min(level, len(PALETTE) - 1)]

            # Add cell
            lines.append(f'  <rect class="cell" style="--delay: {delay:.3f}s" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}" rx="{CELL_ROUND}"/>')

    # Legend
    legend_y = MARGIN_TOP + DAYS * (CELL_SIZE + CELL_GAP) + 15
    legend_x = MARGIN_LEFT

    lines.append(f'  <text class="legend-text" x="{legend_x}" y="{legend_y}">Less</text>')

    for i, color in enumerate(PALETTE):
        box_x = legend_x + 40 + i * (CELL_SIZE + CELL_GAP)
        lines.append(f'  <rect x="{box_x}" y="{legend_y - 10}" width="{CELL_SIZE}" height="{CELL_SIZE}" fill="{color}" rx="{CELL_ROUND}"/>')

    lines.append(f'  <text class="legend-text" x="{legend_x + 40 + len(PALETTE) * (CELL_SIZE + CELL_GAP) + 8}" y="{legend_y}">More</text>')

    # Stats footer
    stats_y = legend_y + LEGEND_HEIGHT + 15
    total = stats.get("total", 0)
    current_streak = stats.get("current_streak", 0)
    longest_streak = stats.get("longest_streak", 0)

    stats_text = f"{total:,} contributions in the last year"
    if current_streak > 0:
        stats_text += f" · {current_streak} day streak"
    stats_text += f" · Longest: {longest_streak} days"

    lines.append(f'  <text class="stats-text" x="{MARGIN_LEFT}" y="{stats_y}">{stats_text}</text>')

    lines.append('</svg>')

    return '\n'.join(lines)


def main():
    data_path = "data/contributions.json"
    if not Path(data_path).exists():
        print(f"Error: {data_path} not found. Run fetch_contributions.py first.")
        sys.exit(1)

    print(f"Loading contribution data from {data_path}...")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Generating heatmap SVG...")
    svg_content = generate_heatmap_svg(data)

    output_path = "contrib-heatmap.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Saved contribution heatmap to {output_path}")


if __name__ == "__main__":
    main()
