#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG - static version."""

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

CARD_WIDTH = 480
CARD_HEIGHT = 320
LINE_HEIGHT = 28
PADDING = 24
HEADER_HEIGHT = 36


def generate_info_card_svg() -> str:
    lines = []
    c = {"bg": "#0d1117", "header_bg": "#161b22", "header_text": "#58a6ff",
         "key": "#7ee787", "value": "#c9d1d9", "border": "#30363d"}

    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" width="{CARD_WIDTH}" height="{CARD_HEIGHT}">')
    lines.append(f'<rect width="100%" height="100%" fill="{c["bg"]}" rx="8"/>')
    lines.append(f'<rect x="1" y="1" width="{CARD_WIDTH-2}" height="{CARD_HEIGHT-2}" fill="none" stroke="{c["border"]}" stroke-width="1" rx="7"/>')

    # Header
    lines.append(f'<rect x="0" y="0" width="{CARD_WIDTH}" height="{HEADER_HEIGHT}" fill="{c["header_bg"]}" rx="8"/>')
    lines.append(f'<rect x="0" y="{HEADER_HEIGHT - 8}" width="{CARD_WIDTH}" height="8" fill="{c["header_bg"]}"/>')
    lines.append(f'<text font-family="monospace" font-size="13" fill="{c["header_text"]}" x="{PADDING}" y="{HEADER_HEIGHT - 12}">╭─ {CARD_CONFIG["username"]}@github ─╮</text>')

    # Content
    content = [
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
    for i, (key, value) in enumerate(content):
        y = y_start + i * LINE_HEIGHT
        lines.append(f'<text font-family="monospace" font-size="13" fill="{c["key"]}" font-weight="bold" x="{PADDING}" y="{y}">{key}</text>')
        lines.append(f'<text font-family="monospace" font-size="13" fill="{c["value"]}" x="{PADDING + 80}" y="{y}">{value}</text>')

    lines.append(f'<line x1="{PADDING}" y1="{CARD_HEIGHT - PADDING}" x2="{CARD_WIDTH - PADDING}" y2="{CARD_HEIGHT - PADDING}" stroke="{c["border"]}" stroke-width="1"/>')
    lines.append('</svg>')
    return '\n'.join(lines)


def main():
    svg_content = generate_info_card_svg()
    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)
    print("Saved info-card.svg")


if __name__ == "__main__":
    main()
