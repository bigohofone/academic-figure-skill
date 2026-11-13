"""Every layout the skill supports, drawn with the current paper package and gathered on one page.

Run from anywhere: python examples/layouts/layouts.py
Writes docs/layouts/, the landing page's Layouts tab. Opened from disk or localhost, the page reloads
itself every 3 s, so it shows the latest run.
"""

import html
import sys
from concurrent.futures import ProcessPoolExecutor
import time
import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "docs/layouts"
sys.path.insert(0, str(HERE.parents[1] / "skills/academic-figure/assets"))
import paper
from paper import finalize_figure, make_part_colors, make_shades

colors = paper.colors
rng = np.random.default_rng(0)
steps = np.arange(0, 2600, 50)
SINGLE, DOUBLE = 3.25, 6.75


def curves(ax, gap=0.08):
    ours = 0.9 - 0.7 * np.exp(-steps / 500)
    ax.plot(steps, ours, color=colors["ours"], label="Ours")
    ax.plot(steps, ours - gap, "--", linewidth=paper.dashed_linewidth, color=colors["neutral"], label="Baseline")
    ax.set_xlabel("Training step")
    ax.set_ylabel("Accuracy")


def one_panel(height, width=SINGLE):
    fig, ax = plt.subplots(figsize=(width, width), layout="constrained")
    curves(ax)
    ax.legend()
    finalize_figure(fig, ax, height=height)
    return fig


def row(n, height, width=DOUBLE):
    fig, axes = plt.subplots(1, n, figsize=(width, width), layout="constrained", sharey=True)
    for i, ax in enumerate(axes):
        curves(ax, gap=0.03 * (i + 1))
        ax.set_title(f"Dataset {i + 1}")
        ax.set_xlabel("")
        if i:
            ax.set_ylabel("")
    axes[0].legend()
    fig.supxlabel("Training step")
    finalize_figure(fig, axes, height=height, min_width=0.45 if n > 3 else 0.9)
    return fig


def grid(rows, cols, width, height="M"):
    fig, axes = plt.subplots(rows, cols, figsize=(width, width), layout="constrained", sharex=True, sharey=True, squeeze=False)
    for (r, c), ax in np.ndenumerate(axes):
        curves(ax, gap=0.02 * (r + c + 1))
        ax.set_xlabel("")
        ax.set_ylabel("")
        if r == 0:
            ax.set_title(f"Benchmark {c + 1}")
    fig.supxlabel("Training step")
    fig.supylabel("Accuracy")
    axes[0, 0].legend()
    finalize_figure(fig, axes, height=height, min_width=0.45 if cols > 4 else 0.7)
    return fig


def stacked():
    fig, axes = plt.subplots(3, 1, figsize=(SINGLE, SINGLE), layout="constrained", sharex=True)
    for ax, name, scale in zip(axes, ["Loss", "Grad norm", "Entropy"], [3, 1.5, 0.8]):
        ax.plot(steps, scale * np.exp(-steps / 800) + 0.05 * rng.standard_normal(len(steps)), color=colors["series-1"])
        ax.set_ylabel(name)
    axes[-1].set_xlabel("Training step")
    finalize_figure(fig, axes, height="XS")
    return fig


def twin_axis():
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    ax.plot(steps, 3 * np.exp(-steps / 600) + 1, color=colors["series-1"], label="Loss")
    twin = ax.twinx()
    twin.plot(steps, np.minimum(steps / 500, 1) * 3, "--", linewidth=paper.dashed_linewidth, color=colors["series-4"], label="Learning rate")
    twin.grid(False)
    ax.set_zorder(twin.get_zorder() + 1)
    ax.patch.set_visible(False)
    ax.set_xlabel("Training step")
    ax.set_ylabel("Loss")
    twin.set_ylabel("Learning rate (×10⁻⁴)")
    ax.legend(*[sum(x, []) for x in zip(ax.get_legend_handles_labels(), twin.get_legend_handles_labels())])
    finalize_figure(fig, ax)
    return fig


def grouped_bars():
    methods, benchmarks = ["Base", "SFT", "Ours"], ["GSM8K", "MATH", "HumanEval"]
    values = np.array([[0.61, 0.32, 0.51], [0.77, 0.45, 0.64], [0.84, 0.53, 0.70]])
    fills = make_shades(colors["neutral"], 2) + [colors["ours"]]
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    x = np.arange(len(benchmarks))
    for i, (name, fill) in enumerate(zip(methods, fills)):
        bars = ax.bar(x + (i - 1) * 0.27, values[i], 0.27, color=fill, label=name)
        ax.bar_label(bars, labels=[f"{v:.2f}" for v in values[i]])
    ax.set_xticks(x, labels=benchmarks)
    ax.set_ylabel("Accuracy")
    ax.legend()
    finalize_figure(fig, ax, height="M")
    return fig


def horizontal_bars():
    names = [f"Model {chr(65 + i)}" for i in range(12)]
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    ax.barh(names, np.sort(rng.uniform(40, 80, 12)), color=colors["neutral"])
    ax.invert_yaxis()
    ax.set_xlabel("Win rate (%)")
    finalize_figure(fig, ax, height="L")
    return fig


def heatmap():
    values = rng.uniform(0.6, 0.8, (4, 5))
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    im = ax.imshow(values, aspect="auto")
    ax.set_xticks(range(5), labels=["16", "32", "64", "128", "256"])
    ax.set_yticks(range(4), labels=["1e−5", "3e−5", "1e−4", "3e−4"])
    for (i, j), v in np.ndenumerate(values):
        fill = im.cmap(im.norm(v))
        ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                color="white" if np.dot(fill[:3], [0.299, 0.587, 0.114]) < 0.5 else "black")
    ax.set_xlabel("Batch size")
    ax.set_ylabel("Learning rate")
    ax.grid(False)
    finalize_figure(fig, ax)
    return fig


def heatmap_colorbar(rows, cols):
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    im = ax.imshow(rng.uniform(0, 1, (rows, cols)), aspect="auto")
    ax.set_xticks(range(cols), labels=[f"L{i}" for i in range(cols)])
    ax.set_yticks(range(rows), labels=[f"H{i}" for i in range(rows)])
    ax.tick_params(length=0)
    ax.grid(False)
    ax.set_xlabel("Layer")
    ax.set_ylabel("Head")
    fig.colorbar(im, ax=ax, label="Attention weight")
    finalize_figure(fig, ax)
    return fig


def square_scatter():
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    for k, c in enumerate(["series-1", "series-4", "series-6"]):
        xy = rng.normal(k * 2, 0.8, (60, 2))
        ax.scatter(*xy.T, s=6, color=colors[c], alpha=0.5, label=f"Class {k + 1}")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend()
    finalize_figure(fig, ax)
    return fig


def stacked_area():
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    shares = rng.dirichlet([5, 2, 1], len(steps)).T
    ax.stackplot(steps, shares, colors=make_part_colors(3), labels=["Web", "Code", "Math"], alpha=0.875, edgecolor="white",
                 linewidth=plt.rcParams["grid.linewidth"])
    ax.set_xlabel("Training step")
    ax.set_ylabel("Share")
    ax.set_ylim(0, 1)
    fig.legend(loc="outside upper center", ncol=3)
    finalize_figure(fig, ax, height="M")
    return fig


def log_axis():
    sizes = np.logspace(7, 10, 8)
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    ax.plot(sizes, 4 * sizes ** -0.05, "o", color=colors["ours"])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Parameters")
    ax.set_ylabel("Loss")
    finalize_figure(fig, ax)
    return fig


def pie():
    fig, ax = plt.subplots(figsize=(SINGLE, SINGLE), layout="constrained")
    ax.pie([45, 25, 15, 10, 5], colors=make_part_colors(5), wedgeprops=dict(width=0.4, edgecolor="white"))
    finalize_figure(fig, ax)
    return fig


CASES = {
    "One panel, XS": lambda: one_panel("XS"),
    "One panel, S": lambda: one_panel("S"),
    "One panel, M": lambda: one_panel("M"),
    "One panel, L": lambda: one_panel("L"),
    "One panel, XL": lambda: one_panel("XL"),
    "One panel, full width, 2XS": lambda: one_panel("2XS", DOUBLE),
    "One panel, full width, 3XS": lambda: one_panel("3XS", DOUBLE),
    "Row of 2": lambda: row(2, "S"),
    "Row of 2, single column, M": lambda: row(2, "M", SINGLE),
    "Row of 3": lambda: row(3, "S"),
    "Row of 4, M": lambda: row(4, "M"),
    "Row of 5, M": lambda: row(5, "M"),
    "Row of 6, M": lambda: row(6, "M"),
    "Grid 2 × 1, single column, S": lambda: grid(2, 1, SINGLE, "S"),
    "Grid 2 × 2, single column": lambda: grid(2, 2, SINGLE),
    "Grid 3 × 2, single column": lambda: grid(3, 2, SINGLE),
    "Grid 2 × 3, full width": lambda: grid(2, 3, DOUBLE),
    "Grid 2 × 4, full width": lambda: grid(2, 4, DOUBLE),
    "Grid 2 × 8, full width": lambda: grid(2, 8, DOUBLE),
    "Grid 3 × 3, full width": lambda: grid(3, 3, DOUBLE),
    "Grid 4 × 4, full width": lambda: grid(4, 4, DOUBLE),
    "Grid 2 × 4, full width, S": lambda: grid(2, 4, DOUBLE, "S"),
    "Stacked 3 × 1": stacked,
    "Second y axis": twin_axis,
    "Grouped bars, M": grouped_bars,
    "Horizontal bars, L": horizontal_bars,
    "Heatmap, square cells": heatmap,
    "Heatmap 6 × 8, colorbar": lambda: heatmap_colorbar(6, 8),
    "Heatmap 8 × 4, colorbar": lambda: heatmap_colorbar(8, 4),
    "Embedding, square": square_scatter,
    "Stacked area, M": stacked_area,
    "Log axes": log_axis,
    "Pie": pie,
}

def describe(fig, panels):
    """The figure's types as labelled rows, read from what was drawn."""
    from matplotlib.collections import PathCollection, PolyCollection
    from matplotlib.patches import Wedge

    panels = [a for a in panels if not any(t is not a and t in panels[:panels.index(a)]
                                           and np.allclose(t.get_position().bounds, a.get_position().bounds) for t in panels)]
    a = panels[0]
    rows = len({round(p.get_position().y0, 3) for p in panels})
    cols = len({round(p.get_position().x0, 3) for p in panels})
    w, h = paper.layout._panel_size(a)
    step = [s for s, r in paper.panel_ratios.items() if abs(r * w - h) < 0.01]
    if any(isinstance(p, Wedge) for p in a.patches):
        height = "round"
    else:
        height = step[0] if step else ("square cells" if a.images else "square")
    lines = a.get_lines()
    chart = (["line"] * any(l.get_linestyle() not in ("None", "") for l in lines)
             + ["markers"] * any(l.get_marker() not in ("None", "", None) and l.get_linestyle() in ("None", "") for l in lines)
             + sorted({"bar" if c.orientation == "vertical" else "horizontal bar" for c in a.containers if hasattr(c, "orientation")})
             + ["heatmap"] * bool(a.images)
             + ["scatter"] * any(isinstance(c, PathCollection) for c in a.collections)
             + ["stacked area"] * any(isinstance(c, PolyCollection) for c in a.collections)
             + ["pie"] * any(isinstance(p, Wedge) for p in a.patches))
    axes = (["shared x"] * (len(a.get_shared_x_axes().get_siblings(a)) > 1)
            + ["shared y"] * (len(a.get_shared_y_axes().get_siblings(a)) > 1)
            + ["second y"] * any(t is not a and np.allclose(t.get_position().bounds, a.get_position().bounds) for t in fig.axes)
            + [f"log {x}" for x, scale in (("x", a.get_xscale()), ("y", a.get_yscale())) if scale == "log"]
            + ["colorbar"] * any(getattr(t, "_colorbar", None) is not None for t in fig.axes))
    labels = ["figure labels"] * bool(fig._supylabel and fig._supylabel.get_text()) + ["panel titles"] * any(p.get_title() for p in panels)
    legend = "above" if fig.legends else ("inside" if any(p.get_legend() for p in panels) else "none")
    return {
        "Column": "single" if fig.get_figwidth() <= SINGLE + 0.01 else "full",
        "Grid": f"{rows} × {cols}",
        "Height": height,
        "Chart": ", ".join(chart) or "—",
        "Axes": ", ".join(axes) or "—",
        "Labels": ", ".join(labels) or "—",
        "Legend": legend,
    }


def render(name):
    """Draw one case; return its card's HTML and a one-line report."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            fig = CASES[name]()
            file = name.lower().replace(",", "").replace(" × ", "x").replace(" ", "-") + ".png"
            fig.savefig(OUT / "img" / file, dpi=200)
            panels = [a for a in fig.axes if a.get_visible() and a.axison and getattr(a, "_colorbar", None) is None]
            pw, ph = paper.layout._panel_size(panels[0])
            image = f'<img src="img/{file}?v={time.time():.0f}" style="width:{fig.get_figwidth()}in">'
            tags = "".join(f"<span><i>{k}</i> {html.escape(v)}</span>" for k, v in describe(fig, panels).items() if v != "—")
            size = f"panel {pw:.2f} × {ph:.2f} in"
            fig_width = fig.get_figwidth()
        except Exception as error:
            size, image, fig_width, tags = "failed", f"<pre>{html.escape(repr(error))}</pre>", DOUBLE, ""
    notes = "".join(f"<li>{html.escape(str(w.message))}</li>" for w in caught)
    wide = ' class="wide"' if fig_width > SINGLE + 0.01 else ""
    card = (f'<figure{wide}>{image}<figcaption><b>{html.escape(name)}</b><div class="meta">{tags}</div></figcaption>'
            f'{f"<ul>{notes}</ul>" if notes else ""}</figure>')
    return card, f"{name}: {size}, {len(caught)} warnings"


if __name__ == "__main__":
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    start = time.time()
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(render, CASES))
    for _, line in results:
        print(line)
    cards = "".join(card for card, _ in results)
    (OUT / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>How layouts line up · academic-figure-skill</title>
<meta name="theme-color" content="#07080b">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{ --panel:#11141a; --bg:#07080b; --line:rgba(255,255,255,.08); --line2:rgba(255,255,255,.14); --ink:#f3f4f6; --ink2:#a9afbb; --ink3:#6e7583; --accent:#ff4d63;
  --page:{DOUBLE}in; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:17px/1.6 Inter, system-ui, sans-serif; -webkit-font-smoothing:antialiased; }}
a {{ color:inherit; }}
nav {{ position:fixed; top:16px; left:50%; transform:translateX(-50%); z-index:10; width:min(820px, calc(100% - 32px));
  display:flex; align-items:center; gap:22px; padding:8px 8px 8px 18px; border:1px solid var(--line2); border-radius:14px;
  background:rgba(12,14,19,.72); backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); }}
nav .logo {{ font-weight:700; text-decoration:none; white-space:nowrap; display:flex; align-items:center; gap:9px; }}
nav .logo i {{ width:18px; height:14px; border:2px solid var(--accent); border-radius:4px; display:inline-block; }}
nav .links {{ display:flex; gap:20px; margin-left:auto; font-size:14.5px; color:var(--ink2); align-items:center; padding-right:10px; }}
nav .links a {{ text-decoration:none; }} nav .links a:hover {{ color:var(--ink); }}
.sec-head {{ text-align:center; max-width:760px; margin:0 auto 46px; padding:150px 24px 0; }}
.label {{ display:inline-block; font:500 12.5px "JetBrains Mono", monospace; letter-spacing:.08em; text-transform:uppercase; color:var(--accent); margin-bottom:14px; }}
h1 {{ font-size:clamp(32px,5vw,58px); letter-spacing:-.04em; line-height:1.03; margin:0 0 16px; font-weight:800; }}
h1 em {{ font-style:normal; color:var(--ink3); }}
.intro {{ color:var(--ink2); font-size:18px; margin:0; }}
/* cards: the gap between them is the page's column gap less both paddings, so every image keeps its printed
   position and single-column and full-width figures line up edge to edge */
main {{ --p:0.0625in; margin:0 auto 110px; display:grid; grid-template-columns:repeat(2, calc({SINGLE}in + 2 * var(--p)));
  gap:calc({DOUBLE - 2 * SINGLE}in - 2 * var(--p)); row-gap:18px; width:calc(var(--page) + 2 * var(--p)); align-items:start; grid-auto-flow:row dense; }}
figure {{ margin:0; padding:var(--p); background:var(--panel); border-radius:14px; box-shadow:0 0 0 1px var(--line); }}
figure.wide {{ grid-column:1 / -1; }}
img {{ display:block; border-radius:8px; background:#fff; }}
figcaption {{ padding:12px 6px 6px; font-size:13px; line-height:1.45; color:var(--ink3); }}
figcaption b {{ color:var(--ink); font-weight:600; }}
.meta {{ display:flex; flex-wrap:wrap; justify-content:space-between; gap:2px 14px; margin-top:6px; font:12px/1.5 "JetBrains Mono", monospace; color:var(--ink2); }}
.meta i {{ font-style:normal; color:var(--ink3); }}
ul {{ margin:6px 0 0; padding-left:16px; color:var(--accent); font-size:12.5px; }}
footer {{ padding:0 0 90px; color:var(--ink3); font-size:14px; }}
footer div {{ max-width:1180px; margin:0 auto; padding:28px 24px 0; border-top:1px solid var(--line); display:flex; justify-content:space-between; flex-wrap:wrap; gap:18px; }}
footer a {{ text-decoration:none; }} footer a:hover {{ color:var(--ink); }}
</style></head><body>
<nav><a class="logo" href="../"><i></i>academic-figure-skill</a>
<div class="links"><a href="../#examples">Examples</a>
  <a href="https://github.com/bigohofone/academic-figure-skill" target="_blank" rel="noopener" style="padding-right:10px">GitHub</a></div></nav>
<div class="sec-head"><span class="label">How layouts line up</span><h1>How layouts line up</h1>
<p class="intro">Every layout the skill draws, at print size on a two-column page: edges line up across figures. Updated {time.strftime("%Y-%m-%d %H:%M")}.</p></div>
<main>{cards}</main>
<footer><div><span>academic-figure-skill · MIT license</span><span><a href="https://github.com/bigohofone/academic-figure-skill">GitHub</a></span></div></footer>
<script>if (location.protocol === "file:" || location.hostname === "localhost") setTimeout(() => location.reload(), 3000);</script>
</body></html>
""")


