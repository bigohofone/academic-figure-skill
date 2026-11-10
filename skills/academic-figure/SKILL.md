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

| Width | Max cols | Max rows | More panels |
|---|---|---|---|
| Single column | 2 | 3 | double column |
| 1.5 column | 3 | 1 | double column |
| Double column | 4 | 2 | split into two figures |

1. Start with the most columns the limits allow.
2. Render. `fit_height` warns when a panel's data area (inside the spines) is narrower than 1.2 in, or when tick labels, titles or axis labels are cut off or overlap.
3. On such a warning, add a row and set the columns to ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 1 × 4 → 2 × 3), then render again. When the rows are at their limit, move to the next wider width.
4. Turn off unused cells (5 panels in 2 × 3: the last cell).
5. When panels plot the same quantity over the same range on an axis, share it (`plt.subplots(..., sharex=True, sharey=True)`); the axis label then goes on the outer panels only.
6. Every panel with a value axis has a label on it (with `sharey`, the outer panels carry it). Embeddings and heatmaps with category axes have none.

### Panel aspect

The aspect (width : height) is per panel. Use one of these, golden ratio φ : 1 by default:

| Aspect | `aspect=` | Fit |
|---|---|---|
| φ² : 1 | 0.382 | a single panel at 1.5- or double-column width |
| φ : 1 | 0.618 | curves, bars, histograms (default) |
| 1 : 1 | 1.0 | heatmap, confusion matrix, embedding |
| 1 : φ | 1.618 | content taller than wide (many horizontal bars) |

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
- `fit_height` also keeps every `mark_value` label inside its panel: it raises the y-limit to make room, and turns labels at a side edge inward.
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
| Text | Inter for all text and math; titles 9 pt, ticks 7 pt, everything else 8 pt |
| Axes | left and bottom spines, black, 0.75 pt; ticks 0.75 pt, 3 pt long (minor 2 pt) |
| Grid | horizontal, #DDDDDD, 0.75 pt, behind the data |
| Lines, markers | lines 1.25 pt; hollow markers, size 4 |
| Color | Paul Tol `bright` cycle, `tol.iridescent` colormap |
| Layout | constrained layout, 0.16 in between panels side by side, 0.08 in stacked |
| Output | 300 dpi; `pdf.fonttype: 42` (text stays text, Inter embedded) |

- Keep these values as they are; the style is tuned for print.
- Name panels with axes titles: in reading order, prefix each with its letter, `"(a) Accuracy on AIME"`, `"(b) …"`. A single panel has no title unless it needs one (dataset, setting). The figure itself has no title; the caption names it.
- Keep matplotlib's default axis limits and margins; `fit_height` makes room for value labels (§1, Height).
- Category axes (bar charts, text tick labels): hide the tick marks on that axis with `ax.tick_params(axis="x", length=0)` (`axis="y"` for horizontal bars), on every panel.

## 3. Lines and text

Every plotted quantity is one of two kinds; decide which before drawing:

- **Reported results**: the numbers the paper claims, measured once per setting (accuracy, F1, latency, throughput, error rate, a score per method). Readers compare them exactly.
- **Diagnostics**: quantities logged along a process to show its behavior (loss, gradient norm, entropy, temperature, queue length per iteration). Readers read their trend and shape.

### Lines

- Curves are plain lines; add markers (the style's hollow markers) only when the user asks.
- Diagnostics, however often they were logged: draw the raw values in the series color at `alpha=0.25` without a label, then `smooth(values)` on top with the label, and add to the caption: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- Reported results are drawn raw.
- Several runs per setting (seeds, folds, trials): draw the mean as the line and a band of ±1 std with `ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)`, and say in the caption what the band is and over how many runs.
- Reference lines (a baseline's score, a threshold): `ax.axhline(..., linestyle="--", linewidth=1, zorder=1)` in #BBBBBB, fully opaque, named by a legend entry. Compared values get their lines from `mark_value` (Value labels below).
- Log axis (`ax.set_yscale("log")`, named in the caption) when values span more than two orders of magnitude and the message is about differences among the small values. When the message is the change in size itself, keep the linear axis.

### Value labels

When the takeaway compares reported results across series, write them on the plot so the reader can read them exactly. Diagnostics carry no value labels; their curves already show the trend.

- Find the point where the paper makes the comparison: the claim decides it. "Ours reaches a higher score" compares each series' best; "ours ends higher" compares final values (at the last x all series share, when they end at different x); "ours is ahead at the same budget" compares values at that shared x. The value is the plotted metric at that point.
- If the request and the paper don't settle the comparison point, ask the user. When you can't ask, compare each series' best and say so in the reply.
- Write each value with three significant figures.
- Mark each value there with `mark_value(ax, x, y, "0.438", color)`: a 1 pt dashed line in `darken(color)` across the whole panel at that value, under the curves; a circle on the point; and the value in bold just above it. One per compared series, in the panels the takeaway is about. The lines let the reader compare heights anywhere in the panel.
- If a label above the point covers a curve, put it below with `below=True`.
- Bar charts of reported results: label every bar with `ax.bar_label(bars, fontweight="bold")`.

### Other text

- Text that belongs to one series (labels, annotations) uses `darken(series_color)`. Titles, axis labels, ticks and legend text are black.

## 4. Plot type

| Plot type | Frame | Gridlines | Other |
|---|---|---|---|
| Line | Base | Horizontal | – |
| Vertical bar, histogram | Base | Horizontal | `linewidth=0` |
| Horizontal bar | Base | Vertical | `linewidth=0` |
| Scatter | Full | Horizontal | `edgecolors="none"`, `alpha=0.5` |
| Embedding (t-SNE, UMAP) | Full | None | ticks hidden; markers as scatter |
| Heatmap, confusion matrix | Full | None | tick marks hidden; cell text `"white" if np.dot(im.cmap(im.norm(v))[:3], [0.299, 0.587, 0.114]) < 0.5 else "black"` |

- Bar charts: name the bars on the x-axis. For several groups (benchmarks, datasets), use one panel per group, titled with the group.
- Bars over several runs: error bars of ±1 std with `ax.bar(..., yerr=std, capsize=2, error_kw=dict(elinewidth=0.75, capthick=0.75, ecolor="black"))`, named in the caption.
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
| Single panel | inside, at an explicit `loc` where it covers no data; when no such spot exists, above the panel with `fig.legend(loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)` |
| Panels with the same series | one `fig.legend(loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)` above the panels |
| Panels with different series | one per panel above its title: `ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=2, frameon=False)` |
| Grouped series | rows = groups, columns = variants |
| One series per panel | none; the title names it |

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

1. Read each cell's output. `fit_height` warns about a panel narrower than 1.2 in, text cut off or overlapping, a value label or legend covering a curve, and a font other than Inter. Fix the cell until it runs without warnings.
2. Look at each PNG for what code can't see: the takeaway reads at a glance; value marks sit on reported results at the comparison points; legend entries follow §6's order; colors follow §5; the caption matches the figure.
3. PDF fonts are embedded TrueType: `pdffonts {id}.pdf` shows `CID TrueType`, emb `yes` (without pdffonts: `grep -ac /Type3 {id}.pdf` prints 0).
