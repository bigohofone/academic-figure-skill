"""Helpers for scripts: smoothing a logged curve and marking a value."""
import numpy as np
from matplotlib import rcParams

from .palette import darken


def moving_average(values):
    """Centered moving average over 5% of the points (2.5% each side). Where a centered window does not fit,
    the first (last) points follow a straight line fitted to the first (last) full window: a window cut at the
    end would pull a steep start (a loss drop) toward later values, and one shrunk to stay centered would leave
    the end points unsmoothed. Centered, not EMA, so the smoothed curve does not lag the raw one."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    width = min(2 * max(1, n // 40) + 1, n)
    half = width // 2
    smoothed = np.convolve(values, np.ones(width) / width, mode="same")
    for ends, window in ((range(half), range(width)), (range(n - half, n), range(n - width, n))):
        slope, intercept = np.polyfit(window, values[window.start:window.stop], 1)
        smoothed[list(ends)] = slope * np.array(ends) + intercept
    return smoothed.tolist()


def mark_value(ax, x, y, text, color, below=False):
    """Mark a compared value: a hollow circle at (x, y) and `text` just above it (`below=True`: just
    below), in `darken(color)`.
    """
    ax.plot(x, y, "o", color=color)
    offset = rcParams["lines.markersize"] / 2 + 2
    ax.annotate(text, (x, y), xytext=(0, -offset if below else offset), textcoords="offset points", ha="center",
                va="top" if below else "bottom", color=darken(color), gid="value-mark")
