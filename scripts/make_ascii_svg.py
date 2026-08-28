#!/usr/bin/env python3
"""Convert a prepped photo to an animated ASCII art SVG.

The SVG features:
- Monochrome light-gray characters
- Row-by-row reveal animation with a typing cursor
- No looping - plays once and freezes
"""

import sys
from pathlib import Path

import cv2
import numpy as np

# ASCII density ramp: bright (sparse) -> dark (dense)
RAMP = " .`:-=+*cs#%@"

# SVG dimensions
WIDTH_CHARS = 100
HEIGHT_CHARS = 53
CHAR_WIDTH = 8
CHAR_HEIGHT = 14
SVG_WIDTH = WIDTH_CHARS * CHAR_WIDTH
SVG_HEIGHT = HEIGHT_CHARS * CHAR_HEIGHT


def image_to_ascii(image_path: str) -> list[list[str]]:
    """Convert image to ASCII character grid."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load image {image_path}")
        sys.exit(1)

    # Resize to character grid dimensions
    img = cv2.resize(img, (WIDTH_CHARS, HEIGHT_CHARS))

    ascii_grid = []
    for row in range(HEIGHT_CHARS):
        ascii_row = []
        for col in range(WIDTH_CHARS):
            brightness = img[row, col]
            # Map brightness to ramp index (inverted: bright = sparse)
            ramp_idx = int((1 - brightness / 255) * (len(RAMP) - 1))
            ramp_idx = max(0, min(ramp_idx, len(RAMP) - 1))
            ascii_row.append(RAMP[ramp_idx])
        ascii_grid.append(ascii_row)

    return ascii_grid


def escape_xml(char: str) -> str:
    """Escape special XML characters."""
    if char == "<":
        return "&lt;"
    elif char == ">":
        return "&gt;"
    elif char == "&":
        return "&amp;"
    elif char == '"':
        return "&quot;"
    elif char == "'":
        return "&apos;"
    return char


def generate_svg(ascii_grid: list[list[str]]) -> str:
    """Generate animated SVG from ASCII grid."""
    svg_parts = []

    # SVG header with styles
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" width="{SVG_WIDTH}" height="{SVG_HEIGHT}">
  <style>
    @keyframes typing {{
      from {{ clip-path: inset(0 100% 0 0); }}
      to {{ clip-path: inset(0 0 0 0); }}
    }}
    @keyframes cursor {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
    .row {{
      animation: typing 0.15s steps(20) forwards;
      animation-delay: var(--delay);
      clip-path: inset(0 100% 0 0);
    }}
    .row.revealed {{
      clip-path: inset(0 0 0 0);
    }}
    .char {{
      font-family: 'Courier New', monospace;
      font-size: 12px;
      fill: #8b949e;
    }}
  </style>
  <rect width="100%" height="100%" fill="#0d1117"/>
''')

    # Generate each row with animation delay
    for row_idx, row in enumerate(ascii_grid):
        delay = row_idx * 0.03  # 30ms stagger per row
        y = row_idx * CHAR_HEIGHT + CHAR_HEIGHT - 2  # Baseline adjustment

        svg_parts.append(f'  <g class="row" style="--delay: {delay:.3f}s">')

        for col_idx, char in enumerate(row):
            if char.strip():  # Only render non-space characters
                x = col_idx * CHAR_WIDTH
                escaped = escape_xml(char)
                svg_parts.append(f'    <text class="char" x="{x}" y="{y}">{escaped}</text>')

        svg_parts.append('  </g>')

    svg_parts.append('</svg>')

    return '\n'.join(svg_parts)


def main():
    image_path = "source-prepped.png"
    if not Path(image_path).exists():
        print(f"Error: {image_path} not found. Run prep_photo.py first.")
        sys.exit(1)

    print(f"Converting {image_path} to ASCII...")
    ascii_grid = image_to_ascii(image_path)

    print("Generating SVG...")
    svg_content = generate_svg(ascii_grid)

    output_path = "ascii-portrait.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Saved ASCII portrait to {output_path}")


if __name__ == "__main__":
    main()
