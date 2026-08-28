#!/usr/bin/env python3
"""Prep a photo for ASCII art conversion.

Steps:
1. Remove background with rembg
2. Boost local contrast with CLAHE
3. Composite onto pure white background
4. Output grayscale source-prepped.png
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def remove_background(input_path: str) -> np.ndarray:
    """Remove background using rembg."""
    try:
        from rembg import remove
        with open(input_path, "rb") as f:
            input_data = f.read()
        output_data = remove(input_data)
        img = Image.open(__import__("io").BytesIO(output_data)).convert("RGBA")
        return np.array(img)
    except ImportError:
        print("rembg not installed. Install with: pip install rembg")
        sys.exit(1)


def boost_contrast(img_array: np.ndarray) -> np.ndarray:
    """Boost local contrast using CLAHE."""
    if img_array.shape[2] == 4:
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGRA2GRAY)
    else:
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return enhanced


def composite_on_white(img_array: np.ndarray) -> np.ndarray:
    """Composite image onto pure white background."""
    if img_array.shape[2] == 4:
        alpha = img_array[:, :, 3] / 255.0
        rgb = img_array[:, :, :3]
        white = np.ones_like(rgb, dtype=np.float32) * 255
        result = (rgb * alpha[:, :, np.newaxis] + white * (1 - alpha[:, :, np.newaxis]))
        return result.astype(np.uint8)
    return img_array


def main():
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not Path(input_path).exists():
        print(f"Error: File {input_path} not found")
        sys.exit(1)

    print(f"Processing {input_path}...")

    # Step 1: Remove background
    print("Removing background...")
    img_array = remove_background(input_path)

    # Step 2: Composite on white
    print("Compositing on white background...")
    img_array = composite_on_white(img_array)

    # Step 3: Boost contrast
    print("Boosting contrast...")
    enhanced = boost_contrast(img_array)

    # Save output
    output_path = "source-prepped.png"
    cv2.imwrite(output_path, enhanced)
    print(f"Saved prepped image to {output_path}")


if __name__ == "__main__":
    main()
