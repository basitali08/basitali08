#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG.

Features:
- Terminal-style header bar
- Colored key/value rows
- Line-by-line fade-in animation
- STATIC=1 env var for frozen preview
"""

import os
import sys

# Card configuration - EDIT THESE
CARD_CONFIG = {
    "name": "Basit Ali",
    "username": "basitali08",
    "role": "Full Stack Developer",
    "location": "Pakistan",
    "stack": "Python, JavaScript, React, Node.js",
    "current_focus": "AI/ML & Web Dev",
    "learning": "LangChain, FastAPI",
    "highlight1": "Open Source Contributor",
    "highlight2": "Building cool stuff",
}

# SVG dimensions
CARD_WIDTH = 480
CARD_HEIGHT = 320
LINE_HEIGHT = 28
PADDING = 24
HEADER_HEIGHT = 36


def generate_info_card_svg(static: bool = False) -> str:
    """Generate the info card SVG."""
    lines = []

    # Color palette
    colors = {
        "bg": "#0d1117",
        "header_bg": "#161b22",
        "header_text": "#58a6ff",
        "key": "#7ee787",
        "value": "#c9d1d9",
        "accent": "#58a6ff",
        "border": "#30363d",
    }

    # SVG header
    lines.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" width="{CARD_WIDTH}" height="{CARD_HEIGHT}">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <style>
    @keyframes fadeInSlide {{
      from {{
        opacity: 0;
        transform: translateY(8px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
    .line {{
      opacity: 0;
      animation: fadeInSlide 0.3s ease forwards;
      animation-delay: var(--delay);
    }}
    .line.revealed {{
      opacity: 1;
    }}
    .header {{
      font-family: 'Courier New', monospace;
      font-size: 13px;
      fill: {colors["header_text"]};
    }}
    .key {{
      font-family: 'Courier New', monospace;
      font-size: 13px;
      fill: {colors["key"]};
      font-weight: bold;
    }}
    .value {{
      font-family: 'Courier New', monospace;
      font-size: 13px;
      fill: {colors["value"]};
    }}
    .separator {{
      font-family: 'Courier New', monospace;
      font-size: 13px;
      fill: {colors["accent"]};
    }}
  </style>
''')

    # Background
    lines.append(f'  <rect width="100%" height="100%" fill="{colors["bg"]}" rx="8"/>')
    lines.append(f'  <rect x="1" y="1" width="{CARD_WIDTH-2}" height="{CARD_HEIGHT-2}" fill="none" stroke="{colors["border"]}" stroke-width="1" rx="7"/>')

    # Header bar
    lines.append(f'  <rect x="0" y="0" width="{CARD_WIDTH}" height="{HEADER_HEIGHT}" fill="{colors["header_bg"]}" rx="8"/>')
    lines.append(f'  <rect x="0" y="{HEADER_HEIGHT - 8}" width="{CARD_WIDTH}" height="8" fill="{colors["header_bg"]}"/>')
    lines.append(f'  <text class="header" x="{PADDING}" y="{HEADER_HEIGHT - 12}">╭─ {CARD_CONFIG["username"]}@github ─╮</text>')

    # Content lines
    content_lines = [
        ("Name:", CARD_CONFIG["name"]),
        ("Role:", CARD_CONFIG["role"]),
        ("Location:", CARD_CONFIG["location"]),
        ("Stack:", CARD_CONFIG["stack"]),
        ("Focus:", CARD_CONFIG["current_focus"]),
        ("Learning:", CARD_CONFIG["learning"]),
        ("✓", CARD_CONFIG["highlight1"]),
        ("✓", CARD_CONFIG["highlight2"]),
    ]

    y_start = HEADER_HEIGHT + PADDING
    for i, (key, value) in enumerate(content_lines):
        delay = 0.5 + i * 0.15 if not static else 0
        y = y_start + i * LINE_HEIGHT

        lines.append(f'  <g class="line" style="--delay: {delay:.2f}s">')
        lines.append(f'    <text class="key" x="{PADDING}" y="{y}">{key}</text>')
        lines.append(f'    <text class="value" x="{PADDING + 80}" y="{y}">{value}</text>')
        lines.append(f'  </g>')

    # Footer
    lines.append(f'  <line x1="{PADDING}" y1="{CARD_HEIGHT - PADDING}" x2="{CARD_WIDTH - PADDING}" y2="{CARD_HEIGHT - PADDING}" stroke="{colors["border"]}" stroke-width="1"/>')

    lines.append('</svg>')

    return '\n'.join(lines)


def main():
    static = os.environ.get("STATIC", "0") == "1"

    print("Generating info card SVG...")
    svg_content = generate_info_card_svg(static)

    output_path = "info-card.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Saved info card to {output_path}")


if __name__ == "__main__":
    main()
