---
name: paper-figure
description: Makes publication-ready figures for academic papers with matplotlib or seaborn, following a DESIGN.md design system (venue widths, print-size type, color-blind-safe colors, chart-type rules) - one script per figure with a paper-style caption. Use it when creating or editing a figure, plot or chart meant for a paper (ICML, CVPR, ACL, NeurIPS, ICLR or any paper), even if only the plotting code is asked for. Not for quick exploratory plots, notebooks, dashboards or slides.
---

# Paper Figures

- Goal: one message at a glance, in print
- `DESIGN.md`: how figures look
- This file: how to work
- Every rule applies unless the user says otherwise

**Prepare → Plan → Write → Run → Check**

## 1. Prepare

Ask the user first. Skip what the request already says.

| Ask | Answer |
|---|---|
| Page size | text and column widths, or a venue name looked up in DESIGN.md Width |
| Column span | single, 1.5 or double |

Then, in one turn:

- Run setup
- Print the data's structure
- Read `figures/DESIGN.md`

Folder: the one the user names, else `figures/` in the user's project.

```
{project}/
└── figures/
    ├── {id}.py      # one script per figure, caption as docstring
    ├── DESIGN.md    # the design; edit to restyle every figure
    ├── style/paper/ # helpers, style, fonts
    └── outputs/     # {id}.pdf, {id}.png
```

Setup, from `{project}/`. `{skill-dir}` is this skill's folder; `-n` keeps a design the user changed.

```bash
mkdir -p figures/style figures/outputs
cp -n {skill-dir}/assets/DESIGN.md figures/
cp -Rn {skill-dir}/assets/paper figures/style/
```

- Requires Python 3.10+, matplotlib 3.10+, numpy 2+, pyyaml, scipy for density curves
- Missing one: ask before installing

## 2. Plan

Before any code, think it through like a person would, and write the answers as a short list.

1. **What is each number?** A reported result or a diagnostic:

| Kind | Example | On the plot |
|---|---|---|
| Reported result | accuracy, F1, latency | value written when the takeaway compares it |
| Diagnostic | loss, gradient norm, entropy per step | trend only, no value labels |
| Both | validation accuracy per epoch | value at the compared point only |

2. **What should the reader take away?** One sentence with a number from the data. It becomes the caption's last sentence.
3. **What does that sentence point at?** Its subject is the emphasis: ours, a gap, a point, a change along x.
4. **Which chart shows it?** From DESIGN.md's chart type table: compare, trend, distribution, parts of a whole, a point.
5. **How does the emphasis stand out in that chart?** Color by DESIGN.md Colors; panel height as a share of its width, 3XS to XL (M square), by DESIGN.md Panel height, unless the chart fixes its shape.
6. **What must the reader tell apart?** Every variable the marks differ by (method, split, compute, seed), each with its own channel: hue, lightness, line style, marker, or panel. One variable per channel, by DESIGN.md Colors (One channel per variable). Write it as a table: variable → channel. Every value of every variable named in the legend or on the plot.

**One figure, one takeaway.** More than one: one script each.

Then read:

- `{skill-dir}/references/{type}.md` for each chart type
- `multi-panel.md` for several panels or a second y axis
- Each whole, once, with the Read tool, not `cat`

## 3. Write

One script, written once, from the plan: `{project}/figures/{id}.py`, kebab-case id.

```python
"""Test accuracy versus training steps on CIFAR-10. Shaded bands show ±1 std over 3 seeds; ..."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "style")
import paper  # applies figures/DESIGN.md
from paper import finalize_figure, make_shades, shift_lightness

colors = paper.colors  # colors["ours"], colors["neutral"], ...

...  # data, plot

finalize_figure(fig, ax)
fig.savefig("outputs/{id}.pdf")
fig.savefig("outputs/{id}.png")
```

**Data from the project's files.** Paths relative to `figures/`. Inline numbers only when there is no file.

```python
# do
runs = json.load(open("../results/runs.json"))
# don't
runs = {"Ours": [0.61, 0.72, 0.84], "Baseline": [0.58, 0.66, 0.79]}
```

**Numbers computed, not typed.** Every number on the plot and in the caption. Every given point drawn.

```python
# do
ax.annotate(f"{best:.1%}", ...)
# don't
ax.annotate("84.2%", ...)
```

**Takeaway printed and asserted.** If the data doesn't support it, tell the user. Don't draw around it.

```python
best = {name: max(curve) for name, curve in runs.items()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()})
assert best["Ours"] > max(v for name, v in best.items() if name != "Ours"), "the takeaway does not hold"
```

**Sizes from the design.** Never write a size, width or color by hand.

```python
# do
ax.plot(x, y, "o-", color=colors["ours"])
ax.plot(x, y, "--", linewidth=paper.dashed_linewidth, color=colors["neutral"])
# don't
ax.plot(x, y, "o-", color="#D55E00", linewidth=1.5, markersize=4)
```

**Placement left to `finalize_figure`.** No `loc` on panel legends, bar values level, no manual margins. It turns crowded bar values upward. The style saves the figure with a transparent background, so it sits on the paper's page: never pass `facecolor` or `transparent=False`.

```python
# do
ax.legend()
ax.bar_label(bars)
finalize_figure(fig, ax)
# don't
ax.legend(loc="upper left")
ax.bar_label(bars, rotation=90)
fig.subplots_adjust(left=0.15)
fig.savefig(..., bbox_inches="tight")
```

**Every mark labelled with its series.** `label=name` on each line, point, bar and band of a series, also when one series is drawn as many artists and the legend is built from handles: `finalize_figure` reads the labels to check that series stay apart.

```python
# do
for run in runs[method]:
    ax.plot(run["x"], run["y"], linestyle=styles[method], color=shade(run), label=method)
ax.legend(handles, names)
# don't
ax.plot(run["x"], run["y"], color=shade(run))  # unlabelled: no check sees it
```

**Plain code, top to bottom.** At most a loop over series.

```python
# do
for name, curve in runs.items():
    ax.plot(steps, curve, color=series_colors[name], label=name)
# don't
def plot_series(ax, runs, style_map): ...
```

Helpers in `paper`:

| Helper | Use |
|---|---|
| `finalize_figure(fig, axs, height="S", min_width=0.9)` | call last: panel height, ticks, layout, checks |
| `shift_lightness(color, stops)` | lighter or darker by stops, −2 to +2: −1 for series text, +2 for box fills |
| `make_shades(color, n)` | n shades light to dark: a sweep, or greys for compared series |
| `make_part_colors(n)` | n colors for the parts of one whole |
| `add_legend_rows(parent, [(name, handles, settings)], **kwargs)` | legend rows like "Depth 4 8 16" |
| `paper.dashed_linewidth`, `.highlight_markersize`, … | token values |

Caption, as the docstring:

- Paper's language, English by default
- Present tense, plain text, Unicode for ±, ×, α
- Stands alone, one sentence per part
- Unknown details as `[TODO: …]`

| Part | Content |
|---|---|
| Lead | what the figure shows; bold in the paper |
| Reading guide | bands, dashed lines, outlines, log axes; skip if none |
| Takeaway | the planned takeaway with its printed number |

> Test accuracy versus training steps on CIFAR-10. Shaded bands show ±1 std over 3 seeds; the dashed line marks the best baseline's final accuracy. Ours reaches it after 12k steps, 2.1× faster.

## 4. Run

```bash
cd figures && python {id}.py && pdffonts outputs/{id}.pdf
```

- Project's Python, from `figures/`
- No pdffonts: `grep -ac /Type3 outputs/{id}.pdf` must print 0
- Fix all warnings by DESIGN.md in one edit, then rerun
- No trial loops, no temp scripts

## 5. Check

| Check | Pass |
|---|---|
| Warnings | none left |
| Numbers | assert passes; caption matches the printout; derived numbers like ECE named as computed |
| Fonts | `CID TrueType`, emb `yes` |
| Look | PNG once at printed size, pixel width / 300 in; emphasis seen first; value labels at compared points; colors and legend per DESIGN.md and chart file |

Reply: what changed, any `[TODO]`.
