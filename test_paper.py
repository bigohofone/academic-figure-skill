import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest

ASSETS = Path(__file__).parent / "skills/paper-figure/assets"
sys.path.insert(0, str(ASSETS))
import paper
from paper import palette
from paper import finalize_figure, shift_lightness

WIDTH = 3.25


@pytest.fixture(autouse=True)
def style():
    with plt.rc_context():
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
    finalize_figure(fig, ax)
    assert fig.get_figwidth() == WIDTH
    assert paper.layout._panel_size(ax)[1] == pytest.approx(paper.panel_ratios["S"] * paper.layout._panel_size(ax)[0], rel=0.01)


def test_two_panels_shared_legend():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3))
    for ax in axes:
        ax.plot([0, 1], [0, 1], label="a")
        ax.plot([0, 1], [1, 0], label="b")
        ax.set_title("T")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside lower center", ncol=2,
               frameon=False, borderaxespad=0)
    check(fig, finalize_figure(fig, axes, _aspect=0.618), 0.618)


def test_grid_with_empty_cell():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 3))
    for ax in axes.flat[:3]:
        ax.plot([0, 1], [0, 1])
    axes[1, 1].axis("off")
    ratios = finalize_figure(fig, axes, _aspect=0.618)
    assert len(ratios) == 3
    check(fig, ratios, 0.618)


def test_heatmap_colorbar():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    im = ax.imshow(np.random.rand(5, 5), aspect="auto")
    fig.colorbar(im, ax=ax)
    check(fig, finalize_figure(fig, fig.axes, _aspect=1.0), 1.0)


def test_imshow_default_aspect_raises():
    fig, ax = plt.subplots(figsize=(WIDTH, 3))
    ax.imshow(np.random.rand(5, 5))
    with pytest.raises(ValueError, match="aspect='auto'"):
        finalize_figure(fig, ax, _aspect=1.0)


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
        check(fig, finalize_figure(fig, ax, _aspect=aspect), aspect)


def test_ticks_that_change_with_height_converge():
    fig, ax = plt.subplots(figsize=(3.0, 2))
    ax.bar(np.arange(3), [84, 92, 89], edgecolor="black")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(78, 95)
    finalize_figure(fig, ax)
    assert fig.get_figwidth() == 3.0
    assert paper.layout._panel_size(ax)[1] == pytest.approx(paper.panel_ratios["S"] * paper.layout._panel_size(ax)[0], rel=0.01)
    assert ax.get_ylim() == (78, 95)


def test_shared_axes():
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH, 3), sharex=True, sharey=True)
    for i, ax in enumerate(axes.flat):
        ax.plot([0, 1], [0, i + 1])
    check(fig, finalize_figure(fig, axes, _aspect=0.618), 0.618)


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


def test_shift_lightness_moves_one_stop_per_step():
    ours = palette._lightness(paper.colors["ours"])
    for stops in (-2, -1, 1, 2):
        assert palette._lightness(shift_lightness(paper.colors["ours"], stops)) == pytest.approx(ours + paper.design.shades["stop"] * stops, abs=0.5)


def test_fit_height_keeps_value_labels_inside():
    fig, ax = plt.subplots(figsize=(WIDTH, 2))
    ax.plot([0, 1, 2], [0, 1, 2])
    ax.annotate("2.0", (2, 2), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", gid="value-label")
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


def test_round_panels_fill_the_width_with_no_empty_height():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3))
    for ax in axes:
        ax.pie([3, 2, 1])
    finalize_figure(fig, axes, _aspect=1.0)
    circle = axes[0].get_position()
    assert fig.get_figheight() - circle.height * fig.get_figheight() < 0.1 + 2 * paper.canvas_pad
    assert circle.width * WIDTH > 0.45 * WIDTH


def test_polar_panel_is_fitted_without_error():
    fig, ax = plt.subplots(figsize=(WIDTH, 3), subplot_kw={"projection": "polar"})
    ax.plot([0, 1, 2], [1, 2, 3])
    finalize_figure(fig, ax, _aspect=1.0)
    assert fig.get_figheight() < WIDTH


def test_point_name_past_the_panel_is_reported_not_moved():
    def draw(name):
        fig, ax = plt.subplots(figsize=(WIDTH, 2))
        ax.plot([3, 72], [0.6, 0.8], "o")
        ax.set_xscale("log")
        if name:
            ax.annotate(name, (72, 0.8), xytext=(3, 3), textcoords="offset points")
        return fig, ax
    fig, ax = draw(None)
    finalize_figure(fig, ax)
    limits = ax.get_xlim()
    fig, ax = draw("Qwen2-72B-Instruct")
    with pytest.warns(UserWarning, match="sticks out of panel"):
        finalize_figure(fig, ax)
    assert ax.get_xlim() == pytest.approx(limits, rel=0.1)  # the margin follows the panel width, the name adds no room



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
    ratios = finalize_figure(fig, axes, _aspect=0.618)
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
        finalize_figure(fig, ax, _aspect=0.3)


def test_colorbar_as_tall_as_its_heatmap():
    fig, ax = plt.subplots(figsize=(WIDTH, WIDTH), layout="constrained")
    im = ax.imshow(np.arange(16).reshape(4, 4), aspect="auto")
    cbar = fig.colorbar(im, ax=ax, label="Accuracy")
    finalize_figure(fig, ax, _aspect=1.0)
    fig.canvas.draw()
    panel, bar = ax.get_window_extent(), cbar.ax.get_window_extent()
    assert abs(panel.y0 - bar.y0) < 0.5 and abs(panel.y1 - bar.y1) < 0.5


def test_colorbar_below_spans_all_panels_at_token_width():
    fig, axes = plt.subplots(1, 3, figsize=(6.75, 6.75), layout="constrained", sharey=True)
    for a in axes:
        im = a.imshow(np.arange(16).reshape(4, 4), aspect="auto", vmin=0, vmax=15)
    cbar = fig.colorbar(im, ax=axes, location="bottom", label="Accuracy")
    finalize_figure(fig, axes, _aspect=1.0, min_width=0.7)
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
        finalize_figure(fig, axes, _aspect=1.0, min_width=0.7)
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
    finalize_figure(fig, ax, _aspect=1.0)
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
        finalize_figure(fig, axes, _aspect=1.0)
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
    legend = paper.add_legend_rows(fig, [("Depth", handles, [4, 8, 16, 32, 64])], loc="outside upper center", borderaxespad=0)
    finalize_figure(fig, axes)
    assert [t.get_text() for t in legend.get_texts()] == ["Depth", "4", "8", "16", "32", "64"]
    fig.canvas.draw()
    box = legend.get_window_extent()
    assert box.x0 >= paper.canvas_pad * fig.dpi - 0.5 and box.x1 <= (WIDTH - paper.canvas_pad) * fig.dpi + 0.5


def test_ramp_of_grey_stays_grey():
    for r, g, b in paper.make_shades("#808080", 3):
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
    fig.supylabel("A label as long as two rows")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, axes, _aspect=0.3)
    assert not [w for w in caught if "longer than its panel" in str(w.message)]


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
        assert all(abs(palette._lightness(g) - ours) >= 12 - 1e-6 for g in paper.make_shades(paper.colors["neutral"], n))


def test_bars_alike_in_grayscale_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    ax.bar([0], [1], color="#4477AA", label="A")
    ax.bar([1], [2], color="#228833", label="B")
    with pytest.warns(UserWarning, match="look alike in grayscale"):
        finalize_figure(fig, ax)


def _series_shaded_by_compute(ax, styles):
    """Two methods drawn a checkpoint at a time, each checkpoint shaded by its compute (the RL/SFT/Init case)."""
    greys = paper.make_shades(paper.colors["neutral"], 4)
    for method, style, shades in (("SFT", styles[0], greys[1:]), ("Init", styles[1], greys[:1])):
        for k, color in enumerate(shades):
            ax.plot([k, k + 1], [k, k + 2], style, color=color, label=method)


def test_series_differing_only_in_a_lightness_already_spent_warn():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    _series_shaded_by_compute(ax, ["o-", "o-"])
    with pytest.warns(UserWarning, match=r"series 'SFT' and 'Init': share line style and marker, and 'SFT' already uses lightness"):
        finalize_figure(fig, ax)


def test_series_with_their_own_line_style_pass_though_lightness_is_spent():
    fig, ax = plt.subplots(figsize=(WIDTH, 2), layout="constrained")
    _series_shaded_by_compute(ax, ["o--", "o:"])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        finalize_figure(fig, ax)
    assert not any("series 'SFT'" in str(w.message) for w in caught)


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
        ax.bar_label(bars, labels=["0.612", "0.774", "0.806"])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        paper.finalize_figure(fig, ax)
    assert not [w for w in caught if "overlap" in str(w.message)]
    assert all(t.get_rotation() == 90 for t in ax.texts)


def test_bar_labels_with_room_stay_level():
    fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
    bars = ax.bar(np.arange(3), [0.6, 0.7, 0.8])
    ax.bar_label(bars, labels=["0.6", "0.7", "0.8"])
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
    shades = paper.make_shades(paper.colors["series-1"], 5)
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
        paper.finalize_figure(fig, ax, _aspect=1.0, min_width=0.7)
    assert not [w for w in caught if "overlap" in str(w.message)]
    sizes = {t.get_fontsize() for t in ax.texts}
    assert len(sizes) == 1 and sizes.pop() < matplotlib.rcParams["font.size"]


@pytest.mark.parametrize("width, rows, columns, height", [(3.25, 1, 1, "S"), (6.75, 1, 4, "M"), (6.75, 2, 3, "M"), (3.25, 3, 1, "XS"), (6.75, 1, 1, "3XS"), (3.25, 1, 1, "XL")])
def test_every_row_takes_its_height_step(width, rows, columns, height):
    fig, axes = plt.subplots(rows, columns, figsize=(width, width), layout="constrained", squeeze=False)
    for a in axes.flat:
        a.plot([0, 1], [0, 1])
    finalize_figure(fig, axes, height=height)
    for a in axes.flat:
        w, h = paper.layout._panel_size(a)
        assert h == pytest.approx(paper.panel_ratios[height] * w, rel=0.01)


def test_taller_panels_get_more_numeric_ticks():
    counts = {}
    for height in ("XS", "M", "XL"):
        fig, ax = plt.subplots(figsize=(WIDTH, WIDTH), layout="constrained")
        ax.plot([0, 1], [0, 1])
        finalize_figure(fig, ax, height=height)
        counts[height] = len([t for t in ax.get_yticks() if 0 <= t <= 1])
    assert 3 <= counts["XS"] <= counts["M"] <= counts["XL"] and counts["XS"] < counts["XL"]


def test_supylabel_takes_the_standard_left_margin():
    def left(sup):
        fig, axes = plt.subplots(2, 2, figsize=(WIDTH, WIDTH), layout="constrained", sharex=True, sharey=True)
        for a in axes.flat:
            a.plot([0, 1], [0, 100])
        if sup:
            fig.supylabel("Accuracy")
        else:
            axes[0, 0].set_ylabel("Accuracy")
        finalize_figure(fig, axes, _aspect=0.618)
        return axes[0, 0].get_position().x0
    assert left(True) == pytest.approx(left(False), abs=1e-3)


def test_problem_names_the_panel_and_the_fix():
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 2))
    axes[1].set_title("Loss")
    axes[1].bar([0], [1], color="#4477AA", label="A")
    axes[1].bar([1], [1], color="#4477AB", label="B")
    with pytest.warns(UserWarning, match=r"panel 2 of 2 'Loss', series 'A' and 'B': look alike in grayscale .*\. Fix: "):
        finalize_figure(fig, axes)


def test_a_registered_check_runs():
    def always(ctx):
        yield paper.checks.Problem("the figure", "is tested", "nothing")
    paper.checks.check(always)
    try:
        fig, ax = plt.subplots(figsize=(WIDTH, 2))
        ax.plot([0, 1], [0, 1])
        with pytest.warns(UserWarning, match="the figure: is tested. Fix: nothing"):
            finalize_figure(fig, ax)
    finally:
        paper.checks.CHECKS.remove(always)


def test_gaps_are_a_share_of_the_panel_size():
    row_gaps = {}
    for height in ("XS", "M"):
        fig, axes = plt.subplots(2, 2, figsize=(WIDTH, WIDTH), layout="constrained", sharex=True, sharey=True)
        for a in axes.flat:
            a.plot([0.1, 0.9], [0.1, 0.9])
        finalize_figure(fig, axes, height=height)
        p = [[a.get_position() for a in row] for row in axes]
        w, h = fig.get_figwidth(), fig.get_figheight()
        assert (p[0][1].x0 - p[0][0].x1) * w >= paper.panel_gap * p[0][0].width * w - 1e-6
        row_gaps[height] = (p[0][0].y0 - p[1][0].y1) * h
        assert row_gaps[height] >= paper.panel_gap * p[0][0].height * h - 1e-6
    assert row_gaps["M"] > row_gaps["XS"]

def test_m_makes_panels_as_tall_as_wide():
    fig, axes = plt.subplots(2, 4, figsize=(6.75, 6.75), layout="constrained")
    for a in axes.flat:
        a.plot([0, 1], [0, 2])
    finalize_figure(fig, axes, height="M")
    w, h = paper.layout._panel_size(axes[0, 0])
    assert h == pytest.approx(w, rel=0.01)


def test_long_tick_labels_narrow_the_panel_on_either_side():
    def panel_width(left_ticks, right_ticks):
        fig, ax = plt.subplots(figsize=(WIDTH, WIDTH), layout="constrained")
        ax.plot([0, 1], [0, 1])
        ax.set_yticks([0, 1], left_ticks)
        twin = ax.twinx()
        twin.plot([0, 1], [0, 1], "--", linewidth=paper.dashed_linewidth)
        twin.set_yticks([0, 1], right_ticks)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            finalize_figure(fig, ax)
        assert not [w for w in caught if "cut off" in str(w.message)]
        return paper.layout._panel_size(ax)[0]
    short = panel_width(["0", "1"], ["0", "1"])
    assert panel_width(["0", "A long name"], ["0", "1"]) < short
    assert panel_width(["0", "1"], ["0", "A long name"]) < short



def test_a_colorbar_keeps_the_height_of_the_figure_without_it():
    def panel(colorbar):
        fig, ax = plt.subplots(figsize=(WIDTH, WIDTH), layout="constrained")
        points = ax.scatter([0, 1, 2], [0, 1, 2], c=[0, 1, 2])
        ax.set_ylabel("Accuracy")
        if colorbar:
            fig.colorbar(points, ax=ax, label="Compute")
        finalize_figure(fig, ax, height="S")
        return paper.layout._panel_size(ax)
    (w0, h0), (w1, h1) = panel(False), panel(True)
    assert w1 < w0
    assert h1 == pytest.approx(h0, rel=0.01)
