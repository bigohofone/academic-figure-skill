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
  neutral: "#737373"
  neutral-light: "#D1D1D1"
  neutral-dark: "#555555"
  ink: "#000000"
typography:
  tick-label:
    fontFamily: Inter
    fontSize: 6pt
  label:
    fontFamily: Inter
    fontSize: 7pt
  legend:
    fontFamily: Inter
    fontSize: 7pt
  legend-inside:
    fontFamily: Inter
    fontSize: 5pt
  value-label:
    fontFamily: Inter
    fontSize: 6pt
    fontWeight: 400
  title:
    fontFamily: Inter
    fontSize: 7pt
    fontWeight: 400
  contour-label:
    fontFamily: Inter
    fontSize: 6pt
  bar-label:
    fontFamily: Inter
    fontSize: 6pt
spacing:
  layout-pad: 0in
  canvas-pad: 0.05in
  panel-gap: 0.05in
  title-pad: 4pt
  label-pad: 1pt
  tick-pad: 1pt
  data-margin: 5%
components:
  axes:
    width: 0.5pt
    textColor: "{colors.neutral}"
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
    gap: 0.05in
---

# Academic Figure

Design system for paper figures. Front matter holds the tokens; `paper.apply_design()` loads them into matplotlib's style, so a token edit changes every figure. Chart type file conflicts with a rule here: chart file wins. In a project, the copy in the figures folder is the design; edit it there for a paper-specific look.

## Overview

Figure is read in print, at its set width, for a few seconds. Goal: one message at a glance, exact numbers the paper claims readable. Case not covered: apply these principles.

1. Print first: sizes are printed sizes, from tokens. Never scale text down; draw at printed width.
2. One message, one emphasis: color only for what the takeaway is about (ours, or series it names). Everything compared or context (baselines, ablations, fronts, reference lines, grids): `neutral` grey or `ink`. Several colors only when takeaway compares series on equal terms.
3. Alike looks alike: one treatment for every item of a kind, or none. Kind = items with one role: bars of one series, levels of one contour plot, shares of one band, models the takeaway cites (and, separately, those it does not). Series keeps color, marker, name in every panel and figure. Kind labelled throughout or not at all; each label may sit where it fits (inside or outside its mark). Style that tells two series apart: used the same way throughout.
4. Nothing hides data: text, legends, marks never cover data or each other, never leave panel or fill. Context (grid, reference lines) behind data, never decides placement.
5. Exact and verifiable: number the takeaway cites written on plot in Value labels table format; in caption if it cannot fit. Every number computed from data in the script. Drawing shows all given data: nothing hidden by limits, dropped, or smoothed away when a reported result.
6. Tested, not judged: collision = what `finalize_figure` reports; resolve by Collisions (Layout).

## Colors

`colors` tokens: Paul Tol's color-blind-safe `bright` set, by role. `paper.apply_design()` returns them by name:

```python
colors = paper.apply_design()
colors["series-1"], colors["ours"]
```

First row that fits:

| Case | Color |
|---|---|
| "Ours" among baselines or ablations: authors' method, else series the takeaway is about (RL-trained model vs. its base) | `ours`; every compared series `neutral` |
| Ours vs. its own ablation (with vs. without a component; takeaway is the component) | full method `ours`, ablated variants `neutral`, as compared series |
| Variants of ours together vs. other methods | all `ours`, apart by marker `"o"`, `"s"`, `"^"` on solid lines (dashes belong to grey series). Curves without markers (ROC/PR staircases, smoothed logs): by line style, full method solid, others `"--"`, `":"`. Full method first in legend |
| Parts of one whole (pie wedges, stacked area bands, stacked bar segments) | each part own color, `paper.part_colors(n)`: palette hues in stacking order, lightness evenly spread, alternating dark/light, every two parts apart in grayscale. Not compared series: all six colors free |
| Some series the takeaway names, among others it does not | named ones in equal-terms order below (`series-1`, `series-4`, …); rest `baseline_greys(n)` |
| Several series on equal terms, no "ours" (models in a survey, correct vs. incorrect answers, error types) | `series-1`, `series-4`, `series-6`, `series-5`, `series-3` in order (alternates light/dark for grayscale). Skip `ours` color: means ours in every figure of the paper |
| More than six unordered classes (embedding) | `tab10` (≤10), `tab20` (≤20), plus own marker per class: `"o"`, `"s"`, `"^"`, `"D"`, `"v"`, `"<"`, `">"`, `"P"`, `"X"`, `"*"` |
| Groups with sizes or sweeps inside (model sizes per family, network depths, batch sizes) | one color per group (ours: `ours`; a baseline family: `neutral`, dashed); within a group `paper.ramp(group_color, n)`: one hue, light to dark (L* 70 → 25), the largest setting darkest |
| Single series, or one quantity over categories (groups in one box plot) | `series-1` |
| Reference lines | `neutral` (white over filled plots, Shapes) |
| Text and tick labels | `ink` |
| Panel box and tick marks | `neutral` (the `axes.textColor` token) |
| Continuous values | `heatmap.colormap` token, `viridis`, low values dark; signed values `RdBu_r` (`heatmap.md`) |

- Grey series: assigned in Order rule's order (Layout). Lines: line style `"--"`, `":"`, `"-."` (solid is ours' alone), dashed/dotted at `linewidth=paper.dashed_width`. Fills (bars, boxes, violins, areas): shade, `baseline_greys(n)` for n grey series, evenly spaced `neutral-light` to `neutral-dark`, light to dark, skipping `ours` lightness. One grey series: `neutral`.
- Many grey series: >4 lines: add markers, one shape per series (`line-chart.md`). >6: draw series the takeaway names; group rest as one grey series, "Other baselines".
- Shared color (ours and its variants, greys): differ by line style or shade as above.
- On white: grey lines, markers, reference lines `neutral` at full opacity; `neutral-light` fills only. Series text: `darken(series_color)` (grey series: `darken(colors["neutral"])`). Text on fill: Typography.
- Grayscale / color blindness: series told apart by color alone also differ in lightness by ≥10 L*: ours (`series-2`, L* 61) vs. darker `neutral` (L* 48); greys skip its lightness. Lines also differ by style or marker, bars by shade. `finalize_figure` warns when two such series look alike in grayscale.
- Emphasis: user names a series to emphasize: color it as ours, all others as compared.
- Other palettes: paper-wide (lab, brand): change `colors` tokens in design copy. One-off for one figure ("match the original"): dict in that figure's script:

```python
PALETTE = {"ours": "#5F16A7", "base": "#63C9D2"}
```

## Typography

One family, `Inter` (bundled), all text and math, regular weight only (nothing bold). Text `ink` unless it belongs to one series.

| Token | Size | Used for |
|---|---|---|
| `tick-label` | 6 pt | tick labels |
| `value-label` | 6 pt | all text inside chart (value labels, cell text, point names, pie labels); default for `ax.text`, `ax.annotate` |
| `bar-label` | 6 pt | values above bars (row must not crowd): `fontsize=paper.bar_label_size` |
| `contour-label` | 6 pt | contour level labels (must not crowd lines): `fontsize=paper.contour_label_size` |
| `label` | 7 pt | axis labels, subcaptions |
| `legend` | 7 pt | legend entries |
| `legend-inside` | 5 pt | entries of a legend inside a panel with no spot at `legend` size (set by `finalize_figure`) |
| `title` | 7 pt | panel titles, row and column headers |

- Values given as text in the data (`"1e-5"`, `"3e-4"`): written as given, keeping the scientific notation; only the hyphen becomes a true minus (`1e−5`).
- Numeric tick labels: horizontal, plain, shortest form (`0, 0.5, 1`, `1024`); never rotated, never `2³` or `1e+06`. `finalize_figure` does this for matplotlib's default numeric ticks (`0.0, 0.5, 1.0` → `0, 0.5, 1`). Formatter, keeps true minus:

  ```python
  ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
  ```

  - Linear axis, values <0.001: scale in axis label ("Learning rate (×10⁻⁴)"), ticks 0, 1, 2, 3.
  - ≥1000: SI suffixes, one unit per axis, when that writes the ticks shorter (`0, 0.5K, 1K, 1.5K, 2K`, `10K`, `1M`; `200 … 1000` and `1024` stay); `finalize_figure` writes matplotlib's default ticks this way. Or the unit scaled in the axis label ("Training step (K)").
  - Log axes: powers of ten plain from 0.001 to 1000; above, SI suffix (10K, 1M); below, `1e−4` (true minus). `finalize_figure` writes them so.
  - Shares: percent, `0%, 50%, 100%`, as values are written (Value labels).
- Tick choice: x values the chart file names (stage switches), else evenly spaced nameable numbers (log axis: powers of the base, every one or every second, fifth, …); label data range ends where axis allows. On tick label overlap report: label every m-th, keep tick and gridline at every step (grid as fine as data). Panels sharing an axis share its ticks.

  ```python
  ax.set_xticks(ticks, labels=[str(t) if i % m == 0 else "" for i, t in enumerate(ticks)])
  ```

- Corner labels: first tick labels of both axes overlap at corner: `finalize_figure` drops y axis's first label itself.
- Text tick labels (non-numeric) reported overlapping:
  - Unordered categories, one value each (methods, models, groups in one bar, error bar or box chart): swap axes, names horizontal down y (horizontal bars, forest plot, horizontal boxes), top to bottom per Order.
  - Names down y axis (heatmap rows, horizontal bars): panel height by widening at own aspect (Collisions step 3).
  - Everything keeping the x axis (named bins, categories of grouped series, benchmarks shared across panels): 45° (`ha="left"` on top axis), then 90°. Still overlapping at 90°: Collisions steps 3 and 4 (colorbar beside panel first moves below it, giving its width to the panel).

    ```python
    ax.set_xticks(x, labels=names, rotation=45, ha="right", rotation_mode="anchor")
    ax.set_xticks(x, labels=names, rotation=90, ha="center")
    ```

- Math: mathtext in Inter (`r"$\mathrm{PPL}_{\mathrm{Base}}$"`). Symbols Inter lacks (∝, ≈): mathtext too (`$\propto$`).
- Text on fill (bar segment, wedge, heatmap cell, area band): black or white, whichever reads, `color=text_color_on(fill)`.
- Text over mixed content (note over bars, gridlines, reference line; no single fill sets contrast): white box. Contour labels: none, they sit in the gap cut for them.

  ```python
  bbox=dict(facecolor="white", edgecolor="none", pad=1)
  ```

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

First row that applies:

| Case | Width |
|---|---|
| User or task gives a figure width (one column of the paper, inches; venue text width alone is not one) | that width |
| User asks for 1.5-column `figure*`, or panels at single column still fail `min_width` after grid's step 3 (`multi-panel.md`) | 1.5 column |
| Single-column venue, several panels | half text width if they fit in one row there (every panel ≥ `min_width`), else full text width; then rows as `multi-panel.md` adds them |
| Single-column venue, one panel | half text width; full only when Collisions step 3 calls for it |
| Two-column venue | single column if the panels fit in one row there, else double column; then rows as `multi-panel.md` adds them |

Venue: the one the user names; default ICLR.

Venue not in the tables (a journal, a workshop, another conference): read its widths from its LaTeX template or author guide (`\textwidth`, `\columnwidth`, `\columnsep`; ask the user when neither is at hand), add its row to the table above in the project's DESIGN.md, then use it like the others. Two-column venue: 1.5 column = (single + double) / 2 + column gap / 4. Single-column venue: half text width = text width / 2.

### Panels

One panel: no title (caption names the figure). Several panels, sub-figures, or second y axis (`ax.twinx()`): read `multi-panel.md` in skill's `references/` for grid, shared axes, axis labels, panel names.

### Panel aspect

Per panel, width : height. Fixed by the chart's geometry for these; pass `aspect=`:

| Aspect | `aspect=` | For |
|---|---|---|
| 1 : 1 | 1.0 | embedding (t-SNE, UMAP), contour plot, stacked area chart (thin bands need the height), reliability diagram, ROC curve, scatter plot of one quantity against itself (predicted vs actual) |
| cells square | `n_rows / n_cols` | heatmap |

Every other chart: leave `aspect` out; `finalize_figure` picks it from the width each panel gets (figure width / columns):

| Panel width | Aspect | For |
|---|---|---|
| < 2.5 in | 1 : 1 | panels in rows (two-factor grids, small multiples, sub-figures): square keeps the vertical room the data's changes need |
| 2.5–3.5 in | φ : 1 | one column's width: a single panel at single column or half text width, two panels across a page |
| > 3.5 in | 2φ : 1 | wider: a single panel at 1.5 column or full width, two golden rectangles side by side |

A horizontal chart with more categories down y than fit (`finalize_figure` reports tick labels overlapping): Collisions step 3 first; still overlapping, 1 : φ (`aspect=1.618`).

Aspect follows data, never room for labels. Pie and radar: circles; `finalize_figure` sizes them to width, ignores `aspect`.

### Collisions

`finalize_figure` reports text overlapping, covering data, cut off at figure edge, out of its panel, or spilling out of its fill: first step that clears, render after each:

1. Move it: that item to next placement its chart file lists (other side of point, below value, next legend spot). Placements may differ per item.
2. Make room inside panel: share axes (`multi-panel.md`); Typography's text-tick rule (swap axes, then 45°, then 90°); shorten text (axis label longer than panel: short name of quantity, detail in caption).
3. Give it width, if crowding is labels along an axis (tick labels, bar values, side-by-side category names, heatmap rows or columns) and no figure width given: full width (aspect by Panel aspect), or own aspect for fixed-aspect panel (heatmap rows grow with it). After widening, retry earlier placements (horizontal before turned). Crowding inside data area (value labels on curves, scatter point names, heatmap cell values, contour labels): step 4 instead.
4. Write less, alike: label every m-th item of an ordered kind (ticks, contour levels), keep every tick, gridline, line; or drop a kind whole (all point names of non-cited models, all bar values, all cell values, all shares of a band), cited numbers to caption.

Never: shrink text, change a token, or change aspect for room. One exception: a heatmap's cell values and row and column names, which `finalize_figure` sets to the size that fits every cell (down to 4 pt).

### Height

Set by `finalize_figure`. Create figure at target width, height = width (too short a start can collapse a layout with outside legend). Draw everything (labels, legend, colorbar), call `finalize_figure` last, save with plain `fig.savefig`:

```python
fig, axes = plt.subplots(2, 1, figsize=(3.25, 2), sharex=True)
...  # plot, labels, legend, colorbar
finalize_figure(fig, axes)
fig.savefig("outputs/{id}.pdf")
```

- Panels: `ax` = one Axes, array, list (also panels from several sub-figures), or `subplot_mosaic` dict; hidden cells and colorbars skipped.
- Standard box: `finalize_figure` sets standard margins, gaps, size; figures of one width and column count line up. Never set margins, `subplots_adjust`, `height_ratios`, `width_ratios`. Figure exactly the text width of a two-column venue (spanning both columns): pass venue's column gap (Width table), e.g. ICML; any other width: none:

  ```python
  finalize_figure(fig, axes, column_gap=0.25)
  ```

  Right of panels: only colorbar or right y axis. Names that would go there (band names, line-end names): legend above panel.
- Labels inside: `finalize_figure` keeps `mark_value` labels, bar labels, tagged value labels inside panel by growing limits; other text never moved.
- Errors: `ValueError` (fixed aspect): images with `aspect="auto"`. "Different widths" warning: give all panels same width.

  ```python
  ax.imshow(image, aspect="auto")
  ```

### Axes

- Limits: matplotlib defaults plus `data-margin` token (5% of data range) each end, edge marks clear the box. Except axis whose marks together fill a bounded whole: fixed to it (stacked shares and areas 0–1, ROC and reliability unit square, radar scale, field on fixed range such as loss landscape −1 to 1). Metrics (accuracy, histogram per-bin fractions): defaults. Never-negative quantity: starts at ≥0; `finalize_figure` raises negative lower limit to 0 when all data >0, never grows one below 0.
- Order: categories and series with no natural order (methods, models, ablation variants): ascending by value the takeaway compares, left to right (top to bottom when horizontal); ours, usually best, ends right. Natural order stays: sizes, time, bins, swept values, any order task or data gives explicitly (benchmark list, list of opponents). Legends of side-by-side series: same order.
- Category axes: tick marks hidden on that axis, every panel (`axis="y"` when horizontal):

  ```python
  ax.tick_params(axis="x", length=0)
  ```

- Log axes: size, count or rate with positive values spanning >100× (max / min > 100, over every panel showing that quantity: one scale per quantity in a figure): log. Positions along a process (training steps, epochs, time): linear. Set log scale before drawing on the axis; name it in caption. Log₁₀ axis spanning ≥1 power of ten: unlabelled minor ticks at 2–9 × each power; with gridlines, gridlines follow them.

  ```python
  ax.set_xscale("log")
  ax.xaxis.set_minor_formatter(NullFormatter())
  ax.grid(True, which="both")
  ```

- Colorbars (heatmaps, contour plots, colored lines): always (except a heatmap with every cell's value written, `heatmap.md`), labelled with quantity, on right. Below panel when `finalize_figure` reports panel narrower than `min_width` with it on right. A colorbar spans its panels: as tall as they are, or below, as wide as all of them.
  - Several panels on one scale (`vmin`, `vmax` shared): one colorbar for all. Scales differ: one beside (or under) each panel, each labelled; `finalize_figure` makes room for it before the next panel.

  ```python
  fig.colorbar(mappable, ax=ax, label="Validation loss")
  fig.colorbar(mappable, ax=ax, label="Validation loss", location="bottom")
  fig.colorbar(mappable, ax=axes, label="Validation loss")  # one scale across panels
  ```

## Shapes

Marks every chart type is built from, sized by `components` tokens. Matplotlib applies them; code reads from `rcParams` or `paper`, never writes the numbers.

| Mark | Token | Look | In code |
|---|---|---|---|
| Panel box | `axes` | full box, all four sides, `neutral` grey, 0.5 pt; tick marks the same grey, tick labels `ink` | `rcParams["axes.linewidth"]` |
| Ticks | `tick` | outside box, 0.5 pt, 1.5 pt long (minor 1 pt) | set by style |
| Grid | `grid` | `ink` at 10% opacity, 0.5 pt, behind data, both directions unless chart file says otherwise | `rcParams["grid.linewidth"]`, `rcParams["grid.alpha"]` |
| Data lines | `line` | 1 pt, solid | set by style |
| Dashed and dotted lines (fits, fronts, series apart by line style) | `dashed-line` | 0.75 pt | `linewidth=paper.dashed_width` with every `linestyle` other than `"-"` |
| Markers | `marker` | hollow: white fill, 0.5 pt edge in series color, 2.5 pt | `rcParams["lines.markersize"]` |
| Filled markers (embedding points) | `marker.filled-edge-width` | black edge, 0.25 pt, translucent fill | `markeredgewidth=paper.filled_edge_width` |
| Points of interest (a minimum, the trained solution) | `marker.highlight-size` | filled star, 5 pt (the style draws markers hollow: fill it) | `"*", markersize=paper.highlight_size, markerfacecolor=color` |
| Outlines and edges (boxes, whiskers, error bars) | `outline` | 0.75 pt, black | `rcParams["patch.linewidth"]` |
| Seams between fills (stacked segments, wedges, area bands) | `grid` | white, 0.5 pt | `edgecolor="white", linewidth=rcParams["grid.linewidth"]` |
| Outline of touching one-color bars, each its own value (reliability bins) | `grid` | darker shade of fill, 0.5 pt, never white | `edgecolor=darken(color), linewidth=rcParams["grid.linewidth"]` |
| Box plot median | `median` | 1 pt, black | set by style |
| Contour lines | `contour` | 0.5 pt | `rcParams["contour.linewidth"]` |
| Colorbar | `colorbar` | 0.1 in wide, 0.06 in from panels, labels in standard margin beside it | placed by `finalize_figure` |

- Opacity: fills at full series color, except bands (`alpha=0.2`), scatter clouds (`alpha=0.5`), light polygon fills (radar, `alpha=0.1`), box plots and violins: `lighten(color)` so black median and points on them stay readable; grey series too (`lighten` of their `baseline_greys(n)` shade). Ours keeps full color there (lightened colors all print pale grey; ours must stay apart).
- Reference lines (baseline score, threshold, diagonal): context, look like no data series. Thin, solid, `neutral`, grid width, thinner than every data line, never dashed (dashes belong to grey series). Across filled plot (stacked area, heatmap, contour gradient; grey sinks into fills): white, dashed. Second and later in one panel: dotted. Line with own value (baseline score, threshold): legend entry if panel has a legend, else caption's reading guide names it with its value (Legend: a single entry). Line whose meaning the axes give (y = x, chance, zero): no entry; caption's reading guide names it.

  ```python
  ax.axhline(y, color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
  ax.axhline(y2, color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1, linestyle=":")
  ```

## Components

### Chart types

Each chart type has its own file next to this one. Read the file of every chart type used before drawing.

| Chart type | Use it for | File |
|---|---|---|
| Line chart | values along continuous x: learning curves, scaling curves, pass@k, ROC and precision-recall curves | `line-chart.md` |
| Bar chart | reported results across methods, ablations or benchmarks; parts of a whole per category | `bar-chart.md` |
| Scatter plot | two quantities per item: accuracy vs. cost; embeddings | `scatter-plot.md` |
| Box plot | spread of many values per group, compared across groups | `box-plot.md` |
| Heatmap | values over two categorical axes: confusion matrix, attention map, hyperparameter grid | `heatmap.md` |
| Histogram | how one quantity's values are spread | `histogram.md` |
| Error bar plot | means with uncertainty, when compared values differ by <10% | `error-bar-plot.md` |
| Area chart | shares of a whole along continuous x | `area-chart.md` |
| Contour plot | function of two continuous variables | `contour-plot.md` |
| Radar chart | a few models' profiles across 5 to 10 benchmarks | `radar-chart.md` |
| Pie chart | composition of one whole, two to six parts | `pie-chart.md` |
| Violin plot | as box plot, when shape of spread matters | `violin-plot.md` |

- Tables: many exact numbers, no trend or comparison to see (every method on every dataset): suggest a table instead.

### Legend

First row that fits:

| Case | Legend |
|---|---|
| Single entry (one series, or one marked point such as a minimum) | none (lone entry above panel reads as title); caption's reading guide names it ("the star marks the trained minimizer") |
| Filled plot (heatmap, contour gradient, stacked area, stacked or win-rate bars, embedding) | outside, above panels (above top row in a grid); none when every segment named inside |
| One panel | `ax.legend()` without `loc`: `finalize_figure` puts it at the first inside spot where it hides nothing (corners, then edge centers): at `legend` size, else at `legend-inside` size, else above the panel in one row at `legend` size |
| Several panels, same series | one legend, shown once: `ax.legend()` without `loc` on the first panel; `finalize_figure` puts it inside the first panel that has a spot where it hides nothing (sizes as for one panel: every panel at `legend` size first), the others carry none; no panel has room: above, centred over the row |
| Row of panels with own series (rows of different plots) | one per row, as for several panels with the same series, within the row |
| Panels with different series | one per panel, placed as for one panel |
| Sub-figures | one per sub-figure, above its panels (`sub-figure legend` below) |
| One series per panel | none; title names it |
| Outside, above one panel | `outside panel legend` below |

```python
# sub-figure legend
left.legend(handles, labels, loc="outside upper center", ncol=n_entries)
# outside panel legend
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=n_entries)
```

- Frame: every legend, inside or outside, in its box (the style's light grey edge, opaque fill); never `frameon=False`.
- Inside: worth a small overlap (opaque frame, no height cost). Hides nothing: no curve, data point, text or bar end; ≤1/10 of its area over filled marks. `finalize_figure` checks this when placing it, and warns when a legend with an explicit `loc` breaks it.
- Outside legend columns: start in one row. On cut-off text or matplotlib layout collapse: `ncol = ceil(n / 2)`, then `ceil(n / 3)`, …, skip repeated counts, down to 1.
- Shared words: entries that share a word and differ by a setting ("Depth 4", "Depth 8", …; a sweep in `ramp` shades): `paper.legend_rows`, one row per shared word, written once at the row's start, each entry only its setting ("Depth  4 8 16 32 64"; two sweeps: two rows). A row too wide for any panel: on the figure, above the panels.

  ```python
  paper.legend_rows(ax, [("Depth", handles, [4, 8, 16, 32, 64])])
  paper.legend_rows(fig, [("Depth", depth_handles, depths), ("Width", width_handles, widths)],
                    loc="outside upper center", borderaxespad=0)
  ```
- Entry order: curves: ours first, then others in color, line-style or shade order. Side-by-side series (grouped bars, boxes): left to right. Stacked bars and areas: segments as met (top to bottom for vertical stacks, left to right for horizontal). Drawing order differs: pass handles in entry order. Always pass entries in reading order: when `finalize_figure` lays a legend out in several columns, it keeps the rows reading left to right.

  ```python
  ax.legend([h_ours, h_a, h_b], ["Ours", "A", "B"])
  ```

- `loc`: none for a panel legend (`finalize_figure` places it); explicit for figure, sub-figure and outside legends. Never `"best"`.

### Value labels

- Reported results the takeaway compares: written on plot.
- Diagnostics: none.
- Distributions: only summary statistics the takeaway cites (means), where chart file places them, else caption.
- Placement per chart file (`ax.bar_label` on bars, cell text in heatmaps). Curves: none; compared values in caption (`line-chart.md`).

Format: first row that applies, labels and caption alike (formats in block below):

| Value | Written as |
|---|---|
| Copied from source (task says numbers as printed in a paper) | exactly as printed: `"0.82"` stays `"0.82"` |
| Count (number of items; a statistic of counts, such as a median, is not one) | integer, `count`: `93`, `1024`; ≥10,000 `count_10k`: `12,345`; ≥1,000,000 three significant figures with axis's SI suffix: `1.47B` |
| Share of a whole (pie, stacked bar, win rate, area; not a metric such as accuracy) | percent: ≥10% whole, `share`; below, two significant figures, `small_share` (small shares keep their size): `38%`, `1.8%`, `1.0%`, `0.69%` |
| Given in data, shown unchanged (not computed by script) | as given; every value of the kind with as many significant figures as the most precise one, at most three (data drops trailing zeros): `0.076` stays `0.076`; `0.64` among `0.612` and `0.774` → `0.640`; `0.82`, `0.0069` stay; `0.54063` → `0.541` |
| ≥1000 | whole number, `large`: `1234`; ≥10,000 `large_10k` |
| Difference of two shown values | decimals of the shown values, so reader's subtraction agrees: 0.879 − 0.865 = `0.014` |
| <0.001 (not 0) | three significant figures as power of ten, true minus, `tiny` with superscript exponent: `3.00×10⁻⁵` |
| Ratio | three significant figures: `1.91×` |
| Anything else | three significant figures, trailing zeros kept, `other`: `85.0`, `0.912`, `439` |

```python
count = f"{round(v)}"
count_10k = f"{round(v):,}"
share = f"{v:.0%}"
small_share = f"{100 * v:#.2g}%"
large = f"{v:.0f}"
large_10k = f"{v:,.0f}"
tiny = f"{m:#.3g}×10{exp}"
other = f"{v:#.3g}".rstrip(".")
```

- Look: 6 pt (`value-label`); beside a mark `darken(series_color)`, for every grey series one color, `darken(colors["neutral"])`; on a fill `text_color_on(fill)`.
- Tag: value label at a data point via `ax.annotate` or `ax.text`: pass `gid="value-label"`, so `finalize_figure` keeps it inside panel. `mark_value` tags its own (`gid="value-mark"`); `ax.bar_label` needs none. No tag: labels outside panel on purpose (histogram means above it), point names (even with a value joined).
