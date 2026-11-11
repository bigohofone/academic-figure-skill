import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

ASSETS = Path(__file__).parent / "skills/academic-figure/assets"
sys.path.insert(0, str(ASSETS))
import paper
from paper import fit_height, group_label, mark_value, smooth, darken, lighten, text_color

WIDTH = 3.25


@pytest.fixture(autouse=True)
def style():
    with plt.rc_context():
        paper.use_design(ASSETS / "DESIGN.md")
        yield
    plt.close("all")


def check(fig, ratios, aspect, tol=0.005):
    assert fig.get_figwidth() == WIDTH
    for r in ratios:
        assert abs(r - aspect) / aspect < tol


def test_single_line():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    ax.plot([0, 1], [0, 1])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    check(fig, fit_height(fig, ax), 0.618)


def test_two_panels_shared_legend():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3))
    for ax in axes:
        ax.plot([0, 1], [0, 1], label="a")
        ax.plot([0, 1], [1, 0], label="b")
        ax.set_title("T")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside lower center", ncol=2,
               frameon=False, borderaxespad=0)
    check(fig, fit_height(fig, axes), 0.618)


def test_grid_with_empty_cell():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 3))
    for ax in axes.flat[:3]:
        ax.plot([0, 1], [0, 1])
    axes[1, 1].axis("off")
    ratios = fit_height(fig, axes)
    assert len(ratios) == 3
    check(fig, ratios, 0.618)


def test_heatmap_colorbar():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    im = ax.imshow(np.random.rand(5, 5), aspect="auto")
    fig.colorbar(im, ax=ax)
    check(fig, fit_height(fig, fig.axes, aspect=1.0), 1.0)


def test_imshow_default_aspect_raises():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    ax.imshow(np.random.rand(5, 5))
    with pytest.raises(ValueError, match="aspect='auto'"):
        fit_height(fig, ax, aspect=1.0)


def test_mosaic_different_widths_warns():
    fig, axd = plt.subplot_mosaic("AAB", figsize=(WIDTH, 3), layout="constrained")
    with pytest.warns(UserWarning, match="different widths"):
        fit_height(fig, axd)


def test_long_labels_converge():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    ax.plot([0, 1], [0, 1_000_000])
    ax.set_yticks([0, 500_000, 1_000_000], ["0", "500,000", "1,000,000"], fontsize=12)
    ax.set_ylabel("A very long y-axis label\nthat spans two lines")
    fit_height(fig, ax)
    short, sax = plt.subplots(figsize=(WIDTH, 3))
    sax.plot([0, 1], [0, 1])
    sax.set_ylabel("y")
    fit_height(short, sax)
    w, h = fig.get_size_inches()
    assert abs(ax.get_position().height * h - sax.get_position().height * short.get_figheight()) < 0.01
    assert abs((1 - ax.get_position().x1) - (1 - sax.get_position().x1)) * w < 0.01


def test_aspect_options():
    for aspect in (0.382, 1.0, 1.618):
        fig, ax = plt.subplots(figsize=(WIDTH, 3))
        ax.plot([0, 1], [0, 1])
        check(fig, fit_height(fig, ax, aspect=aspect), aspect)


def test_ticks_that_change_with_height_converge():
    fig, ax = plt.subplots(figsize=(3.0, 2))
    ax.bar(np.arange(3), [84, 92, 89], edgecolor="black")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(78, 95)
    ratios = fit_height(fig, ax)
    assert fig.get_figwidth() == 3.0
    assert abs(ratios[0] - 0.618) / 0.618 < 0.005
    assert ax.get_ylim() == (78, 95)


def test_shared_axes():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 3), sharex=True, sharey=True)
    for i, ax in enumerate(axes.flat):
        ax.plot([0, 1], [0, i + 1])
    check(fig, fit_height(fig, axes), 0.618)


def test_pdf_embeds_inter_as_text(tmp_path):
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1])
    ax.set_title(r"$\alpha=0.1$, $\sum_i x_i \leq \sqrt{2}$")
    ax.set_xlabel(r"FLOPs ($\times 10^{18}$)")
    fig.savefig(tmp_path / "f.pdf")
    pdf = (tmp_path / "f.pdf").read_bytes()
    assert b"Inter" in pdf and b"DejaVu" not in pdf
    assert b"/Type3" not in pdf
    assert pdf.count(b"/FontFile2") == pdf.count(b"/CIDFontType2") > 0
    assert b"/ToUnicode" in pdf


def test_smooth_is_centered():
    values = [0.0] * 50 + [1.0] * 50
    smoothed = smooth(values)
    assert len(smoothed) == len(values)
    assert smoothed[49] < 0.5 < smoothed[50]
    assert smoothed[0] == 0.0 and smoothed[-1] == 1.0


def test_darken_darkens():
    assert darken("#FFFFFF") == [0.8, 0.8, 0.8]


def test_lighten_mixes_with_white():
    assert lighten("#000000") == [0.6, 0.6, 0.6]


def test_mark_value_line_point_and_label():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    mark_value(ax, 1, 1, "1.0", "#4477AA")
    line, circle = ax.lines
    assert line.get_linestyle() == "-"
    assert circle.get_marker() == "o"
    assert line.get_zorder() < circle.get_zorder()
    assert [t.get_text() for t in ax.texts] == ["1.0"]


def test_mark_value_below():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    mark_value(ax, 0, 0, "0.0", "#4477AA", below=True)
    assert ax.texts[0].get_va() == "top"


def test_fit_height_keeps_value_labels_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1, 2], [0, 1, 2])
    mark_value(ax, 2, 2, "2.0", "#4477AA")
    fit_height(fig, ax)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    label = ax.texts[0]
    assert ax.get_window_extent(renderer).contains(*label.get_window_extent(renderer).p1)



def test_fit_height_warns_narrow_panel():
    fig, axes = plt.subplots(1, 3, figsize=(WIDTH, 2))
    for a in axes:
        a.plot([0, 1], [0, 1])
    with pytest.warns(UserWarning, match="narrower than 1.2 in"):
        fit_height(fig, axes)


def test_fit_height_warns_overlapping_text():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1])
    ax.text(0.5, 0.5, "first")
    ax.text(0.5, 0.5, "second")
    with pytest.warns(UserWarning, match="overlap"):
        fit_height(fig, ax)


def test_fit_height_warns_legend_over_curve():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1], label="a line through the middle")
    ax.legend(loc="center")
    with pytest.warns(UserWarning, match="the legend covers a curve"):
        fit_height(fig, ax)


def test_fit_height_quiet_on_clean_figure():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1], label="line")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="lower right")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fit_height(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]


def test_rotated_tick_labels_that_fit_do_not_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    labels = [f"({i / 10:.1f},{(i + 1) / 10:.1f}]" for i in range(10)]
    ax.bar(range(10), range(10))
    ax.set_xticks(range(10), labels=labels, rotation=45, ha="right", rotation_mode="anchor")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fit_height(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]


def test_rotated_tick_labels_that_collide_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar(range(40), range(40))
    ax.set_xticks(range(40), labels=["long label"] * 40, rotation=45, ha="right", rotation_mode="anchor")
    with pytest.warns(UserWarning, match="overlap"):
        fit_height(fig, ax)


def test_bar_labels_are_kept_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar_label(ax.bar(range(3), [3, 5, 2]), fontweight="bold")
    fit_height(fig, ax)
    fig.canvas.draw()
    box = ax.get_window_extent()
    assert all(t.get_window_extent().y1 <= box.y1 + 0.5 for t in ax.texts)


def test_horizontal_bar_labels_are_kept_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar_label(ax.barh(range(3), [3, 113, 2]), fontweight="bold")
    fit_height(fig, ax)
    fig.canvas.draw()
    box = ax.get_window_extent()
    assert all(t.get_window_extent().x1 <= box.x1 + 0.5 for t in ax.texts)


def test_fit_height_warns_legend_over_bar():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar(range(3), [5, 5, 5], label="a")
    ax.legend(loc="center")
    with pytest.warns(UserWarning, match="the legend covers filled marks"):
        fit_height(fig, ax)


def test_fit_height_allows_legend_over_a_bar_corner():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar(range(3), [1, 1, 4.6], label="a")
    ax.set_ylim(0, 5.3)
    ax.legend(loc="upper right")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fit_height(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]


def test_panels_in_subfigures_get_the_aspect():
    fig = plt.figure(figsize=(6.75, 2))
    left, right = fig.subfigures(1, 2, width_ratios=[2, 1])
    axes = [*left.subplots(1, 2), right.subplots()]
    for ax in axes:
        ax.plot([0, 1], [0, 1])
    left.supxlabel("(a) Left")
    right.supxlabel("(b) Right")
    ratios = fit_height(fig, axes, aspect=0.618)
    assert all(abs(r - 0.618) / 0.618 < 0.02 for r in ratios)


def test_round_panels_fill_the_width_with_no_empty_height():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3))
    for ax in axes:
        ax.pie([3, 2, 1])
    fit_height(fig, axes, aspect=1.0)
    circle = axes[0].get_position()
    assert fig.get_figheight() - circle.height * fig.get_figheight() < 0.1 + 2 * paper.canvas_pad
    assert circle.width * WIDTH > 0.45 * WIDTH


def test_polar_panel_is_fitted_without_error():
    fig, ax = plt.subplots(figsize=(WIDTH, 3), subplot_kw={"projection": "polar"})
    ax.plot([0, 1, 2], [1, 2, 3])
    fit_height(fig, ax, aspect=1.0)
    assert fig.get_figheight() < WIDTH


def test_point_name_past_the_panel_is_reported_not_moved():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([3, 72], [0.6, 0.8], "o")
    ax.set_xscale("log")
    ax.annotate("Qwen2-72B-Instruct", (72, 0.8), xytext=(3, 3), textcoords="offset points")
    limits = ax.get_xlim()
    with pytest.warns(UserWarning, match="sticks out of panel"):
        fit_height(fig, ax)
    assert ax.get_xlim() == limits


def test_text_color_reads_on_its_fill():
    assert text_color("#08306B") == "white"
    assert text_color("#F7FBFF") == "black"


def test_legend_over_scatter_points_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    rng = np.random.default_rng(0)
    ax.scatter(rng.uniform(0, 0.3, 50), rng.uniform(0.7, 1, 50), label="a")
    ax.scatter([0.9], [0.1], label="b")
    ax.legend(loc="upper left")
    with pytest.warns(UserWarning, match="covers data points"):
        fit_height(fig, ax)


def test_legend_over_markers_only_line_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0.05, 0.1, 0.15], [0.9, 0.95, 0.92], "o", label="a")
    ax.plot([0.9], [0.1], "o", label="b")
    ax.legend(loc="upper left")
    with pytest.warns(UserWarning, match="covers"):
        fit_height(fig, ax)


def test_tall_outside_legend_does_not_collapse_the_layout():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 12))
    for ax in axes:
        ax.plot([0, 1], [0, 1], label="a long legend entry")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper center", ncol=1, frameon=False)
    ratios = fit_height(fig, axes)
    assert all(abs(r - 0.618) / 0.618 < 0.02 for r in ratios)


def test_min_width_sets_the_narrow_panel_threshold():
    fig, axes = plt.subplots(1, 4, figsize=(5.5, 2), sharey=True)
    for ax in axes:
        ax.plot([0, 1], [0, 1])
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        fit_height(fig, axes, min_width=1.0)


def test_fit_height_warns_legend_over_band():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    x = np.linspace(0, 1, 50)
    ax.fill_between(x, 0, 1, label="band")
    ax.legend(loc="center")
    with pytest.warns(UserWarning, match="the legend covers filled marks"):
        fit_height(fig, ax)


def test_fit_height_warns_text_spilling_out_of_its_fill():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar([0], [1], width=0.05)
    ax.set_xlim(-1, 1)
    ax.text(0, 0.5, "a long label", ha="center", va="center")
    with pytest.warns(UserWarning, match="spills out of its fill"):
        fit_height(fig, ax)


def test_wide_legend_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 3), layout="constrained")
    for i in range(8):
        ax.plot([0, 1], [i, i + 1], label=f"A long series name {i}")
    fig.legend(loc="outside upper center", ncol=8)
    with pytest.warns(UserWarning, match="wider than the figure"):
        fit_height(fig, ax)


def test_column_gaps_are_standard():
    sizes = []
    for label in ("Accuracy", "A much longer label"):
        fig, axes = plt.subplots(1, 3, figsize=(5.5, 2), layout="constrained", sharey=True)
        for a in axes:
            a.plot([0, 1], [0, 1])
        axes[0].set_ylabel(label)
        fit_height(fig, axes)
        p = [a.get_position() for a in axes]
        sizes.append(round((p[1].x0 - p[0].x1) * 5.5, 3))
    assert sizes[0] == sizes[1]


def test_grouped_columns_gap_by_what_they_show():
    fig, axes = plt.subplots(1, 4, figsize=(5.5, 2), layout="constrained")
    for a in axes:
        a.plot([0, 1], [0, 1])
    for a, b in ((axes[0], axes[1]), (axes[2], axes[3])):
        b.sharey(a)
        b.tick_params(labelleft=False)
    axes[0].set_ylabel("Accuracy")
    axes[2].set_ylabel("Loss")
    group_label(axes[:2], "Step")
    group_label(axes[2:], "Step")
    fit_height(fig, list(axes))
    p = [a.get_position() for a in axes]
    inside, between = (p[1].x0 - p[0].x1) * 5.5, (p[2].x0 - p[1].x1) * 5.5
    assert between > 3 * inside
    center = (p[0].x0 + p[1].x1) / 2
    assert abs(p[0].x0 + axes[0].xaxis.label.get_position()[0] * p[0].width - center) < 1e-6


def test_right_axis_mirrors_left():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.plot([0, 1], [0, 1])
    ax.set_ylabel("Accuracy")
    twin = ax.twinx()
    twin.plot([0, 1], [1, 0])
    twin.set_ylabel("Loss")
    fit_height(fig, ax)
    p = ax.get_position()
    assert abs(p.x0 - (1 - p.x1)) < 1e-6
    assert np.allclose(twin.get_position().bounds, p.bounds)


def test_legend_over_bar_ends_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.bar([0, 1, 2, 3], [0.2, 0.5, 0.9, 0.95], label="Accuracy")
    ax.bar([0], [0.1], bottom=[0.2], label="Gap")
    ax.legend(loc="upper right")
    with pytest.warns(UserWarning, match="end of a bar"):
        fit_height(fig, ax)


def test_legend_over_twin_curve_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.plot([0, 1], [0, 0.1], label="Loss")
    twin = ax.twinx()
    twin.plot([0, 1], [1, 1], color="C1", label="Learning rate")
    ax.legend(loc="upper right")
    with pytest.warns(UserWarning, match="covers a curve"):
        fit_height(fig, ax)


def test_axis_label_longer_than_panel_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 1), layout="constrained")
    ax.plot([0, 1], [0, 1])
    ax.set_ylabel("A very long response length label (tokens)")
    with pytest.warns(UserWarning, match="longer than its panel"):
        fit_height(fig, ax, aspect=0.3)


def test_column_gap_lines_groups_up_with_single_columns():
    fig, axes = plt.subplots(1, 4, figsize=(6.75, 2), layout="constrained")
    for a in axes:
        a.plot([0, 1], [0, 1])
    for a, b in ((axes[0], axes[1]), (axes[2], axes[3])):
        b.sharey(a)
        b.tick_params(labelleft=False)
    axes[0].set_ylabel("Accuracy")
    axes[2].set_ylabel("Loss")
    fit_height(fig, list(axes), aspect=1.0, column_gap=0.25)
    single, _ = plt.subplots(figsize=(3.25, 2), layout="constrained")
    single.axes[0].plot([0, 1], [0, 1])
    single.axes[0].set_ylabel("Accuracy")
    fit_height(single, single.axes[0])
    p, s = [a.get_position() for a in axes], single.axes[0].get_position()
    assert abs(p[0].x0 * 6.75 - s.x0 * 3.25) < 1e-3
    assert abs(p[3].x1 * 6.75 - (3.5 + s.x1 * 3.25)) < 1e-3


def test_legend_sticking_out_of_its_panel_warns():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2), layout="constrained")
    for a in axes:
        a.plot([0, 1], [0, 0.2], label="Average confidence over all samples")
    axes[0].legend(loc="upper left")
    with pytest.warns(UserWarning, match="sticks out of panel"):
        fit_height(fig, list(axes), min_width=0.9)


def test_legend_above_a_row_is_centred_over_it():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2), layout="constrained", sharey=True)
    for a in axes:
        a.bar([0, 1], [1, 2], label="Accuracy")
    axes[0].legend(loc="lower left", bbox_to_anchor=(0, 1), ncol=2)
    fit_height(fig, list(axes), min_width=0.9)
    box = axes[0].get_legend().get_window_extent()
    row = (axes[0].get_window_extent().x0 + axes[1].get_window_extent().x1) / 2
    assert abs((box.x0 + box.x1) / 2 - row) < 1


def test_point_name_may_touch_its_own_curve():
    import warnings
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.plot([0, 1, 2], [0, 1, 2], "o-")
    ax.annotate("B1", (1, 1), xytext=(-3, 3), textcoords="offset points", ha="right")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fit_height(fig, ax)
    assert not any("covers a curve" in str(w.message) for w in caught)
