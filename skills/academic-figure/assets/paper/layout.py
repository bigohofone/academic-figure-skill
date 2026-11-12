"""Sizes: finalize_figure sets each figure's height, the standard margins and panel widths, and where legends
and labels sit."""
import warnings

import numpy as np
from matplotlib import rcParams
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.legend import Legend
from matplotlib.transforms import Bbox
from matplotlib.text import Annotation
from matplotlib.ticker import AutoLocator, FixedLocator, FuncFormatter, LogFormatterSciNotation, MaxNLocator, NullFormatter, ScalarFormatter

from . import design, checks


def _panel_size(a, original=False):
    """Panel width and height in inches; a panel's position is relative to its subfigure, if any."""
    box = a.get_position(original=original).transformed(a.figure.transSubfigure)
    return box.width / a.figure.dpi, box.height / a.figure.dpi


def _measure_panels(fig, panels):
    """Each panel's height / width and width. NaN ratios when the layout collapsed at this height:
    matplotlib then leaves the panels where they were, so their sizes mean nothing."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fig.canvas.draw()
    sizes = [_panel_size(a) for a in panels]
    if any("constrained_layout not applied" in str(w.message) for w in caught):
        return [np.nan] * len(panels), [w for w, _ in sizes]
    for w in caught:
        warnings.warn_explicit(w.message, w.category, w.filename, w.lineno)
    return [h / w for w, h in sizes], [w for w, _ in sizes]


def _fit_height_to_aspect(fig, panels, aspect, iters, tol):
    h0 = fig.get_figheight()
    ratios, widths = _measure_panels(fig, panels)
    for _ in range(6):  # the start is too short for the decorations: grow until the layout stands
        if np.isfinite(ratios[0]):
            break
        h0 *= 2
        fig.set_figheight(h0)
        ratios, widths = _measure_panels(fig, panels)
    if not np.isfinite(ratios[0]):
        warnings.warn("the layout collapses at any height: the panels are too narrow for their labels and "
                      "legend; use one column fewer or a wider figure")
        return ratios, widths
    r0 = ratios[0]
    h1 = h0 * aspect / r0
    for _ in range(iters):
        fig.set_figheight(h1)
        ratios, widths = _measure_panels(fig, panels)
        r1 = ratios[0]
        if not np.isfinite(r1) or r1 <= 0:
            # too short for the decorations (titles, outside legends): the layout collapsed
            h0, r0, h1 = h1, r0, 2 * h1
            continue
        if abs(r1 - aspect) / aspect < tol or r1 == r0:
            break
        step = h1 + (aspect - r1) * (h1 - h0) / (r1 - r0)
        # a secant step can overshoot below zero while the layout is still settling: halve instead; on a
        # nearly flat ratio (a legend wider than its panel) it can shoot far up: at most four times taller
        h0, r0, h1 = h1, r1, min(step, 4 * h1) if np.isfinite(step) and step > 0 else h1 / 2
    return ratios, widths


def _set_canvas_pad(fig):
    """Free space on all four sides of the canvas, for text that reaches past the panels."""
    if isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        # left and right as a rect; top and bottom as the layout's edge pad, which outside legends obey too
        x = design.canvas_pad / fig.get_figwidth()
        fig.get_layout_engine().set(rect=(x, 0, 1 - 2 * x, 1), h_pad=design.canvas_pad)


def _freeze_ticks(panels):
    """Fix the ticks where they are now; the locator they came from is kept for `_unfreeze_ticks`."""
    for a in panels:
        for axis in (a.xaxis, a.yaxis):
            if not hasattr(axis, "_auto_locator"):
                axis._auto_locator = axis.get_major_locator()
            lo, hi = sorted(axis.get_view_interval())
            axis.set_major_locator(FixedLocator([t for t in axis.get_majorticklocs() if lo <= t <= hi]))


def _unfreeze_ticks(panels):
    for a in panels:
        for axis in (a.xaxis, a.yaxis):
            if hasattr(axis, "_auto_locator"):
                axis.set_major_locator(axis._auto_locator)


def _limit_leaving_room(axis, lo, hi, v, reach, size, upper):
    """The new upper (or lower) limit that leaves `reach` pixels between value `v` and the panel edge,
    solved in the axis's scale (linear, log), where data maps linearly to pixels."""
    scale = axis.get_transform()
    lo, hi, v = scale.transform([lo, hi, v])
    limit = lo + (v - lo) * size / (size - reach) if upper else (v * size - reach * hi) / (size - reach)
    return scale.inverted().transform([limit])[0]


def _keep_value_labels_inside(fig, panels):
    """Grow each panel's limits so every `mark_value` label, bar label (`ax.bar_label`) and point name
    (an annotation in data coordinates) lies inside its panel. `mark_value` labels at a side edge
    turn inward instead. A point name gets at most a quarter more axis range; one that needs more
    is left out and reported, to be moved. Returns whether any limits changed."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    changed = False
    for a in panels:
        if checks._is_round_panel(a):
            continue
        box = a.get_window_extent(renderer)
        for t in a.texts:
            from_mark_value = t.get_gid() == "value-mark"  # these turn inward at a side edge
            value_label = checks._is_value_label(a, t)
            point_name = not value_label and isinstance(t, Annotation) and t.xycoords == "data"
            if not (value_label or point_name):
                continue
            label = t.get_window_extent(renderer)
            gap = 0.35 * t.get_fontsize() * fig.dpi / 72  # clear space between a label and the panel edge
            # a label's reach past its point is fixed in pixels, so solve for the limit
            # that leaves exactly that much room between the point and the box
            x, y = t.xy if isinstance(t, Annotation) else t.get_position()
            point_x, point_y = a.transData.transform((x, y))
            for axis, low_edge, high_edge, v, point, size, set_lim, get_lim in (
                    (a.xaxis, label.x0 < box.x0 + gap, label.x1 > box.x1 - gap, x, point_x, box.width, a.set_xlim, a.get_xlim),
                    (a.yaxis, label.y0 < box.y0 + gap, label.y1 > box.y1 - gap, y, point_y, box.height, a.set_ylim, a.get_ylim)):
                if not (low_edge or high_edge):
                    continue
                if from_mark_value and axis is a.xaxis:
                    t.set_ha("left" if low_edge else "right")
                    continue
                lo, hi = get_lim()
                if high_edge:
                    reach = (label.x1 if axis is a.xaxis else label.y1) - point + gap
                    new = (lo, _limit_leaving_room(axis, lo, hi, v, reach, size, True))
                else:
                    reach = point - (label.x0 if axis is a.xaxis else label.y0) + gap
                    new = (_limit_leaving_room(axis, lo, hi, v, reach, size, False), hi)
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


HEATMAP_MIN_SIZE = 4  # points: smaller cell values are dropped instead (DESIGN.md Collisions step 4)


def _fit_heatmap_values(fig, panels):
    """Every row and column of a heatmap is named and every cell's value written, so they all fit their
    cells: the cell values take one size, the largest (up to the value-label size) at which each fits its
    cell; the row and column names one size (up to the tick-label size) at which they clear each other.
    Never below HEATMAP_MIN_SIZE."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    heatmaps = [a for a in panels if a.images]
    space = 0.7 * fig.dpi / 72  # the word space checks._texts_overlap asks between neighbours, per point of size
    names_fit = rcParams["xtick.labelsize"]
    for a in heatmaps:
        rows, cols = a.images[0].get_array().shape[:2]
        panel = a.get_window_extent(renderer)
        cell_w, cell_h = panel.width / cols, panel.height / rows
        cells = [t for t in a.texts if t.get_ha() == "center" and t.get_va() == "center" and t.get_visible() and t.get_text()]
        if cells:
            size = rcParams["font.size"]
            for t in cells:
                t.set_fontsize(size)
            boxes = [t.get_window_extent(renderer) for t in cells]
            fit = min(min(0.9 * cell_w * size / b.width, 0.8 * cell_h * size / b.height) for b in boxes)
            for t in cells:
                t.set_fontsize(max(HEATMAP_MIN_SIZE, min(size, fit)))
                t._in_cell = True
        for axis, along in ((a.xaxis, cell_w), (a.yaxis, cell_h)):
            names = [t for t in axis.get_ticklabels() if t.get_visible() and t.get_text()]
            for t in names:
                size = t.get_fontsize()
                box = t.get_window_extent(renderer)
                need = box.width / size + space if axis is a.xaxis else box.height / size
                names_fit = min(names_fit, along / need)
    if heatmaps:
        for a in heatmaps:
            for axis in (a.xaxis, a.yaxis):
                axis.set_tick_params(labelsize=max(HEATMAP_MIN_SIZE, names_fit))


def _turn_crowded_bar_labels(fig, panels):
    """Bar values written side by side that overlap all turn upward, in every panel where any two do."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for a in panels:
        anchors = checks._bar_label_anchors(a)
        labels = [t for t in a.texts if isinstance(t, Annotation) and t.get_rotation() == 0 and len(anchors)
                  and bool(np.isclose(anchors, t.xy).all(axis=1).any()) and t.get_va() in ("bottom", "top")]
        boxes = [t.get_window_extent(renderer) for t in labels]
        if any(checks._texts_overlap(labels[i], boxes[i], labels[j], boxes[j], renderer)
               for i in range(len(labels)) for j in range(i + 1, len(labels))):
            for t in labels:
                t.set_rotation(90)
                t.xyann = (0, 2 if t.get_va() == "bottom" else -2)


INSIDE_SPOTS = ["upper left", "upper right", "lower left", "lower right",
                "upper center", "lower center", "center left", "center right"]


def _clear_spot(fig, a, legend, panels, renderer):
    """Put the legend at the first inside spot of panel `a` where it hides nothing; whether one was found.
    The legend is marked as placed here, so `_recheck_legends` can move it again at the final size."""
    legend._placed_inside = True
    for spot in INSIDE_SPOTS:
        legend.set_loc(spot)
        if not checks._legend_problems(fig, a, panels, renderer):
            return True
    return False


def _recheck_legends(fig, panels):
    """Panels change size a little when they are put on the standard box: a legend placed inside earlier
    may now touch data; look again for a clear spot in its panel, else put it above. Returns whether
    any went above (the panels then need placing again)."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    above = False
    for a in panels:
        legend = a.get_legend()
        if legend is None or not getattr(legend, "_placed_inside", False) or not checks._legend_problems(fig, a, panels, renderer):
            continue
        if not _clear_spot(fig, a, legend, panels, renderer):
            handles, labels, layout = _legend_entries(legend)
            legend.remove()
            if not _place_inside(fig, [a], handles, labels, panels, renderer, layout):
                _legend_above(fig, a, handles, labels, several=len(panels) > 1, layout=layout)
                above = True
    return above


def _legend_entries(legend):
    """A legend's handles and labels in the order it was made, and its layout (columns, spacing) when its
    rows are set (`legend_rows`), else None."""
    if hasattr(legend, "_entries"):
        return legend._entries
    return legend.legend_handles, [t.get_text() for t in legend.get_texts()], None


def _place_inside(fig, candidates, handles, labels, panels, renderer, layout=None):
    """Put the legend inside the first of `candidates` with a spot where it hides nothing: at the legend
    size in every candidate first, then at the smaller legend-inside size. Whether it found one."""
    for size in (rcParams["legend.fontsize"], design.legend_inside_size):
        for a in candidates:
            legend = a.legend(handles, labels, fontsize=size, **(layout or {}))
            if layout:
                legend._entries = (handles, labels, layout)
            if _clear_spot(fig, a, legend, panels, renderer):
                return True
            legend.remove()
    return False


def _legend_above(fig, a, handles, labels, several, layout=None):
    """A legend above the panels, in as few rows as fit the figure's width (or in its set rows, `layout`).
    Above several panels it is the figure's legend: an axes legend that wide would count as part of its one
    panel and collapse the layout."""
    room = fig.get_figwidth() * fig.dpi - 2 * design.canvas_pad * fig.dpi
    fixed = layout is not None
    style = {k: v for k, v in (layout or {}).items() if k != "ncols"}
    for ncols in [layout["ncols"]] if fixed else range(len(labels), 0, -1):
        # matplotlib fills a legend column by column; reorder so its rows read left to right in entry order
        # (set rows come in matplotlib's order already)
        order = list(range(len(labels))) if fixed else [i for c in range(ncols) for i in range(c, len(labels), ncols)]
        h, l = [handles[i] for i in order], [labels[i] for i in order]
        if several:
            legend = fig.legend(h, l, loc="outside upper center", ncols=ncols, borderaxespad=0, **style)
        else:
            legend = a.legend(h, l, loc="lower center", bbox_to_anchor=(0.5, 1), ncols=ncols, borderaxespad=0.5, **style)
        if fixed or ncols == 1 or legend.get_window_extent(fig.canvas.get_renderer()).width <= room:
            return
        legend.remove()


def _lift_legends_wider_than_panel(fig, panels):
    """A panel legend made without `loc` that is wider than its panel can never go inside it, and while it
    stays there matplotlib's layout collapses: it goes above the panels at once."""
    renderer = fig.canvas.get_renderer()
    for a in panels:
        legend = a.get_legend()
        if legend is None or legend._loc != Legend.codes["best"]:
            continue
        if legend.get_window_extent(renderer).width > a.get_position().width * fig.bbox.width:
            handles, labels, layout = _legend_entries(legend)
            legend.remove()
            _legend_above(fig, a, handles, labels, several=len(panels) > 1, layout=layout)


def _place_legends(fig, panels):
    """A panel legend made without `loc` names series that may run through every panel, so it goes
    inside the first panel, starting with its own, that has a spot where it hides nothing (at the legend
    size, then the smaller legend-inside size); the other panels carry none. Where no panel has room even
    then, it goes above its own panel at the legend size. Returns
    whether any went above."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    above = False
    for a in panels:
        legend = a.get_legend()
        if legend is None or legend._loc != Legend.codes["best"]:
            continue
        handles, labels, layout = _legend_entries(legend)
        legend.remove()
        candidates = [a, *[o for o in panels if o is not a and o.get_legend() is None]]
        if not _place_inside(fig, candidates, handles, labels, panels, renderer, layout):
            _legend_above(fig, a, handles, labels, several=len(panels) > 1, layout=layout)
            above = True
    return above


def _standard_y_widths(fig):
    """The standard widths, in inches, of the y decorations: four-character tick labels with a sign
    and their pads, and one line of the axis label with its pad."""
    renderer = fig.canvas.get_renderer()
    sample = fig.text(0, 0, "\u22120.00", fontsize=rcParams["ytick.labelsize"])  # four characters and a sign: −0.75, 1000, 100%
    text = sample.get_window_extent(renderer).width / fig.dpi
    sample.remove()
    ticks = text + (rcParams["ytick.major.pad"] + rcParams["ytick.major.size"]) / 72
    label = (rcParams["axes.labelsize"] * 1.35 + rcParams["axes.labelpad"]) / 72  # rotated, with room for (, β, _
    return ticks, label, text / 2


def _standard_side_margins(fig):
    """The left and right margins, in inches, of a standard panel: on the left a y-axis label and
    four-character tick labels with a sign, on the right half of one at the x axis' end."""
    ticks, label, half = _standard_y_widths(fig)
    return design.canvas_pad + label + ticks, design.canvas_pad + half


def set_group_label(axes, text, axis="x"):
    """One axis label for a group of panels: `axis="x"` under the group's columns (pass its bottom
    panels), `axis="y"` beside its rows (pass its left panels). The label sits on the first panel and
    `finalize_figure` centres it on the group once the panels are placed."""
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


def _y_decoration_width(axes, side="left"):
    """How far, in inches, the y tick labels and y label of these axes reach out from their panels on
    `side`; 0 when they show none."""
    renderer = axes[0].figure.canvas.get_renderer()
    widths = [0.0]
    for a in axes:
        if not any(t.get_visible() and t.get_text() for t in a.get_yticklabels()) and not a.yaxis.label.get_text():
            continue
        box, panel = a.yaxis.get_tightbbox(renderer), a.get_window_extent(renderer)
        if box is not None:
            widths.append((panel.x0 - box.x0 if side == "left" else box.x1 - panel.x1) / a.figure.dpi)
    return max(widths)


def _x_end_clearance(left_column, right_column):
    """The gap, in inches, that keeps the last x tick label of the panels on the left half an em clear of
    the first one of the panels on the right, so "2000" and "0" never read as "20000"."""
    renderer = left_column[0].figure.canvas.get_renderer()

    def end_label(a, last):
        lo, hi = sorted(a.xaxis.get_view_interval())
        shown = [(loc, t) for loc, t in zip(a.xaxis.get_majorticklocs(), a.xaxis.get_majorticklabels())
                 if lo <= loc <= hi and t.get_visible() and t.get_text()]
        return (max if last else min)(shown, key=lambda p: p[0])[1] if shown else None

    def reach(a, last):
        label = end_label(a, last)
        if label is None:
            return 0.0
        box, panel = label.get_window_extent(renderer), a.get_window_extent(renderer)
        return max(0.0, (box.x1 - panel.x1) if last else (panel.x0 - box.x0)) / a.figure.dpi

    half_em = rcParams["xtick.labelsize"] / 72 / 2
    return max(reach(a, True) for a in left_column) + max(reach(a, False) for a in right_column) + half_em


def _colorbar_end_clearance(left_bar, right_bar):
    """The gap, in inches, that keeps two colorbars side by side clear at their facing ends: their ticks are
    laid out again at the final length, so a tick may land on either end, its label centered there; half the
    widest tick label of each, and half an em between."""
    renderer = left_bar.figure.canvas.get_renderer()
    half_widest = [max((t.get_window_extent(renderer).width for t in bar.get_xticklabels() if t.get_text()), default=0) / 2
                   for bar in (left_bar, right_bar)]
    return sum(half_widest) / left_bar.figure.dpi + rcParams["xtick.labelsize"] / 72 / 2


def _standard_column_gap(fig, column, column_gap, starts_group):
    """The gap before a grid column: the `panel-gap` token of free space, plus what the column's own y tick
    labels and y label take (`_x_end_clearance` widens it where x end labels would touch). A column that
    starts a new group begins as if a new figure began there: the standard right and left margins, plus the
    column gap in a figure spanning both text columns (`column_gap` > 0), so its panels line up with the
    single-column figures above and below. New groups: each sub-figure, and in a figure spanning both text
    columns, a column with its own y label (`starts_group`)."""
    ticks, label, half = _standard_y_widths(fig)
    label_lines = max(_line_count(a.yaxis.label) for a in column)
    if starts_group:
        return (design.canvas_pad + half) + column_gap + (design.canvas_pad + ticks + label * label_lines)
    return design.panel_gap + _y_decoration_width(column)


def _x_tick_height(fig):
    """x tick labels with their pad and tick mark, in inches."""
    sample = fig.text(0, 0, "0", fontsize=rcParams["xtick.labelsize"])
    height = sample.get_window_extent(fig.canvas.get_renderer()).height / fig.dpi
    sample.remove()
    return height + (rcParams["xtick.major.pad"] + rcParams["xtick.major.size"]) / 72


def _half_tick_label_height(fig):
    """Half a tick label: how far the top y tick label reaches above its panel."""
    return (_x_tick_height(fig) - (rcParams["xtick.major.pad"] + rcParams["xtick.major.size"]) / 72) / 2


def _title_line_height():
    return (rcParams["axes.titlesize"] * 1.35 + rcParams["axes.titlepad"]) / 72


def _line_count(text):
    return text.get_text().count("\n") + 1 if text.get_text() else 0


def _subfigures_to_groups(fig):
    """Sub-figures side by side become groups of panels on the figure's own grid: each is stretched,
    transparent, over the whole figure, so its panels' positions are figure positions, and the panels stay
    where the layout put them. Returns each panel's group (0 without sub-figures)."""
    if not fig.subfigs:
        return {a: 0 for a in fig.axes}
    fig.canvas.draw()
    to_figure = fig.transFigure.inverted()
    boxes = {a: a.get_window_extent().transformed(to_figure) for a in fig.axes}
    group = {a: i for i, sf in enumerate(fig.subfigs) for a in sf.axes}
    fig.set_layout_engine("none")
    for sf in fig.subfigs:
        sf._redo_transform_rel_fig(bbox=Bbox.unit())
        sf.patch.set_visible(False)
    for a, box in boxes.items():
        a.set_position(box)
    return group


def _place_on_standard_box(fig, panels, aspect, column_gap):
    """Panels sit at the standard margins and take the standard size, so the boxes of all figures at
    one width (and one number of columns) line up and match. The right margin is fixed; left labels
    that need more room widen the left margin and narrow the panels, which keep the standard height
    (the aspect gives way). The gaps between columns are standard (`_standard_column_gap`); the gaps between rows stay as the layout
    found them; the columns share what is left.
    One colorbar is kept beside the panels (right) or under them (bottom), its labels inside a standard
    margin of their own; several colorbars stand one beside each column of panels, each with the room its
    labels take before the next column, or one under each column of a single row, their end labels apart. Returns whether they moved."""
    cbars = [a for a in fig.axes if getattr(a, "_colorbar", None) is not None]
    others = [a for a in fig.axes if a not in panels and a not in cbars]
    twin_of = {t: p for t in others for p in panels
               if np.allclose(t.get_position().bounds, p.get_position().bounds)}  # ax.twinx(): a right y axis
    nested = any(sf.subfigs for sf in fig.subfigs)
    stacked = len({round(sf.bbox_relative.y0, 3) for sf in fig.subfigs}) > 1
    owned = (all(getattr(c._colorbar.mappable, "axes", None) in panels for c in cbars)
             and len({c._colorbar.orientation for c in cbars}) == 1)
    if (nested or stacked or (fig.subfigs and cbars) or (len(cbars) > 1 and not owned) or len(twin_of) != len(others)
            or checks._is_round_panel(panels[0])):
        return False
    group = _subfigures_to_groups(fig)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    w, h = fig.get_size_inches()
    boxes = {a: a.get_position() for a in panels}
    columns = sorted({round(b.x0 * w, 2) for b in boxes.values()})
    col_of = {a: columns.index(round(b.x0 * w, 2)) for a, b in boxes.items()}
    # rows counted in each group: sub-figures lay out their rows apart
    group_rows = {g: sorted({round(boxes[a].y0 * h, 2) for a in panels if group[a] == g}, reverse=True)
                  for g in set(group[a] for a in panels)}
    row_of = {a: group_rows[group[a]].index(round(b.y0 * h, 2)) for a, b in boxes.items()}
    rows = range(max(row_of.values()) + 1)
    column_cbar = {col_of[c._colorbar.mappable.axes]: c for c in cbars} if len(cbars) > 1 else {}
    if len(cbars) > 1 and len(column_cbar) < len(cbars):
        return False  # two colorbars for one column
    vertical_bars = bool(cbars) and cbars[0]._colorbar.orientation == "vertical"
    beside = column_cbar if vertical_bars else {}
    under = {} if vertical_bars else column_cbar
    if under and len(rows) > 1:
        return False
    first_column = [a for a in panels if col_of[a] == 0]
    if not any(a.yaxis.label.get_text() or any(t.get_visible() and t.get_text() for t in a.get_yticklabels())
               for a in first_column):
        return False  # no y labels to align (an embedding): the layout centres the panel
    left, right = _standard_side_margins(fig)
    side = left - design.canvas_pad  # an axis label and four-character tick labels
    pad = design.canvas_pad
    cbar = cbars[0] if len(cbars) == 1 else None
    vertical = cbar is not None and cbar._colorbar.orientation == "vertical"
    cb_gap, cb_w = design.colorbar_gap, design.colorbar_width
    # the right margin never moves, so every figure's right edge lines up; a left label that needs
    # more room takes it from the panels' width, never their height, so one width keeps one height
    # a colorbar's labels take the standard margin, or what they need when wider ("0.945"), so the canvas pad stays clear
    last_cbar = cbar if vertical else beside.get(len(columns) - 1)
    if last_cbar is not None:
        right = pad + max(side, _y_decoration_width([last_cbar], "right")) + cb_w + cb_gap
    std_left, std_right = left, right
    ticks, label, half = _standard_y_widths(fig)
    for a, b in boxes.items():
        if col_of[a] == 0:
            left = max(left, b.x0 * w - a.get_tightbbox(renderer).x0 / fig.dpi + pad)
    sup_y = fig._supylabel if fig._supylabel and fig._supylabel.get_text() else None
    if sup_y:
        left += label
    # a right y axis mirrors the left one: its tick labels and label take room from the panels' width
    right_column = {col_of[p] for p in twin_of.values()}
    right_axis = ticks + label * max((_line_count(t.yaxis.label) for t in twin_of), default=0)
    if len(columns) - 1 in right_column and not vertical:
        right = pad + right_axis
    # inside the grid, a right y axis takes only what it shows (none when its tick labels are hidden)
    group_of_column = {col_of[a]: group[a] for a in panels}
    column_panels = {c: [a for a in panels if col_of[a] == c] for c in range(len(columns))}
    starts_group = {c: group_of_column[c] != group_of_column[c - 1]
                    or bool(column_gap and any(a.yaxis.label.get_text() for a in column_panels[c]))
                    for c in range(1, len(columns))}
    col_gaps = [max(_standard_column_gap(fig, column_panels[c], column_gap, starts_group[c])
                    + (_y_decoration_width([t for t, p in twin_of.items() if col_of[p] == c - 1], "right") if c - 1 in right_column else 0)
                    + (cb_gap + cb_w + _y_decoration_width([beside[c - 1]], "right") if c - 1 in beside else 0),
                    _x_end_clearance([a for a in panels if col_of[a] == c - 1], [a for a in panels if col_of[a] == c]),
                    _colorbar_end_clearance(under[c - 1], under[c]) if c in under and c - 1 in under else 0)
                for c in range(1, len(columns))]
    # rows: above each, half a tick label or a title line; below, x tick labels and x label lines;
    # anything more (a legend above a panel, a second line, turned labels) widens that margin
    above, below = [], []
    # a y label set for a group of rows is centred on their whole span (gaps included), so it is no row's own
    # margin: measured with its first row, it would widen the gap it is then centred on
    group_y_labels = [axes[0].yaxis.label for axes, axis in getattr(fig, "_group_labels", []) if axis == "y"]
    for t in group_y_labels:
        t.set_visible(False)
    for r in range(len(rows)):
        row = [a for a in panels if row_of[a] == r]
        tight = [Bbox.union([a.get_tightbbox(renderer)] + [t.get_tightbbox(renderer) for t, p in twin_of.items() if p is a])
                 for a in row]
        y0, y1 = boxes[row[0]].y0 * h, boxes[row[0]].y1 * h
        std_above = max(_half_tick_label_height(fig), max(_line_count(a.title) for a in row) * _title_line_height())
        std_below = (_x_tick_height(fig) * any(t.label1.get_visible() and t.label1.get_text()
                                             for a in row for t in a.xaxis.get_major_ticks())
                     + label * max(_line_count(a.xaxis.label) for a in row))
        above.append(max(std_above, max(b.y1 for b in tight) / fig.dpi - y1))
        below.append(max(std_below, y0 - min(b.y0 for b in tight) / fig.dpi))
    for t in group_y_labels:
        t.set_visible(True)
    row_gaps = [below[r] + above[r + 1] for r in range(len(rows) - 1)]
    # a legend made "outside upper" belongs above the panels even while it is still drawn over them
    top_legends = [lg for lg in fig.legends if getattr(lg, "_outside_loc", None) == "upper"
                   or lg.get_window_extent(renderer).y0 / fig.dpi >= max(b.y1 for b in boxes.values()) * h - 1e-3]
    legend_h = sum(lg.get_window_extent(renderer).height / fig.dpi for lg in top_legends)
    # a sub-figure's legend stands above its own group, under the figure's legends
    group_legends = {g: list(sf.legends) for g, sf in enumerate(fig.subfigs) if sf.legends}
    group_legend_h = max((sum(lg.get_window_extent(renderer).height / fig.dpi for lg in lgs) for lgs in group_legends.values()), default=0)
    top = pad + legend_h + group_legend_h + above[0]
    sup_x = fig._supxlabel if fig._supxlabel and fig._supxlabel.get_text() else None
    subcaptions = {g: sf._supxlabel for g, sf in enumerate(fig.subfigs) if sf._supxlabel and sf._supxlabel.get_text()}
    caption_lines = max(_line_count(t) for t in [*subcaptions.values(), sup_x] if t) if sup_x or subcaptions else 0
    bottom = pad + below[-1] + label * caption_lines
    if (cbar is not None and not vertical) or under:
        # a colorbar under the panels (or one under each column): as thick as one beside them, the colorbar gap
        # under the x labels; its own tick labels and label keep the room the layout gave them below it
        cb_bottom, cb_h = min(c.get_position().y0 for c in cbars) * h, design.colorbar_width
        bottom = cb_bottom + cb_h + design.colorbar_gap + below[-1]
    n = len(columns)
    panel_h = aspect * (w - std_left - std_right - sum(col_gaps)) / n
    # each column's left edge and width; a group starting halfway across a figure spanning both text columns
    # starts exactly where a single-column figure in the second text column does, and the group before it ends
    # where one in the first ends, so wider left labels narrow only the panels of their own half
    mid = n // 2
    halves = column_gap and not vertical and not column_cbar and n % 2 == 0 and n > 1 and starts_group[mid]
    if halves:
        half = (w - column_gap) / 2
        second = half + col_gaps[mid - 1] - std_right
        spans = [(left, half - std_right, range(mid)), (second, w - right, range(mid, n))]
    else:
        spans = [(left, w - right, range(n))]
    col_x, col_w = {}, {}
    for x, end, cols in spans:
        width = (end - x - sum(col_gaps[c - 1] for c in cols if c != cols[0])) / len(cols)
        for c in cols:
            col_x[c], col_w[c] = x, width
            x += width + (col_gaps[c] if c < n - 1 else 0)
    row_h = [panel_h] * len(rows)
    new_h = bottom + top + sum(row_h) + sum(row_gaps)
    fig.set_layout_engine("none")
    fig.set_figheight(new_h)
    for a in panels:
        c, r = col_of[a], row_of[a]
        y0 = bottom + sum(row_h[r + 1:]) + sum(row_gaps[r:])
        a.set_position([col_x[c] / w, y0 / new_h, col_w[c] / w, row_h[r] / new_h])
    for t, p in twin_of.items():
        t.set_position(p.get_position())
    for c, cb in beside.items():
        y0 = min(a.get_position().y0 for a in column_panels[c])
        y1 = max(a.get_position().y1 for a in column_panels[c])
        cb.set_position([(col_x[c] + col_w[c] + cb_gap) / w, y0, cb_w / w, y1 - y0])
    for c, cb in under.items():
        cb.set_position([col_x[c] / w, cb_bottom / new_h, col_w[c] / w, cb_h / new_h])
    span_w = col_x[n - 1] + col_w[n - 1] - left
    span_h = sum(row_h) + sum(row_gaps)
    if sup_x:
        sup_x.set_x((left + span_w / 2) / w)
        sup_x.set_y(pad / new_h)
        sup_x.set_verticalalignment("bottom")
    for g, caption in subcaptions.items():
        x0 = min(a.get_position().x0 for a in panels if group[a] == g)
        x1 = max(a.get_position().x1 for a in panels if group[a] == g)
        caption.set_x((x0 + x1) / 2)
        caption.set_y(pad / new_h)
        caption.set_verticalalignment("bottom")
    y = new_h - pad
    for lg in top_legends:
        # centred over the panels, but never past the canvas pad: a wide legend shifts toward the figure's middle
        half_w = lg.get_window_extent(renderer).width / fig.dpi / 2
        x = min(max(left + span_w / 2, pad + half_w), w - pad - half_w)
        lg.set_loc("upper center")
        lg.set_bbox_to_anchor((x / w, y / new_h), transform=fig.transFigure)
        y -= lg.get_window_extent(renderer).height / fig.dpi
    for g, lgs in group_legends.items():
        x0 = min(a.get_position().x0 for a in panels if group[a] == g)
        x1 = max(a.get_position().x1 for a in panels if group[a] == g)
        y_group = y
        for lg in lgs:
            lg.set_loc("upper center")
            lg.set_bbox_to_anchor(((x0 + x1) / 2, y_group / new_h), transform=fig.transFigure)
            y_group -= lg.get_window_extent(renderer).height / fig.dpi
    if sup_y:
        sup_y.set_x(pad / w)
        sup_y.set_horizontalalignment("left")
        sup_y.set_y((bottom + span_h / 2) / new_h)
    if vertical:
        cbar.set_position([(left + span_w + cb_gap) / w, bottom / new_h, cb_w / w, span_h / new_h])
    elif cbar is not None:
        cbar.set_position([left / w, cb_bottom / new_h, span_w / w, cb_h / new_h])
    for c in cbars:
        c.set_box_aspect(None)  # placed at their exact size: no cap on their length (`_colorbars_span_panels`)
    return True


def _blank_touching_corner_label(fig, panels):
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
        if checks._texts_overlap(tx, tx.get_window_extent(renderer), ty, ty.get_window_extent(renderer), renderer):
            label = a.yaxis.get_major_formatter()
            a.yaxis.set_major_formatter(FuncFormatter(lambda v, pos, first=loc, label=label: "" if np.isclose(v, first) else label(v, pos)))


def _start_at_zero(panels):
    """A quantity that is never negative never shows negative values: raise a default margin below 0 to 0."""
    for a in panels:
        if checks._is_round_panel(a):
            continue
        lim = a.dataLim
        for get, set_, low, scale in ((a.get_xlim, a.set_xlim, lim.x0, a.get_xscale()),
                                      (a.get_ylim, a.set_ylim, lim.y0, a.get_yscale())):
            lo, hi = get()
            if scale == "linear" and np.isfinite(low) and low > 0 and lo < 0 < hi:
                set_(0, hi)


def _denser_y_ticks(fig):
    """matplotlib's default y ticks, but at least four where the axis has room: rounding the step to
    1, 2, 2.5 or 5 often leaves a short panel with only 0, 200, 400."""
    for a in fig.axes:
        if type(a.yaxis.get_major_locator()) is AutoLocator and a.get_yscale() == "linear":
            a.yaxis.set_major_locator(MaxNLocator(nbins="auto", steps=[1, 2, 2.5, 5, 10], min_n_ticks=4))


def _tick_text(axis):
    """Tick numbers as plain numbers (0, 0.5, 1) with a true minus sign; from 1000 up with an SI suffix,
    one unit for the whole axis, when that writes the ticks shorter (0.5K, 1K, 1.5K, 2K; but 200 ... 1000
    and 1024 stay)."""
    def plain(v):
        return f"{v:.10g}".replace("-", "\u2212")

    def text(v, _):
        ticks = list(axis.get_majorticklocs())
        top = max((abs(t) for t in ticks), default=0)
        for scale, suffix in ((1e9, "B"), (1e6, "M"), (1e3, "K")):
            if top >= scale:
                short = lambda t: "0" if t == 0 else plain(t / scale) + suffix
                if sum(map(len, map(short, ticks))) < sum(map(len, map(plain, ticks))):
                    return short(v)
                break
        return plain(v)
    return text


def _log_tick_text(v, _):
    """A log axis's tick: plain from 0.001 to 1000, an SI suffix above (10K, 1M), 1e−4 below."""
    for scale, suffix in ((1e9, "B"), (1e6, "M"), (1e4, "K")):
        if v >= scale:
            return f"{v / (1e3 if suffix == 'K' else scale):.10g}{suffix}"
    if v >= 1e-3:
        return f"{v:.10g}"
    return f"1e{np.log10(v):.0f}".replace("-", "\u2212") if np.isclose(v, 10 ** np.round(np.log10(v))) else f"{v:.1e}".replace("-", "\u2212")


def _write_plain_tick_numbers(fig):
    """Write matplotlib's default numeric ticks short and plain (`_tick_text`, `_log_tick_text`); a log
    axis's minor ticks stay unlabelled."""
    for a in fig.axes:
        for axis in (a.xaxis, a.yaxis):
            if type(axis.get_major_formatter()) is ScalarFormatter:
                axis.set_major_formatter(FuncFormatter(_tick_text(axis)))
            elif type(axis.get_major_formatter()) is LogFormatterSciNotation:
                axis.set_major_formatter(FuncFormatter(_log_tick_text))
                axis.set_minor_formatter(NullFormatter())


def _pad_outside_legends(fig):
    """The layout puts a figure legend outside the panels flush with the canvas edge; give it the
    canvas pad like everything else, keeping every panel where it is in inches."""
    fig.canvas.draw()
    h = fig.get_figheight()
    tops = [lg for lg in fig.legends if lg.get_window_extent().y1 / fig.dpi > h - design.canvas_pad]
    if not tops:
        return
    need = max(design.canvas_pad - (h - lg.get_window_extent().y1 / fig.dpi) for lg in tops)
    boxes = {a: a.get_position() for a in fig.axes}
    centers = {lg: (lg.get_window_extent().x0 + lg.get_window_extent().x1) / 2 / fig.bbox.width for lg in tops}
    fig.set_layout_engine("none")
    fig.set_figheight(h + need)
    for a, b in boxes.items():
        a.set_position([b.x0, b.y0 * h / (h + need), b.width, b.height * h / (h + need)])
    for lg in tops:
        lg.set_loc("upper center")
        lg.set_bbox_to_anchor((centers[lg], 1 - design.canvas_pad / (h + need)), transform=fig.transFigure)


def _trim_round_panel_height(fig, panels):
    """A round panel (pie, polar) is always a circle, as large as its slot allows. Start tall so the
    figure width sets its size, then cut the empty height of its slot above and below it."""
    fig.set_figheight(3 * fig.get_figwidth())
    for _ in range(10):
        fig.canvas.draw()
        rows = {}
        for a in panels:
            row = round(a.get_position(original=True).transformed(a.figure.transSubfigure).y0)
            rows[row] = min(rows.get(row, np.inf), _panel_size(a, original=True)[1] - _panel_size(a)[1])
        empty = sum(rows.values())
        if empty < 0.005:
            break
        fig.set_figheight(fig.get_figheight() - empty)


def _colorbars_span_panels(fig):
    """Each colorbar runs the full height (or width) of the panels it belongs to, at the thickness the layout
    made room for. matplotlib caps its length at 20 times its thickness and constrained layout sets that cap
    again at every draw, so the layout is fixed first."""
    cbars = [a for a in fig.axes if getattr(a, "_colorbar", None) is not None]
    if not cbars:
        return
    fig.canvas.draw()
    fig.set_layout_engine("none")
    for a in cbars:
        drawn, slot = a.get_position(), a.get_position(original=True)
        a.set_box_aspect(None)
        if a._colorbar.orientation == "vertical":
            a.set_position([drawn.x0, slot.y0, drawn.width, slot.height])
        else:
            a.set_position([slot.x0, drawn.y0, slot.width, drawn.height])


def _default_aspect(fig, panels):
    """DESIGN.md Panel aspect, by the width each panel gets (figure width / columns): narrow panels
    square, a column's width at φ : 1, wider two golden rectangles side by side."""
    columns = len({round(a.get_position().x0, 3) for a in panels})
    slot = fig.get_figwidth() / columns
    return 1.0 if slot < 2.5 else 0.618 if slot <= 3.5 else 0.309


def finalize_figure(fig, ax, aspect=None, iters=10, tol=0.005, min_width=0.9, column_gap=0):
    """Change only the figure height so each panel's height / width equals `aspect`; without
    one, the panel width picks it (DESIGN.md Panel aspect).

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

    Bar values side by side that overlap all turn upward (rotation 90), panel by panel.

    A panel legend made without `loc` is placed here: the first spot of `INSIDE_SPOTS` where it
    hides no data or text, else above its panel in one row.

    Last, it warns about what reads badly in print: a panel narrower than `min_width` (0.9 in; a
    two-factor grid passes 0.7, small multiples 0.45); text cut off at the
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
    _write_plain_tick_numbers(fig)
    _denser_y_ticks(fig)
    _start_at_zero(panels)
    if isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        _set_canvas_pad(fig)
    checks._warn_legends_wider_than_figure(fig)
    _lift_legends_wider_than_panel(fig, panels)
    if any(checks._is_round_panel(a) for a in panels):
        _trim_round_panel_height(fig, panels)
        _pad_outside_legends(fig)
        checks._warn_hard_to_read(fig, panels, min_width)
        return _measure_panels(fig, panels)[0]
    for a in panels:
        if a.get_aspect() != "auto" or a.get_box_aspect() is not None:
            raise ValueError(
                f"panel {a.get_title()!r} has a fixed aspect, so the figure height cannot set "
                "its ratio; use aspect='auto' (e.g. imshow(..., aspect='auto')).")
    if not isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        warnings.warn("finalize_figure expects layout='constrained'; ratios may be off.")
    if aspect is None:
        aspect = _default_aspect(fig, panels)

    ratios, widths = _fit_height_to_aspect(fig, panels, aspect, iters, tol)
    _turn_crowded_bar_labels(fig, panels)
    if _keep_value_labels_inside(fig, panels):
        ratios, widths = _fit_height_to_aspect(fig, panels, aspect, iters, tol)
    if _place_legends(fig, panels):
        ratios, widths = _fit_height_to_aspect(fig, panels, aspect, iters, tol)
    if abs(ratios[0] - aspect) / aspect >= tol:
        _freeze_ticks(fig.axes)  # colorbars too: their auto ticks change width with the height
        ratios, widths = _fit_height_to_aspect(fig, panels, aspect, iters, tol)
    if abs(ratios[0] - aspect) / aspect >= tol:
        warnings.warn(f"finalize_figure did not converge in {iters} iterations: ratio {ratios[0]:.3f}; "
                      "check for an inside legend or text wider than the panel.")
    # the author's layout; sub-figures' widths come from matplotlib's layout, not the author
    if not fig.subfigs and max(widths) - min(widths) > tol * max(widths):
        warnings.warn("panels have different widths, so not all can match the aspect; "
                      f"panel ratios: {[round(r, 3) for r in ratios]}")
    _blank_touching_corner_label(fig, panels)
    placed = _place_on_standard_box(fig, panels, aspect, column_gap)
    if placed:
        # ticks frozen while the height was searched fit a smaller panel: lay them out again at the final size,
        # then fix them, since growing limits for labels must not add ticks the layout has no room for
        _unfreeze_ticks(fig.axes)
        fig.canvas.draw()
        _freeze_ticks(panels)
        _turn_crowded_bar_labels(fig, panels)  # the panels may now be narrower than when bar values were first checked
        if _recheck_legends(fig, panels):
            _place_on_standard_box(fig, panels, aspect, column_gap)
        _keep_value_labels_inside(fig, panels)
        ratios = _measure_panels(fig, panels)[0]
    _colorbars_span_panels(fig)
    _fit_heatmap_values(fig, panels)
    _center_group_labels(fig)
    _center_row_legends(fig, panels)
    # on the standard box, shapes follow its rules (a half with wider left labels has narrower panels)
    if not placed and max(ratios) - min(ratios) > tol * max(ratios):
        warnings.warn("panels have different shapes; one figure takes one aspect (no height_ratios or width_ratios)")
    checks._warn_hard_to_read(fig, panels, min_width)
    return ratios
