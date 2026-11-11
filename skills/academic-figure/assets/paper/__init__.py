"""Paper figures in the academic-figure design. Scripts import everything from here:
`import paper`, `colors = paper.apply_design("DESIGN.md")`, `from paper import finalize_figure, baseline_greys`.

design.py reads DESIGN.md; layout.py sizes the figure; palette.py keeps colors apart for color-blind
readers and in black and white; checks.py reports what reads badly; helpers.py holds helpers for drawing."""
from . import design as _design
from .design import apply_design
from .helpers import mark_value, moving_average
from .layout import finalize_figure, set_group_label
from .palette import darken, baseline_greys, lighten, part_colors, text_color_on

__all__ = ["apply_design", "finalize_figure", "set_group_label", "baseline_greys", "part_colors", "darken", "lighten", "text_color_on",
           "moving_average", "mark_value"]


def __getattr__(name):
    # design values (dashed_width, highlight_size, ...) are set by apply_design(), so they are read live
    return getattr(_design, name)
