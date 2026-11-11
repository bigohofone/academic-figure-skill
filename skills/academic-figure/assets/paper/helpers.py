"""Helpers for scripts: smoothing a logged curve, marking a value, a legend in named rows."""
import numpy as np
from matplotlib import rcParams
from matplotlib.lines import Line2D

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


def legend_rows(target, rows, **legend_kw):
    """A legend for series named by a shared word and a setting ("Depth 4", "Depth 8", ...): one row per
    shared word, written once at the row's start, each entry only its setting ("4", "8", ...). `rows` is a
    list of (name, handles, settings). On an Axes without `loc`, `finalize_figure` places it like any panel
    legend and keeps its rows; on the figure with `loc="outside upper center"`, it stands above the panels."""
    width = 1 + max(len(handles) for _, handles, _ in rows)
    grid = []
    for name, handles, settings in rows:
        row = [(Line2D([], [], linestyle="none"), name), *zip(handles, map(str, settings))]
        grid.append(row + [(Line2D([], [], linestyle="none"), "")] * (width - len(row)))
    # matplotlib fills a legend column by column
    handles, labels = zip(*[grid[r][c] for c in range(width) for r in range(len(grid))])
    # entries are short settings: columns close together, markers without a line need only a short handle
    markers_only = all(h.get_linestyle() == "None" for _, row, _ in rows for h in row)
    layout = dict(ncols=width, columnspacing=0.8, handletextpad=0.4, handlelength=1.0 if markers_only else 1.5)
    legend = target.legend(handles, labels, **layout, **legend_kw)
    legend._entries = (list(handles), list(labels), layout)
    return legend


def mark_value(ax, x, y, text, color, below=False):
    """Mark a compared value: a hollow circle at (x, y) and `text` just above it (`below=True`: just
    below), in `darken(color)`.
    """
    ax.plot(x, y, "o", color=color)
    offset = rcParams["lines.markersize"] / 2 + 2
    ax.annotate(text, (x, y), xytext=(0, -offset if below else offset), textcoords="offset points", ha="center",
                va="top" if below else "bottom", color=darken(color), gid="value-mark")
