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
  neutral-light: "#D1D1D1"
  neutral-dark: "#707070"
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
    highlight-size: 5pt
  outline:
    width: 0.75pt
  median:
    width: 1pt
  contour:
    width: 0.5pt
  heatmap:
    colormap: viridis
---

# Academic Figure

The design system for paper figures. The front matter holds the tokens: `paper.use_design()` reads them and sets matplotlib's style, so editing a token changes every figure. The sections below say how to apply them. In a project, the copy in the figures folder is the design; edit it there to give a paper its own look.

## Overview

A figure is read printed in a paper, at the width it is set at, by a reader who looks at it for a few seconds. Every rule serves one goal: the reader gets the figure's one message at a glance and can read the exact numbers the paper claims.

- **Print first**: sizes are printed sizes; text is never scaled down; the figure is drawn at the width it is printed at.
- **One message**: the takeaway is stated by what is drawn; everything else recedes (thin black box, faint grid, grey for context).
- **Color for emphasis**: everything is `ink` and `neutral` grey by default; color goes only to what the reader must look at (ours, the series being compared). Several colors only when several series are compared on equal terms.
- **Consistent**: a series keeps its color, marker and name in every figure of the paper.
- **Tested, not judged**: where a rule depends on how the figure renders, `fit_height` reports it; every rule says what to do on its warning.

## Colors

The `colors` tokens are Paul Tol's color-blind-safe `bright` set by role; `colors = paper.use_design()` returns them by name: `colors["series-1"]`, `colors["ours"]`. Pick the first row that fits:

| Case | Color |
|---|---|
| "Ours" among baselines or ablations | `ours` for ours; every series it is compared against in `neutral` |
| Variants of ours (with and without a component) | all `ours`; the full method solid and first in the legend, each reduced variant in the next line style |
| Several series compared on equal terms, no "ours" (models in a survey, data sources, error types) | `series-1` to `series-6`, in order |
| More than six unordered classes (an embedding) | matplotlib's `tab10` (up to 10), `tab20` (up to 20) |
| Groups with sizes or sweeps inside (model sizes per family) | one color per group; within a group, blended with white at 40 / 70 / 100%, light to dark |
| Single series | `series-1` |
| Reference lines | `neutral` (white over filled plots, Shapes) |
| Text, axes, ticks | `ink` |
| Continuous values | the `heatmap.colormap` token, `viridis`, low values dark; signed values `RdBu_r` (`heatmap.md`) |

- **Grey series**: told apart in the Order rule's order (Layout), on lines by line style, `"-"`, `"--"`, `":"`, `"-."` (dashed and dotted at `linewidth=paper.dashed_width`), and on fills (bars, boxes, violins, areas) by shade, `greys(n)` for n grey series, evenly spaced from `neutral-light` to `neutral-dark`, light to dark (one grey series takes `neutral`).
- **Many grey series**: more than four lines: add markers, one shape per series (`line-chart.md`); more than six: draw the series the takeaway names, and group the rest as one grey series, "Other baselines".
- **Same color, several series**: whenever two or more drawn series share a color (ours and its variants, greys), they differ by line style or shade as above.
- **Readable on white**: grey lines, markers and reference lines are `neutral` at full opacity; `neutral-light` only as a fill. Text that belongs to a series is `darken(series_color)` (any grey series: `darken(colors["neutral"])`), so light series still get readable labels; text on a fill follows Typography.
- **Emphasis**: when the user names a series to emphasize, it is colored as ours and every other series as compared ones.
- **Other palettes**: a paper-wide palette (a lab's or a brand's) changes the `colors` tokens in the design copy; a one-off palette for one figure ("match the original") is a dict in that figure's script, `PALETTE = {"ours": "#5F16A7", "base": "#63C9D2"}`.

## Typography

One family, `Inter` (bundled), for all text and math, regular weight everywhere (nothing bold). Text is `ink` unless it belongs to one series. Sizes by role:

| Token | Size | Used for |
|---|---|---|
| `tick-label` | 7 pt | tick labels |
| `value-label` | 7 pt | everything written inside the chart (value labels, cell text, point names, pie labels); the default for `ax.text` and `ax.annotate` |
| `label` | 9 pt | axis labels, subcaptions |
| `legend` | 7 pt | legend entries |
| `title` | 11 pt | panel titles, row and column headers |

- **Numeric tick labels**: horizontal plain numbers, written as short as they read, `0, 0.5, 1` and `1,000`, never rotated, never `2³` or `1e+06`: `ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.10g}".replace("-", "−"))` (keeping the minus sign). On log axes, powers of ten are plain from 0.001 to 1000, then `1e-4` below and SI suffixes above (`10K`, `1M`, `1B`).
- **Tick choice**: numbers the reader can name, evenly spaced (on a log axis, powers of the base, every one or every second, fifth, …), with the ends of the data range labelled where the axis allows; within that, choose what reads best. When `fit_height` reports tick labels overlapping, take fewer ticks. Panels that share an axis share its ticks.
- **Corner labels**: when `fit_height` reports the first tick labels of both axes overlapping at the shared corner, drop the y axis's first label: `ticks = [t for t in ax.get_yticks() if lo <= t <= hi]` (`lo, hi = ax.get_ylim()`), `ax.set_yticks(ticks, labels=["", *[f"{t:,.10g}" for t in ticks[1:]]])`.
- **Text tick labels** (non-numeric names) that `fit_height` reports overlapping, by what they name:
  - **Unordered categories, one value each** (methods, models, groups in one bar, error bar or box chart): swap the axes so the names read horizontally down the y axis (horizontal bars, a forest plot, horizontal boxes), ordered top to bottom as under Order.
  - **Everything that keeps the x axis** (named bins, the categories of grouped series, benchmarks shared across panels): turn them 45°, `ax.set_xticks(x, labels=names, rotation=45, ha="right", rotation_mode="anchor")`, then 90° (`rotation=90, ha="center"`) if they still overlap.
- **Math**: mathtext, set in Inter like the rest (`r"$\mathrm{PPL}_{\mathrm{Base}}$"`); symbols Inter lacks (∝, ≈) go in mathtext too (`$\propto$`).
- **Text on a fill** (a bar segment, a wedge, a heatmap cell, an area band): black or white, whichever reads on it, `color=text_color(fill)`.
- **Text over mixed content** (a note over bars, gridlines and a reference line, where no single fill sets its contrast): on a white box, `bbox=dict(facecolor="white", edgecolor="none", pad=1)`. Contour labels take none: they sit in the gap cut for them.

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

Pick the first row that applies:

| Case | Width |
|---|---|
| The user or the task gives a width (one column of the paper, a size in inches) | that width; the rules below fit the figure into it |
| The user asks for a 1.5-column `figure*`, or the panels at single column still fail `min_width` after Grid step 3 | 1.5 column |
| Single-column venue, several panels | the full text width |
| Single-column venue, one panel | half the text width; the full width at φ² : 1 only when its x tick labels still overlap at half width after Typography's fixes |
| Two-column venue | single column, or double column when the panels fail `min_width` there |

The venue is the one the user names; with none, ICLR.

### Grid

| Width | Max columns |
|---|---|
| Half text width (2.75 in) | 1 |
| Single column (3–3.25 in) | 2 |
| Full text width of a single-column venue (5.5 in) | 3 |
| 1.5 column | 3 |
| Double column | 4 |

0. **Two-factor grid** (models × benchmarks, methods × datasets; also rows of different plots over the same columns, where the plot type is the row factor and each row's y label names it): one factor per row, the other per column, whatever the column limit: 4 models × 4 benchmarks is 4 × 4. An axis that shows the same quantity in every panel has one range across the grid (`sharex=True` / `sharey=True`); an axis whose quantity changes between columns or rows is shared only down a column (`sharex="col"`) or across a row (`sharey="row"`). Tick numbers only on the left column and bottom row (step 5 does not apply), so panels may be as narrow as 1.0 in, `fit_height(fig, axes, min_width=1.0)`; if still narrower, put the factor with fewer levels on the columns; never reflow it. No value marks or other emphasis in single panels; numbers go in the caption.
1. **Start**: every panel in one row, up to the column limit.
2. **Render**: `fit_height` warns when a panel's data area is narrower than `min_width` (1.2 in), or when text is cut off or overlaps.
3. **On a warning**, first free room inside the row: share the y axis when the panels plot the same quantity (step 5), apply Typography's text tick rule, shorten labels. Only when a panel is still too narrow, add a row and set the columns to ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 2 × 3), then render again. Rows have no limit.
4. **Unused cells**: turned off (5 panels in 2 × 3: the last one).
5. **Shared axes**: when panels plot the same quantity over the same range, share it (`plt.subplots(..., sharex=True, sharey=True)`); outside a two-factor grid, every panel keeps its tick numbers, `ax.tick_params(labelleft=True, labelbottom=True)`.
6. **Axis labels**: once per row or column of panels that plot the same quantity: the y label on the leftmost panel, the x label on the bottom one, or once for the whole row with `fig.supxlabel(label)` (`fig.supylabel` down a column); inside sub-figures, whose `supxlabel` is the subcaption, each panel keeps its own. A panel whose quantity differs carries its own label.

### Panel names

The figure never has a title; the caption names it. Pick the first row that fits:

| Panels | Names |
|---|---|
| Two-factor grid | headers: each column once above the top row, `ax.set_title(col_name)`; each row once left of the first column's y label, `axes[r, 0].annotate(row_name, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0), textcoords="offset points", ha="right", va="center", rotation=90, fontsize=rcParams["axes.titlesize"])` (rows of different plots: the y labels name them) |
| Sub-figures side by side, each a group of panels with its own message and legend | `left, right = fig.subfigures(1, 2, width_ratios=[3, 2])` (ratios = panel counts), panels from `left.subplots(1, 3)`; a lettered subcaption below each, `left.supxlabel("(a) Reward gating ablation")`, and its panels titled as in the next row. Only sub-figures carry letters |
| Several panels the reader must tell apart | a title above each, `ax.set_title("Response length")` |
| One panel | none |

### Panel aspect

The aspect (width : height) is per panel, φ : 1 unless a row below applies:

| Aspect | `aspect=` | For |
|---|---|---|
| 1 : 1 | 1.0 | heatmap (rows / columns instead when not square), embedding, contour plot, stacked area chart, reliability diagram, ROC curve, and every panel of a two-factor grid |
| φ² : 1 | 0.382 | a single panel at full width (Width) |
| 1 : φ | 1.618 | a horizontal chart with more categories down y than its width holds at φ : 1 (`fit_height` reports the tick labels overlapping) |
| φ : 1 | 0.618 | everything else: curves, bars, histograms, box plots, violins, scatter plots, and panels reflowed into rows |

The aspect follows the data, never room for labels. Pie and radar charts are circles: `fit_height` sizes them to the width and ignores `aspect`.

### Height

`fit_height` sets it. Create the figure at the target width with any height, draw everything (labels, legend, colorbar), call `fit_height` last, then save with plain `fig.savefig`:

```python
fig, axes = plt.subplots(2, 1, figsize=(3.25, 2), sharex=True)
...  # plot, labels, legend, colorbar
fit_height(fig, axes, aspect=0.618)
fig.savefig("outputs/{id}.pdf")
```

- **Panels**: `ax` may be one Axes, an array, a list (also of panels from several sub-figures), or the `subplot_mosaic` dict; hidden cells and colorbars are skipped.
- **Value labels**: `fit_height` keeps every `mark_value` label and bar label (`ax.bar_label`) inside its panel, by raising the y-limit (the x-limit for horizontal bars) and turning `mark_value` labels at a side edge inward. It never moves other text: it reports it instead.
- **Errors**: on `ValueError` (fixed aspect), draw images with `imshow(..., aspect="auto")`; on the "different widths" warning, give all panels the same width.

### Axes

- **Limits**: matplotlib's defaults and margins, except an axis that is a bounded whole, fixed to it: shares (0–1), probabilities and the unit square (ROC, reliability), a radar's scale.
- **Order**: categories and series with no natural order (methods, models, ablation variants) run in ascending order of the value the takeaway compares, left to right (top to bottom when horizontal), so ours, usually the best, ends at the right. A natural order stays: sizes, time, bins, swept values, a benchmark list the paper fixes. Legends of side-by-side series follow the same order.
- **Category axes**: tick marks hidden on that axis on every panel, `ax.tick_params(axis="x", length=0)` (`axis="y"` when horizontal).
- **Log axes**: an axis whose positive values span over 100× (max / min > 100) is log, `ax.set_xscale("log")`, named in the caption; a log₁₀ axis keeps its minor ticks at 2–9 × each power, unlabelled (`ax.xaxis.set_minor_formatter(NullFormatter())`), and in a chart with gridlines its gridlines follow them, `ax.grid(True, which="both")`.
- **Colorbars** (heatmaps, contour plots, colored lines): always, labelled with the quantity, on the right, `fig.colorbar(mappable, ax=ax, label="Validation loss")`; below the panel (`location="bottom"`) when `fit_height` reports the panel narrower than `min_width` with it on the right.

## Shapes

The marks every chart type is built from, sized by the `components` tokens. Matplotlib applies them; code reads them from `rcParams` or `paper` and never writes the numbers.

| Mark | Token | Look | In code |
|---|---|---|---|
| Panel box | `axes` | a full box on all four sides, `ink`, 0.5 pt | `rcParams["axes.linewidth"]` |
| Ticks | `tick` | outside the box, 0.5 pt, 1.5 pt long (minor 1 pt) | set by the style |
| Grid | `grid` | `ink` at 10% opacity, 0.5 pt, behind the data, both directions unless the chart file says otherwise | `rcParams["grid.linewidth"]`, `rcParams["grid.alpha"]` |
| Data lines | `line` | 1 pt, solid | set by the style |
| Dashed and dotted lines (reference lines, value marks, fits, fronts, series told apart by line style) | `dashed-line` | 0.75 pt | `linewidth=paper.dashed_width` with every `linestyle` other than `"-"` |
| Markers | `marker` | hollow: white fill, a 0.5 pt edge in the series color, 2.5 pt | `rcParams["lines.markersize"]` |
| Points of interest (a minimum, the trained solution) | `marker.highlight-size` | a filled star, 5 pt | `markersize=paper.highlight_size` |
| Outlines and edges (boxes, whiskers, error bars, outlined cells) | `outline` | 0.75 pt, black | `rcParams["patch.linewidth"]` |
| Seams between fills (stacked segments, wedges, area bands) | `grid` | white, 0.5 pt | `edgecolor="white", linewidth=rcParams["grid.linewidth"]` |
| Box plot median | `median` | 1 pt, black | set by the style |
| Contour lines | `contour` | 0.5 pt | `rcParams["contour.linewidth"]` |

- **Opacity**: fills take the series color at full opacity, except bands (`alpha=0.2`), scatter clouds (`alpha=0.5`), light polygon fills (radar, `alpha=0.1`), and box plots and violins, which take `lighten(color)` so the black median and the points on them stay readable.
- **Reference lines** (a baseline's score, a threshold, a diagonal): `ax.axhline(..., linestyle="--", linewidth=paper.dashed_width, zorder=1)` in `neutral`, white across a filled plot (stacked area, heatmap, contour gradient), where grey sinks into the fills. A line with a value of its own (a baseline's score, a threshold) gets a legend entry; a line whose meaning the axes give (y = x, chance, zero) gets none, and the caption's reading guide names it.

## Components

### Chart types

Each chart type has its own file next to this one: read the file of every chart type the figure uses before drawing.

| Chart type | Use it for | File |
|---|---|---|
| Line chart | values along a continuous x: learning curves, scaling curves, pass@k, ROC and precision-recall curves | `line-chart.md` |
| Bar chart | reported results compared across methods, ablations or benchmarks; parts of a whole per category | `bar-chart.md` |
| Scatter plot | two quantities per item: accuracy against cost; embeddings | `scatter-plot.md` |
| Box plot | the spread of many values per group, compared across groups | `box-plot.md` |
| Heatmap | values over two categorical axes: confusion matrix, attention map, hyperparameter grid | `heatmap.md` |
| Histogram | how one quantity's values are spread | `histogram.md` |
| Error bar plot | means with their uncertainty, when the compared values differ by less than 10% | `error-bar-plot.md` |
| Area chart | shares of a whole along a continuous x | `area-chart.md` |
| Contour plot | a function of two continuous variables | `contour-plot.md` |
| Radar chart | a few models' profiles across 5 to 10 benchmarks | `radar-chart.md` |
| Pie chart | the composition of one whole with two to six parts | `pie-chart.md` |
| Violin plot | as a box plot, when the shape of the spread matters | `violin-plot.md` |

- **Tables**: many exact numbers with no trend or comparison to see (every method on every dataset): suggest a table instead of a figure.

### Legend

Pick the first row that fits:

| Case | Legend |
|---|---|
| A filled plot (heatmap, contour gradient, stacked area, embedding) | outside, above the panel (last row), or none when the bands are named directly |
| One panel | inside, at the first spot where `fit_height` stays silent: the corners `"upper left"`, `"upper right"`, `"lower left"`, `"lower right"`, then `"upper center"`, `"lower center"`, `"center left"`, `"center right"`; when none works, outside, above the panel (last row) |
| Several panels with the same series | one legend for the figure, above the panels: `fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)` |
| A row of panels with its own series (rows of different plots) | one legend per row, in that row's first panel where it fits, else the next, placed as for one panel |
| Panels with different series | one per panel, placed as for one panel |
| Sub-figures | one per sub-figure, above its panels, `left.legend(..., loc="outside upper center", ...)` |
| One series per panel | none; the title names it |
| Outside, above one panel | `ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=<entries>, frameon=False)` |

- **Inside is worth a small overlap**: the legend's opaque frame keeps it readable, and it costs no height. It must not hide values: `fit_height` warns when it covers a curve, data points or text, or when more than a tenth of its area lies over filled marks (bars, boxes, bands, violins, areas).
- **Columns**: an outside legend takes one row of entries; when that row is wider than the figure (`fit_height` reports text cut off or the layout collapsing), fewer columns.
- **Entry order**: curves: ours first, then the other series in color, line-style or shade order; side-by-side series (grouped bars, boxes): left to right; stacked bars and areas: the order the segments stack from the top. When the drawing order differs, pass the handles in entry order: `ax.legend([h_ours, h_a, h_b], ["Ours", "A", "B"], loc=...)`.
- **`loc`**: always explicit, never `"best"`.

### Value labels

Reported results the takeaway compares are written on the plot, so the reader reads them exactly; diagnostics and distributions carry none. Each chart file says where (`mark_value` on curves, `ax.bar_label` on bars). Values are written by the first row that applies, in labels and caption alike:

| Value | Written as |
|---|---|
| Copied from the source (a paper's table) | exactly as printed: `"0.82"` stays `"0.82"` |
| A count or other whole number | an integer, `f"{round(v):,}"`: `93`, `1,024` |
| A share of a whole (pie, stacked bar, win rate, area) | a whole percent, `f"{v:.0%}"`: `38%` |
| 1000 or more | a whole number, `f"{v:,.0f}"`: `1,234` |
| Anything else | three significant figures, trailing zeros kept, `f"{v:#.3g}"`: `85.0`, `0.912` |

- **Look**: 7 pt (`value-label`), in `darken(series_color)` beside a mark, `text_color(fill)` on a fill.

## Do's and Don'ts

- **Size**: do draw at the printed width and let `fit_height` set the height; don't save with `bbox_inches="tight"`, which changes the size.
- **Tokens**: do read sizes from the tokens; don't write line widths, marker or font sizes as numbers, and don't shrink text to make room.
- **Legend**: do give every legend an explicit `loc`; don't use `"best"`.
- **Names**: do letter sub-figures with subcaptions below and title panels above; don't give the figure a title.
- **Ticks**: do write numeric ticks as plain horizontal numbers; don't rotate them or write `2³`.
- **Colors**: do use the color roles; don't pick colors outside them unless the user asks.
- **3D**: do draw a contour plot for a function of two variables; don't draw 3D surfaces.
- **Pies**: do use a bar chart for more than six parts or several wholes; don't draw such a pie.
