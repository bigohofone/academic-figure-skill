"""Builds theme.pptx: the Academic theme (colors, fonts, master, slide layouts, and one example slide per layout) that every deck starts from.

Run `python theme.py` after changing anything below, and commit the new theme.pptx.
"""
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from pptx.util import Inches

from slides import CARD_FILL, add_slide, box, card_corner, figure

OUT = Path(__file__).parent / "theme.pptx"

KAIST_BLUE = "1F4899"  # the KAIST logo blue; the other blues are tints and shades of it
NAVY = "13285B"  # all text is dark navy, never black
TEXT = NAVY
MUTED = "5B6B8A"
ACCENT = KAIST_BLUE
ACCENT2 = "4F86C6"
CARD = CARD_FILL
SKY = "E3EEF9"  # title slide background
BG = "FFFFFF"
HEAD_FONT = "Inter SemiBold"  # titles, headers and lead-ins use the SemiBold family; nothing is bold
BODY_FONT = "Inter"
LINE = 115000  # line spacing 1.15

NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def emu(inches):
    return int(Inches(inches))


def level_style(size, color=None, semibold=False, bullet=False, align="l", space_after=10):
    bu = (f'<a:buFont typeface="Arial"/><a:buChar char="•"/>' if bullet else "<a:buNone/>")
    indent = f'marL="{emu(0.25)}" indent="{-emu(0.25)}"' if bullet else 'marL="0" indent="0"'
    fill = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>' if color else ""
    latin = f'<a:latin typeface="{HEAD_FONT}"/>' if semibold else ""
    return (f'<a:lvl1pPr {indent} algn="{align}"><a:lnSpc><a:spcPct val="{LINE}"/></a:lnSpc>'
            f'<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="{space_after * 100}"/></a:spcAft>{bu}'
            f'<a:defRPr sz="{size * 100}" b="0">{fill}{latin}</a:defRPr></a:lvl1pPr>')


def placeholder(shape_id, name, ph, box, prompt, style, anchor="t"):
    x, y, w, h = (emu(v) for v in box)
    return (f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{shape_id}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr>{ph}</p:nvPr></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"><a:noAutofit/></a:bodyPr>'
            f'<a:lstStyle>{style}</a:lstStyle><a:p><a:r><a:rPr lang="en-US"/><a:t>{prompt}</a:t></a:r></a:p></p:txBody></p:sp>')


def card(shape_id, rect):
    x, y, w, h = (emu(v) for v in rect)
    corner = int(card_corner(rect[2], rect[3]) * 100000)
    return (f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{shape_id}" name="Card"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {corner}"/></a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{CARD}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>')


# Same padding on every slide: 0.5 in left and right, 0.4 in top and bottom. The 12-column grid (box) is in slides.py.
TOP, BOTTOM = 0.4, 5.625 - 0.4


TITLE_BOX = box(0, 12, TOP, 1.0)
CONTENT_TOP, CONTENT_H = 1.6, 3.15
FOOTNOTE_BOX = box(0, 10, BOTTOM - 0.375, 0.375)
PAGE_NUMBER_BOX = box(10, 2, BOTTOM - 0.375, 0.375)


def title(prompt="Story title: one sentence, at most two lines"):
    return placeholder(2, "Title", '<p:ph type="title"/>', TITLE_BOX, prompt, "")


def body(idx, box, prompt, anchor="t", **style):
    return placeholder(10 + idx, f"Body {idx}", f'<p:ph type="body" idx="{idx}"/>', box, prompt, level_style(**style) if style else "", anchor)


def header(idx, box, prompt):
    return body(idx, box, prompt, size=20, color=ACCENT, semibold=True, space_after=0)


def footnote():
    return body(13, FOOTNOTE_BOX, "Footnote or source", size=11, color=MUTED, space_after=0)


def picture(idx, box):
    return placeholder(10 + idx, f"Figure {idx}", f'<p:ph type="pic" idx="{idx}"/>', box, "Figure", "")


def big_title(box, size, prompt, color):
    return placeholder(2, "Title", '<p:ph type="title"/>', box, prompt, level_style(size, color=color, semibold=True, space_after=0))


def page_number():
    x, y, w, h = (emu(v) for v in PAGE_NUMBER_BOX)
    return (f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="30" name="Page number"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr><a:lstStyle/>'
            f'<a:p><a:pPr algn="r"/><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum">'
            f'<a:rPr lang="en-US" sz="1100" b="0"><a:solidFill><a:srgbClr val="{MUTED}"/></a:solidFill><a:latin typeface="{BODY_FONT}"/></a:rPr>'
            f'<a:t>‹#›</a:t></a:fld></a:p></p:txBody></p:sp>')


LAYOUTS = [
    ("Title", SKY, [
        big_title(box(0, 12, 0.9, 2.2), 32, "Talk title: the claim or question", NAVY),
        body(1, box(0, 10, 3.2, BOTTOM - 3.2), "Venue · date, then authors, then affiliations: one per line", size=16, color=NAVY, space_after=6),
    ]),
    ("Title and Content", None, [
        title(),
        body(1, box(0, 12, CONTENT_TOP, CONTENT_H), "Bullets: a semibold lead-in, then the point"),
        footnote(),
    ]),
    ("Statement", None, [
        title(),
        card(20, box(0, 12, CONTENT_TOP, 1.5)),
        body(1, box(1, 10, CONTENT_TOP, 1.5), "The research question, in one or two sentences", anchor="ctr", size=20, align="ctr", space_after=0),
        body(2, box(0, 12, CONTENT_TOP + 1.7, CONTENT_H - 1.7), "Contribution", size=16),
        footnote(),
    ]),
    ("Two Content", None, [
        title(),
        header(1, box(0, 6, CONTENT_TOP, 0.45), "Left header"),
        body(2, box(0, 6, CONTENT_TOP + 0.55, CONTENT_H - 0.55), "Left bullets"),
        header(3, box(6, 6, CONTENT_TOP, 0.45), "Right header"),
        body(4, box(6, 6, CONTENT_TOP + 0.55, CONTENT_H - 0.55), "Right bullets"),
        footnote(),
    ]),
    ("Figure and Text", None, [
        title(),
        picture(1, box(0, 8, CONTENT_TOP, CONTENT_H)),
        body(2, box(8, 4, CONTENT_TOP, CONTENT_H), "Two or three points the figure can't show", size=16, bullet=True),
        footnote(),
    ]),
    ("Section Header", SKY, [
        body(1, box(0, 12, 1.8, 0.45), "Part 2", size=18, color=NAVY, space_after=0),
        big_title(box(0, 12, 2.3, 1.4), 32, "Section name", NAVY),
    ]),
    ("References", None, [
        title("References"),
        body(1, box(0, 12, CONTENT_TOP, CONTENT_H), "One reference per paragraph, one citation style", size=16),
    ]),
    ("Title Only", None, [title()]),
    ("Blank", None, []),
]


def set_theme(master):
    theme = master.part.part_related_by(RT.THEME)
    root = etree.fromstring(theme.blob)
    root.set("name", "Academic")
    scheme = root.find(f".//{A}clrScheme")
    scheme.set("name", "Academic")
    colors = {"dk1": TEXT, "lt1": "FFFFFF", "dk2": NAVY, "lt2": CARD, "accent1": ACCENT, "accent2": ACCENT2,
              "accent3": MUTED, "accent4": SKY, "accent5": "8C8C8C", "accent6": "BFBFBF", "hlink": ACCENT, "folHlink": MUTED}
    for el in scheme:
        el.clear()
        etree.SubElement(el, f"{A}srgbClr", val=colors[etree.QName(el).localname])
    fonts = root.find(f".//{A}fontScheme")
    fonts.set("name", "Academic")
    fonts.find(f"{A}majorFont/{A}latin").set("typeface", HEAD_FONT)
    fonts.find(f"{A}minorFont/{A}latin").set("typeface", BODY_FONT)
    theme._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def set_background(element, color):
    c_sld = element.find(f"{P}cSld")
    old = c_sld.find(f"{P}bg")
    if old is not None:
        c_sld.remove(old)
    c_sld.insert(0, parse_xml(f'<p:bg {NS}><p:bgPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'))


def set_shapes(element, shapes):
    tree = element.find(f"{P}cSld/{P}spTree")
    for sp in tree.findall(f"{P}sp"):
        tree.remove(sp)
    for xml in shapes:
        tree.append(parse_xml(xml))


def set_master(master):
    set_background(master._element, BG)
    set_shapes(master._element, [title(), body(1, box(0, 12, CONTENT_TOP, CONTENT_H), "Body"), page_number()])
    styles = master._element.find(f"{P}txStyles")
    styles.find(f"{P}titleStyle").clear()
    styles.find(f"{P}titleStyle").append(parse_xml(
        f'<a:lvl1pPr {NS} algn="l"><a:lnSpc><a:spcPct val="{LINE}"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/>'
        f'<a:defRPr sz="2400" b="0"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill><a:latin typeface="+mj-lt"/></a:defRPr></a:lvl1pPr>'))
    body_style = styles.find(f"{P}bodyStyle")
    body_style.clear()
    for level in range(1, 4):
        margin = emu(0.25 * level)
        body_style.append(parse_xml(
            f'<a:lvl{level}pPr {NS} marL="{margin}" indent="{-emu(0.25)}" algn="l"><a:lnSpc><a:spcPct val="{LINE}"/></a:lnSpc>'
            f'<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="1000"/></a:spcAft><a:buFont typeface="Arial"/><a:buChar char="•"/>'
            f'<a:defRPr sz="1600"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill><a:latin typeface="+mn-lt"/></a:defRPr></a:lvl{level}pPr>'))


prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(5.625)
master = prs.slide_master
set_theme(master)
set_master(master)

layouts = list(prs.slide_layouts)
for layout, (name, bg, shapes) in zip(layouts, LAYOUTS):
    element = layout._element
    element.attrib.pop("type", None)
    element.find(f"{P}cSld").set("name", name)
    if bg:
        set_background(element, bg)
    set_shapes(element, shapes)
for layout in layouts[len(LAYOUTS):]:
    prs.slide_layouts.remove(layout)


# Example slides, one per layout, so the theme can be seen filled in. slides.new_deck() drops them.
add_slide(prs, "Title", "Title slide: the talk's claim or question as its title",
          p1=["Venue · date", "Authors with affiliation marks¹ ²", "¹ University · ² Lab"])
add_slide(prs, "Title and Content", "A story title states the takeaway in one sentence",
          p1=[[("Semibold lead-in: ", True), ("then the point in a few words", False)],
              [("Three or four bullets: ", True), ("about 40 words per slide at most", False)],
              [("Sources: ", True), ("a superscript number here¹, the reference in the footnote", False)]],
          p13=["¹ Author et al. (2025), Venue."])
add_slide(prs, "Statement", "The research question gets its own slide, by slide 3",
          p1=["The question, stated precisely in one or two sentences, on the card"],
          p2=[[("Contribution: ", True), ("what this work adds that prior work does not.", False)]])
add_slide(prs, "Two Content", "Methods and discussion split into two labeled columns",
          p1=["Design"],
          p2=[[("Data: ", True), ("what and how much", False)], [("Method: ", True), ("only what the audience needs", False)]],
          p3=["Outcomes"],
          p4=[[("Primary: ", True), ("the main measure", False)], [("Secondary: ", True), ("supporting measures", False)]],
          p13=["Full details: Appendix A"])
results = add_slide(prs, "Figure and Text", "Results: the finding in the title, the figure as evidence",
                    p2=["The figure keeps its aspect ratio", "Points add what the figure can't show", "One finding per slide"],
                    p13=["Figure: example data."])
figure(results, 1, Path(__file__).parent / "theme_example.png")  # made-up data
add_slide(prs, "Section Header", "Section name", p1=["Part 2"])
add_slide(prs, "References", "References",
          p1=["Author, A., et al. (2025). Title of the paper. Venue.",
              "Author, B., and Author, C. (2024). Title of the paper. arXiv:0000.00000."])
add_slide(prs, "Title Only", "Title Only: draw anything below the title")

prs.save(OUT)
print("wrote", OUT)
