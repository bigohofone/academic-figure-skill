"""Helpers for scripts: smoothing a logged curve and marking a value."""
import numpy as np
from matplotlib import rcParams

from .palette import darken


def moving_average(values):
    """Centered moving average over 5% of the points (2.5% each side), shrinking at the ends.
    Centered, not EMA, so the smoothed curve does not lag the raw one."""
    half = max(1, len(values) // 40)
    return [np.mean(values[max(0, i - half):i + half + 1]) for i in range(len(values))]


def mark_value(ax, x, y, text, color, below=False):
    """Mark a compared value: a hollow circle at (x, y) and `text` just above it (`below=True`: just
    below), in `darken(color)`.
    """
    ax.plot(x, y, "o", color=color)
    offset = rcParams["lines.markersize"] / 2 + 2
    ax.annotate(text, (x, y), xytext=(0, -offset if below else offset), textcoords="offset points", ha="center",
                va="top" if below else "bottom", color=darken(color), gid="value-mark")
