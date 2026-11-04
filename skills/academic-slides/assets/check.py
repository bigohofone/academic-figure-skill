"""Usage: python check.py deck.pptx

Runs every check in CHECKS on the deck and reports the problems. Exits with 1 if anything is reported.

- check_fit: measures every text box with Inter's real metrics and reports text that overflows
  its box or titles longer than two lines.
"""
import sys
from pathlib import Path

from PIL import ImageFont
from pptx import Presentation
from pptx.enum.shapes import PP_PLACEHOLDER

ASSETS = Path(__file__).parent
FONT_FILES = {"Inter": ASSETS / "Inter-Regular.ttf", "Inter SemiBold": ASSETS / "Inter-SemiBold.ttf"}
FONT_FILES["+mn-lt"], FONT_FILES["+mj-lt"] = FONT_FILES["Inter"], FONT_FILES["Inter SemiBold"]  # the theme's body and heading fonts
LINE_EM = (1984 + 494) / 2048  # Inter's ascent + descent, the line height before line spacing
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
EMU_PER_PT = 12700
fonts = {}


def font(typeface, size):
    key = (typeface, size)
    if key not in fonts:
        fonts[key] = ImageFont.truetype(str(FONT_FILES.get(typeface, FONT_FILES["Inter"])), size * 10)
    return fonts[key]


def style_chain(shape, slide):
    """lvl1pPr elements that style this shape's text, nearest first."""
    chain = [shape.text_frame._txBody.find(f"{A}lstStyle/{A}lvl1pPr")]
    if shape.is_placeholder:
        layout_ph = slide.slide_layout.placeholders.get(idx=shape.placeholder_format.idx)
        if layout_ph is not None:
            chain.append(layout_ph.text_frame._txBody.find(f"{A}lstStyle/{A}lvl1pPr"))
        is_title = shape.placeholder_format.type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE)
        styles = slide.slide_layout.slide_master._element.find(
            "{http://schemas.openxmlformats.org/presentationml/2006/main}txStyles")
        chain.append(styles.find(f"*/{A}lvl1pPr") if is_title else styles[1].find(f"{A}lvl1pPr"))
    return [el for el in chain if el is not None]


def lookup(elements, path, attr, default):
    for el in elements:
        found = el.find(path) if path else el
        if found is not None and found.get(attr) is not None:
            return found.get(attr)
    return default


def measure(shape, slide):
    chain = style_chain(shape, slide)
    width_pt = shape.width / EMU_PER_PT
    height_pt = 0
    lines_total = 0
    for i, p in enumerate(shape.text_frame.paragraphs):
        pPr = p._p.find(f"{A}pPr")
        pchain = ([pPr] if pPr is not None else []) + chain
        size = int(lookup(pchain, f"{A}defRPr", "sz", 1800)) / 100
        face_default = lookup(pchain, f"{A}defRPr/{A}latin", "typeface", "Inter")
        spacing = int(lookup(pchain, f"{A}lnSpc/{A}spcPct", "val", 100000)) / 100000
        after = int(lookup(pchain, f"{A}spcAft/{A}spcPts", "val", 0)) / 100
        indent = int(lookup(pchain, None, "marL", 0)) / EMU_PER_PT
        words = []
        for run in p.runs:
            size = run.font.size.pt if run.font.size else size
            face = run.font.name or face_default
            words += [(word, face) for word in run.text.split(" ")]
        lines, line_width = 1, 0
        for word, face in words:
            w = (font(face, size).getlength(word) + font(face, size).getlength(" ")) / 10
            if line_width and line_width + w > width_pt - indent:
                lines, line_width = lines + 1, 0
            line_width += w
        lines_total += lines
        height_pt += lines * size * LINE_EM * spacing + (after if i < len(shape.text_frame.paragraphs) - 1 else 0)
    return height_pt / 72, shape.height / 914400, lines_total


def check_fit(prs):
    problems = []
    for n, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue
            need, box, lines = measure(shape, slide)
            if need > box + 0.01:
                problems.append(f"slide {n}, {shape.name}: text needs {need:.2f} in, box is {box:.2f} in")
            if shape.is_placeholder and shape.placeholder_format.type == PP_PLACEHOLDER.TITLE and lines > 2:
                problems.append(f"slide {n}, {shape.name}: title runs {lines} lines, max 2")
    return problems


CHECKS = [check_fit]


def main(path):
    prs = Presentation(path)
    problems = [problem for check in CHECKS for problem in check(prs)]
    print("\n".join(problems) or "No problems found.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
