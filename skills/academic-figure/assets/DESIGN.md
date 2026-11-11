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
    fontSize: 8pt
  legend:
    fontFamily: Inter
    fontSize: 7pt
  value-label:
    fontFamily: Inter
    fontSize: 7pt
    fontWeight: 400
  title:
    fontFamily: Inter
    fontSize: 9pt
    fontWeight: 400
  contour-label:
    fontFamily: Inter
    fontSize: 6pt
  bar-label:
    fontFamily: Inter
    fontSize: 6pt
spacing:
  layout-pad: 0.02in
  canvas-pad: 0.05in
  title-pad: 6pt
  label-pad: 1pt
  tick-pad: 1.75pt
  data-margin: 0.05
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
    filled-edge-width: 0.25pt
  outline:
    width: 0.75pt
  median:
    width: 1pt
  contour:
    width: 0.5pt
  heatmap:
    colormap: viridis
  colorbar:
    width: 0.1in
    gap: 0.06in
---

# Academic Figure

The design system for paper figures. The front matter holds the tokens: `paper.use_design()` reads them and sets matplotlib's style, so editing a token changes every figure. The sections below say how to apply them; a chart type's file is more specific, and where it differs from a general rule here, the chart file wins. In a project, the copy in the figures folder is the design; edit it there to give a paper its own look.

## Overview

A figure is read printed in a paper, at the width it is set at, by a reader who looks at it for a few seconds. Every rule serves one goal: the reader gets the figure's one message at a glance and can read the exact numbers the paper claims.

Every rule below follows from these principles; when a case is not covered, apply them directly:

1. **Print first**: sizes are printed sizes, from the tokens; text is never scaled down, and the figure is drawn at the width it is printed at.
2. **One message, one emphasis**: color goes to what the takeaway is about (ours, or the series it names); everything it is compared against or that gives context (baselines, ablations, fronts, reference lines, grids) is `neutral` grey or `ink`. Several colors only when the takeaway compares series on equal terms.
3. **Alike looks alike**: one treatment for every item of a kind, or for none. A kind is the items that play one role: the bars of one series, the levels of one contour plot, the shares of one band, the models the takeaway cites (and, separately, the ones it does not). A series keeps its color, marker and name in every panel and figure; a kind is labelled throughout or not at all, though each label may sit where it fits (inside or outside its mark); a style that tells two series apart is used the same way throughout.
4. **Nothing hides data**: text, legends and marks never cover data, each other, or leave their panel or fill. Context (grid, reference lines) sits behind the data and never decides placement.
5. **Exact and verifiable**: a number the takeaway cites is written on the plot, in the format of the value table, or in the caption when it cannot fit; every number is computed from the data in the script, and the drawing shows all the data it was given (nothing hidden by limits, dropped, or smoothed away when it is a reported result).
6. **Tested, not judged**: whether text collides is what `fit_height` reports, not a judgment; on a report, resolve it by Collisions (Layout).

## Colors

The `colors` tokens are Paul Tol's color-blind-safe `bright` set by role; `colors = paper.use_design()` returns them by name: `colors["series-1"]`, `colors["ours"]`. Pick the first row that fits:

| Case | Color |
|---|---|
| "Ours" among baselines or ablations: the authors' method, or else the series the takeaway is about (an RL-trained model against its base) | `ours` for ours; every series it is compared against in `neutral` |
| Ours against its own ablation (with vs. without a component, the takeaway is the component) | the full method `ours`, the ablated variants `neutral`, as compared series |
| Variants of ours compared together against other methods | all `ours`, told apart by marker shape, `"o"`, `"s"`, `"^"`, on solid lines (the dashes belong to grey series); on curves drawn without markers (ROC and PR staircases, smoothed logs), by line style instead, the full method solid and the others `"--"`, `":"`; the full method first in the legend |
| Parts of one whole (a pie's wedges, a stacked area's bands, a stacked bar's segments) | every part its own color, `series-1` to `series-6` in order: each part must be told from its neighbours, and all of them make the whole (parts are not compared series, so all six colors are free here) |
| Some series the takeaway names, among others it does not | the named ones `series-1`, `series-2`, …; the rest `greys(n)` |
| Several series compared on equal terms, no "ours" (models in a survey, correct vs. incorrect answers, error types) | `series-1`, `series-3`, `series-4`, … in order, skipping the `ours` color, which means ours in every figure of the paper |
| More than six unordered classes (an embedding) | matplotlib's `tab10` (up to 10), `tab20` (up to 20) |
| Groups with sizes or sweeps inside (model sizes per family) | one color per group; within a group, blended with white at 40 / 70 / 100%, light to dark |
| Single series, or one quantity over categories (groups in one box plot) | `series-1` |
| Reference lines | `neutral` (white over filled plots, Shapes) |
| Text, axes, ticks | `ink` |
| Continuous values | the `heatmap.colormap` token, `viridis`, low values dark; signed values `RdBu_r` (`heatmap.md`) |

- **Grey series**: told apart in the Order rule's order (Layout), on lines by line style, `"--"`, `":"`, `"-."` (a solid line is ours' alone) (dashed and dotted at `linewidth=paper.dashed_width`), and on fills (bars, boxes, violins, areas) by shade, `greys(n)` for n grey series, evenly spaced from `neutral-light` to `neutral-dark`, light to dark (one grey series takes `neutral`).
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
| `bar-label` | 6 pt | values written above bars, which sit in a row and must not crowd: `fontsize=paper.bar_label_size` |
| `contour-label` | 6 pt | contour level labels, which sit on the lines and must not crowd them: `fontsize=paper.contour_label_size` |
| `label` | 8 pt | axis labels, subcaptions |
| `legend` | 7 pt | legend entries |
| `title` | 9 pt | panel titles, row and column headers |

- **Numeric tick labels**: horizontal plain numbers (`fit_height` writes matplotlib's default numeric ticks this way, so `0.0, 0.5, 1.0` print as `0, 0.5, 1`), written as short as they read, `0, 0.5, 1`, `1024`, never rotated, never `2³` or `1e+06`: `ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))` (keeping the minus sign). On a linear axis, values below 0.001 are scaled in the axis label ("Learning rate (×10⁻⁴)"), so the ticks read 0, 1, 2, 3. Values of 10,000 and up take SI suffixes (`10K`, `1M`, `1B`), or the unit is scaled in the axis label ("Training step (K)"); on log axes, powers of ten are plain from 0.001 to 1000, then `1e−4` below (with the true minus). An axis of shares is labelled in percent, `0%, 50%, 100%`, as its values are written (Value labels).
- **Tick choice**: the x values a chart file names (stage switches), or else numbers the reader can name, evenly spaced (on a log axis, powers of the base, every one or every second, fifth, …), with the ends of the data range labelled where the axis allows; within that, choose what reads best. When `fit_height` reports tick labels overlapping, label fewer of them, but keep a tick and gridline at every step, so the grid stays as fine as the data: `ax.set_xticks(ticks, labels=[str(t) if i % m == 0 else "" for i, t in enumerate(ticks)])`. Panels that share an axis share its ticks.
- **Corner labels**: when the first tick labels of both axes would overlap at the shared corner, `fit_height` drops the y axis's first label itself.
- **Text tick labels** (non-numeric names) that `fit_height` reports overlapping, by what they name:
  - **Unordered categories, one value each** (methods, models, groups in one bar, error bar or box chart): swap the axes so the names read horizontally down the y axis (horizontal bars, a forest plot, horizontal boxes), ordered top to bottom as under Order.
  - **Names down the y axis** (a heatmap's rows, horizontal bars) that overlap: give the panel height, by widening it at its own aspect (Collisions step 3).
  - **Everything that keeps the x axis** (named bins, the categories of grouped series, benchmarks shared across panels): turn them 45°, `ax.set_xticks(x, labels=names, rotation=45, ha="right", rotation_mode="anchor")` (`ha="left"` on a top axis), then 90° (`rotation=90, ha="center"`) if they still overlap; if they overlap at 90°, Collisions steps 3 and 4 (a colorbar beside the panel moves below it first, giving its width to the panel).
- **Math**: mathtext, set in Inter like the rest (`r"$\mathrm{PPL}_{\mathrm{Base}}$"`); symbols Inter lacks (∝, ≈) go in mathtext too (`$\propto$`).
- **Text on a fill** (a bar segment, a wedge, a heatmap cell, an area band): black or white, whichever reads on it, `color=text_color(fill)`.
- **Text over mixed content** (a note over bars, gridlines and a reference line, where no single fill sets its contrast): on a white box, `bbox=dict(facecolor="white", edgecolor="none", pad=1)`. Contour labels take none: they sit in the gap cut for them.

## Layout

### Width

| Venue | Single column | 1.5 column | Double column | Column gap |
|---|---|---|---|---|
| ICML | 3.25 in | 5.0625 in | 6.75 in | 0.25 in |
| CVPR | 3.25 in | 5.15625 in | 6.875 in | 0.375 in |
| ACL (ARR) | 3 in | 4.6875 in | 6.25 in | 0.25 in |

| Single-column venue | Half text width | Full text width |
|---|---|---|
| ICLR, NeurIPS | 2.75 in | 5.5 in |

Pick the first row that applies:

| Case | Width |
|---|---|
| The user or the task gives a figure width (one column of the paper, a size in inches; a venue's text width alone is not one) | that width; the rules below fit the figure into it |
| The user asks for a 1.5-column `figure*`, or the panels at single column still fail `min_width` after Grid step 3 | 1.5 column |
| Single-column venue, several panels | half the text width when every panel there is at least `min_width` wide by the Standard box formula, else the full text width |
| Single-column venue, one panel | half the text width; the full width only when Collisions step 3 calls for it |
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

0. **Two-factor grid** (models × benchmarks, methods × datasets; also rows of different plots over the same columns, where the plot type is the row factor and each row's y label names it): one factor per row, the other per column, whatever the column limit (a layout the user or task asks for, such as all panels side by side in one row, wins: then each factor's groups are the Grouped axes of step 6): 4 models × 4 benchmarks is 4 × 4. An axis that shows the same quantity in every panel has one range across the grid (`sharex=True` / `sharey=True`); an axis whose quantity changes between columns or rows is shared only down a column (`sharex="col"`) or across a row (`sharey="row"`). Tick numbers only on the left column and bottom row (step 5 does not apply), so panels may be as narrow as 0.9 in, `fit_height(fig, axes, min_width=0.9)` (two columns fit half the text width); if still narrower, put the factor with fewer levels on the columns; never reflow it. No value marks or emphasis that singles out one panel; compared numbers go in the caption.
1. **Start**: every panel in one row, up to the column limit.
2. **Render**: `fit_height` warns when a panel's data area is narrower than `min_width` (1.2 in), or when text is cut off or overlaps.
3. **On a warning**, first free room inside the row: share the y axis when the panels plot the same quantity (step 5), apply Typography's text tick rule, shorten labels. Only when a panel is still too narrow, add a row and set the columns to ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 2 × 3), then render again. Rows have no limit.
4. **Unused cells**: turned off (5 panels in 2 × 3: the last one).
5. **Shared axes**: when panels plot the same quantity over the same range, share it (`plt.subplots(..., sharex=True, sharey=True)`), and a shared axis shows its tick numbers once, as matplotlib does by default: y on the leftmost panel of each row, x on the bottom row. The panels then sit close (Standard box), so small multiples read as one figure. A panel whose axis is not shared keeps its own tick numbers.
6. **Axis labels**: each quantity named once. Panels side by side with the same x quantity: one `fig.supxlabel(label)` under the row, none on the panels; panels stacked with the same y quantity: the y label on the leftmost panel of each row only (or `fig.supylabel` once down the column); inside sub-figures, whose `supxlabel` is the subcaption, each panel keeps its own. Panels side by side with the same y quantity, shared or not: the y label on the leftmost panel only. A panel whose quantity differs carries its own label.
   **Grouped axes**: when columns fall into groups that each plot their own quantity (two panels of accuracy, then two of loss), the first column of each group carries the group's y label and tick numbers, `sharey` within the group, `labelleft=False` on the rest, and the x label follows the same rule: one `fig.supxlabel` when every group has the same x quantity, else one label centred under each group, `paper.group_label(bottom_panels_of_group, "Step")` (`axis="y"` for a group of rows, passing its left panels). The gaps follow from what each column shows (Standard box), so a group's columns sit close and the groups stand apart.
   **Right y axis** (`ax.twinx()`, a second quantity on the same x): it mirrors the left one, four-character tick labels and a label line, in the right margin; the panel narrows and keeps its standard height. The two quantities are equal terms (Colors: `series-1` on the left axis, `series-3` on the right, unless one is ours), gridlines from the left axis only (`twin.grid(False)`), one legend for both, on the left axes raised above the twin so nothing draws over it (`ax.set_zorder(twin.get_zorder() + 1)`, `ax.patch.set_visible(False)`), and a set schedule (learning rate, a warmup) is drawn as given, never smoothed.

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
| 1 : 1 | 1.0 | heatmap (rows / columns instead when not square), scatter plot and embedding (both axes are data), contour plot, stacked area chart, reliability diagram, ROC curve, and every panel of a two-factor grid |
| φ² : 1 | 0.382 | a single panel at full width (Width) |
| 1 : φ | 1.618 | a horizontal chart with more categories down y than its width holds at φ : 1 (`fit_height` reports the tick labels overlapping) |
| φ : 1 | 0.618 | everything else: curves, bars, histograms, box plots, violins, and panels reflowed into rows |

The aspect follows the data, never room for labels. Pie and radar charts are circles: `fit_height` sizes them to the width and ignores `aspect`.

### Collisions

When `fit_height` reports text overlapping, covering data, cut off at the figure edge, sticking out of its panel or spilling out of its fill, resolve it by the first step that clears, rendering after each:

1. **Move it**: that one item to the next placement its chart file lists (another side of the point, below the value, the next legend spot); placements may differ item by item.
2. **Make room inside the panel**: share axes (Grid step 5), apply Typography's text-tick rule (swap axes, then turn 45°, then 90°), shorten the text (an axis label longer than its panel: the short name of the quantity, its detail in the caption).
3. **Give it width**, when the crowding is in labels along an axis (tick labels, bar values, category names side by side, a heatmap's rows or columns) and no figure width is given: the full width, at φ² : 1, or at its own aspect for a fixed-aspect panel (a heatmap's rows grow with it); after widening, try the earlier placements again (horizontal before turned). Crowding inside the data area (value labels on curves, point names on a scatter, a heatmap's cell values, contour labels) goes to step 4 instead.
4. **Write less, alike**: label every m-th item of an ordered kind (ticks, contour levels), keeping every tick, gridline and line; or drop a kind whole (all point names of non-cited models, all bar values, all cell values, all shares of a band) and give the cited numbers in the caption.

Never resolve a collision by shrinking text, changing a token, or changing the aspect for room.

### Height

`fit_height` sets it. Create the figure at the target width with a height equal to it (a start; too short a start can collapse a layout with an outside legend), draw everything (labels, legend, colorbar), call `fit_height` last, then save with plain `fig.savefig`:

```python
fig, axes = plt.subplots(2, 1, figsize=(3.25, 2), sharex=True)
...  # plot, labels, legend, colorbar
fit_height(fig, axes, aspect=0.618)
fig.savefig("outputs/{id}.pdf")
```

- **Panels**: `ax` may be one Axes, an array, a list (also of panels from several sub-figures), or the `subplot_mosaic` dict; hidden cells and colorbars are skipped.
- **Standard box**: every panel's size follows from the figure width W and its number of columns c, never from what the layout engine found, so figures of one width and column count have panels of one size and line up: panel width p = (W − L − R − sum of gaps) / c, with the standard margins L = `canvas-pad` + one line of axis label + four-character tick labels (`−0.00`) and R = `canvas-pad` + half a tick label, and a gap before each later column: half a tick label when the column shares its neighbour's y axis (so the end labels of neighbouring x axes clear each other), a tick label more when it shows its own tick numbers for the same quantity (small multiples), and R + L when its own y label names a new quantity, which starts a new group as if a new figure began there (plus a label line for each further line of its y label), so the groups of a full-width figure line up with half-width figures; in a double-column figure of a two-column venue, a new group also takes the venue's column gap (Width table), `fit_height(..., column_gap=0.25)` for ICML, so its groups line up with the single-column figures above and below. A `fig.supylabel` adds a label line to L; a right y axis (Grid step 6) sets R to `canvas-pad` + a tick label + its label lines, and adds the same to the gap after an inner column that has one. Vertically the same way: the top margin is `canvas-pad` + half a tick label (the top y tick label's reach) or a title line, the bottom margin `canvas-pad` + x tick labels + a line per x label line (or `fig.supxlabel` line), and the gap between rows the upper row's bottom part plus the lower row's top part; an outside legend adds its own height, one row as the standard and each further row more, and anything taller (turned labels, a second title line) widens its margin. Panel height = aspect × p: one figure, one aspect, so every panel of a figure has the same shape (a reliability grid whose diagrams are square has square histograms too; no `height_ratios`). Nothing but a colorbar or a right y axis sits right of the panels, so R never changes otherwise: names that would go there (band names, line-end names) go in a legend above the panel, and a label cut off at the right edge is a collision (see Collisions). Left labels that need more than L (category names) widen the left margin and narrow the panels, which keep the standard height: the aspect gives way. `fit_height` does all this.
- **Labels inside**: `fit_height` keeps every `mark_value` label and bar label (`ax.bar_label`) inside its panel, by growing the limits and turning `mark_value` labels at a side edge inward. Point names (annotations in data coordinates) get at most a quarter more axis range; a name that needs more is reported as sticking out, to be moved. Other text is never moved.
- **Errors**: on `ValueError` (fixed aspect), draw images with `imshow(..., aspect="auto")`; on the "different widths" warning, give all panels the same width.

### Axes

- **Limits**: matplotlib's defaults, with the `data-margin` token (5% of the data range) left at each end so marks at the edges clear the box, except an axis whose marks together fill a bounded whole, fixed to it: stacked shares and areas (0–1), the unit square of ROC and reliability diagrams, a radar's scale, a field given on a fixed range (a loss landscape's −1 to 1). Metrics such as accuracy and the per-bin fractions of a histogram keep the defaults. An axis of a quantity that is never negative starts at 0 or above: `fit_height` raises a negative lower limit to 0 when all the data is above 0, and never grows one below 0.
- **Order**: categories and series with no natural order (methods, models, ablation variants) run in ascending order of the value the takeaway compares, left to right (top to bottom when horizontal), so ours, usually the best, ends at the right. A natural order stays: sizes, time, bins, swept values, and any order the task or data gives explicitly (a benchmark list, a list of opponents). Legends of side-by-side series follow the same order.
- **Category axes**: tick marks hidden on that axis on every panel, `ax.tick_params(axis="x", length=0)` (`axis="y"` when horizontal).
- **Log axes**: an axis of a size, count or rate whose positive values span over 100× (max / min > 100) is log; positions along a process (training steps, epochs, time) stay linear. A log axis is `ax.set_xscale("log")` set before anything is drawn on it, named in the caption; a log₁₀ axis that spans at least one power of ten keeps its minor ticks at 2–9 × each power, unlabelled (`ax.xaxis.set_minor_formatter(NullFormatter())`), and in a chart with gridlines its gridlines follow them, `ax.grid(True, which="both")`.
- **Colorbars** (heatmaps, contour plots, colored lines): always, labelled with the quantity, on the right, `fig.colorbar(mappable, ax=ax, label="Validation loss")`; below the panel (`location="bottom"`) when `fit_height` reports the panel narrower than `min_width` with it on the right.

## Shapes

The marks every chart type is built from, sized by the `components` tokens. Matplotlib applies them; code reads them from `rcParams` or `paper` and never writes the numbers.

| Mark | Token | Look | In code |
|---|---|---|---|
| Panel box | `axes` | a full box on all four sides, `ink`, 0.5 pt | `rcParams["axes.linewidth"]` |
| Ticks | `tick` | outside the box, 0.5 pt, 1.5 pt long (minor 1 pt) | set by the style |
| Grid | `grid` | `ink` at 10% opacity, 0.5 pt, behind the data, both directions unless the chart file says otherwise | `rcParams["grid.linewidth"]`, `rcParams["grid.alpha"]` |
| Data lines | `line` | 1 pt, solid | set by the style |
| Dashed and dotted lines (fits, fronts, series told apart by line style) | `dashed-line` | 0.75 pt | `linewidth=paper.dashed_width` with every `linestyle` other than `"-"` |
| Markers | `marker` | hollow: white fill, a 0.5 pt edge in the series color, 2.5 pt | `rcParams["lines.markersize"]` |
| Filled markers (embedding points) | `marker.filled-edge-width` | a black edge, 0.25 pt, around a translucent fill | `markeredgewidth=paper.filled_edge_width` |
| Points of interest (a minimum, the trained solution) | `marker.highlight-size` | a filled star, 5 pt | `markersize=paper.highlight_size` |
| Outlines and edges (boxes, whiskers, error bars, outlined cells) | `outline` | 0.75 pt, black | `rcParams["patch.linewidth"]` |
| Seams between fills (stacked segments, wedges, area bands) | `grid` | white, 0.5 pt | `edgecolor="white", linewidth=rcParams["grid.linewidth"]` |
| Outline of bars of one color that touch, each bar its own value (reliability bins) | `grid` | a darker shade of the fill, 0.5 pt, never white | `edgecolor=darken(color), linewidth=rcParams["grid.linewidth"]` |
| Box plot median | `median` | 1 pt, black | set by the style |
| Contour lines | `contour` | 0.5 pt | `rcParams["contour.linewidth"]` |
| Colorbar | `colorbar` | a bar 0.1 in wide, 0.06 in from the panels, its labels in a standard margin beside it | placed by `fit_height` |

- **Opacity**: fills take the series color at full opacity, except bands (`alpha=0.2`), scatter clouds (`alpha=0.5`), light polygon fills (radar, `alpha=0.1`), and box plots and violins, which take `lighten(color)` so the black median and the points on them stay readable (grey series too: `lighten(greys(n)[i])`, so the median stays readable on every fill).
- **Reference lines** (a baseline's score, a threshold, a diagonal) are context, so they look like no data series: thin and solid in `neutral`, at the grid's width, `ax.axhline(..., color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)`, thinner than every data line and never dashed, the dash patterns being taken by grey series. Across a filled plot (stacked area, heatmap, contour gradient), where grey sinks into the fills, they are white and dashed. Several reference lines in one panel: the second and later ones dotted, `linestyle=":"`. A line with a value of its own (a baseline's score, a threshold) gets a legend entry when the panel has a legend, else the caption's reading guide names it with its value (Legend: a single entry); a line whose meaning the axes give (y = x, chance, zero) gets none, and the caption's reading guide names it.

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
| A single entry (one series, or one marked point such as a minimum) | none: a lone entry above a panel reads as a title; the caption's reading guide names it ("the star marks the trained minimizer") |
| A filled plot (heatmap, contour gradient, stacked area, stacked or win-rate bars, embedding) | outside, above the panels (above the top row in a grid), or none when every segment is named inside it |
| One panel | inside, at the first spot where `fit_height` stays silent: the corners `"upper left"`, `"upper right"`, `"lower left"`, `"lower right"`, then `"upper center"`, `"lower center"`, `"center left"`, `"center right"`; when none works, outside, above the panel (above its row in a grid) |
| Several panels with the same series | one legend for the figure, above the panels: `fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)` |
| A row of panels with its own series (rows of different plots) | one legend per row, in that row's first panel where it fits, else the next, placed as for one panel; above the row when none fits, centred over the row (`fit_height` centres it) |
| Panels with different series | one per panel, placed as for one panel |
| Sub-figures | one per sub-figure, above its panels, `left.legend(..., loc="outside upper center", ...)` |
| One series per panel | none; the title names it |
| Outside, above one panel | `ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=<entries>, frameon=False)` |

- **Inside is worth a small overlap**: the legend's opaque frame keeps it readable, and it costs no height. It must fit inside its panel: one wider or taller than the free corner of its panel goes above the panel (above its row in a grid), and `fit_height` warns when it sticks out. It must not hide values: `fit_height` warns when it covers a curve, data points or text, when more than a tenth of its area lies over filled marks (bars, boxes, bands, violins, areas), or when it covers any part of a bar's end, which is the bar's value.
- **Columns**: an outside legend starts with all entries in one row; when `fit_height` reports text cut off or matplotlib reports the layout collapsing, `ncol = ceil(n / 2)`, then `ceil(n / 3)`, and so on, skipping a count that repeats, down to one column.
- **Entry order**: curves: ours first, then the other series in color, line-style or shade order; side-by-side series (grouped bars, boxes): left to right; stacked bars and areas: the order of the segments as the reader meets them (top to bottom for vertical stacks, left to right for horizontal ones). When the drawing order differs, pass the handles in entry order: `ax.legend([h_ours, h_a, h_b], ["Ours", "A", "B"], loc=...)`. A legend of several rows reads across each row, left to right, but matplotlib fills it column by column, so pass the entries reordered: `order = [i for c in range(ncol) for i in range(c, n, ncol)]`, `handles = [handles[i] for i in order]`, likewise the labels.
- **`loc`**: always explicit, never `"best"`.

### Value labels

Reported results the takeaway compares are written on the plot, so the reader reads them exactly; diagnostics carry none, and distributions only the summary statistics the takeaway cites (means), where their chart file places them, or in the caption when it gives no place. Each chart file says where (`mark_value` on curves, `ax.bar_label` on bars). Values are written by the first row that applies, in labels and caption alike:

| Value | Written as |
|---|---|
| Copied from the source (the task says the numbers are as printed in a paper) | exactly as printed: `"0.82"` stays `"0.82"` |
| A count (a number of items; a statistic of counts, such as a median, is not one) | an integer, `f"{round(v)}"`: `93`, `1024` (from 10,000, `f"{round(v):,}"`: `12,345`; from 1,000,000, three significant figures with the axis's SI suffix: `1.47B`) |
| A share of a whole (pie, stacked bar, win rate, area; not a metric such as accuracy) | a percent: whole from 10% up, `f"{v:.0%}"`; below, two significant figures, `f"{100 * v:#.2g}%"`, so small shares keep their size: `38%`, `1.8%`, `1.0%`, `0.69%` |
| Given in the data and shown unchanged (not computed by the script) | as given, every value of the kind with as many significant figures as the most precise one has, at most three (the data drops trailing zeros): `0.076` stays `0.076`; `0.64` among `0.612` and `0.774` is `0.640`; `0.82` and `0.0069` stay as they are; `0.54063` is `0.541` |
| 1000 or more | a whole number, `f"{v:.0f}"`: `1234` (from 10,000, `f"{v:,.0f}"`) |
| A difference of two values shown | the decimals of the shown values, so the reader's own subtraction agrees: 0.879 − 0.865 = `0.014` |
| Below 0.001 (not 0) | three significant figures as a power of ten, with the true minus: `3.00×10⁻⁵` (`f"{m:#.3g}×10{exp}"` with a superscript exponent) |
| A ratio | three significant figures: `1.91×` |
| Anything else | three significant figures, trailing zeros kept, `f"{v:#.3g}".rstrip(".")`: `85.0`, `0.912`, `439` |

- **Look**: 7 pt (`value-label`), in `darken(series_color)` beside a mark, `text_color(fill)` on a fill.
- **Tag**: a value label written at a data point with `ax.annotate` or `ax.text` (not by `mark_value`, which tags its own `gid="value-mark"`, or `ax.bar_label`) passes `gid="value-label"`, so `fit_height` keeps it inside its panel like theirs. Labels placed outside the panel on purpose (a histogram's means above it) and point names (even with a value joined) take no tag.

## Do's and Don'ts

- **Size**: do draw at the printed width and let `fit_height` set the height; don't save with `bbox_inches="tight"`, which changes the size.
- **Tokens**: do read sizes from the tokens; don't write line widths, marker or font sizes as numbers, and don't shrink text to make room.
- **Legend**: do give every legend an explicit `loc`; don't use `"best"`.
- **Names**: do letter sub-figures with subcaptions below and title panels above; don't give the figure a title.
- **Ticks**: do write numeric ticks as plain horizontal numbers; don't rotate them or write `2³`.
- **Colors**: do use the color roles; don't pick colors outside them unless the user asks.
- **3D**: do draw a contour plot for a function of two variables; don't draw 3D surfaces.
- **Pies**: do use a bar chart for more than six parts or several wholes; don't draw such a pie.
