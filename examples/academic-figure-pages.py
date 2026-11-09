"""Put the redrawn figures into the DAPO paper's pages, next to the original pages.

Each figure is replaced at the width LaTeX would give it (\\textwidth, or 0.75\\textwidth for 1.5 column);
the text below moves down by however much taller or shorter the new figure is.
Run after academic-figure.py: uv run -p 3.12 --with pymupdf python examples/academic-figure-pages.py
"""
import tempfile
import urllib.request
from pathlib import Path

import pymupdf

OUT = Path(__file__).parent / "academic-figure"
TEXT_LEFT, TEXT_RIGHT = 70.9, 541.1  # the paper's text block, in points
DPI = 150

# figure number: (page index, top of the caption, fraction of \textwidth)
FIGURES = {1: (0, 696, 1), 2: (2, 280, 1), 3: (4, 280, 1), 4: (5, 280, 1),
           5: (6, 280, 1), 6: (7, 274, 0.75), 7: (9, 426, 1)}


def figure_top(page, caption_top):
    backgrounds = [d["rect"] for d in page.get_drawings()
                   if d.get("fill") == (1.0, 1.0, 1.0) and d.get("color") is None
                   and d["rect"].height > 80 and d["rect"].y1 <= caption_top]
    if page.number == 0:  # the first page also has a white box behind the abstract
        backgrounds = [r for r in backgrounds if r.y0 > 500]
    return min(r.y0 for r in backgrounds)


pdf_path = Path(tempfile.gettempdir()) / "dapo-2503.14476.pdf"
if not pdf_path.exists():
    urllib.request.urlretrieve("https://arxiv.org/pdf/2503.14476", pdf_path)
paper = pymupdf.open(pdf_path)

for n, (index, caption_top, fraction) in FIGURES.items():
    page = paper[index]
    page.get_pixmap(dpi=DPI).save(OUT / f"page{n}-before.png")

    top, bottom = figure_top(page, caption_top), caption_top - 4
    image = OUT / f"fig{n}-after.png"
    pixmap = pymupdf.Pixmap(str(image))
    width = (TEXT_RIGHT - TEXT_LEFT) * fraction
    height = width * pixmap.height / pixmap.width
    left = (page.rect.width - width) / 2

    out = pymupdf.open()
    new = out.new_page(width=page.rect.width, height=page.rect.height)
    new.show_pdf_page(pymupdf.Rect(0, 0, page.rect.width, top), paper, index,
                      clip=pymupdf.Rect(0, 0, page.rect.width, top))
    new.insert_image(pymupdf.Rect(left, top, left + width, top + height), filename=str(image))
    rest = pymupdf.Rect(0, bottom, page.rect.width, page.rect.height)
    new.show_pdf_page(rest + (0, top + height - bottom, 0, top + height - bottom), paper, index, clip=rest)
    new.get_pixmap(dpi=DPI).save(OUT / f"page{n}-after.png")
