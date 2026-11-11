"""Sizes: finalize_figure sets each figure's height, the standard margins and panel widths, and where legends
and labels sit."""
import warnings

import numpy as np
from matplotlib import rcParams
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.legend import Legend
from matplotlib.transforms import Bbox
from matplotlib.text import Annotation
from matplotlib.ticker import FixedLocator, FuncFormatter, ScalarFormatter

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
    while not np.isfinite(ratios[0]):  # the start is too short for the decorations: grow until the layout stands
        h0 *= 2
        fig.set_figheight(h0)
        ratios, widths = _measure_panels(fig, panels)
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
        # a secant step can overshoot below zero while the layout is still settling: halve instead
        h0, r0, h1 = h1, r1, step if np.isfinite(step) and step > 0 else h1 / 2
    return ratios, widths


def _set_canvas_pad(fig):
    """Free space on all four sides of the canvas, for text that reaches past the panels."""
    if isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        # left and right as a rect; top and bottom as the layout's edge pad, which outside legends obey too
        x = design.canvas_pad / fig.get_figwidth()
        fig.get_layout_engine().set(rect=(x, 0, 1 - 2 * x, 1), h_pad=design.canvas_pad)


def _freeze_ticks(panels):
    for a in panels:
        for axis in (a.xaxis, a.yaxis):
            lo, hi = sorted(axis.get_view_interval())
            axis.set_major_locator(FixedLocator([t for t in axis.get_majorticklocs() if lo <= t <= hi]))


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


def _place_legends(fig, panels):
    """A panel legend made without `loc` goes to the first inside spot where it hides nothing, else
    above its panel in one row. Returns whether any went above."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    above = False
    for a in panels:
        legend = a.get_legend()
        if legend is None or legend._loc != Legend.codes["best"]:
            continue
        for spot in INSIDE_SPOTS:
            legend.set_loc(spot)
            if not checks._legend_problems(fig, a, panels, renderer):
                break
        else:
            legend.set_loc("lower center")
            legend.set_bbox_to_anchor((0.5, 1), transform=a.transAxes)
            legend.set_ncols(len(legend.get_texts()))
            legend.set_frame_on(False)
            legend.borderaxespad = 0.5
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


def _standard_column_gap(fig, column, column_gap):
    """The standard gap before a grid column. A column with its own y label shows a new quantity, so
    it starts a new group, as if a new figure began there: the right margin plus the left margin (more
    for a longer y label), plus `column_gap`, the space between the page's text columns, so in a
    double-column figure the groups line up with single-column figures. A column with only its own
    tick numbers (the same quantity over its own range) sits close: half a tick label, so the end
    labels of neighbouring x axes clear each other, plus its tick labels. Otherwise half a tick label."""
    ticks, label, half = _standard_y_widths(fig)
    shows_ticks = any(t.get_visible() and t.get_text() for a in column for t in a.get_yticklabels())
    label_lines = max(_line_count(a.yaxis.label) for a in column)
    if label_lines:
        return (design.canvas_pad + half) + column_gap + (design.canvas_pad + ticks + label * label_lines)
    return half + ticks * shows_ticks


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


def _place_on_standard_box(fig, panels, aspect, column_gap):
    """Panels sit at the standard margins and take the standard size, so the boxes of all figures at
    one width (and one number of columns) line up and match. The right margin is fixed; left labels
    that need more room widen the left margin and narrow the panels, which keep the standard height
    (the aspect gives way). The gaps between columns are standard (`_standard_column_gap`); the gaps between rows stay as the layout
    found them; the columns share what is left.
    One colorbar is kept beside the panels (right) or under them (bottom), at the size and gap the
    layout gave it, its labels inside a standard margin of their own. Returns whether they moved."""
    cbars = [a for a in fig.axes if getattr(a, "_colorbar", None) is not None]
    others = [a for a in fig.axes if a not in panels and a not in cbars]
    twin_of = {t: p for t in others for p in panels
               if np.allclose(t.get_position().bounds, p.get_position().bounds)}  # ax.twinx(): a right y axis
    if fig.subfigs or len(cbars) > 1 or len(twin_of) != len(others) or checks._is_round_panel(panels[0]):
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
    left, right = _standard_side_margins(fig)
    side = left - design.canvas_pad  # an axis label and four-character tick labels
    pad = design.canvas_pad
    cbar = cbars[0] if cbars else None
    vertical = cbar is not None and cbar._colorbar.orientation == "vertical"
    # the right margin never moves, so every figure's right edge lines up; a left label that needs
    # more room takes it from the panels' width, never their height, so one width keeps one height
    if vertical:
        cb_gap, cb_w = design.colorbar_gap, design.colorbar_width
        right = pad + side + cb_w + cb_gap
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
    col_gaps = [_standard_column_gap(fig, [a for a in panels if col_of[a] == c], column_gap) + right_axis * (c - 1 in right_column)
                for c in range(1, len(columns))]
    # rows: above each, half a tick label or a title line; below, x tick labels and x label lines;
    # anything more (a legend above a panel, a second line, turned labels) widens that margin
    above, below = [], []
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
    row_gaps = [below[r] + above[r + 1] for r in range(len(rows) - 1)]
    top_legends = [lg for lg in fig.legends if lg.get_window_extent(renderer).y0 / fig.dpi >= max(b.y1 for b in boxes.values()) * h - 1e-3]
    legend_h = sum(lg.get_window_extent(renderer).height / fig.dpi for lg in top_legends)
    top = pad + legend_h + above[0]
    sup_x = fig._supxlabel if fig._supxlabel and fig._supxlabel.get_text() else None
    bottom = pad + below[-1] + label * (_line_count(sup_x) if sup_x else 0)
    if cbar is not None and not vertical:
        bottom = boxes[next(a for a in panels if row_of[a] == len(rows) - 1)].y0 * h  # a colorbar under the panels keeps the layout's room
        cb = cbar.get_position()
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


def _write_plain_tick_numbers(fig):
    """Write matplotlib's default numeric ticks as plain numbers (0, 0.5, 1; 1024), with a true minus sign."""
    for a in fig.axes:
        for axis in (a.xaxis, a.yaxis):
            if type(axis.get_major_formatter()) is ScalarFormatter:
                axis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.10g}".replace("-", "\u2212")))


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


def finalize_figure(fig, ax, aspect=0.618, iters=10, tol=0.005, min_width=1.2, column_gap=0):
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

    Bar values side by side that overlap all turn upward (rotation 90), panel by panel.

    A panel legend made without `loc` is placed here: the first spot of `INSIDE_SPOTS` where it
    hides no data or text, else above its panel in one row.

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
    _write_plain_tick_numbers(fig)
    _start_at_zero(panels)
    if isinstance(fig.get_layout_engine(), ConstrainedLayoutEngine):
        _set_canvas_pad(fig)
    checks._warn_legends_wider_than_figure(fig)
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
    if max(widths) - min(widths) > tol * max(widths):
        warnings.warn("panels have different widths, so not all can match the aspect; "
                      f"panel ratios: {[round(r, 3) for r in ratios]}")
    _blank_touching_corner_label(fig, panels)
    if _place_on_standard_box(fig, panels, aspect, column_gap):
        _freeze_ticks(panels)  # growing limits for labels now must not add ticks the layout has no room for
        _keep_value_labels_inside(fig, panels)
        ratios = _measure_panels(fig, panels)[0]
    _center_group_labels(fig)
    _center_row_legends(fig, panels)
    if max(ratios) - min(ratios) > tol * max(ratios):
        warnings.warn("panels have different shapes; one figure takes one aspect (no height_ratios or width_ratios)")
    checks._warn_hard_to_read(fig, panels, min_width)
    return ratios
