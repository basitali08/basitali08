"""Prep a portrait using OpenCV grabCut (no 1GB rembg model download).

grabCut isolates the subject, local contrast is boosted (CLAHE), then the
subject is composited onto pure white so the background maps to blank in the
ASCII ramp. Output: source-prepped.png (grayscale) for make_ascii_svg.py.
"""
import sys
import os
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

img = cv2.imread(INP)
if img is None:
    raise SystemExit(f"cannot read {INP}")
h, w = img.shape[:2]

pad = int(min(h, w) * 0.04)
rect = (pad, pad, w - 2 * pad, h - 2 * pad)
mask = np.zeros((h, w), np.uint8)
bgd = np.zeros((1, 65), np.float64)
fgd = np.zeros((1, 65), np.float64)
cv2.grabCut(img, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)

fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)
kernel = np.ones((5, 5), np.uint8)
fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel)

rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
gray = clahe.apply(gray)
gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

alpha = fg.astype(np.float32)
alpha = cv2.GaussianBlur(alpha, (0, 0), 3.0)
out = gray.astype(np.float32) * alpha + 255.0 * (1.0 - alpha)
out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out, mode="L").save(OUT)
print("wrote", OUT, out.shape)
