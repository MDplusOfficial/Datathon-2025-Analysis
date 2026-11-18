#!/usr/bin/env python3
"""
s10_resize_figures.py — write a 1200-px copy of every figure, named as the
manuscript numbers them.

Figures are rendered at full resolution by s07-s09, then Lanczos-downsampled so
that neither side exceeds 1200 px. Figure 1 is drawn at exactly 1200 x 1200 and
is copied unchanged.

Output: ../figures/1200px/
"""
import os
import shutil
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import FIG_DIR

MAX_SIDE = 1200
MAP = {
    "Figure1_flow.png": "Figure1.png",
    "Figure2_demographics.png": "Figure2.png",
    "Figure3_survey.png": "Figure3.png",
    "Figure4_sentiment.png": "Figure4.png",
    "Figure5_cooccurrence.png": "Figure5.png",
    "SupplementaryFigureS1_silhouette.png": "SupplementaryFigureS1.png",
}


def main():
    dest_dir = os.path.join(FIG_DIR, "1200px")
    os.makedirs(dest_dir, exist_ok=True)
    missing = []
    for src_name, out_name in MAP.items():
        src = os.path.join(FIG_DIR, src_name)
        if not os.path.exists(src):
            missing.append(src_name)
            continue
        dest = os.path.join(dest_dir, out_name)
        im = Image.open(src).convert("RGB")
        w, h = im.size
        if max(w, h) <= MAX_SIDE:
            shutil.copyfile(src, dest)
            print("  %-34s -> %-28s %dx%d (copied)" % (src_name, out_name, w, h))
            continue
        scale = MAX_SIDE / max(w, h)
        tw, th = max(1, round(w * scale)), max(1, round(h * scale))
        im.resize((tw, th), Image.LANCZOS).save(dest, "PNG", optimize=True)
        print("  %-34s -> %-28s %dx%d" % (src_name, out_name, tw, th))
    if missing:
        print("\n  missing (run s07-s09 first): " + ", ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
