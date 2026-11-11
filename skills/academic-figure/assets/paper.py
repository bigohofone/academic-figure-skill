import warnings
from pathlib import Path

import matplotlib.path as mpath
import matplotlib.style
import numpy as np
import yaml
from cycler import cycler
from matplotlib import colors, font_manager, rcParams
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.collections import FillBetweenPolyCollection, LineCollection, PathCollection, PolyCollection
from matplotlib.contour import ContourSet
from matplotlib.transforms import Bbox
from matplotlib.patches import Rectangle, Wedge
from matplotlib.text import Annotation
from matplotlib.ticker import FixedLocator

# Inter ships with the skill because no environment has it installed; DESIGN.md names it.
for _font in Path(__file__).parent.glob("Inter-*.ttf"):
    font_manager.fontManager.addfont(str(_font))


def _size(a, original=False):
    """Panel width and height in inches; a panel's position is relative to its subfigure, if any."""
    box = a.get_position(original=original).transformed(a.figure.transSubfigure)
    return box.width / a.figure.dpi, box.height / a.figure.dpi

dashed_width = 0.75  # the dashed-line token, set by use_design(); pass it to dashed and dotted lines
highlight_size = 5  # the marker highlight-size token, set by use_design(); for a point of interest
filled_edge_width = 0.25  # the marker filled-edge-width token, set by use_design(); for filled markers


def _resolve(value, tokens):
    """Replace token references such as "{colors.series-2}" with the value they point to."""
    if isinstance(value, dict):
        return {k: _resolve(v, tokens) for k, v in value.items()}
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        target = tokens
        for key in value[1:-1].split("."):
            target = target[key]
        return _resolve(target, tokens)
    return value


def _number(value):
    """A token dimension such as "0.5pt" or "0.02in" as a number in its unit."""
    return float(str(value).rstrip("ptin"))


def use_design(path="DESIGN.md"):
    """Set matplotlib's style from paper.mplstyle and the tokens in the front matter of `path`, a DESIGN.md.
    Returns the colors by name, e.g. colors["series-1"], colors["ours"]."""
    global dashed_width, highlight_size, filled_edge_width, _greys
    tokens = yaml.safe_load(Path(path).read_text().split("---")[1])
    tokens = _resolve(tokens, tokens)
    c, t, s, k = tokens["colors"], tokens["typography"], tokens["spacing"], tokens["components"]
    _greys = c["neutral"], c["neutral-light"], c["neutral-dark"]
    matplotlib.style.use(Path(__file__).parent / "paper.mplstyle")
    label, tick_label, legend, value_label, title = (
        _number(t[name]["fontSize"]) for name in ("label", "tick-label", "legend", "value-label", "title"))
    tick_pad, tick_width = _number(s["tick-pad"]), _number(k["tick"]["width"])
    rcParams.update({
        "font.sans-serif": [t["label"]["fontFamily"]],
        "font.size": value_label, "axes.labelsize": label, "figure.labelsize": label, "legend.fontsize": legend,
        "xtick.labelsize": tick_label, "ytick.labelsize": tick_label,
        "axes.titlesize": title, "axes.titleweight": t["title"].get("fontWeight", 400),
        "axes.titlepad": _number(s["title-pad"]), "axes.labelpad": _number(s["label-pad"]),
        "xtick.major.pad": tick_pad, "xtick.minor.pad": tick_pad, "ytick.major.pad": tick_pad, "ytick.minor.pad": tick_pad,
        "xtick.major.width": tick_width, "xtick.minor.width": tick_width,
        "ytick.major.width": tick_width, "ytick.minor.width": tick_width,
        "xtick.major.size": _number(k["tick"]["size"]), "ytick.major.size": _number(k["tick"]["size"]),
        "xtick.minor.size": _number(k["tick"]["minor-size"]), "ytick.minor.size": _number(k["tick"]["minor-size"]),
        "text.color": c["ink"], "axes.labelcolor": c["ink"], "xtick.color": c["ink"], "ytick.color": c["ink"],
        "axes.edgecolor": k["axes"]["textColor"], "axes.linewidth": _number(k["axes"]["width"]),
        "grid.color": k["grid"]["color"], "grid.alpha": k["grid"]["opacity"], "grid.linewidth": _number(k["grid"]["width"]),
        "lines.linewidth": _number(k["line"]["width"]),
        "lines.markersize": _number(k["marker"]["size"]), "lines.markeredgewidth": _number(k["marker"]["edge-width"]),
        "patch.linewidth": _number(k["outline"]["width"]),
        "boxplot.boxprops.linewidth": _number(k["outline"]["width"]),
        "boxplot.whiskerprops.linewidth": _number(k["outline"]["width"]),
        "boxplot.capprops.linewidth": _number(k["outline"]["width"]),
        "boxplot.medianprops.linewidth": _number(k["median"]["width"]),
        "boxplot.flierprops.markersize": _number(k["marker"]["size"]), "boxplot.flierprops.markeredgewidth": _number(k["marker"]["edge-width"]),
        "contour.linewidth": _number(k["contour"]["width"]),
        "axes.prop_cycle": cycler(color=[v for name, v in c.items() if name.startswith("series-")] + [c["neutral"]]),
        "image.cmap": k["heatmap"]["colormap"],
        "figure.constrained_layout.w_pad": _number(s["layout-pad"]),
        "figure.constrained_layout.h_pad": _number(s["layout-pad"]),
    })
    dashed_width = _number(k["dashed-line"]["width"])
    highlight_size = _number(k["marker"]["highlight-size"])
    filled_edge_width = _number(k["marker"]["filled-edge-width"])
    return c


def _panel_ratios(fig, panels):
    fig.canvas.draw()
    sizes = [_size(a) for a in panels]
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
        if not np.isfinite(r1) or r1 <= 0:
            # too short for the decorations (titles, outside legends): the layout collapsed
            h0, r0, h1 = h1, r0, 2 * h1
            continue
        if abs(r1 - aspect) / aspect < tol or r1 == r0:
            break
        step = h1 + (aspect - r1) * (h1 - h0) / (r1 - r0)
        # a secant step can overshoot below zero while the layout is still settling: halve instead
        h0, r0, h1 = h1, r1, step if np.isfinite(step) and step > 0 else h1 / 2
    return ratios, widths


def _freeze_ticks(panels):
    for a in panels:
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            axis.set_major_locator(FixedLocator([t for t in axis.get_majorticklocs() if lo <= t <= hi]))


def _limit_for_reach(axis, lo, hi, v, reach, size, upper):
    """The new upper (or lower) limit that leaves `reach` pixels between value `v` and the panel edge,
    solved in the axis's scale (linear, log), where data maps linearly to pixels."""
    scale = axis.get_transform()
    lo, hi, v = scale.transform([lo, hi, v])
    limit = lo + (v - lo) * size / (size - reach) if upper else (v * size - reach * hi) / (size - reach)
    return scale.inverted().transform([limit])[0]


def _bar_ends(a):
    """The points `ax.bar_label` anchors its labels to: each bar's ends and middle, in data coordinates."""
    ends = []
    for p in a.patches:
        if isinstance(p, Rectangle):
            x, y, w, h = p.get_x(), p.get_y(), p.get_width(), p.get_height()
            ends += [(x + w / 2, y + h), (x + w / 2, y), (x + w, y + h / 2), (x, y + h / 2), (x + w / 2, y + h / 2)]
    return np.array(ends)


def _is_value_label(a, t):
    """A `mark_value` label or a bar label (`ax.bar_label`), the labels fit_height keeps inside the panel."""
    if t.get_gid() == "value-label":
        return True
    ends = _bar_ends(a)
    return (isinstance(t, Annotation) and t.xycoords == "data" and len(ends) > 0
            and bool(np.isclose(ends, t.xy).all(axis=1).any()))


def _keep_value_labels_inside(fig, panels):
    """Grow each panel's limits so every `mark_value` label, bar label (`ax.bar_label`) and point name
    (an annotation in data coordinates) lies inside its panel. `mark_value` labels at a side edge
    turn inward instead. A point name gets at most a quarter more axis range; one that needs more
    is left out and reported, to be moved. Returns whether any limits changed."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    changed = False
    for a in panels:
        if _is_round(a):
            continue
        box = a.get_window_extent(renderer)
        for t in a.texts:
            value_label = t.get_gid() == "value-label"
            point_name = not _is_value_label(a, t) and isinstance(t, Annotation) and t.xycoords == "data"
            if not (_is_value_label(a, t) or point_name):
                continue
            label = t.get_window_extent(renderer)
            # a label's reach past its point is fixed in pixels, so solve for the limit
            # that leaves exactly that much room between the point and the box
            x, y = t.xy
            point_x, point_y = a.transData.transform((x, y))
            for axis, low_edge, high_edge, v, point, size, set_lim, get_lim in (
                    (a.xaxis, label.x0 < box.x0, label.x1 > box.x1, x, point_x, box.width, a.set_xlim, a.get_xlim),
                    (a.yaxis, label.y0 < box.y0, label.y1 > box.y1, y, point_y, box.height, a.set_ylim, a.get_ylim)):
                if not (low_edge or high_edge):
                    continue
                if value_label and axis is a.xaxis:
                    t.set_ha("left" if low_edge else "right")
                    continue
                lo, hi = get_lim()
                if high_edge:
                    reach = (label.x1 if axis is a.xaxis else label.y1) - point + 1
                    new = (lo, _limit_for_reach(axis, lo, hi, v, reach, size, True))
                else:
                    reach = point - (label.x0 if axis is a.xaxis else label.y0) + 1
                    new = (_limit_for_reach(axis, lo, hi, v, reach, size, False), hi)
                scale = axis.get_transform()
                old_span = np.ptp(scale.transform([lo, hi]))
                if point_name and np.ptp(scale.transform(list(new))) > 1.25 * old_span:
                    continue
                set_lim(*new)
                changed = True
    return changed


def _rotated_outline(t, box, renderer):
    """The text's outline as a closed path in display coordinates: its upright box turned by its
    rotation about the center of `box`, its upright bounding box once rotated."""
    angle = t.get_rotation()
    t.set_rotation(0)
    upright = t.get_window_extent(renderer)
    t.set_rotation(angle)
    along = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))]) * upright.width / 2
    across = np.array([-along[1], along[0]]) / np.hypot(*along) * upright.height / 2
    center = np.array([box.x0 + box.x1, box.y0 + box.y1]) / 2
    corners = [center - along - across, center + along - across, center + along + across, center - along + across]
    return mpath.Path(corners + corners[:1], closed=True)


def _texts_overlap(a, box_a, b, box_b, renderer):
    """Whether two texts overlap. A rotated text (e.g. a 45° tick label) is compared by its turned
    outline, since its upright bounding box also covers the empty corners around it."""
    a_rotated, b_rotated = a.get_rotation() % 180 != 0, b.get_rotation() % 180 != 0
    if not (a_rotated or b_rotated):
        # side by side, upright texts need a gap (1 pt each side), or neighbouring numbers read as one ("2561024")
        gap = a.figure.dpi / 72
        return Bbox.from_extents(box_a.x0 - gap, box_a.y0, box_a.x1 + gap, box_a.y1).overlaps(box_b)
    if a_rotated and b_rotated:
        outline_a, outline_b = _rotated_outline(a, box_a, renderer), _rotated_outline(b, box_b, renderer)
        return outline_a.intersects_path(outline_b, filled=True)
    rotated, box_rotated, other_box = (a, box_a, box_b) if a_rotated else (b, box_b, box_a)
    return _rotated_outline(rotated, box_rotated, renderer).intersects_bbox(other_box, filled=True)

def _warn_layout_problems(fig, panels, min_width):
    """Warn about what makes a figure hard to read in print, so it can be fixed before saving."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for a in panels:
        if a.get_window_extent(renderer).width / fig.dpi < min_width:
            warnings.warn(f"panel {a.get_title()!r} is narrower than {min_width} in; use one column fewer")

    figures = [fig, *fig.subfigs]
    texts = [t for f in figures for t in f.texts]
    for legend in [l for f in figures for l in f.legends] + [a.get_legend() for a in fig.axes if a.get_legend()]:
        texts += legend.get_texts()
    for a in fig.axes:
        if not (a.get_visible() and a.axison):
            continue
        texts += [a.title, a.xaxis.label, a.yaxis.label, *a.texts]
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            # matplotlib keeps labels for ticks just outside the view, which are never drawn
            texts += [label for loc, label in zip(axis.get_majorticklocs(), axis.get_majorticklabels())
                      if lo <= loc <= hi]
    texts = [t for t in texts if t.get_visible() and t.get_text()]
    boxes = [t.get_window_extent(renderer) for t in texts]
    for t, box in zip(texts, boxes):
        if box.x0 < 0 or box.y0 < 0 or box.x1 > fig.bbox.x1 or box.y1 > fig.bbox.y1:
            warnings.warn(f"text {t.get_text()!r} is cut off at the figure edge")
        if t.get_fontname() != rcParams["font.sans-serif"][0]:
            warnings.warn(f"text {t.get_text()!r} is in {t.get_fontname()}; call paper.use_design() before plotting")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if _texts_overlap(texts[i], boxes[i], texts[j], boxes[j], renderer):
                warnings.warn(f"texts {texts[i].get_text()!r} and {texts[j].get_text()!r} overlap")

    for a in panels:
        # data drawn in data coordinates; reference lines (axhline) and value marks span the panel on purpose
        data_lines = [line for line in a.get_lines() if line.get_transform() == a.transData and len(line.get_xdata())]
        curves = [line.get_path().transformed(line.get_transform())
                  for line in data_lines if line.get_linestyle() not in ("None", "none", "")]
        points = [line.get_transform().transform(line.get_xydata())
                  for line in data_lines if line.get_marker() not in (None, "None", "none", "")]
        points += [c.get_offset_transform().transform(c.get_offsets()) for c in a.collections
                   if isinstance(c, PathCollection) and len(c.get_offsets())]
        curves += [path.transformed(c.get_transform()) for c in a.collections
                   if isinstance(c, LineCollection) and not isinstance(c, PolyCollection) for path in c.get_paths()]
        # filled shapes: bars and boxes, and bands, violins and stacked areas (PolyCollections)
        fills = [p.get_path().transformed(p.get_transform()) for p in a.patches if p.get_visible() and p.get_fill()]
        fills += [path.transformed(c.get_transform()) for c in a.collections
                  if type(c) in (PolyCollection, FillBetweenPolyCollection) and c.get_visible() for path in c.get_paths()]
        contour_labels = [t for c in a.collections if isinstance(c, ContourSet) for t in c.labelTexts]
        # text on a white box is meant to sit over data, and contour labels sit in gaps cut for them
        plain = [t for t in a.texts if t.get_visible() and t.get_text() and t.get_bbox_patch() is None
                 and t not in contour_labels and t.get_gid() != "contour-label"]
        panel = a.get_window_extent(renderer)
        for t in plain:
            box = t.get_window_extent(renderer)
            if not _is_value_label(a, t) and not _is_round(a) and isinstance(t, Annotation) and t.xycoords == "data" and not (
                    panel.x0 - 1 <= box.x0 and box.x1 <= panel.x1 + 1 and panel.y0 - 1 <= box.y0 and box.y1 <= panel.y1 + 1):
                warnings.warn(f"text {t.get_text()!r} sticks out of panel {a.get_title()!r}; move it")
            corners = [(box.x0, box.y0), (box.x1, box.y0), (box.x1, box.y1), (box.x0, box.y1)]
            for fill in fills:
                if fill.contains_point(((box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)) and not fill.contains_points(corners).all():
                    warnings.warn(f"text {t.get_text()!r} spills out of its fill in panel {a.get_title()!r}; drop or move it")
                    break
        covers = [(t.get_text(), t.get_window_extent(renderer)) for t in plain]
        if a.get_legend():
            covers.append(("the legend", a.get_legend().get_window_extent(renderer)))
        for name, box in covers:
            if any(curve.intersects_bbox(box, filled=False) for curve in curves):
                warnings.warn(f"{name} covers a curve in panel {a.get_title()!r}; move it")
            elif any(box.contains(x, y) for xy in points for x, y in xy):
                warnings.warn(f"{name} covers data points in panel {a.get_title()!r}; move it")
        if a.get_legend():
            box = a.get_legend().get_window_extent(renderer)
            if any(t.get_visible() and t.get_text() and box.overlaps(t.get_window_extent(renderer)) for t in a.texts):
                warnings.warn(f"the legend covers text in panel {a.get_title()!r}; move it")
            # the filled area under the legend, not the shapes' bounding boxes: a histogram is one wide polygon
            covered = sum(_polygon_area(poly) for shape in fills for poly in shape.clip_to_bbox(box).to_polygons())
            if covered > box.width * box.height / 10:
                warnings.warn(f"the legend covers filled marks (bars, boxes, bands, areas) in panel {a.get_title()!r}; move it")


def _polygon_area(xy):
    x, y = xy[:, 0], xy[:, 1]
    return abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2


def _is_round(a):
    return a.name == "polar" or any(isinstance(p, Wedge) for p in a.patches)


def _trim_height(fig, panels):
    """A round panel (pie, polar) is always a circle, as large as its slot allows. Start tall so the
    figure width sets its size, then cut the empty height of its slot above and below it."""
    fig.set_figheight(3 * fig.get_figwidth())
    for _ in range(10):
        fig.canvas.draw()
        rows = {}
        for a in panels:
            row = round(a.get_position(original=True).transformed(a.figure.transSubfigure).y0)
            rows[row] = min(rows.get(row, np.inf), _size(a, original=True)[1] - _size(a)[1])
        empty = sum(rows.values())
        if empty < 0.005:
            break
        fig.set_figheight(fig.get_figheight() - empty)


def fit_height(fig, ax, aspect=0.618, iters=10, tol=0.005, min_width=1.2):
    """Change only the figure height so each panel's height / width equals `aspect`.

    The panel is the data area inside the axes spines; tick labels, axis labels, titles,
    outside legends and colorbars are not measured. Call it last, after everything is drawn,
    on a figure that uses constrained layout. `ax` is an Axes, an array or list of Axes, or
    the dict from `subplot_mosaic`. Hidden axes and colorbar axes are skipped. If panels have
    different widths, the first panel is fitted. Returns the final panel ratios.

    Auto ticks can change with the height (e.g. 75, 80 → 77.5, 80.0), which changes the tick
    label width and so the panel width. If that keeps the ratio from converging, the major
    ticks are fixed at their current positions and the height is solved again.

    `mark_value` labels and bar labels that would stick out of their panel are brought inside:
    the limits grow to make room, and `mark_value` labels at the left or right edge turn inward.
    Other text is never moved.

    Last, it warns about what reads badly in print: a panel narrower than `min_width` (1.2 in; a
    two-factor grid with shared axes and outer tick labels only passes 1.0); text cut off at the
    figure edge, overlapping, sticking out of its panel or spilling out of its fill; text or a
    legend covering a curve or data points; a legend over text or with more than a tenth of its
    area over filled marks; a font other than Inter. Text on a white box and contour labels may
    sit over data.

    Round panels (pie charts, polar axes such as radar charts) are always circles, so `aspect`
    does not apply: the height is cut to the content once the circles are as large as the width
    allows.

    Never save with `bbox_inches="tight"`: it changes the final size and breaks the width and
    the ratio this function set.
    """
    axes = list(ax.values()) if isinstance(ax, dict) else list(np.ravel(ax))
    panels = [a for a in axes
              if a.get_visible() and a.axison and getattr(a, "_colorbar", None) is None]
    if any(_is_round(a) for a in panels):
        _trim_height(fig, panels)
        _warn_layout_problems(fig, panels, min_width)
        return _panel_ratios(fig, panels)[0]
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
    _warn_layout_problems(fig, panels, min_width)
    return ratios


def greys(n):
    """n grey fills, evenly spaced from the design's neutral-light to neutral-dark; one series takes neutral."""
    neutral, light, dark = (np.array(colors.to_rgb(g)) for g in _greys)
    if n == 1:
        return [tuple(neutral)]
    return [tuple(light + (dark - light) * i / (n - 1)) for i in range(n)]


def darken(color):
    """`color` darkened to 80%: for text or edges that belong to a series, so they read on white."""
    return [c * 0.8 for c in colors.to_rgb(color)]



def text_color(fill):
    """Black or white, whichever reads on `fill`: for numbers written on bars, wedges, areas or heatmap cells."""
    return "white" if np.dot(colors.to_rgb(fill), [0.299, 0.587, 0.114]) < 0.5 else "black"


def lighten(color):
    """`color` mixed with white, 40% color: a box or violin fill, so the black median and points on it stay readable."""
    return [0.4 * c + 0.6 for c in colors.to_rgb(color)]


def smooth(values):
    """Centered moving average over 5% of the points (2.5% each side), shrinking at the ends.
    Centered, not EMA, so the smoothed curve does not lag the raw one."""
    half = max(1, len(values) // 40)
    return [np.mean(values[max(0, i - half):i + half + 1]) for i in range(len(values))]


def mark_value(ax, x, y, text, color, below=False):
    """Mark a compared value: a dashed line in `darken(color)` across the panel at y, under the curves,
    a hollow circle at (x, y), and `text` just above it (`below=True`: just below), in `darken(color)`.
    """
    ax.axhline(y, linestyle="--", linewidth=dashed_width, color=darken(color), zorder=1)
    ax.plot(x, y, "o", color=color)
    offset = rcParams["lines.markersize"] / 2 + 2
    ax.annotate(text, (x, y), xytext=(0, -offset if below else offset), textcoords="offset points", ha="center",
                va="top" if below else "bottom", color=darken(color), gid="value-label")

