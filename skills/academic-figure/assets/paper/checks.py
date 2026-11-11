"""Readability checks finalize_figure runs last: text cut off or overlapping, labels and legends covering data,
series that merge in grayscale, panels too narrow to read; and the tests on texts and panels that the
layout shares (does a text overlap another, is it a value label, is a panel round)."""
import math
import warnings

import matplotlib.path as mpath
import numpy as np
from matplotlib import rcParams
from matplotlib.collections import FillBetweenPolyCollection, LineCollection, PathCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.contour import ContourSet
from matplotlib.transforms import Bbox
from matplotlib.lines import AxLine
from matplotlib.patches import Rectangle, Wedge
from matplotlib.text import Annotation

from . import design, palette


def _is_value_label(a, t):
    """A `mark_value` label or a bar label (`ax.bar_label`), the labels layout.finalize_figure keeps inside the panel."""
    if t.get_gid() in ("value-label", "value-mark"):
        return True
    ends = _bar_label_anchors(a)
    return (isinstance(t, Annotation) and t.xycoords == "data" and len(ends) > 0
            and bool(np.isclose(ends, t.xy).all(axis=1).any()))


def _bar_label_anchors(a):
    """The points `ax.bar_label` anchors its labels to: each bar's ends and middle, in data coordinates."""
    ends = []
    for p in a.patches:
        if isinstance(p, Rectangle):
            x, y, w, h = p.get_x(), p.get_y(), p.get_width(), p.get_height()
            ends += [(x + w / 2, y + h), (x + w / 2, y), (x + w, y + h / 2), (x, y + h / 2), (x + w / 2, y + h / 2)]
    return np.array(ends)


def _is_round_panel(a):
    return a.name == "polar" or any(isinstance(p, Wedge) for p in a.patches)


def _rotated_text_outline(t, box, renderer):
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
        outline_a, outline_b = _rotated_text_outline(a, box_a, renderer), _rotated_text_outline(b, box_b, renderer)
        return outline_a.intersects_path(outline_b, filled=True)
    rotated, box_rotated, other_box = (a, box_a, box_b) if a_rotated else (b, box_b, box_a)
    return _rotated_text_outline(rotated, box_rotated, renderer).intersects_bbox(other_box, filled=True)


def _warn_hard_to_read(fig, panels, min_width):
    """Warn about what makes a figure hard to read in print, so it can be fixed before saving."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for a in panels:
        if a.get_window_extent(renderer).width / fig.dpi < min_width:
            warnings.warn(f"panel {a.get_title()!r} is narrower than {min_width} in; use one column fewer")
    _warn_text_problems(fig, renderer)
    for a in panels:
        fills = _filled_shapes(a)
        _warn_text_over_data(fig, a, panels, fills, renderer)
        _warn_grayscale_lookalikes(a)
        if a.get_legend():
            _warn_legend_over_data(a, fills, renderer)


def _shown_texts(fig):
    """Every visible text of the figure, and the ids of the x and y tick labels among them."""
    figures = [fig, *fig.subfigs]
    texts = [t for f in figures for t in f.texts]
    x_ticks, y_ticks = set(), set()
    for legend in [lg for f in figures for lg in f.legends] + [a.get_legend() for a in fig.axes if a.get_legend()]:
        texts += legend.get_texts()
    for a in fig.axes:
        if not (a.get_visible() and a.axison):
            continue
        texts += [a.title, a.xaxis.label, a.yaxis.label, *a.texts]
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            # matplotlib keeps labels for ticks just outside the view, which are never drawn;
            # label2 is the right (top) side's: a twin axis draws its labels there
            labels = [label for loc, tick in zip(axis.get_majorticklocs(), axis.get_major_ticks())
                      if lo <= loc <= hi and axis.get_visible() for label in (tick.label1, tick.label2)]
            texts += labels
            (x_ticks if axis is a.xaxis else y_ticks).update(map(id, labels))
    return [t for t in texts if t.get_visible() and t.get_text()], x_ticks, y_ticks


def _warn_text_problems(fig, renderer):
    """Text cut off at the figure edge, overlapping other text, in a font other than the design's, or
    an axis label longer than its panel."""
    texts, x_ticks, y_ticks = _shown_texts(fig)
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
            warnings.warn(f"text {t.get_text()!r} is in {t.get_fontname()}; call design.apply_design() before plotting")
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if _texts_overlap(texts[i], boxes[i], texts[j], boxes[j], renderer):
                pair = {id(texts[i]), id(texts[j])}
                if pair & x_ticks and pair & y_ticks:
                    warnings.warn(f"tick labels {texts[i].get_text()!r} and {texts[j].get_text()!r} overlap at the corner; "
                                  "drop the y axis's first label (DESIGN.md Corner labels)")
                else:
                    warnings.warn(f"texts {texts[i].get_text()!r} and {texts[j].get_text()!r} overlap")


def _filled_shapes(a):
    """Bars and boxes, and bands, violins and stacked areas (PolyCollections), as paths in display coordinates."""
    fills = [p.get_path().transformed(p.get_transform()) for p in a.patches if p.get_visible() and p.get_fill()]
    return fills + [path.transformed(c.get_transform()) for c in a.collections
                    if type(c) in (PolyCollection, FillBetweenPolyCollection) and c.get_visible() for path in c.get_paths()]


def _warn_text_over_data(fig, a, panels, fills, renderer):
    """Text in a panel that sticks out of it, spills out of the fill it sits on, or covers a curve or
    data points; the legend covering a curve or points too."""
    # reference lines (axhline, axline) span the panel on purpose and are not data;
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
    contour_labels = [t for c in a.collections if isinstance(c, ContourSet) for t in c.labelTexts]
    # text on a white box is meant to sit over data, and contour labels sit in gaps cut for them
    plain = [t for t in a.texts if t.get_visible() and t.get_text() and t.get_bbox_patch() is None
             and t not in contour_labels and t.get_gid() != "contour-label"]
    panel = a.get_window_extent(renderer)
    for t in plain:
        box = t.get_window_extent(renderer)
        if not _is_value_label(a, t) and not _is_round_panel(a) and isinstance(t, Annotation) and t.xycoords == "data" and not (
                panel.x0 - 1 <= box.x0 and box.x1 <= panel.x1 + 1 and panel.y0 - 1 <= box.y0 and box.y1 <= panel.y1 + 1):
            warnings.warn(f"text {t.get_text()!r} sticks out of panel {a.get_title()!r}; move it")
        corners = [(box.x0, box.y0), (box.x1, box.y0), (box.x1, box.y1), (box.x0, box.y1)]
        for fill in fills:
            if fill.contains_point(((box.x0 + box.x1) / 2, (box.y0 + box.y1) / 2)) and not fill.contains_points(corners).all():
                warnings.warn(f"text {t.get_text()!r} spills out of its fill in panel {a.get_title()!r}; drop or move it")
                break
    # a label anchored on a data point may touch the curve through that point (its own series)
    covers = [(t.get_text(), t.get_window_extent(renderer),
               a.transData.transform(t.xy) if isinstance(t, Annotation) and t.xycoords == "data" else None) for t in plain]
    if a.get_legend():
        covers.append(("the legend", a.get_legend().get_window_extent(renderer), None))
    for name, box, anchor in covers:
        others = [c for c in curves if anchor is None or np.hypot(*(c.vertices - anchor).T).min() > 2]
        if any(curve.intersects_bbox(box, filled=False) for curve in others):
            warnings.warn(f"{name} covers a curve in panel {a.get_title()!r}; move it")
        elif any(box.contains(x, y) for xy in points for x, y in xy):
            warnings.warn(f"{name} covers data points in panel {a.get_title()!r}; move it")


def _warn_legend_over_data(a, fills, renderer):
    """An inside legend that sticks out of its panel, or covers text, filled marks or a bar's end."""
    box, panel = a.get_legend().get_window_extent(renderer), a.get_window_extent(renderer)
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
    if any(_bar_value_edge(bar, c.orientation, renderer).overlaps(box)
           for c in a.containers if isinstance(c, BarContainer) for bar in c.patches):
        warnings.warn(f"the legend covers the end of a bar in panel {a.get_title()!r}; move it")


def _bar_value_edge(bar, orientation, renderer):
    """The edge of a bar at its value, as a thin box: the top (bottom when negative) of a vertical
    bar, the right (left) end of a horizontal one."""
    box, value = bar.get_window_extent(renderer), (bar.get_height() if orientation == "vertical" else bar.get_width())
    if orientation == "vertical":
        y = box.y1 if value >= 0 else box.y0
        return Bbox([[box.x0, y - 0.5], [box.x1, y + 0.5]])
    x = box.x1 if value >= 0 else box.x0
    return Bbox([[x - 0.5, box.y0], [x + 0.5, box.y1]])


def _polygon_area(xy):
    x, y = xy[:, 0], xy[:, 1]
    return abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2


def _warn_legends_wider_than_figure(fig):
    fig.draw_without_rendering()
    room = fig.bbox.width - 2 * design.canvas_pad * fig.dpi
    for legend in fig.legends + [a.get_legend() for a in fig.axes if a.get_legend()]:
        if legend.get_window_extent().width > room:
            n, ncol = len(legend.get_texts()), legend._ncols
            fewer = [math.ceil(n / k) for k in range(2, n + 1) if math.ceil(n / k) < ncol]
            fix = f"use ncol={fewer[0]}" if fewer else "shorten its entries"
            warnings.warn(f"a legend of {n} entries in {ncol} columns is wider than the figure; {fix}")


def _warn_grayscale_lookalikes(a):
    """Series told apart by color alone (lines of one style and marker, or bars) must differ in lightness,
    or they merge when printed in black and white."""
    groups = {}
    for line in a.get_lines():
        if not line.get_label().startswith("_"):
            key = ("line", str(line.get_linestyle()), str(line.get_marker()))
            groups.setdefault(key, []).append((line.get_label(), line.get_color()))
    for c in a.containers:
        if isinstance(c, BarContainer) and c.patches and not str(c.get_label()).startswith("_"):
            groups.setdefault(("bar",), []).append((c.get_label(), palette._over_white(c.patches[0].get_facecolor())))
    # histograms (step outlines or filled shapes) and labelled bands, translucent fills as seen over white
    for p in a.patches:
        label = p.get_label() or ""
        if not isinstance(p, Rectangle) and label and not label.startswith("_"):
            color = palette._over_white(p.get_facecolor()) if p.get_fill() else p.get_edgecolor()
            groups.setdefault(("fill",), []).append((label, color))
    for c in a.collections:
        label = c.get_label() or ""
        if isinstance(c, PolyCollection) and label and not label.startswith("_") and len(c.get_facecolor()):
            groups.setdefault(("fill",), []).append((label, palette._over_white(c.get_facecolor()[0])))
    for series in groups.values():
        for i in range(len(series)):
            for j in range(i + 1, len(series)):
                (n1, c1), (n2, c2) = series[i], series[j]
                if abs(palette._lightness(c1) - palette._lightness(c2)) < 10:
                    warnings.warn(f"series {n1!r} and {n2!r} look alike in grayscale in panel {a.get_title()!r} "
                                  f"(L* {palette._lightness(c1):.0f} vs {palette._lightness(c2):.0f}); use baseline_greys(n), or tell them "
                                  "apart by line style or marker (DESIGN.md Colors)")
