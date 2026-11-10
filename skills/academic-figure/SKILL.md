---
name: academic-figure
description: Makes publication-ready figures for academic papers with matplotlib or seaborn - sizing to the venue's column width, print typography, color-blind-safe colors, value labels where the paper makes its claim, a paper-style caption - delivered as cells in `figures/figures.ipynb` in the user's project. Use it whenever creating or editing any figure, plot, graph, chart, heatmap or visualization for a paper, even if no venue (ICML, CVPR, ACL, NeurIPS, ICLR) is mentioned and even if the user asks only for the plotting code.
---

# Paper Figure Rules

Goal: a figure that reads well printed in the paper, where the reader gets its one message at a glance. Apply every rule unless the user says otherwise. A figure is delivered when its cell is in the notebook with its caption and has run.

Steps, in order:

1. **Takeaway**: work out what the paper uses this figure to show (from the user's request, the paper text or caption, the figure's role), then write it as one sentence with a number from the data. It sets the value labels (§3) and becomes the caption's takeaway (§7).
2. **Size**: width, grid and aspect (§1).
3. **Draw**: base style (§2), lines and text (§3), plot type (§4), color (§5), legend (§6).
4. **Save, caption, notebook** (§7, §8), then **check** (§9).

## 1. Size

### Width

| Venue | Single column | 1.5 column | Double column |
|---|---|---|---|
| ICML | 3.25 in | 5.0625 in | 6.75 in |
| CVPR | 3.25 in | 5.15625 in | 6.875 in |
| ACL (ARR) | 3 in | 4.6875 in | 6.25 in |
| NeurIPS | – | – | 5.5 in |
| ICLR | – | – | 5.5 in |

- Use the width the user names. Otherwise: the venue's single column (NeurIPS/ICLR: 5.5 in); with no venue, ICML single column.
- 1.5 column (0.75 × double) is a `figure*` narrower than the text: use it when the user asks, or when single column is too narrow and double column leaves the content sparse.

### Grid

| Width | Max cols |
|---|---|
| Single column | 2 |
| 1.5 column | 3 |
| Double column | 4 |

1. Start with every panel in one row, up to the width's column limit: a single column holds two panels side by side, and panels the reader compares (two problems, two settings) stay side by side, as in the paper being redrawn.
2. Render. `fit_height` warns when a panel's data area (inside the box) is narrower than 1.2 in, or when tick labels, titles or axis labels are cut off or overlap.
3. On such a warning, first free room inside the row: share the y axis when the panels plot the same quantity (step 5), turn long text tick labels 45° (§2), shorten labels. Only when a panel is still narrower than 1.2 in, add a row and set the columns to ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 1 × 4 → 2 × 3), then render again. Rows have no limit.
4. Turn off unused cells (5 panels in 2 × 3: the last cell).
5. When panels plot the same quantity over the same range on an axis, share it (`plt.subplots(..., sharex=True, sharey=True)`). Every panel keeps its tick numbers, since sharing hides them on inner panels: `ax.tick_params(labelleft=True, labelbottom=True)` on each panel.
6. Each axis quantity is labelled once per row or column of panels, shared axis or not: panels side by side that plot the same quantity on y carry the y label on the leftmost panel only, and panels stacked that plot the same quantity on x carry the x label on the bottom panel only. When a whole row of panels shares one x label, write it once under the row with `fig.supxlabel(label)` (`fig.supylabel` for one y label down a column). A panel whose quantity differs from its neighbours' carries its own label. Embeddings and heatmaps with category axes have none.

### Panel aspect

The aspect (width : height) is per panel. Use one of these, golden ratio φ : 1 by default:

| Aspect | `aspect=` | Fit |
|---|---|---|
| φ² : 1 | 0.382 | a single panel at 1.5- or double-column width |
| φ : 1 | 0.618 | curves, bars, histograms (default) |
| 1 : 1 | 1.0 | heatmap, confusion matrix, embedding |
| 1 : φ | 1.618 | content taller than wide (box plots, panels side by side in one column) |

Slopes and gaps between curves need height, many x categories need width, matrices need square cells. If curves look flat after rendering, pick a taller aspect. The aspect follows the data, never room for labels: a value label that covers a curve goes below the point (`below=True`), and if it still covers one, the comparison uses another point whose label stands clear.

### Height

Let `fit_height` set it. Create the figure at the target width with any height, draw everything (labels, legend, colorbar), call `fit_height` last, then save with plain `fig.savefig`:

```python
fig, axes = plt.subplots(2, 1, figsize=(3.25, 2), sharex=True)
...  # plot, labels, legend, colorbar
fit_height(fig, axes, aspect=0.618)
fig.savefig("{id}.pdf")
```

- `ax` may be one Axes, an array, a list, or the `subplot_mosaic` dict; hidden cells and colorbars are skipped.
- `fit_height` also keeps every `mark_value` label and every bar label (`ax.bar_label`) inside its panel: it raises the y-limit to make room (the x-limit for horizontal bars), and turns `mark_value` labels at a side edge inward.
- On `ValueError` (fixed aspect), draw images with `imshow(..., aspect="auto")`.
- On the "different widths" warning, give all panels the same width (plain grid, equal columns).

## 2. Base style

Start every figure with the bundled style, copied into the project's `figures/` (§8). In the notebook, which runs from `figures/`:

```python
import tol_colors as tc
from paper import fit_height, mark_value, smooth, darken  # importing paper registers the bundled Inter font
plt.style.use("paper.mplstyle")
```

It needs `tol-colors` (Python 3.10+). If it is missing, tell the user and ask before installing it.

| The style sets | |
|---|---|
| Text | Inter for all text and math; titles and row/column headers 11 pt, tick labels 7 pt, everything else (axis labels, legends, value labels) 9 pt |
| Axes | a full box, black, 0.5 pt; ticks 0.5 pt, 1.5 pt long (minor 1 pt); tick labels 1.75 pt from the ticks, axis labels 1 pt from the tick labels |
| Grid | both directions, black at 10% opacity, 0.5 pt, behind the data |
| Lines, markers | lines 1 pt, dashed lines 0.75 pt; hollow markers, size 2.25 with a 0.75 pt edge |
| Color | Paul Tol `bright` cycle, `tol.iridescent` colormap |
| Layout | constrained layout: panels sit as close as their labels allow, with 0.02 in of white space on each side |
| Output | 300 dpi; `pdf.fonttype: 42` (text stays text, Inter embedded) |

- Keep these values as they are; the style is tuned for print.
- Name panels with axes titles: in reading order, prefix each with its letter, `"(a) Accuracy on AIME"`, `"(b) …"`. A single panel has no title unless it needs one (dataset, setting). The figure itself has no title; the caption names it.
- Grids of two factors (models × benchmarks, methods × datasets): name each row and column once instead of each panel, and either factor may be the rows. Headers are 11 pt, like panel titles. Column headers are the top row's axes titles (`ax.set_title(col_name)`); row headers go left of the first column's y-label: `axes[r, 0].annotate(row_name, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0), textcoords="offset points", ha="right", va="center", rotation=90, fontsize=11)`. Such panels carry no letters; the caption names a panel by its row and column.
- Keep matplotlib's default axis limits and margins; `fit_height` makes room for value labels (§1, Height).
- Numeric tick labels are horizontal plain numbers (`1, 2, 4, 8`, never rotated, never `2³`). When `fit_height` reports overlapping numeric tick labels, use fewer ticks in that panel (every other one), not smaller text or rotation.
- Text tick labels (categories, bins, method names) that don't fit side by side turn 45°: `ax.set_xticks(x, labels=names, rotation=45, ha="right", rotation_mode="anchor")`. Keep the panels side by side and the bins on the x-axis rather than switching to horizontal bars or stacked panels to avoid the rotation.
- Log₂ axes (number of samples, batch size, model size): `ax.set_xscale("log", base=2)`, a tick at every power of 2 up to the first one at or above the largest x (`top`) with `ax.set_xticks(ks, labels=[str(k) for k in ks])`, and no minor ticks (`ax.set_xticks([], minor=True)`). The axis ends at `top` with the usual 5% margin, so every panel ends on a labelled tick: `margin = 2 ** (0.05 * math.log2(top))`, `ax.set_xlim(1 / margin, top * margin)`. Where those labels overlap, step by 4 (`1, 4, 16, 64`).
- Category axes (bar charts, text tick labels): hide the tick marks on that axis with `ax.tick_params(axis="x", length=0)` (`axis="y"` for horizontal bars), on every panel.

## 3. Lines and text

Every plotted quantity is one of two kinds; decide which before drawing:

- **Reported results**: the numbers the paper claims, measured once per setting (accuracy, F1, latency, throughput, error rate, a score per method). Readers compare them exactly.
- **Diagnostics**: quantities logged along a process to show its behavior (loss, gradient norm, entropy, temperature, queue length per iteration). Readers read their trend and shape.

### Lines

- Curves are plain lines; add markers (the style's hollow markers) only when the user asks. Then each series gets its own marker shape, in series order: `"o"`, `"s"`, `"^"`, `"D"`, `"v"`, `"P"`, the same shape for a series in every panel.
- Diagnostics, however often they were logged: draw the raw values in the series color at `alpha=0.25` without a label, then `smooth(values)` on top with the label, and add to the caption: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- Reported results are drawn raw.
- Several runs per setting (seeds, folds, trials): draw the mean as the line and a band of ±1 std with `ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)`, and say in the caption what the band is and over how many runs.
- Reference lines (a baseline's score, a threshold): `ax.axhline(..., linestyle="--", linewidth=0.75, zorder=1)` in #BBBBBB, fully opaque, named by a legend entry. Compared values get their lines from `mark_value` (Value labels below).
- Log axis (`ax.set_yscale("log")`, named in the caption) when values span more than two orders of magnitude and the message is about differences among the small values. When the message is the change in size itself, keep the linear axis.

### Value labels

When the takeaway compares reported results across series, write them on the plot so the reader can read them exactly. Diagnostics carry no value labels; their curves already show the trend. Neither do distributions (histograms, box plots): their shape is the message, and the caption gives the numbers.

- Find the point where the paper makes the comparison: the claim decides it. "Ours reaches a higher score" compares each series' best; "ours ends higher" compares final values (at the last x all series share, when they end at different x); "ours is ahead at the same budget" compares values at that shared x. The value is the plotted metric at that point.
- If the request and the paper don't settle the comparison point, ask the user. When you can't ask, compare each series' best and say so in the reply.
- Write each value with three significant figures.
- Mark each value there with `mark_value(ax, x, y, "0.438", color)`: a 0.75 pt dashed line in `darken(color)` across the whole panel at that value, under the curves; a circle on the point; and the value in bold just above it. One per compared series, in the panels the takeaway is about. The lines let the reader compare heights anywhere in the panel.
- If a label above the point covers a curve, put it below with `below=True`.
- Bar charts of reported results: label every bar (§4).

### Other text

- Text that belongs to one series (labels, annotations) uses `darken(series_color)`. Titles, axis labels, ticks and legend text are black.

## 4. Plot type

Every plot type uses the same parts as lines: the style's full black box, data lines 1 pt, black outlines and edges 0.75 pt (box plots get theirs from the style), dashed lines 0.75 pt, and points as the style's markers (2.25 pt, 0.75 pt edge). Fills take the series color at full opacity, except bands and scatter clouds.

- **Line**: `ax.plot(x, y, color=color)`; markers only on request (§3). Gridlines in both directions (style).
- **Bar** (reported results, one bar per category on the x-axis): `bars = ax.bar(x, values, width, color=color, linewidth=0)`, grouped bars sharing 0.8 of each slot (`width = 0.8 / n_series`), every bar labelled with `ax.bar_label(bars, fontweight="bold")`. Horizontal gridlines only: `ax.grid(axis="x", visible=False)`. For several groups (benchmarks, datasets), one panel per group, titled with the group. Over several runs, error bars of ±1 std, named in the caption: `ax.bar(..., yerr=std, capsize=2, error_kw=dict(elinewidth=0.75, capthick=0.75, ecolor="black"))`.
- **Horizontal bar**: only for unordered categories with long names. As bars, with `ax.barh` and vertical gridlines only: `ax.grid(axis="y", visible=False)`.
- **Stacked bar**: segments in series order from the bottom with white 0.5 pt seams, `ax.bar(x, v, bottom=below, color=color, edgecolor="white", linewidth=0.5)`; horizontal gridlines only.
- **Histogram**: raw values as touching bars, `ax.hist(values, bins=bins, color=color, linewidth=0)`; several series on one axis as outlines, `histtype="step", linewidth=1`. Counts per bin (e.g. accuracy intervals) as grouped bars with the bins in order on the x-axis, never horizontal bars. No value labels (§3); horizontal gridlines only.
- **Box plot**: `box = ax.boxplot(values, positions=[x], widths=0.7, showfliers=False)` (the box fills 0.7 of its slot), filled with its series color, `box["boxes"][0].set_facecolor(color)`; the style draws the black outline, whiskers, caps and median. With under ~30 points per box, show every point on top, jittered within the box, as the style's markers in black on white: `ax.plot(x + rng.uniform(-0.2, 0.2, len(values)), values, "o", color="black", markerfacecolor="white", linestyle="none")`. Horizontal gridlines only.
- **Violin**: `parts = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)`; fill the body with its series color at full opacity with a black 0.75 pt edge (`body = parts["bodies"][0]`, `body.set_facecolor(color)`, `body.set_edgecolor("black")`, `body.set_linewidth(0.75)`, `body.set_alpha(1)`), and draw the median as a black 1 pt line across it; points as in box plots. Horizontal gridlines only.
- **Scatter**: `ax.scatter(x, y, s=5, color=color, edgecolors="none", alpha=0.5)`, dots the size of the style's markers, translucent so dense regions read darker. Gridlines in both directions.
- **Embedding** (t-SNE, UMAP): as scatter, with ticks hidden and no gridlines (`ax.grid(False)`).
- **Heatmap, confusion matrix**: `ax.imshow(..., aspect="auto")`, tick marks hidden, no gridlines (`ax.grid(False)`), a colorbar for continuous values; cell text 7 pt in `"white" if np.dot(im.cmap(im.norm(v))[:3], [0.299, 0.587, 0.114]) < 0.5 else "black"`.
- **Pie chart**: draw a bar chart instead.
- Many exact numbers with no trend or comparison to see (e.g. every method on every dataset): suggest a table to the user instead of a figure.

## 5. Color

Paul Tol's color-blind-safe `bright` set, from `tol_colors` (`tc`): `cset = tc.colorsets["bright"]`, then colors by name (`cset.red`). The same set across the whole paper, so a method keeps its color in every figure.

| Case | Color |
|---|---|
| Single series | `cset.blue` |
| Categorical | blue, red, green, yellow, cyan, purple, in this order |
| "Ours" (the proposed method among baselines or ablations) | `cset.red`; the others take the categorical order without red. Without such a series, use the categorical order. |
| Neutral, baselines, reference lines | `cset.grey` (#BBBBBB) |
| Grouped (sizes, sweeps) | one color per group; within a group blend with white at 40 / 70 / 100 %, light → dark |
| Sequential (heatmap) | `cmap="tol.iridescent"`; few levels: `tol.YlOrBr_discrete` |
| Signed (heatmap) | `cmap="tol.sunset"` centered at 0 (symmetric `vmin`/`vmax`); few levels: `tol.sunset_discrete` |

- More than six series: group them (one color per group, shades within) or split them into panels.
- Series are told apart by color with solid fills. When color alone can't separate them (grayscale printing, close shades), also vary line style.
- Grey lines, series and bands are #BBBBBB at full opacity; grey text is `darken("#BBBBBB")`.
- Emphasis, when the user names a series to emphasize: that series is `cset.red`, every other series #BBBBBB (bands too), told apart by line style.
- Custom colors (hex codes, a brand palette, "match the original"): use them for the data series, defined once in the setup cell as a dict (`PALETTE = {"ours": "#5F16A7", "base": "#63C9D2"}`); everything else keeps the style. If some are very light (cyan, yellow), tell the user they read weakly on white.

## 6. Legend

| Case | Legend |
|---|---|
| One panel, or several panels with the same series | one legend for the figure, placed by the first of these that covers no data: (1) a corner of a panel, tried in the order `loc="upper left"`, `"upper right"`, `"lower left"`, `"lower right"`, in the first panel that has one free; (2) another free spot inside a panel (`"upper center"`, `"lower center"`, `"center left"`, `"center right"`); (3) outside, above the panels: `fig.legend(loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)` |
| Panels with different series | one per panel, placed inside that panel in the same order; outside, it goes above the panel's title: `ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=2, frameon=False)` |
| Grouped series | rows = groups, columns = variants |
| One series per panel | none; the title names it |

- Always pass an explicit `loc`, never `"best"`. `fit_height` warns when a legend covers a curve, a bar or a box; on that warning, try the next spot.
- Entry order: "ours" first, then the other series in color order, reference lines last.

## 7. Save and caption

- Save `{id}.pdf` and `{id}.png` (kebab-case id) into `figures/` with relative paths. The style embeds fonts as TrueType, which venues accept; keep text as text.
- LaTeX line for the reply: single column → `figure`, `width=\columnwidth`; 1.5 column → `figure*`, `width=0.75\textwidth`; double → `figure*`, `width=\textwidth`.

The caption is written as it appears under the figure in the paper, in the paper's language (default English), and stands alone:

| Part | Content |
|---|---|
| Lead (bold) | what the figure shows, one short sentence |
| Reading guide | encodings the axes and legend don't explain: bands (±1 std over N seeds), dashed lines, panels by letter, log scale |
| Takeaway | the takeaway from step 1, with its number |

- One sentence per part (skip the reading guide when there is nothing to explain), present tense, plain text with Unicode (±, ×, α).
- Unknown details become `[TODO: …]` and go in the reply.

> **Figure 1: Test accuracy versus training steps on CIFAR-10.** Shaded bands show ±1 std over 3 seeds; the dashed line marks the best baseline's final accuracy. Ours reaches it after 12k steps, 2.1× faster.

## 8. Notebook (required)

All figure work happens in `figures/` at the root of the user's project, even for one figure or a script-only request. The user runs, edits and re-exports figures there, without this skill, so each cell is plain, readable code.

```
figures/
├── paper.py, paper.mplstyle, Inter-*.ttf, Inter-LICENSE.txt   # copied from {skill-dir}/assets/
├── figures.ipynb
└── {id}.pdf, {id}.png
```

- `{skill-dir}` is this skill's base directory. Copy with `cp -n {skill-dir}/assets/{paper.py,paper.mplstyle,Inter-*} figures/`, which keeps copies already there. The notebook uses only these copies.

| Cell | Content |
|---|---|
| First (code, once) | `%matplotlib inline`, `%config InlineBackend.print_figure_kwargs = {"bbox_inches": None}`, `%config InlineBackend.figure_formats = ["retina"]`, imports, the §2 setup |
| Per figure (markdown) | `## {id}`, then the caption |
| Per figure (code) | everything for that figure: load data, plot, `fit_height`, save PDF + PNG, `plt.show()` |

- Each figure cell runs on its own after the setup cell.
- Load data from the project's result files (paths relative to `figures/`); write numbers inline only when there is no file.
- Write the notebook yourself, top to bottom, the way a person would: create `figures/figures.ipynb` with `Write` as an empty notebook, then add each cell with `NotebookEdit` (insert after the last cell), and fix a cell by replacing it with `NotebookEdit`. The same `id` replaces its two cells; a new id appends two cells. If `NotebookEdit` is a deferred tool, load it first.

  ```json
  {"cells": [], "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
  ```

- Write each code cell as a person would write it by hand: top to bottom, plain matplotlib calls, data and labels spelled out where they are used. Use the `paper` helpers and write everything else inline in the cell; a loop over the series being plotted is as far as abstraction goes.
- Run it with the project's Python: `jupyter nbconvert --to notebook --execute --inplace figures/figures.ipynb`. If jupyter is missing, tell the user and ask before installing it.
- **Reply**: changes, LaTeX line, any `[TODO]`.

## 9. Check

After the notebook has run:

1. Read each cell's output. `fit_height` warns about a panel narrower than 1.2 in, text cut off or overlapping (rotated labels included), a value label or legend covering a curve, a legend covering a bar or box, and a font other than Inter. Fix the cell until it runs without warnings.
2. Look at each PNG for what code can't see: the takeaway reads at a glance; value marks sit on reported results at the comparison points; legend entries follow §6's order; colors follow §5; the caption matches the figure.
3. PDF fonts are embedded TrueType: `pdffonts {id}.pdf` shows `CID TrueType`, emb `yes` (without pdffonts: `grep -ac /Type3 {id}.pdf` prints 0).
