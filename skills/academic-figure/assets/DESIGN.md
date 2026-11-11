---
version: alpha
name: Academic Figure
description: Print-first figures for machine learning papers, read at the size they are printed, where the reader gets one message at a glance.
colors:
  series-1: "#4477AA"
  series-2: "#EE6677"
  series-3: "#228833"
  series-4: "#CCBB44"
  series-5: "#66CCEE"
  series-6: "#AA3377"
  ours: "{colors.series-2}"
  neutral: "#8C8C8C"
  ink: "#000000"
typography:
  tick-label:
    fontFamily: Inter
    fontSize: 7pt
  label:
    fontFamily: Inter
    fontSize: 9pt
  legend:
    fontFamily: Inter
    fontSize: 7pt
  value-label:
    fontFamily: Inter
    fontSize: 7pt
    fontWeight: 400
  title:
    fontFamily: Inter
    fontSize: 11pt
    fontWeight: 400
spacing:
  layout-pad: 0.02in
  title-pad: 6pt
  label-pad: 1pt
  tick-pad: 1.75pt
components:
  axes:
    width: 0.5pt
    textColor: "{colors.ink}"
  tick:
    width: 0.5pt
    size: 1.5pt
    minor-size: 1pt
  grid:
    width: 0.5pt
    color: "{colors.ink}"
    opacity: 0.1
  line:
    width: 1pt
  dashed-line:
    width: 0.75pt
  marker:
    size: 2.5pt
    edge-width: 0.5pt
  outline:
    width: 0.75pt
  median:
    width: 1pt
  contour:
    width: 0.5pt
  heatmap:
    colormap: Blues
---

# Academic Figure

The design system for paper figures. The front matter holds the tokens: `paper.use_design()` reads them and sets matplotlib's style, so editing a token changes every figure. The sections below say how to apply them. In a project, `figures/DESIGN.md` is the design; edit it there to give a paper its own look.

## Overview

A figure is read printed in a paper, at the column width it is set at, by a reader who looks at it for a few seconds. Every rule serves one goal: the reader gets the figure's one message at a glance and can read the exact numbers the paper claims.

- Print first: sizes are the printed sizes, text is never scaled down, and the figure is drawn at the width it is printed at.
- One message per figure, stated by the takeaway and supported by what is drawn; everything else recedes (thin black box, faint grid, neutral grey for context).
- Color only for emphasis: by default everything is `ink` and `neutral` grey, and color goes only to what the reader must look at (ours, the series being compared). Context (baselines, fronts, reference lines, other models) stays grey. Several colors only when several series are compared on equal terms.
- Color-blind safe colors, told apart in grayscale too where needed.
- Plain and consistent: the same series keeps its color, marker and name in every figure of the paper.

## Colors

The `colors` tokens are Paul Tol's color-blind-safe `bright` set by role; continuous values use matplotlib's standard colormaps. `colors = paper.use_design()` returns them by name, references resolved: `colors["series-1"]`, `colors["ours"]`.

Pick the first row that fits:

| Case | Color |
|---|---|
| "Ours" (the proposed method) among baselines or ablations | `ours` for ours; every series it is compared against in `neutral` grey. Several grey series are told apart by line style on lines, in order `"-"`, `"--"`, `":"`, `"-."` (dashed and dotted at `linewidth=paper.dashed_width`), and by shade on fills (bars, boxes, violins, areas), in order `colors["neutral"]`, `darken(colors["neutral"])`, `lighten(colors["neutral"])` |
| Several series compared on equal terms, with no "ours" (models in a survey, classes, data sources, error types) | `series-1` to `series-6`, in this order |
| Single series | `series-1` |
| Reference lines (a baseline's score, a threshold, chance) | `neutral` |
| Grouped (sizes, sweeps) | one color per group; within a group blend with white at 40 / 70 / 100 %, light → dark |
| Text, axes, ticks | `ink` |
| Continuous values | the `heatmap.colormap` component, matplotlib's `Blues` (the default colormap); signed values `RdBu_r`, in heatmap.md |

- Several variants of ours (with and without a component): all in `ours`, told apart by line style on lines and by shade on fills, as grey series are.
- More compared series than grey line styles (four): add the design's markers, a different shape per series; more than eight: draw the series the takeaway names, and the rest as one grey group named "Other baselines" in the legend.
- More than six series with no "ours": group them (one color per group, shades within) or split them into panels. Classes in an embedding (ten or more, unordered) are the exception: one color each from matplotlib's `tab10` (`tab20` beyond ten), defined in the cell.
- Series are told apart by color. When color alone can't separate them (grayscale printing, close shades), also vary line style.
- Grey must stay readable on white: lines, markers and reference lines are `neutral` (#8C8C8C, 3.4:1 contrast, above the 3:1 that graphics need) at full opacity, and grey text is `darken(colors["neutral"])` (4.9:1, above the 4.5:1 that text needs). Lighter greys, such as `lighten(colors["neutral"])`, only as fills that have an outline or sit next to darker fills; never for lines, markers or text.
- Text that belongs to one series (labels, annotations) uses `darken(series_color)`.
- Emphasis, when the user names a series to emphasize: color it as ours, and every other series as the series ours is compared against.
- A paper-wide palette (a lab's or a brand's): change the `colors` tokens in `figures/DESIGN.md`. A one-off palette for a single figure ("match the original"): a dict in that figure's cell, `PALETTE = {"ours": "#5F16A7", "base": "#63C9D2"}`; everything else keeps the design. If some colors are very light (cyan, yellow), tell the user they read weakly on white.

## Typography

One family, `Inter` (bundled), for all text and math. Sizes by role:

| Token | Size | Used for |
|---|---|---|
| `tick-label` | 7 pt | tick labels |
| `value-label` | 7 pt | everything written inside the chart: value labels on markers and bars, heatmap cell text, labels next to points, pie labels; the default for any text drawn with `ax.text` or `ax.annotate` |
| `label` | 9 pt | axis labels, subcaptions |
| `legend` | 7 pt | legend entries |
| `title` | 11 pt | panel titles, row and column headers |

- All text is regular weight, inside the chart and out; nothing is bold. Text is black (`ink`) unless it belongs to one series.
- Numeric tick labels are horizontal plain numbers (`1, 2, 4, 8`, never rotated, never `2³`), written as short as they read: `0, 0.5, 1`, not `0.0, 0.5, 1.0` (`ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}")`). When `fit_height` reports overlapping numeric tick labels along an axis, use fewer ticks in that panel (every other one), not smaller text or rotation.
- Where both axes start at the same corner (0 and 0, −1 and −1), their first tick labels touch: keep the tick and drop only the y axis's corner label, `ax.set_yticks(ticks, labels=["", *labels[1:]])`.
- Log axes: powers of ten as plain numbers from 0.001 up to 1000 (`0.01, 0.1, 1, 10`), and beyond that `1e-4, 1e-5` below and SI suffixes above (`10K, 1M, 1B`), never `10⁻⁵`.
- Text tick labels (categories, bins, method names) that don't fit side by side turn 45°: `ax.set_xticks(x, labels=names, rotation=45, ha="right", rotation_mode="anchor")`, and 90° (`rotation=90, ha="center"`) when they still overlap at 45°. Keep the panels side by side and the bins on the x-axis rather than switching to horizontal bars or stacked panels to avoid the rotation.
- Math in labels uses mathtext (`r"$\mathrm{PPL}_{\mathrm{Base}}$"`); it is set in Inter like the rest. Symbols Inter lacks (∝, ≈ in some weights) go in mathtext too (`$\propto$`).
- Text written on a fill (a bar segment, a wedge, a heatmap cell, an area) is black or white, whichever reads on that fill: `color=text_color(fill)`; it is never `darken(fill)` on its own fill.

## Layout

### Width

| Venue | Single column | 1.5 column | Double column |
|---|---|---|---|
| ICML | 3.25 in | 5.0625 in | 6.75 in |
| CVPR | 3.25 in | 5.15625 in | 6.875 in |
| ACL (ARR) | 3 in | 4.6875 in | 6.25 in |

| Single-column venue | Half text width | Full text width |
|---|---|---|
| ICLR, NeurIPS | 2.75 in | 5.5 in |

- Use the venue and width the user names. With no venue, ICLR.
- Single-column venues (ICLR, NeurIPS) have one text width, 5.5 in. A figure with several panels takes the full width; a single panel takes half of it, 2.75 in, so it is not blown up to the page width, unless it needs width (many x categories, a long time axis read in detail), then the full width at φ² : 1.
- 1.5 column (0.75 × double) is a `figure*` narrower than the text: use it when the user asks, or when single column is too narrow and double column leaves the content sparse.

### Grid

| Width | Max cols |
|---|---|
| Half text width (2.75 in) | 1 |
| Single column (3–3.25 in) | 2 |
| Full text width of a single-column venue (5.5 in) | 3 |
| 1.5 column | 3 |
| Double column | 4 |

0. A grid of two factors (models × benchmarks, methods × datasets) keeps one factor per row and the other per column, whatever the column limit below: 4 models × 4 benchmarks is a 4 × 4 grid, so the reader compares along rows and down columns at a glance. Its panels share y across each row and x down each column, with tick numbers only on the left column and the bottom row (`plt.subplots(rows, cols, sharex="col", sharey="row")`, inner tick labels left hidden; step 5 does not apply). Because inner panels carry no tick labels, such a grid may go down to 1.0 in per panel: `fit_height(fig, axes, min_width=1.0)`. If a panel is still narrower, put the factor with fewer levels on the columns, and keep axis titles once per figure (`fig.supxlabel`, `fig.supylabel`); never reflow the grid into another shape.
1. Start with every panel in one row, up to the width's column limit: a single column holds two panels side by side, and panels the reader compares (two problems, two settings) stay side by side, as in the paper being redrawn.
2. Render. `fit_height` warns when a panel's data area (inside the box) is narrower than 1.2 in, or when tick labels, titles or axis labels are cut off or overlap.
3. On such a warning, first free room inside the row: share the y axis when the panels plot the same quantity (step 5), turn long text tick labels 45° (Typography), shorten labels. Only when a panel is still narrower than 1.2 in, add a row and set the columns to ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 1 × 4 → 2 × 3), then render again. Rows have no limit.
4. Turn off unused cells (5 panels in 2 × 3: the last cell).
5. When panels plot the same quantity over the same range on an axis, share it (`plt.subplots(..., sharex=True, sharey=True)`). Outside a two-factor grid, every panel keeps its tick numbers, since sharing hides them on inner panels: `ax.tick_params(labelleft=True, labelbottom=True)` on each panel.
6. Each axis quantity is labelled once per row or column of panels, shared axis or not: panels side by side that plot the same quantity on y carry the y label on the leftmost panel only, and panels stacked that plot the same quantity on x carry the x label on the bottom panel only. When a whole row of panels shares one x label, write it once under the row with `fig.supxlabel(label)` (`fig.supylabel` for one y label down a column); inside sub-figures, whose `supxlabel` is the subcaption, each panel keeps its own x label. A panel whose quantity differs from its neighbours' carries its own label. Embeddings and heatmaps with category axes have none.

### Panel names

By default none. The figure never has a title; the caption names it. Pick the first row that fits:

| Panels | Names |
|---|---|
| A grid of two factors (models × benchmarks, methods × datasets) | headers, never subcaptions or letters: each column named once above the top row, `ax.set_title(col_name)`, and each row once left of the first column's y-label, `axes[r, 0].annotate(row_name, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0), textcoords="offset points", ha="right", va="center", rotation=90, fontsize=11)`; either factor may be the rows; the caption names a panel by its row and column |
| A figure split into sub-figures side by side, each a group of panels with its own message and legend (an ablation next to a scaling study) | build each group as a sub-figure, `left, right = fig.subfigures(1, 2, width_ratios=[3, 2])` (ratios = panel counts), panels from `left.subplots(1, 3)`; each sub-figure gets a lettered subcaption below it, in reading order, `left.supxlabel("(a) Reward gating ablation")`, and its panels are named by titles as in the next row. Only sub-figures carry letters |
| Several panels the reader must tell apart (different metrics, problems, settings) | a title above each, no letter: `ax.set_title("Response length")` |
| One panel | none |

### Panel aspect

The aspect (width : height) is per panel. Use one of these, golden ratio φ : 1 by default:

| Aspect | `aspect=` | Fit |
|---|---|---|
| φ² : 1 | 0.382 | a single panel at 1.5-column, double-column or full text width |
| φ : 1 | 0.618 | curves, bars, histograms, box plots and violins (default) |
| 1 : 1 | 1.0 | heatmap, confusion matrix, embedding, contour plot, and every panel of a two-factor grid, so rows and columns compare alike |
| 1 : φ | 1.618 | content that is itself taller than wide (a long list of categories down a horizontal bar chart or forest plot) |

Slopes and gaps between curves need height, many x categories need width, matrices need square cells. If curves look flat after rendering, pick a taller aspect. The aspect follows the data, never room for labels: a value label that covers a curve goes below the point (`below=True`), and if it still covers one, the comparison uses another point whose label stands clear. Pie and radar charts are circles: `fit_height` sizes them to the width and ignores `aspect`.

### Height

Let `fit_height` set it. Create the figure at the target width with any height, draw everything (labels, legend, colorbar), call `fit_height` last, then save with plain `fig.savefig`:

```python
fig, axes = plt.subplots(2, 1, figsize=(3.25, 2), sharex=True)
...  # plot, labels, legend, colorbar
fit_height(fig, axes, aspect=0.618)
fig.savefig("outputs/{id}.pdf")
```

- `ax` may be one Axes, an array, a list (also of panels from several sub-figures), or the `subplot_mosaic` dict; hidden cells and colorbars are skipped.
- `fit_height` also keeps every `mark_value` label and every bar label (`ax.bar_label`) inside its panel: it raises the y-limit to make room (the x-limit for horizontal bars), and turns `mark_value` labels at a side edge inward.
- On `ValueError` (fixed aspect), draw images with `imshow(..., aspect="auto")`.
- On the "different widths" warning, give all panels the same width (plain grid, equal columns).

### Axes

- Keep matplotlib's default axis limits and margins unless the chart type's file says otherwise; `fit_height` makes room for value labels.
- Category axes (bar charts, text tick labels): hide the tick marks on that axis with `ax.tick_params(axis="x", length=0)` (`axis="y"` for horizontal bars), on every panel.
- Colorbars (heatmaps, contour plots, colored lines): always, labelled with the quantity, on the right, `fig.colorbar(mappable, ax=ax, label="Validation loss")`; below the panel (`location="bottom"`) when on the right it would leave the panel narrower than the minimum width.
- Log axis (`ax.set_yscale("log")`, named in the caption) when values span more than two orders of magnitude and the message is about differences among the small values. When the message is the change in size itself, keep the linear axis.

## Shapes

The marks every chart type is built from, sized by the `components` tokens:

| Mark | Token | Look |
|---|---|---|
| Panel box | `axes` | a full box on all four sides, `ink`, 0.5 pt |
| Ticks | `tick` | outside the box, 0.5 pt, 1.5 pt long (minor 1 pt) |
| Grid | `grid` | `ink` at 10% opacity, 0.5 pt, behind the data; both directions unless the chart type's file says otherwise |
| Data lines | `line` | 1 pt, solid |
| Dashed and dotted lines (reference lines, value marks, fits, fronts, and series told apart by line style) | `dashed-line` | 0.75 pt: matplotlib has no separate default for them, so pass `linewidth=paper.dashed_width` with every `linestyle` other than `"-"` |
| Markers | `marker` | hollow: white fill, a 0.5 pt edge in the series color, 2.5 pt |
| Outlines and edges (boxes, whiskers, bar edges where drawn) | `outline` | 0.75 pt, black |
| Box plot median | `median` | 1 pt, black |
| Contour lines | `contour` | 0.5 pt |

- Fills take the series color at full opacity, except bands (`alpha=0.2`), scatter clouds (`alpha=0.5`), and box plots and violins, which take `lighten(color)` so the black median and the points on them stay readable.
- Reference lines (a baseline's score, a threshold): `ax.axhline(..., linestyle="--", linewidth=paper.dashed_width, zorder=1)` in `neutral`, fully opaque, named by a legend entry.

## Components

### Chart types

Each chart type has its own file next to this one, with its marks, variants and the code for them. Before drawing, read the file of every chart type the figure uses. Rows run from the most common chart type in ML papers to the least.

| Chart type | Use it for | File |
|---|---|---|
| Line chart | values along a continuous x: learning curves, scaling curves, pass@k, ROC and precision-recall curves | `line-chart.md` |
| Bar chart | reported results compared across methods, ablations or benchmarks; parts of a whole per category (stacked) | `bar-chart.md` |
| Scatter plot | two quantities per item: accuracy against parameters, FLOPs or latency; t-SNE and UMAP embeddings | `scatter-plot.md` |
| Box plot | the spread of many values per group, compared across groups | `box-plot.md` |
| Heatmap | values over two categorical axes: confusion matrix, attention map, hyperparameter grid | `heatmap.md` |
| Histogram | how one quantity's values are spread: scores, lengths, counts per bin | `histogram.md` |
| Error bar plot | means with confidence intervals, when the differences are small next to the values | `error-bar-plot.md` |
| Area chart | shares of a whole along a continuous x: data mixture over training | `area-chart.md` |
| Contour plot | a function of two continuous variables: loss landscape, decision boundary | `contour-plot.md` |
| Radar chart | a few models' profiles across 5–10 benchmarks | `radar-chart.md` |
| Pie chart | the composition of one whole with few parts: dataset composition | `pie-chart.md` |
| Violin plot | as a box plot, when the shape of the spread (several modes) matters | `violin-plot.md` |

- Many exact numbers with no trend or comparison to see (e.g. every method on every dataset): suggest a table to the user instead of a figure.

### Legend

| Case | Legend |
|---|---|
| One panel | placed by the first of these that covers no data: (1) a corner, tried in the order `loc="upper left"`, `"upper right"`, `"lower left"`, `"lower right"`; (2) another free spot inside the panel (`"upper center"`, `"lower center"`, `"center left"`, `"center right"`); (3) outside, above the panel, as below |
| Several panels with the same series | one legend for the figure, outside above the panels, never tucked into one panel where the reader has to hunt for it: `fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)`, with fewer columns (more rows) when one row of entries is wider than the figure |
| Panels with different series | one per panel, placed inside that panel in the same order; outside, it goes above the panel: `ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=<entries>, frameon=False)`, with fewer columns (more rows) when one row is wider than the panel |
| Sub-figures | one per sub-figure, above its panels, by the rows above: `left.legend(..., loc="outside upper center", ...)` |
| Grouped series | rows = groups, columns = variants |
| One series per panel | none; the title names it |

- Always pass an explicit `loc`, never `"best"`. `fit_height` warns when a legend covers a curve, data points, a bar or a box; on that warning, try the next spot. A filled plot (heatmap, filled contour, stacked area) has no free spot inside: its legend goes outside.
- Entry order: "ours" first, then the other series in their color, line style or shade order, reference lines last; for stacked bars and areas, the order the segments stack from the top. When the drawing order differs (ours drawn last to sit on top), pass the handles in entry order: `ax.legend([h_ours, h_a, h_b], ["Ours", "A", "B"], ...)`.

### Value labels

Reported results the takeaway compares are written on the plot, so the reader reads them exactly; diagnostics and distributions carry none. Each chart type's file says how (`mark_value` on curves, `ax.bar_label` on bars). Values have three significant figures, trailing zeros kept (`f"{v:#.3g}"`: 85.0, not 85), or the precision the source gives when it has fewer (a paper's printed 0.82 stays 0.82); 7 pt (`value-label`), in `darken(series_color)` beside a mark, or `text_color(fill)` on a fill.

## Do's and Don'ts

- Do draw at the printed width and let `fit_height` set the height; don't save with `bbox_inches="tight"`, which changes the size.
- Do keep the tokens' sizes; don't shrink text to make room, and don't change line widths or marker sizes per figure.
- Do give every legend an explicit `loc`; don't use `"best"`.
- Do name sub-figures with lettered subcaptions below and panels with titles above; don't give the figure a title.
- Do write numeric ticks as plain horizontal numbers; don't rotate them or write `2³`.
- Do use the color roles; don't pick colors outside the tokens unless the user asks.
- Do draw a contour plot for a function of two variables; don't draw 3D surfaces, which can't be read in print.
- Do use a bar chart when parts are many or close in size; don't draw a pie chart for more than six parts.
