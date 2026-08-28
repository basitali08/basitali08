#!/usr/bin/env python3
"""Generate a neofetch-style info card SVG.

Uses SMIL animations so GitHub renders them in <img> tags.
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


def generate_info_card_svg() -> str:
    """Generate the info card SVG with SMIL animations."""
    lines = []

    colors = {
        "bg": "#0d1117",
        "header_bg": "#161b22",
        "header_text": "#58a6ff",
        "key": "#7ee787",
        "value": "#c9d1d9",
        "accent": "#58a6ff",
        "border": "#30363d",
    }

    # SVG header - no <style> block
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CARD_WIDTH} {CARD_HEIGHT}" width="{CARD_WIDTH}" height="{CARD_HEIGHT}">')

    # Background
    lines.append(f'<rect width="100%" height="100%" fill="{colors["bg"]}" rx="8"/>')
    lines.append(f'<rect x="1" y="1" width="{CARD_WIDTH-2}" height="{CARD_HEIGHT-2}" fill="none" stroke="{colors["border"]}" stroke-width="1" rx="7"/>')

    # Header bar
    lines.append(f'<rect x="0" y="0" width="{CARD_WIDTH}" height="{HEADER_HEIGHT}" fill="{colors["header_bg"]}" rx="8"/>')
    lines.append(f'<rect x="0" y="{HEADER_HEIGHT - 8}" width="{CARD_WIDTH}" height="8" fill="{colors["header_bg"]}"/>')
    lines.append(f'<text font-family="monospace" font-size="13" fill="{colors["header_text"]}" x="{PADDING}" y="{HEADER_HEIGHT - 12}">╭─ {CARD_CONFIG["username"]}@github ─╮</text>')

    # Content lines with SMIL fade-in
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
        delay = 0.5 + i * 0.15
        y = y_start + i * LINE_HEIGHT

        # Group with SMIL animation
        lines.append(f'<g opacity="0">')
        lines.append(f'<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{delay:.2f}s" fill="freeze"/>')
        lines.append(f'<text font-family="monospace" font-size="13" fill="{colors["key"]}" font-weight="bold" x="{PADDING}" y="{y}">{key}</text>')
        lines.append(f'<text font-family="monospace" font-size="13" fill="{colors["value"]}" x="{PADDING + 80}" y="{y}">{value}</text>')
        lines.append(f'</g>')

    # Footer line
    lines.append(f'<line x1="{PADDING}" y1="{CARD_HEIGHT - PADDING}" x2="{CARD_WIDTH - PADDING}" y2="{CARD_HEIGHT - PADDING}" stroke="{colors["border"]}" stroke-width="1"/>')

    lines.append('</svg>')
    return '\n'.join(lines)


def main():
    print("Generating info card SVG...")
    svg_content = generate_info_card_svg()

    output_path = "info-card.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Saved info card to {output_path}")


if __name__ == "__main__":
    main()
