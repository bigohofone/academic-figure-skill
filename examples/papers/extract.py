"""Dump what a vector figure PDF draws, to recover its numbers: every text with its position, and every
path with its color, width, dashes and points, all in PDF points (y grows downward).

Run: python examples/papers/extract.py figure.pdf > figure.txt
Map a path to data with two tick labels per axis: data = a + b * position.
"""

import sys

import pymupdf

page = pymupdf.open(sys.argv[1])[0]
print(f"page {page.rect.width:.1f} x {page.rect.height:.1f}")
for block in page.get_text("dict")["blocks"]:
    for line in block.get("lines", []):
        for span in line["spans"]:
            x0, y0, x1, y1 = span["bbox"]
            print(f"text {span['text']!r} center=({(x0 + x1) / 2:.2f}, {(y0 + y1) / 2:.2f}) size={span['size']:.1f}")
for d in page.get_drawings():
    color = d.get("color") or d.get("fill")
    rgb = "#%02x%02x%02x" % tuple(round(c * 255) for c in color[:3]) if color else "none"
    points = []
    for item in d["items"]:
        for p in item[1:]:
            if hasattr(p, "x"):
                points.append(f"{p.x:.2f},{p.y:.2f}")
            elif hasattr(p, "x0"):
                points.append(f"rect({p.x0:.2f},{p.y0:.2f},{p.x1:.2f},{p.y1:.2f})")
    kind = "fill" if d.get("fill") and not d.get("color") else "stroke"
    print(f"path {kind} {rgb} width={d.get('width') or 0:.2f} dashes={d.get('dashes')!r} n={len(points)} {' '.join(points)}")
