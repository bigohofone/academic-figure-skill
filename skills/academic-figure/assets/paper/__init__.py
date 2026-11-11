"""Paper figures in the academic-figure design. Scripts import everything from here:
`import paper`, `colors = paper.use_design("DESIGN.md")`, `from paper import fit_height, greys`.

design.py reads DESIGN.md; layout.py sizes the figure; palette.py keeps colors apart for color-blind
readers and in black and white; checks.py reports what reads badly; draw.py holds drawing helpers."""
from . import design as _design
from .design import use_design
from .draw import mark_value, smooth
from .layout import fit_height, group_label
from .palette import darken, greys, lighten, parts, text_color

__all__ = ["use_design", "fit_height", "group_label", "greys", "parts", "darken", "lighten", "text_color",
           "smooth", "mark_value"]


def __getattr__(name):
    # design values (dashed_width, highlight_size, ...) are set by use_design(), so they are read live
    return getattr(_design, name)
