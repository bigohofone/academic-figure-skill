"""Build a deck from theme.pptx.

    import sys; sys.path.insert(0, "{skill-dir}/assets")
    from slides import new_deck, add_slide, figure, add_card, save

    prs = new_deck()
    add_slide(prs, "Title and Content", "A story title", p1=[[("Lead-in: ", True), ("the point", False)]], p13=["¹ Source."])
    s = add_slide(prs, "Figure and Text", "The finding", p2=["A point the figure can't show"])
    figure(s, 1, "figures/result.png")
    save(prs, "talk.pptx")
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.util import Inches

THEME = Path(__file__).parent / "theme.pptx"
SEMIBOLD = "Inter SemiBold"

# The 9 in between the 0.5 in side margins is a 12-column grid with 0.2 in gutters; every x and width comes from it.
LEFT, WIDTH = 0.5, 9.0
COLUMNS, GUTTER = 12, 0.2
COLUMN = (WIDTH - (COLUMNS - 1) * GUTTER) / COLUMNS

# Cards: one fill, 16 pt corners, no border, never nested.
CARD_FILL = "E8EDF6"
CARD_RADIUS = 16 / 72  # in


def box(first_column, span, y, h):
    """(x, y, w, h) in inches for a box that starts at a grid column (0-11) and spans `span` columns."""
    return (LEFT + first_column * (COLUMN + GUTTER), y, span * COLUMN + (span - 1) * GUTTER, h)


def card_corner(w, h):
    """roundRect's adj value that gives CARD_RADIUS corners on a w x h card (adj is a share of the shorter side)."""
    return CARD_RADIUS / min(w, h)


def new_deck():
    """The theme without its example slides."""
    prs = Presentation(THEME)
    for sld_id in list(prs.slides._sldIdLst):
        prs.part.drop_rel(sld_id.rId)
        prs.slides._sldIdLst.remove(sld_id)
    return prs


def fill(placeholder, paragraphs):
    """paragraphs: list of str, or of lists of (text, semibold) runs."""
    tf = placeholder.text_frame
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        for text, semibold in [(para, False)] if isinstance(para, str) else para:
            run = p.add_run()
            run.text = text
            if semibold:
                run.font.name = SEMIBOLD


def add_slide(prs, layout_name, title, **placeholders):
    """placeholders: p<idx>=paragraphs, e.g. p1=[...], p13=["footnote"]."""
    layout = next(layout for layout in prs.slide_layouts if layout.name == layout_name)
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = title
    for key, paragraphs in placeholders.items():
        fill(slide.placeholders[int(key[1:])], paragraphs)
    return slide


def figure(slide, idx, path):
    """Put an image in a picture placeholder whole: aspect ratio kept, top-left aligned, no crop."""
    ph = slide.placeholders[idx]
    x, y, w, h = ph.left, ph.top, ph.width, ph.height
    pic = ph.insert_picture(str(path))
    pic.crop_left = pic.crop_right = pic.crop_top = pic.crop_bottom = 0
    iw, ih = pic.image.size
    scale = min(w / iw, h / ih)
    pic.width, pic.height = int(iw * scale), int(ih * scale)
    pic.left, pic.top = x, y


def add_card(slide, first_column, span, y, h):
    """A card on the grid, drawn behind what is added after it. Never put a card inside another card."""
    x, y, w, h = box(first_column, span, y, h)
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.adjustments[0] = card_corner(w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor.from_string(CARD_FILL)
    card.line.fill.background()
    card._element.remove(card._element.find(qn("p:style")))  # drops the default shadow and white text
    return card


def save(prs, path):
    """Delete empty placeholders, whose prompt text would show in the editor, then save."""
    for slide in prs.slides:
        for ph in list(slide.placeholders):
            if ph.has_text_frame and not ph.text_frame.text:
                ph.element.getparent().remove(ph.element)
    prs.save(path)
