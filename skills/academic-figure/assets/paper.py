import warnings
from pathlib import Path

import numpy as np
import tol_colors  # registers the tol.* colormaps that paper.mplstyle names
from matplotlib import colors, font_manager, rcParams
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.markers import MarkerStyle
from matplotlib.ticker import FixedLocator

# Inter ships with the skill because no environment has it installed; paper.mplstyle names it.
for _font in Path(__file__).parent.glob("Inter-*.ttf"):
    font_manager.fontManager.addfont(str(_font))


def _panel_ratios(fig, panels):
    fig.canvas.draw()
    fw, fh = fig.get_size_inches()
    sizes = [(p.width * fw, p.height * fh) for p in (a.get_position() for a in panels)]
    return [h / w for w, h in sizes], [w for w, _ in sizes]


def _solve(fig, panels, aspect, iters, tol):
    h0 = fig.get_figheight()
    ratios, widths = _panel_ratios(fig, panels)
    r0 = ratios[0]
    h1 = h0 * aspect / r0
    for _ in range(iters):
        fig.set_figheight(h1)
        ratios, widths = _panel_ratios(fig, panels)
        r1 = ratios[0]
        if abs(r1 - aspect) / aspect < tol or r1 == r0:
            break
        h0, r0, h1 = h1, r1, h1 + (aspect - r1) * (h1 - h0) / (r1 - r0)
    return ratios, widths


def _freeze_ticks(panels):
    for a in panels:
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            axis.set_major_locator(FixedLocator([t for t in axis.get_majorticklocs() if lo <= t <= hi]))


def _keep_value_labels_inside(fig, panels):
    """Grow each panel's y-limits, and turn labels at the side edges inward, so every
    `mark_value` label lies inside its panel. Returns whether any y-limits changed."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    changed = False
    for a in panels:
        box = a.get_window_extent(renderer)
        for t in a.texts:
            if t.get_gid() != "value-label":
                continue
            label = t.get_window_extent(renderer)
            if label.x1 > box.x1:
                t.set_ha("right")
            elif label.x0 < box.x0:
                t.set_ha("left")
            # the label's reach above / below its point is fixed in pixels, so solve for the limit
            # that leaves exactly that much room between the point and the spine
            y = t.xy[1]
            point = a.transData.transform((t.xy[0], y))[1]
            lo, hi = a.get_ylim()
            if label.y1 > box.y1:
                above = label.y1 - point + 1
                a.set_ylim(lo, lo + (y - lo) * box.height / (box.height - above))
                changed = True
            elif label.y0 < box.y0:
                below = point - label.y0 + 1
                a.set_ylim((y * box.height - below * hi) / (box.height - below), hi)
                changed = True
    return changed


def fit_height(fig, ax, aspect=0.618, iters=10, tol=0.005):
    """Change only the figure height so each panel's height / width equals `aspect`.

    The panel is the data area inside the axes spines; tick labels, axis labels, titles,
    outside legends and colorbars are not measured. Call it last, after everything is drawn,
    on a figure that uses constrained layout. `ax` is an Axes, an array or list of Axes, or
    the dict from `subplot_mosaic`. Hidden axes and colorbar axes are skipped. If panels have
    different widths, the first panel is fitted. Returns the final panel ratios.

    Auto ticks can change with the height (e.g. 75, 80 → 77.5, 80.0), which changes the tick
    label width and so the panel width. If that keeps the ratio from converging, the major
    ticks are fixed at their current positions and the height is solved again.

    `mark_value` labels that would stick out of their panel are brought inside: the y-limits
    grow to make room above (or below), and labels at the left or right edge turn inward.

    Never save with `bbox_inches="tight"`: it changes the final size and breaks the width and
    the ratio this function set.
    """
    axes = list(ax.values()) if isinstance(ax, dict) else list(np.ravel(ax))
    panels = [a for a in axes
              if a.get_visible() and a.axison and getattr(a, "_colorbar", None) is None]
    for a in panels:
        if a.get_aspect() != "auto" or a.get_box_aspect() is not None:
            raise ValueError(
                f"panel {a.get_title()!r} has a fixed aspect, so the figure height cannot set "
                "its ratio; use aspect='auto' (e.g. imshow(..., aspect='auto')).")
    if not isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        warnings.warn("fit_height expects layout='constrained'; ratios may be off.")

    ratios, widths = _solve(fig, panels, aspect, iters, tol)
    if _keep_value_labels_inside(fig, panels):
        ratios, widths = _solve(fig, panels, aspect, iters, tol)
    if abs(ratios[0] - aspect) / aspect >= tol:
        _freeze_ticks(panels)
        ratios, widths = _solve(fig, panels, aspect, iters, tol)
    if abs(ratios[0] - aspect) / aspect >= tol:
        warnings.warn(f"fit_height did not converge in {iters} iterations: ratio {ratios[0]:.3f}; "
                      "check for an inside legend or text wider than the panel.")
    if max(widths) - min(widths) > tol * max(widths):
        warnings.warn("panels have different widths, so not all can match the aspect; "
                      f"panel ratios: {[round(r, 3) for r in ratios]}")
    return ratios


def darken(color):
    """`color` darkened to 80%: for text or edges that belong to a series, so they read on white."""
    return [c * 0.8 for c in colors.to_rgb(color)]


def smooth(values):
    """Centered moving average over 5% of the points (2.5% each side), shrinking at the ends.
    Centered, not EMA, so the smoothed curve does not lag the raw one."""
    half = max(1, len(values) // 40)
    return [np.mean(values[max(0, i - half):i + half + 1]) for i in range(len(values))]


def mark_value(ax, x, y, text, color, star=False, below=False):
    """Mark a compared value: a dashed line in `darken(color)` across the panel at y, under the curves,
    a point at (x, y), and `text` in bold just above it (`below=True`: just below), in `darken(color)`.

    The point is a hollow circle, or with `star=True` a filled star twice the marker size (its thin
    points vanish at the normal size).
    """
    ax.axhline(y, linestyle="--", linewidth=1, color=darken(color), zorder=1)
    size = rcParams["lines.markersize"] * (2 if star else 1)
    if star:
        # matplotlib bevels star corners by default, which blunts the points; miter keeps them sharp
        ax.plot(x, y, marker=MarkerStyle("*", joinstyle="miter"), markersize=size,
                markerfacecolor=color, markeredgecolor=darken(color))
    else:
        ax.plot(x, y, "o", color=color)
    offset = size / 2 + 2
    ax.annotate(text, (x, y), xytext=(0, -offset if below else offset), textcoords="offset points", ha="center",
                va="top" if below else "bottom", fontweight="bold", color=darken(color), gid="value-label")
