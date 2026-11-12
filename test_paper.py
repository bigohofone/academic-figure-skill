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
from paper import palette
from paper import finalize_figure, set_group_label, mark_value, moving_average, darken, lighten, text_color_on

WIDTH = 3.25


@pytest.fixture(autouse=True)
def style():
    with plt.rc_context():
        paper.apply_design(ASSETS / "DESIGN.md")
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
    check(fig, finalize_figure(fig, ax), 0.618)


def test_two_panels_shared_legend():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3))
    for ax in axes:
        ax.plot([0, 1], [0, 1], label="a")
        ax.plot([0, 1], [1, 0], label="b")
        ax.set_title("T")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside lower center", ncol=2,
               frameon=False, borderaxespad=0)
    check(fig, finalize_figure(fig, axes, aspect=0.618), 0.618)


def test_grid_with_empty_cell():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 3))
    for ax in axes.flat[:3]:
        ax.plot([0, 1], [0, 1])
    axes[1, 1].axis("off")
    ratios = finalize_figure(fig, axes, aspect=0.618)
    assert len(ratios) == 3
    check(fig, ratios, 0.618)


def test_heatmap_colorbar():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    im = ax.imshow(np.random.rand(5, 5), aspect="auto")
    fig.colorbar(im, ax=ax)
    check(fig, finalize_figure(fig, fig.axes, aspect=1.0), 1.0)


def test_imshow_default_aspect_raises():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    ax.imshow(np.random.rand(5, 5))
    with pytest.raises(ValueError, match="aspect='auto'"):
        finalize_figure(fig, ax, aspect=1.0)


def test_mosaic_different_widths_warns():
    fig, axd = plt.subplot_mosaic("AAB", figsize=(WIDTH, 3), layout="constrained")
    with pytest.warns(UserWarning, match="different widths"):
        finalize_figure(fig, axd)


def test_long_labels_converge():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    ax.plot([0, 1], [0, 1_000_000])
    ax.set_yticks([0, 500_000, 1_000_000], ["0", "500,000", "1,000,000"], fontsize=12)
    ax.set_ylabel("A very long y-axis label\nthat spans two lines")
    finalize_figure(fig, ax)
    short, sax = plt.subplots(figsize=(WIDTH, 3))
    sax.plot([0, 1], [0, 1])
    sax.set_ylabel("y")
    finalize_figure(short, sax)
    w, h = fig.get_size_inches()
    assert abs(ax.get_position().height * h - sax.get_position().height * short.get_figheight()) < 0.01
    assert abs((1 - ax.get_position().x1) - (1 - sax.get_position().x1)) * w < 0.01


def test_aspect_options():
    for aspect in (0.382, 1.0, 1.618):
        fig, ax = plt.subplots(figsize=(WIDTH, 3))
        ax.plot([0, 1], [0, 1])
        check(fig, finalize_figure(fig, ax, aspect=aspect), aspect)


def test_ticks_that_change_with_height_converge():
    fig, ax = plt.subplots(figsize=(3.0, 2))
    ax.bar(np.arange(3), [84, 92, 89], edgecolor="black")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(78, 95)
    ratios = finalize_figure(fig, ax)
    assert fig.get_figwidth() == 3.0
    assert abs(ratios[0] - 0.618) / 0.618 < 0.005
    assert ax.get_ylim() == (78, 95)


def test_shared_axes():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 3), sharex=True, sharey=True)
    for i, ax in enumerate(axes.flat):
        ax.plot([0, 1], [0, i + 1])
    check(fig, finalize_figure(fig, axes, aspect=0.618), 0.618)


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
    smoothed = moving_average(values)
    assert len(smoothed) == len(values)
    assert smoothed[49] < 0.5 < smoothed[50]
    assert smoothed[0] == pytest.approx(0.0) and smoothed[-1] == pytest.approx(1.0)


def test_smooth_ends_follow_a_steep_start_and_damp_noise():
    line = [10 - 0.1 * i for i in range(200)]
    assert moving_average(line) == pytest.approx(line)
    noise = [(-1) ** i for i in range(200)]
    smoothed = moving_average(noise)
    assert abs(smoothed[0]) < 0.3 and abs(smoothed[-1]) < 0.3


def test_darken_darkens():
    assert darken("#FFFFFF") == [0.8, 0.8, 0.8]


def test_lighten_mixes_with_white():
    assert lighten("#000000") == [0.6, 0.6, 0.6]


def test_mark_value_line_point_and_label():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    mark_value(ax, 1, 1, "1.0", "#4477AA")
    circle, = ax.lines
    assert circle.get_marker() == "o"
    assert [t.get_text() for t in ax.texts] == ["1.0"]


def test_mark_value_below():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    mark_value(ax, 0, 0, "0.0", "#4477AA", below=True)
    assert ax.texts[0].get_va() == "top"


def test_fit_height_keeps_value_labels_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1, 2], [0, 1, 2])
    mark_value(ax, 2, 2, "2.0", "#4477AA")
    finalize_figure(fig, ax)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    label = ax.texts[0]
    assert ax.get_window_extent(renderer).contains(*label.get_window_extent(renderer).p1)



def test_fit_height_warns_narrow_panel():
    fig, axes = plt.subplots(1, 4, figsize=(WIDTH, 2))
    for a in axes:
        a.plot([0, 1], [0, 1])
    with pytest.warns(UserWarning, match="narrower than 0.9 in"):
        finalize_figure(fig, axes)


def test_fit_height_warns_overlapping_text():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1])
    ax.text(0.5, 0.5, "first")
    ax.text(0.5, 0.5, "second")
    with pytest.warns(UserWarning, match="overlap"):
        finalize_figure(fig, ax)


def test_fit_height_warns_legend_over_curve():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1], label="a line through the middle")
    ax.legend(loc="center")
    with pytest.warns(UserWarning, match="the legend covers a curve"):
        finalize_figure(fig, ax)


def test_fit_height_quiet_on_clean_figure():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1], [0, 1], label="line")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="lower right")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]


def test_rotated_tick_labels_that_fit_do_not_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    labels = [f"({i / 10:.1f},{(i + 1) / 10:.1f}]" for i in range(10)]
    ax.bar(range(10), range(10))
    ax.set_xticks(range(10), labels=labels, rotation=45, ha="right", rotation_mode="anchor")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]


def test_rotated_tick_labels_that_collide_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar(range(40), range(40))
    ax.set_xticks(range(40), labels=["long label"] * 40, rotation=45, ha="right", rotation_mode="anchor")
    with pytest.warns(UserWarning, match="overlap"):
        finalize_figure(fig, ax)


def test_bar_labels_are_kept_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar_label(ax.bar(range(3), [3, 5, 2]), fontweight="bold")
    finalize_figure(fig, ax)
    fig.canvas.draw()
    box = ax.get_window_extent()
    assert all(t.get_window_extent().y1 <= box.y1 + 0.5 for t in ax.texts)


def test_horizontal_bar_labels_are_kept_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar_label(ax.barh(range(3), [3, 113, 2]), fontweight="bold")
    finalize_figure(fig, ax)
    fig.canvas.draw()
    box = ax.get_window_extent()
    assert all(t.get_window_extent().x1 <= box.x1 + 0.5 for t in ax.texts)


def test_fit_height_warns_legend_over_bar():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar(range(3), [5, 5, 5], label="a")
    ax.legend(loc="center")
    with pytest.warns(UserWarning, match="the legend covers filled marks"):
        finalize_figure(fig, ax)


def test_fit_height_allows_legend_over_a_bar_corner():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar(range(3), [1, 1, 4.6], label="a")
    ax.set_ylim(0, 5.3)
    ax.legend(loc="upper right")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]


def test_panels_in_subfigures_get_the_aspect():
    fig = plt.figure(figsize=(6.75, 2))
    left, right = fig.subfigures(1, 2, width_ratios=[2, 1])
    axes = [*left.subplots(1, 2), right.subplots()]
    for ax in axes:
        ax.plot([0, 1], [0, 1])
    left.supxlabel("(a) Left")
    right.supxlabel("(b) Right")
    ratios = finalize_figure(fig, axes, aspect=0.618)
    assert all(abs(r - 0.618) / 0.618 < 0.02 for r in ratios)


def test_round_panels_fill_the_width_with_no_empty_height():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3))
    for ax in axes:
        ax.pie([3, 2, 1])
    finalize_figure(fig, axes, aspect=1.0)
    circle = axes[0].get_position()
    assert fig.get_figheight() - circle.height * fig.get_figheight() < 0.1 + 2 * paper.canvas_pad
    assert circle.width * WIDTH > 0.45 * WIDTH


def test_polar_panel_is_fitted_without_error():
    fig, ax = plt.subplots(figsize=(WIDTH, 3), subplot_kw={"projection": "polar"})
    ax.plot([0, 1, 2], [1, 2, 3])
    finalize_figure(fig, ax, aspect=1.0)
    assert fig.get_figheight() < WIDTH


def test_point_name_past_the_panel_is_reported_not_moved():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([3, 72], [0.6, 0.8], "o")
    ax.set_xscale("log")
    ax.annotate("Qwen2-72B-Instruct", (72, 0.8), xytext=(3, 3), textcoords="offset points")
    limits = ax.get_xlim()
    with pytest.warns(UserWarning, match="sticks out of panel"):
        finalize_figure(fig, ax)
    assert ax.get_xlim() == limits


def test_text_color_reads_on_its_fill():
    assert text_color_on("#08306B") == "white"
    assert text_color_on("#F7FBFF") == "black"


def test_legend_over_scatter_points_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    rng = np.random.default_rng(0)
    ax.scatter(rng.uniform(0, 0.3, 50), rng.uniform(0.7, 1, 50), label="a")
    ax.scatter([0.9], [0.1], label="b")
    ax.legend(loc="upper left")
    with pytest.warns(UserWarning, match="covers data points"):
        finalize_figure(fig, ax)


def test_legend_over_markers_only_line_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0.05, 0.1, 0.15], [0.9, 0.95, 0.92], "o", label="a")
    ax.plot([0.9], [0.1], "o", label="b")
    ax.legend(loc="upper left")
    with pytest.warns(UserWarning, match="covers"):
        finalize_figure(fig, ax)


def test_tall_outside_legend_does_not_collapse_the_layout():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 12))
    for ax in axes:
        ax.plot([0, 1], [0, 1], label="a long legend entry")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper center", ncol=1, frameon=False)
    ratios = finalize_figure(fig, axes, aspect=0.618)
    assert all(abs(r - 0.618) / 0.618 < 0.02 for r in ratios)


def test_min_width_sets_the_narrow_panel_threshold():
    fig, axes = plt.subplots(1, 4, figsize=(5.5, 2), sharey=True)
    for ax in axes:
        ax.plot([0, 1], [0, 1])
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        finalize_figure(fig, axes, min_width=1.0)


def test_fit_height_warns_legend_over_band():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    x = np.linspace(0, 1, 50)
    ax.fill_between(x, 0, 1, label="band")
    ax.legend(loc="center")
    with pytest.warns(UserWarning, match="the legend covers filled marks"):
        finalize_figure(fig, ax)


def test_fit_height_warns_text_spilling_out_of_its_fill():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.bar([0], [1], width=0.05)
    ax.set_xlim(-1, 1)
    ax.text(0, 0.5, "a long label", ha="center", va="center")
    with pytest.warns(UserWarning, match="spills out of its fill"):
        finalize_figure(fig, ax)


def test_wide_legend_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 3), layout="constrained")
    for i in range(8):
        ax.plot([0, 1], [i, i + 1], label=f"A long series name {i}")
    fig.legend(loc="outside upper center", ncol=8)
    with pytest.warns(UserWarning, match="wider than the figure"):
        finalize_figure(fig, ax)


def test_column_gaps_are_standard():
    sizes = []
    for label in ("Accuracy", "A much longer label"):
        fig, axes = plt.subplots(1, 3, figsize=(5.5, 2), layout="constrained", sharey=True)
        for a in axes:
            a.plot([0, 1], [0, 1])
        axes[0].set_ylabel(label)
        finalize_figure(fig, axes)
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
    set_group_label(axes[:2], "Step")
    set_group_label(axes[2:], "Step")
    finalize_figure(fig, list(axes))
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
    finalize_figure(fig, ax)
    p = ax.get_position()
    assert abs(p.x0 - (1 - p.x1)) < 1e-6
    assert np.allclose(twin.get_position().bounds, p.bounds)


def test_legend_over_bar_ends_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.bar([0, 1, 2, 3], [0.2, 0.5, 0.9, 0.95], label="Accuracy")
    ax.bar([0], [0.1], bottom=[0.2], label="Gap")
    ax.legend(loc="upper right")
    with pytest.warns(UserWarning, match="end of a bar"):
        finalize_figure(fig, ax)


def test_legend_over_twin_curve_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.plot([0, 1], [0, 0.1], label="Loss")
    twin = ax.twinx()
    twin.plot([0, 1], [1, 1], color="C1", label="Learning rate")
    ax.legend(loc="upper right")
    with pytest.warns(UserWarning, match="covers a curve"):
        finalize_figure(fig, ax)


def test_axis_label_longer_than_panel_warns():
    fig, ax = plt.subplots(figsize=(WIDTH, 1), layout="constrained")
    ax.plot([0, 1], [0, 1])
    ax.set_ylabel("A very long response length label (tokens)")
    with pytest.warns(UserWarning, match="longer than its panel"):
        finalize_figure(fig, ax, aspect=0.3)


def test_column_gap_lines_groups_up_with_single_columns():
    fig, axes = plt.subplots(1, 4, figsize=(6.75, 2), layout="constrained")
    for a in axes:
        a.plot([0, 1], [0, 1])
    for a, b in ((axes[0], axes[1]), (axes[2], axes[3])):
        b.sharey(a)
        b.tick_params(labelleft=False)
    axes[0].set_ylabel("Accuracy")
    axes[2].set_ylabel("Loss")
    finalize_figure(fig, list(axes), aspect=1.0, column_gap=0.25)
    single, _ = plt.subplots(figsize=(3.25, 2), layout="constrained")
    single.axes[0].plot([0, 1], [0, 1])
    single.axes[0].set_ylabel("Accuracy")
    finalize_figure(single, single.axes[0])
    p, s = [a.get_position() for a in axes], single.axes[0].get_position()
    assert abs(p[0].x0 * 6.75 - s.x0 * 3.25) < 1e-3
    assert abs(p[3].x1 * 6.75 - (3.5 + s.x1 * 3.25)) < 1e-3


def test_subfigures_are_groups_lined_up_with_single_columns():
    fig = plt.figure(figsize=(6.75, 2), layout="constrained")
    left, right = fig.subfigures(1, 2)
    axes = [*left.subplots(1, 2, sharey=True), *right.subplots(1, 2, sharey=True)]
    for a in axes:
        a.plot([0, 1], [0, 1])
    axes[0].set_ylabel("Accuracy")
    axes[0].set_yticks([0, 1], ["A long method name", "Ours"])
    axes[2].set_ylabel("Tokens")
    left.supxlabel("(a) Accuracy")
    right.supxlabel("(b) Length")
    finalize_figure(fig, axes, aspect=0.618, column_gap=0.25)
    single, _ = plt.subplots(figsize=(3.25, 2), layout="constrained")
    single.axes[0].plot([0, 1], [0, 1])
    single.axes[0].set_ylabel("Accuracy")
    finalize_figure(single, single.axes[0])
    p, s = [a.get_position() for a in axes], single.axes[0].get_position()
    assert abs((p[1].x0 - p[0].x1) * 6.75 - paper.panel_gap) < 1e-3
    assert abs(p[1].x1 * 6.75 - s.x1 * 3.25) < 1e-3
    assert abs(p[3].x1 * 6.75 - (3.5 + s.x1 * 3.25)) < 1e-3
    assert abs(right._supxlabel.get_position()[0] - (p[2].x0 + p[3].x1) / 2) < 1e-6


def test_colorbar_as_tall_as_its_heatmap():
    fig, ax = plt.subplots(figsize=(WIDTH, WIDTH), layout="constrained")
    im = ax.imshow(np.arange(16).reshape(4, 4), aspect="auto")
    cbar = fig.colorbar(im, ax=ax, label="Accuracy")
    finalize_figure(fig, ax, aspect=1.0)
    fig.canvas.draw()
    panel, bar = ax.get_window_extent(), cbar.ax.get_window_extent()
    assert abs(panel.y0 - bar.y0) < 0.5 and abs(panel.y1 - bar.y1) < 0.5


def test_colorbar_below_spans_all_panels_at_token_width():
    fig, axes = plt.subplots(1, 3, figsize=(6.75, 6.75), layout="constrained", sharey=True)
    for a in axes:
        im = a.imshow(np.arange(16).reshape(4, 4), aspect="auto", vmin=0, vmax=15)
    cbar = fig.colorbar(im, ax=axes, location="bottom", label="Accuracy")
    finalize_figure(fig, axes, aspect=1.0, min_width=0.7)
    fig.canvas.draw()
    first, last, bar = axes[0].get_window_extent(), axes[-1].get_window_extent(), cbar.ax.get_window_extent()
    assert abs(bar.x0 - first.x0) < 0.5 and abs(bar.x1 - last.x1) < 0.5
    assert abs(bar.height / fig.dpi - paper.colorbar_width) < 1e-3


def test_colorbar_beside_each_heatmap():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, WIDTH), layout="constrained", sharey=True)
    bars = []
    for a, offset in zip(axes, (0, 100)):
        im = a.imshow(np.arange(16).reshape(4, 4) + offset, aspect="auto")
        a.set_yticks(range(4), ["1e-5", "2e-5", "3e-5", "5e-5"])
        bars.append(fig.colorbar(im, ax=a, label="Accuracy"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, axes, aspect=1.0, min_width=0.7)
    assert not [w for w in caught if "overlap" in str(w.message) or "cut off" in str(w.message)]
    fig.canvas.draw()
    for a, bar in zip(axes, bars):
        panel, box = a.get_window_extent(), bar.ax.get_window_extent()
        assert abs(panel.y0 - box.y0) < 0.5 and abs(panel.y1 - box.y1) < 0.5
        assert box.x0 > panel.x1


def test_wide_colorbar_labels_keep_the_canvas_pad():
    fig, ax = plt.subplots(figsize=(WIDTH, WIDTH), layout="constrained")
    im = ax.imshow([[0.9301, 0.9452], [0.9375, 0.9405]], aspect="auto")
    ax.set_yticks([0, 1], ["1e-5", "2e-5"])
    cbar = fig.colorbar(im, ax=ax, label="Accuracy")
    finalize_figure(fig, ax, aspect=1.0)
    fig.canvas.draw()
    assert cbar.ax.get_tightbbox().x1 / fig.dpi <= WIDTH - paper.canvas_pad + 1e-3


def test_colorbar_under_each_heatmap():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, WIDTH), layout="constrained", sharey=True)
    bars = []
    for a, (lo, hi) in zip(axes, ((0.928, 0.949), (0.85, 0.879))):
        im = a.imshow(np.linspace(lo, hi, 16).reshape(4, 4), aspect="auto")
        a.set_xlabel("Batch size")
        bars.append(fig.colorbar(im, ax=a, label="Accuracy", location="bottom"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, axes, aspect=1.0)
    assert not [w for w in caught if "overlap" in str(w.message) or "cut off" in str(w.message)]
    fig.canvas.draw()
    for a, bar in zip(axes, bars):
        panel, box = a.get_window_extent(), bar.ax.get_window_extent()
        assert abs(panel.x0 - box.x0) < 0.5 and abs(panel.x1 - box.x1) < 0.5
        assert abs(box.height / fig.dpi - paper.colorbar_width) < 1e-3
    ends = [t.get_window_extent() for bar in bars for t in bar.ax.get_xticklabels() if t.get_text()]
    assert all(not x.overlaps(y) for i, x in enumerate(ends) for y in ends[i + 1:])


def test_legend_full_size_inside_when_it_fits_and_above():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.plot([0, 1], [0, 0.1], label="Ours")
    ax.legend()
    finalize_figure(fig, ax)
    assert ax.get_legend().get_texts()[0].get_fontsize() == plt.rcParams["legend.fontsize"]
    full, fax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    for y in np.linspace(0, 1, 12):
        fax.plot([0, 0.5, 1], [y, 1 - y, y], label=f"Series {y:.2f}")
    fax.legend()
    finalize_figure(full, fax)
    legends = [*full.legends, *([fax.get_legend()] if fax.get_legend() else [])]
    assert legends[0].get_texts()[0].get_fontsize() == plt.rcParams["legend.fontsize"]


def test_legend_rows_write_the_shared_word_once_and_stay_in_the_canvas():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, WIDTH), layout="constrained")
    handles = [axes[0].plot([0, 1], [0, d])[0] for d in (4, 8, 16, 32, 64)]
    axes[1].plot([0, 1], [0, 1])
    axes[0].set_ylabel("Time at goal")
    legend = paper.legend_rows(fig, [("Depth", handles, [4, 8, 16, 32, 64])], loc="outside upper center", borderaxespad=0)
    finalize_figure(fig, axes)
    assert [t.get_text() for t in legend.get_texts()] == ["Depth", "4", "8", "16", "32", "64"]
    fig.canvas.draw()
    box = legend.get_window_extent()
    assert box.x0 >= paper.canvas_pad * fig.dpi - 0.5 and box.x1 <= (WIDTH - paper.canvas_pad) * fig.dpi + 0.5


def test_ramp_of_grey_stays_grey():
    for r, g, b in paper.ramp("#808080", 3):
        assert abs(r - g) < 1e-6 and abs(g - b) < 1e-6


def test_log_ticks_plain_with_si_suffix_above_1000():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.plot([1, 1e7], [1e-5, 10])
    ax.set_xscale("log")
    ax.set_yscale("log")
    finalize_figure(fig, ax)
    fig.canvas.draw()
    shown = lambda axis: {t.get_text() for t in axis.get_majorticklabels() if t.get_text()}
    assert {"1", "10", "100", "1000", "10K", "1M"} <= shown(ax.xaxis)
    assert "1e\u22124" in shown(ax.yaxis)


def test_group_y_label_measured_against_its_rows():
    fig, axes = plt.subplots(2, 1, figsize=(WIDTH, 2), layout="constrained", sharex=True)
    for a in axes:
        a.plot([0, 1], [0, 1])
    set_group_label(axes, "A label as long as two rows", axis="y")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, axes, aspect=0.3)
    assert not [w for w in caught if "longer than its panel" in str(w.message)]


def test_group_y_label_does_not_widen_the_row_gap():
    def gap(label):
        fig, axes = plt.subplots(2, 1, figsize=(WIDTH, 2), layout="constrained", sharex=True)
        for a in axes:
            a.plot([0, 1], [0, 1])
        set_group_label(axes, label, axis="y")
        finalize_figure(fig, axes, aspect=0.3)
        return axes[0].get_position().y0 - axes[1].get_position().y1
    assert gap("A label as long as two rows") == pytest.approx(gap("Short"), abs=1e-3)


def test_subfigure_legends_stand_above_their_own_group():
    fig = plt.figure(figsize=(6.75, 2), layout="constrained")
    left, right = fig.subfigures(1, 2)
    axes = [*left.subplots(1, 2, sharey=True), *right.subplots(1, 2, sharey=True)]
    for a in axes:
        a.plot([0, 1], [0, 1], label="Ours")
        a.plot([0, 1], [1, 0], label="Baseline")
    axes[0].set_ylabel("Accuracy")
    axes[2].set_ylabel("Tokens")
    for sf, a in ((left, axes[0]), (right, axes[2])):
        sf.legend(*a.get_legend_handles_labels(), loc="outside upper center", ncols=2)
    finalize_figure(fig, axes, aspect=0.618, column_gap=0.25)
    fig.canvas.draw()
    for sf, (a, b) in ((left, axes[:2]), (right, axes[2:])):
        box = sf.legends[0].get_window_extent()
        assert a.get_window_extent().x0 <= (box.x0 + box.x1) / 2 <= b.get_window_extent().x1
        assert box.y0 >= a.get_window_extent().y1


def test_legend_sticking_out_of_its_panel_warns():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2), layout="constrained")
    for a in axes:
        a.plot([0, 1], [0, 0.2], label="Average confidence over all samples")
    axes[0].legend(loc="upper left")
    with pytest.warns(UserWarning, match="sticks out of panel"):
        finalize_figure(fig, list(axes), min_width=0.9)


def test_legend_above_a_row_is_centred_over_it():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2), layout="constrained", sharey=True)
    for a in axes:
        a.bar([0, 1], [1, 2], label="Accuracy")
    axes[0].legend(loc="lower left", bbox_to_anchor=(0, 1), ncol=2)
    finalize_figure(fig, list(axes), min_width=0.9)
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
        finalize_figure(fig, ax)
    assert not any("covers a curve" in str(w.message) for w in caught)


def test_greys_skip_ours_lightness():
    ours = palette._lightness(paper.colors["ours"])
    for n in (2, 3, 4):
        assert all(abs(palette._lightness(g) - ours) >= 12 - 1e-6 for g in paper.baseline_greys(n))


def test_bars_alike_in_grayscale_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.bar([0], [1], color="#4477AA", label="A")
    ax.bar([1], [2], color="#228833", label="B")
    with pytest.warns(UserWarning, match="look alike in grayscale"):
        finalize_figure(fig, ax)


def test_legend_without_loc_takes_the_first_clear_spot():
    fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
    x = np.linspace(0, 1, 50)
    ax.plot(x, 1 - x, label="falling")
    ax.plot(x, 1 - x ** 2, label="bowed")
    ax.legend()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]
    box, panel = ax.get_legend().get_window_extent(), ax.get_window_extent()
    assert panel.x0 <= box.x0 and box.x1 <= panel.x1 and panel.y0 <= box.y0 and box.y1 <= panel.y1


def test_legend_without_loc_goes_above_when_no_spot_is_clear():
    fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
    ax.bar(range(6), [1, 1, 1, 1, 1, 1], width=1.0, label="full")
    ax.bar(range(6), [0.5] * 6, width=1.0, label="half")
    ax.set_ylim(0, 1)
    ax.legend()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, ax)
    assert not [w for w in caught if "legend" in str(w.message)]
    box, panel = ax.get_legend().get_window_extent(), ax.get_window_extent()
    assert box.y0 >= panel.y1 - 1


def test_crowded_bar_labels_turn_upward():
    fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
    x = np.arange(3)
    for i in range(4):
        bars = ax.bar(x + (i - 1.5) * 0.2, [0.612, 0.774, 0.806], 0.2)
        ax.bar_label(bars, labels=["0.612", "0.774", "0.806"], fontsize=paper.bar_label_size)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, ax)
    assert not [w for w in caught if "overlap" in str(w.message)]
    assert all(t.get_rotation() == 90 for t in ax.texts)


def test_bar_labels_with_room_stay_level():
    fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
    bars = ax.bar(np.arange(3), [0.6, 0.7, 0.8])
    ax.bar_label(bars, labels=["0.6", "0.7", "0.8"], fontsize=paper.bar_label_size)
    paper.finalize_figure(fig, ax)
    assert all(t.get_rotation() == 0 for t in ax.texts)


def test_height_search_skips_collapsed_layouts():
    # four titled panels under a figure legend: short trial heights collapse the layout, which must not count
    fig, axes = plt.subplots(1, 4, figsize=(5.5, 5.5), sharex=True)
    for a, title in zip(axes, ["CIFAR-10", "CIFAR-100", "CIFAR-10", "CIFAR-100"]):
        a.plot(np.arange(60), np.linspace(0, 1, 60), label="Ours")
        a.plot(np.arange(60), np.linspace(0, 0.9, 60), label="Baseline")
        a.set_title(title)
    axes[1].sharey(axes[0])
    axes[3].sharey(axes[2])
    axes[1].tick_params(labelleft=False)
    axes[3].tick_params(labelleft=False)
    axes[0].set_ylabel("Accuracy")
    axes[2].set_ylabel("Loss")
    fig.supxlabel("Epoch")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False, borderaxespad=0)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, axes, min_width=0.9)
    assert not caught, [str(w.message) for w in caught]
    fig.canvas.draw()
    legend_bottom = fig.legends[0].get_window_extent().y0
    assert all(legend_bottom >= a.title.get_window_extent().y1 for a in axes)
    assert all(a.title.get_window_extent().y1 <= fig.bbox.y1 for a in axes)


def test_ramp_spreads_one_hue_light_to_dark():
    shades = paper.ramp(paper.colors["series-1"], 5)
    lightness = [palette._lightness(c) for c in shades]
    assert lightness == sorted(lightness, reverse=True)
    assert all(a - b >= 10 for a, b in zip(lightness, lightness[1:]))



def test_shared_legend_moves_to_a_panel_with_room():
    fig, axes = plt.subplots(1, 2, figsize=(5.5, 2), layout="constrained")
    x = np.linspace(0, 1, 50)
    for name, offset in (("a", 0), ("b", 0.05), ("c", 0.1)):
        axes[0].plot(x, np.full_like(x, 0.5) + offset, label=name)
        axes[1].plot(x, x * 0.2 + offset, label=name)
    axes[0].fill_between(x, 0, 1, alpha=0.2, linewidth=0)  # a band over the whole first panel: no room there
    axes[0].legend()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, axes)
    assert not [w for w in caught if "legend" in str(w.message)]
    assert axes[0].get_legend() is None and axes[1].get_legend() is not None


def test_heatmap_values_shrink_to_fit_their_cells():
    fig, ax = plt.subplots(figsize=(2.4, 2.4), layout="constrained")
    values = np.arange(64).reshape(8, 8) * 12.345  # 8 columns of "777.7" do not fit at the value-label size
    ax.imshow(values, aspect="auto")
    for i in range(8):
        for j in range(8):
            ax.text(j, i, f"{values[i, j]:.1f}", ha="center", va="center")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, ax, aspect=1.0, min_width=0.7)
    assert not [w for w in caught if "overlap" in str(w.message)]
    sizes = {t.get_fontsize() for t in ax.texts}
    assert len(sizes) == 1 and sizes.pop() < matplotlib.rcParams["font.size"]


@pytest.mark.parametrize("width, columns, aspect", [(6.75, 4, 1.0), (4.4, 2, 1.0), (3.25, 1, 0.618), (6.08, 2, 0.618), (5.5, 1, 0.309)])
def test_default_aspect_follows_panel_width(width, columns, aspect):
    fig, axes = plt.subplots(1, columns, figsize=(width, width), layout="constrained", squeeze=False)
    for a in axes.flat:
        a.plot([0, 1], [0, 1])
    ratios = finalize_figure(fig, axes)
    assert ratios[0] == pytest.approx(aspect, rel=0.01)
