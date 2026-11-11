import math
import warnings
from pathlib import Path

import matplotlib
import matplotlib.path as mpath
import matplotlib.style
import numpy as np
import yaml
from cycler import cycler
from matplotlib import colors, font_manager, rcParams
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.collections import FillBetweenPolyCollection, LineCollection, PathCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.contour import ContourSet
from matplotlib.transforms import Bbox
from matplotlib.patches import Rectangle, Wedge
from matplotlib.lines import AxLine
from matplotlib.text import Annotation
from matplotlib.ticker import FixedLocator, FuncFormatter, ScalarFormatter

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
canvas_pad = 0.1  # the canvas-pad token, in inches, set by use_design(): free space at the left and right edges
colorbar_width, colorbar_gap = 0.1, 0.06  # the colorbar tokens, in inches, set by use_design()


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
    global dashed_width, highlight_size, filled_edge_width, canvas_pad, colorbar_width, colorbar_gap, _greys
    # one renderer everywhere: screen backends measure text differently, so fit_height's layout and
    # checks would differ from what Agg saves; the scripts write files and never open a window
    matplotlib.use("agg", force=True)
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
        "axes.xmargin": _number(s["data-margin"]), "axes.ymargin": _number(s["data-margin"]),
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
    canvas_pad = _number(s["canvas-pad"])
    colorbar_width, colorbar_gap = _number(k["colorbar"]["width"]), _number(k["colorbar"]["gap"])
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


def _set_canvas_pad(fig):
    """Free space on all four sides of the canvas, for text that reaches past the panels."""
    if isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        # left and right as a rect; top and bottom as the layout's edge pad, which outside legends obey too
        x = canvas_pad / fig.get_figwidth()
        fig.get_layout_engine().set(rect=(x, 0, 1 - 2 * x, 1), h_pad=canvas_pad)


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
    if t.get_gid() in ("value-label", "value-mark"):
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
            value_label = t.get_gid() == "value-mark"  # mark_value labels turn inward at a side edge
            point_name = not _is_value_label(a, t) and isinstance(t, Annotation) and t.xycoords == "data"
            if not (_is_value_label(a, t) or point_name):
                continue
            label = t.get_window_extent(renderer)
            # a label's reach past its point is fixed in pixels, so solve for the limit
            # that leaves exactly that much room between the point and the box
            x, y = t.xy if isinstance(t, Annotation) else t.get_position()
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
                if lo >= 0 and new[0] < 0:
                    # a non-negative quantity never shows negative values to make room
                    new = (0, new[1])
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
        # side by side, upright texts need a clear word space between them (0.35 of the type size on each
        # side), or neighbours read as one at print size ("2561024", "Prefix tuningAdapter")
        gap = 0.35 * max(a.get_fontsize(), b.get_fontsize()) * a.figure.dpi / 72
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
    x_ticks, y_ticks = set(), set()
    for legend in [l for f in figures for l in f.legends] + [a.get_legend() for a in fig.axes if a.get_legend()]:
        texts += legend.get_texts()
    for a in fig.axes:
        if not (a.get_visible() and a.axison):
            continue
        texts += [a.title, a.xaxis.label, a.yaxis.label, *a.texts]
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            # matplotlib keeps labels for ticks just outside the view, which are never drawn
            # label2 is the right (top) side's: a twin axis draws its labels there
            labels = [label for loc, tick in zip(axis.get_majorticklocs(), axis.get_major_ticks())
                      if lo <= loc <= hi and axis.get_visible() for label in (tick.label1, tick.label2)]
            texts += labels
            (x_ticks if axis is a.xaxis else y_ticks).update(map(id, labels))
    texts = [t for t in texts if t.get_visible() and t.get_text()]
    boxes = [t.get_window_extent(renderer) for t in texts]
    axis_label_of = {id(a.yaxis.label): a for a in fig.axes}
    for t, box in zip(texts, boxes):
        owner = axis_label_of.get(id(t))
        if owner is not None and box.height > owner.get_window_extent(renderer).height:
            warnings.warn(f"axis label {t.get_text()!r} is longer than its panel is tall; shorten it, "
                          "the detail in the caption (DESIGN.md Collisions step 2)")
        elif box.x0 < 0 or box.y0 < 0 or box.x1 > fig.bbox.x1 or box.y1 > fig.bbox.y1:
            warnings.warn(f"text {t.get_text()!r} is cut off at the figure edge")
        if t.get_fontname() != rcParams["font.sans-serif"][0]:
            warnings.warn(f"text {t.get_text()!r} is in {t.get_fontname()}; call paper.use_design() before plotting")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if _texts_overlap(texts[i], boxes[i], texts[j], boxes[j], renderer):
                pair = {id(texts[i]), id(texts[j])}
                if pair & x_ticks and pair & y_ticks:
                    warnings.warn(f"tick labels {texts[i].get_text()!r} and {texts[j].get_text()!r} overlap at the corner; "
                                  "drop the y axis's first label (DESIGN.md Corner labels)")
                else:
                    warnings.warn(f"texts {texts[i].get_text()!r} and {texts[j].get_text()!r} overlap")

    for a in panels:
        # data drawn in data coordinates; reference lines (axhline) and value marks span the panel on purpose
        # reference lines (axhline, axline) span the panel on purpose and are not data
        # a twin axis (ax.twinx()) draws its curves over the same panel
        owners = [a] + [t for t in fig.axes if t is not a and t not in panels
                        and np.allclose(t.get_position().bounds, a.get_position().bounds)]
        data_lines = [line for o in owners for line in o.get_lines() if line.get_transform() == o.transData
                      and len(line.get_xdata()) and not isinstance(line, AxLine)]
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
        # a label anchored on a data point may touch the curve through that point (its own series)
        anchors = [a.transData.transform(t.xy) if isinstance(t, Annotation) and t.xycoords == "data" else None
                   for t in plain]
        covers = [(t.get_text(), t.get_window_extent(renderer), anchor) for t, anchor in zip(plain, anchors)]
        if a.get_legend():
            covers.append(("the legend", a.get_legend().get_window_extent(renderer), None))
        for name, box, anchor in covers:
            others = [c for c in curves if anchor is None or np.hypot(*(c.vertices - anchor).T).min() > 2]
            if any(curve.intersects_bbox(box, filled=False) for curve in others):
                warnings.warn(f"{name} covers a curve in panel {a.get_title()!r}; move it")
            elif any(box.contains(x, y) for xy in points for x, y in xy):
                warnings.warn(f"{name} covers data points in panel {a.get_title()!r}; move it")
        if a.get_legend():
            box = a.get_legend().get_window_extent(renderer)
            # an inside legend (one that overlaps its panel) must fit in it; a wider one goes above
            if box.overlaps(panel) and (box.x0 < panel.x0 - 1 or box.x1 > panel.x1 + 1 or box.y1 > panel.y1 + 1):
                warnings.warn(f"the legend sticks out of panel {a.get_title()!r}; put it above the panel "
                              "(above its row in a grid, DESIGN.md Legend)")
            if any(t.get_visible() and t.get_text() and box.overlaps(t.get_window_extent(renderer)) for t in a.texts):
                warnings.warn(f"the legend covers text in panel {a.get_title()!r}; move it")
            # the filled area under the legend, not the shapes' bounding boxes: a histogram is one wide polygon
            covered = sum(_polygon_area(poly) for shape in fills for poly in shape.clip_to_bbox(box).to_polygons())
            if covered > box.width * box.height / 10:
                warnings.warn(f"the legend covers filled marks (bars, boxes, bands, areas) in panel {a.get_title()!r}; move it")
            # a bar's value is its end: covering even a sliver of it hides the number the bar shows
            if any(_bar_end(bar, c.orientation, renderer).overlaps(box)
                   for c in a.containers if isinstance(c, BarContainer) for bar in c.patches):
                warnings.warn(f"the legend covers the end of a bar in panel {a.get_title()!r}; move it")


def _bar_end(bar, orientation, renderer):
    """The edge of a bar at its value, as a thin box: the top (bottom when negative) of a vertical
    bar, the right (left) end of a horizontal one."""
    box, value = bar.get_window_extent(renderer), (bar.get_height() if orientation == "vertical" else bar.get_width())
    if orientation == "vertical":
        y = box.y1 if value >= 0 else box.y0
        return Bbox([[box.x0, y - 0.5], [box.x1, y + 0.5]])
    x = box.x1 if value >= 0 else box.x0
    return Bbox([[x - 0.5, box.y0], [x + 0.5, box.y1]])


def _standard_parts(fig):
    """The standard widths, in inches, of the y decorations: four-character tick labels with a sign
    and their pads, and one line of the axis label with its pad."""
    renderer = fig.canvas.get_renderer()
    sample = fig.text(0, 0, "\u22120.00", fontsize=rcParams["ytick.labelsize"])  # four characters and a sign: −0.75, 1000, 100%
    ticks = sample.get_window_extent(renderer).width / fig.dpi
    sample.remove()
    ticks += (rcParams["ytick.major.pad"] + rcParams["ytick.major.size"]) / 72
    label = (rcParams["axes.labelsize"] * 1.35 + rcParams["axes.labelpad"]) / 72  # rotated, with room for (, β, _
    half = (ticks - (rcParams["ytick.major.pad"] + rcParams["ytick.major.size"]) / 72) / 2
    return ticks, label, half


def _standard_margins(fig):
    """The left and right margins, in inches, of a standard panel: on the left a y-axis label and
    four-character tick labels with a sign, on the right half of one at the x axis' end."""
    ticks, label, half = _standard_parts(fig)
    return canvas_pad + label + ticks, canvas_pad + half


def group_label(axes, text, axis="x"):
    """One axis label for a group of panels: `axis="x"` under the group's columns (pass its bottom
    panels), `axis="y"` beside its rows (pass its left panels). The label sits on the first panel and
    `fit_height` centres it on the group once the panels are placed."""
    (axes[0].set_xlabel if axis == "x" else axes[0].set_ylabel)(text)
    fig = axes[0].figure
    fig._group_labels = getattr(fig, "_group_labels", []) + [(list(axes), axis)]
    _center_group_labels(fig)


def _center_row_legends(fig, panels):
    """A legend above a panel names the series of its whole row, so it is centred over the row."""
    fig.canvas.draw()
    for a in panels:
        legend = a.get_legend()
        box, panel = (legend.get_window_extent() if legend else None), a.get_position()
        if not legend or box.y0 < a.get_window_extent().y1 - 1:
            continue
        row = [p.get_position() for p in panels if abs(p.get_position().y1 - panel.y1) < 1e-3]
        center = (min(r.x0 for r in row) + max(r.x1 for r in row)) / 2
        legend.set_loc("lower center")
        legend.set_bbox_to_anchor((center, box.y0 / fig.bbox.height), transform=fig.transFigure)


def _center_group_labels(fig):
    for axes, axis in getattr(fig, "_group_labels", []):
        boxes = [a.get_position() for a in axes]
        first = boxes[0]
        if axis == "x":
            center = (min(b.x0 for b in boxes) + max(b.x1 for b in boxes)) / 2
            axes[0].xaxis.label.set_x((center - first.x0) / first.width)
        else:
            center = (min(b.y0 for b in boxes) + max(b.y1 for b in boxes)) / 2
            axes[0].yaxis.label.set_y((center - first.y0) / first.height)


def _standard_gap(fig, column, column_gap):
    """The standard gap before a grid column. A column with its own y label shows a new quantity, so
    it starts a new group, as if a new figure began there: the right margin plus the left margin (more
    for a longer y label), plus `column_gap`, the space between the page's text columns, so in a
    double-column figure the groups line up with single-column figures. A column with only its own
    tick numbers (the same quantity over its own range) sits close: half a tick label, so the end
    labels of neighbouring x axes clear each other, plus its tick labels. Otherwise half a tick label."""
    ticks, label, half = _standard_parts(fig)
    shows_ticks = any(t.get_visible() and t.get_text() for a in column for t in a.get_yticklabels())
    label_lines = max(_lines(a.yaxis.label) for a in column)
    if label_lines:
        return (canvas_pad + half) + column_gap + (canvas_pad + ticks + label * label_lines)
    return half + ticks * shows_ticks


def _tick_height(fig):
    """x tick labels with their pad and tick mark, in inches."""
    sample = fig.text(0, 0, "0", fontsize=rcParams["xtick.labelsize"])
    height = sample.get_window_extent(fig.canvas.get_renderer()).height / fig.dpi
    sample.remove()
    return height + (rcParams["xtick.major.pad"] + rcParams["xtick.major.size"]) / 72


def _half_tick_height(fig):
    """Half a tick label: how far the top y tick label reaches above its panel."""
    return (_tick_height(fig) - (rcParams["xtick.major.pad"] + rcParams["xtick.major.size"]) / 72) / 2


def _title_height():
    return (rcParams["axes.titlesize"] * 1.35 + rcParams["axes.titlepad"]) / 72


def _lines(text):
    return text.get_text().count("\n") + 1 if text.get_text() else 0


def _standard_box(fig, panels, aspect, column_gap):
    """Panels sit at the standard margins and take the standard size, so the boxes of all figures at
    one width (and one number of columns) line up and match. The right margin is fixed; left labels
    that need more room widen the left margin and narrow the panels, which keep the standard height
    (the aspect gives way). The
    gaps between columns are standard (`_standard_gap`); the gaps between rows stay as the layout
    found them; the columns share what is left.
    One colorbar is kept beside the panels (right) or under them (bottom), at the size and gap the
    layout gave it, its labels inside a standard margin of their own. Returns whether they moved."""
    cbars = [a for a in fig.axes if getattr(a, "_colorbar", None) is not None]
    others = [a for a in fig.axes if a not in panels and a not in cbars]
    twin_of = {t: p for t in others for p in panels
               if np.allclose(t.get_position().bounds, p.get_position().bounds)}  # ax.twinx(): a right y axis
    if fig.subfigs or len(cbars) > 1 or len(twin_of) != len(others) or _is_round(panels[0]):
        return False
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    w, h = fig.get_size_inches()
    boxes = {a: a.get_position() for a in panels}
    columns = sorted({round(b.x0 * w, 2) for b in boxes.values()})
    rows = sorted({round(b.y0 * h, 2) for b in boxes.values()}, reverse=True)
    col_of = {a: columns.index(round(b.x0 * w, 2)) for a, b in boxes.items()}
    row_of = {a: rows.index(round(b.y0 * h, 2)) for a, b in boxes.items()}
    first_column = [a for a in panels if col_of[a] == 0]
    if not any(a.yaxis.label.get_text() or any(t.get_visible() and t.get_text() for t in a.get_yticklabels())
               for a in first_column):
        return False  # no y labels to align (an embedding): the layout centres the panel
    left, right = _standard_margins(fig)
    side = left - canvas_pad  # an axis label and four-character tick labels
    pad = canvas_pad
    panels_x1 = max(b.x1 for b in boxes.values()) * w
    cbar = cbars[0] if cbars else None
    vertical = cbar is not None and cbar._colorbar.orientation == "vertical"
    # the right margin never moves, so every figure's right edge lines up; a left label that needs
    # more room takes it from the panels' width, never their height, so one width keeps one height
    if vertical:
        cb = cbar.get_position()
        cb_gap, cb_w = colorbar_gap, colorbar_width
        right = pad + side + cb_w + cb_gap
    std_left, std_right = left, right
    ticks, label, half = _standard_parts(fig)
    for a, b in boxes.items():
        if col_of[a] == 0:
            left = max(left, b.x0 * w - a.get_tightbbox(renderer).x0 / fig.dpi + pad)
    sup_y = fig._supylabel if fig._supylabel and fig._supylabel.get_text() else None
    if sup_y:
        left += label
    # a right y axis mirrors the left one: its tick labels and label take room from the panels' width
    right_column = {col_of[p] for p in twin_of.values()}
    right_axis = ticks + label * max((_lines(t.yaxis.label) for t in twin_of), default=0)
    if len(columns) - 1 in right_column and not vertical:
        right = pad + right_axis
    col_gaps = [_standard_gap(fig, [a for a in panels if col_of[a] == c], column_gap) + right_axis * (c - 1 in right_column)
                for c in range(1, len(columns))]
    # rows: above each, half a tick label or a title line; below, x tick labels and x label lines;
    # anything more (a legend above a panel, a second line, turned labels) widens that margin
    above, below = [], []
    for r in range(len(rows)):
        row = [a for a in panels if row_of[a] == r]
        tight = [Bbox.union([a.get_tightbbox(renderer)] + [t.get_tightbbox(renderer) for t, p in twin_of.items() if p is a])
                 for a in row]
        y0, y1 = boxes[row[0]].y0 * h, boxes[row[0]].y1 * h
        std_above = max(_half_tick_height(fig), max(_lines(a.title) for a in row) * _title_height())
        std_below = (_tick_height(fig) * any(t.label1.get_visible() and t.label1.get_text()
                                             for a in row for t in a.xaxis.get_major_ticks())
                     + label * max(_lines(a.xaxis.label) for a in row))
        above.append(max(std_above, max(b.y1 for b in tight) / fig.dpi - y1))
        below.append(max(std_below, y0 - min(b.y0 for b in tight) / fig.dpi))
    row_gaps = [below[r] + above[r + 1] for r in range(len(rows) - 1)]
    top_legends = [lg for lg in fig.legends if lg.get_window_extent(renderer).y0 / fig.dpi >= max(b.y1 for b in boxes.values()) * h - 1e-3]
    legend_h = sum(lg.get_window_extent(renderer).height / fig.dpi for lg in top_legends)
    top = pad + legend_h + above[0]
    sup_x = fig._supxlabel if fig._supxlabel and fig._supxlabel.get_text() else None
    bottom = pad + below[-1] + label * (_lines(sup_x) if sup_x else 0)
    if cbar is not None and not vertical:
        bottom = boxes[next(a for a in panels if row_of[a] == len(rows) - 1)].y0 * h  # a colorbar under the panels keeps the layout's room
        cb = cbar.get_position()
        cb_below = bottom - cb.y1 * h  # the gap between the panels and the colorbar under them
        cb_h, cb_bottom = cb.height * h, cb.y0 * h
    panel_w = (w - left - right - sum(col_gaps)) / len(columns)
    panel_h = aspect * (w - std_left - std_right - sum(col_gaps)) / len(columns)
    row_h = [panel_h] * len(rows)
    new_h = bottom + top + sum(row_h) + sum(row_gaps)
    fig.set_layout_engine("none")
    fig.set_figheight(new_h)
    for a in panels:
        c, r = col_of[a], row_of[a]
        x0 = left + c * panel_w + sum(col_gaps[:c])
        y0 = bottom + sum(row_h[r + 1:]) + sum(row_gaps[r:])
        a.set_position([x0 / w, y0 / new_h, panel_w / w, row_h[r] / new_h])
    for t, p in twin_of.items():
        t.set_position(p.get_position())
    span_w = len(columns) * panel_w + sum(col_gaps)
    span_h = sum(row_h) + sum(row_gaps)
    if sup_x:
        sup_x.set_x((left + span_w / 2) / w)
        sup_x.set_y(pad / new_h)
        sup_x.set_verticalalignment("bottom")
    y = new_h - pad
    for lg in top_legends:
        lg.set_loc("upper center")
        lg.set_bbox_to_anchor(((left + span_w / 2) / w, y / new_h), transform=fig.transFigure)
        y -= lg.get_window_extent(renderer).height / fig.dpi
    if sup_y:
        sup_y.set_x(pad / w)
        sup_y.set_horizontalalignment("left")
        sup_y.set_y((bottom + span_h / 2) / new_h)
    if vertical:
        cbar.set_position([(left + span_w + cb_gap) / w, bottom / new_h, cb_w / w, span_h / new_h])
    elif cbar is not None:
        cbar.set_position([left / w, cb_bottom / new_h, span_w / w, cb_h / new_h])
    return True


def _clear_corners(fig, panels):
    """Where the first tick labels of both axes would touch at the shared corner, blank the y one."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for a in panels:
        firsts = []
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            shown = [(loc, t) for loc, t in zip(axis.get_majorticklocs(), axis.get_majorticklabels())
                     if lo <= loc <= hi and t.get_visible() and t.get_text()]
            firsts.append(min(shown, key=lambda p: p[0]) if shown else None)
        if None in firsts:
            continue
        (_, tx), (loc, ty) = firsts
        if _texts_overlap(tx, tx.get_window_extent(renderer), ty, ty.get_window_extent(renderer), renderer):
            label = a.yaxis.get_major_formatter()
            a.yaxis.set_major_formatter(FuncFormatter(lambda v, pos, first=loc, label=label: "" if np.isclose(v, first) else label(v, pos)))


def _start_at_zero(panels):
    """A quantity that is never negative never shows negative values: raise a default margin below 0 to 0."""
    for a in panels:
        if _is_round(a):
            continue
        lim = a.dataLim
        for get, set_, low, scale in ((a.get_xlim, a.set_xlim, lim.x0, a.get_xscale()),
                                      (a.get_ylim, a.set_ylim, lim.y0, a.get_yscale())):
            lo, hi = get()
            if scale == "linear" and np.isfinite(low) and low > 0 and lo < 0 < hi:
                set_(0, hi)


def _plain_numbers(fig):
    """Write matplotlib's default numeric ticks as plain numbers (0, 0.5, 1; 1024), with a true minus sign."""
    for a in fig.axes:
        for axis in (a.xaxis, a.yaxis):
            if type(axis.get_major_formatter()) is ScalarFormatter:
                axis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.10g}".replace("-", "\u2212")))


def _polygon_area(xy):
    x, y = xy[:, 0], xy[:, 1]
    return abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2


def _is_round(a):
    return a.name == "polar" or any(isinstance(p, Wedge) for p in a.patches)


def _pad_outside_legends(fig):
    """The layout puts a figure legend outside the panels flush with the canvas edge; give it the
    canvas pad like everything else, keeping every panel where it is in inches."""
    fig.canvas.draw()
    h = fig.get_figheight()
    tops = [lg for lg in fig.legends if lg.get_window_extent().y1 / fig.dpi > h - canvas_pad]
    if not tops:
        return
    need = max(canvas_pad - (h - lg.get_window_extent().y1 / fig.dpi) for lg in tops)
    boxes = {a: a.get_position() for a in fig.axes}
    centers = {lg: (lg.get_window_extent().x0 + lg.get_window_extent().x1) / 2 / fig.bbox.width for lg in tops}
    fig.set_layout_engine("none")
    fig.set_figheight(h + need)
    for a, b in boxes.items():
        a.set_position([b.x0, b.y0 * h / (h + need), b.width, b.height * h / (h + need)])
    for lg in tops:
        lg.set_loc("upper center")
        lg.set_bbox_to_anchor((centers[lg], 1 - canvas_pad / (h + need)), transform=fig.transFigure)


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


def fit_height(fig, ax, aspect=0.618, iters=10, tol=0.005, min_width=1.2, column_gap=0):
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
    two-factor grid with shared axes and outer tick labels only passes 0.9); text cut off at the
    figure edge, overlapping, sticking out of its panel or spilling out of its fill; text or a
    legend covering a curve or data points; a legend over text or with more than a tenth of its
    area over filled marks; a font other than Inter. Text on a white box and contour labels may
    sit over data.

    Round panels (pie charts, polar axes such as radar charts) are always circles, so `aspect`
    does not apply: the height is cut to the content once the circles are as large as the width
    allows.

    `column_gap` (inches) is the space between a two-column page's text columns, for a figure
    spanning both (DESIGN.md Width): a column with its own y axis starts after it, so the figure's
    groups line up with the single-column figures above and below.

    Never save with `bbox_inches="tight"`: it changes the final size and breaks the width and
    the ratio this function set.
    """
    axes = list(ax.values()) if isinstance(ax, dict) else list(np.ravel(ax))
    panels = [a for a in axes
              if a.get_visible() and a.axison and getattr(a, "_colorbar", None) is None]
    _plain_numbers(fig)
    _start_at_zero(panels)
    if isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        _set_canvas_pad(fig)
    _warn_wide_legends(fig)
    if any(_is_round(a) for a in panels):
        _trim_height(fig, panels)
        _pad_outside_legends(fig)
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
        _freeze_ticks(fig.axes)  # colorbars too: their auto ticks change width with the height
        ratios, widths = _solve(fig, panels, aspect, iters, tol)
    if abs(ratios[0] - aspect) / aspect >= tol:
        warnings.warn(f"fit_height did not converge in {iters} iterations: ratio {ratios[0]:.3f}; "
                      "check for an inside legend or text wider than the panel.")
    if max(widths) - min(widths) > tol * max(widths):
        warnings.warn("panels have different widths, so not all can match the aspect; "
                      f"panel ratios: {[round(r, 3) for r in ratios]}")
    _clear_corners(fig, panels)
    if _standard_box(fig, panels, aspect, column_gap):
        _freeze_ticks(panels)  # growing limits for labels now must not add ticks the layout has no room for
        _keep_value_labels_inside(fig, panels)
        ratios = _panel_ratios(fig, panels)[0]
    _center_group_labels(fig)
    _center_row_legends(fig, panels)
    if max(ratios) - min(ratios) > tol * max(ratios):
        warnings.warn("panels have different shapes; one figure takes one aspect (no height_ratios or width_ratios)")
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


def _warn_wide_legends(fig):
    fig.draw_without_rendering()
    room = fig.bbox.width - 2 * canvas_pad * fig.dpi
    for legend in fig.legends + [a.get_legend() for a in fig.axes if a.get_legend()]:
        if legend.get_window_extent().width > room:
            n, ncol = len(legend.get_texts()), legend._ncols
            fewer = [math.ceil(n / k) for k in range(2, n + 1) if math.ceil(n / k) < ncol]
            fix = f"use ncol={fewer[0]}" if fewer else "shorten its entries"
            warnings.warn(f"a legend of {n} entries in {ncol} columns is wider than the figure; {fix}")


def mark_value(ax, x, y, text, color, below=False):
    """Mark a compared value: a thin solid line in `darken(color)` across the panel at y, under the curves
    (a reference line, so it is never taken for a dashed grey series),
    a hollow circle at (x, y), and `text` just above it (`below=True`: just below), in `darken(color)`.
    """
    ax.axhline(y, linewidth=rcParams["grid.linewidth"], color=darken(color), zorder=1)
    ax.plot(x, y, "o", color=color)
    offset = rcParams["lines.markersize"] / 2 + 2
    ax.annotate(text, (x, y), xytext=(0, -offset if below else offset), textcoords="offset points", ha="center",
                va="top" if below else "bottom", color=darken(color), gid="value-mark")

