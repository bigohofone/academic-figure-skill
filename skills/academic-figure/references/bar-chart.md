# Bar chart

Reported results across categories, one value each: methods, ablations or settings on one or more benchmarks. Values differ by < 10% (`(max - min) / max < 0.1`): error bar plot instead (`error-bar-plot.md`). Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Bars: horizontal gridlines only; y from 0 (matplotlib default).
  ```python
  bars = ax.bar(x, values, width, color=color, linewidth=0)
  ax.grid(axis="x", visible=False)
  ```
- Error bars (several runs): ±1 std.
  ```python
  ax.bar(..., yerr=std, capsize=2, error_kw=dict(ecolor=colors["ink"]))
  ```

## Variants

- Grouped (several series per category): series share 0.8 of category slot; one legend entry per series. Category groups in different units or ranges (one group's max < half another's max): one panel each, titled with group.
  ```python
  width = 0.8 / n_series
  x_i = x + (i - (n_series - 1) / 2) * width  # series i
  ```
- Horizontal (category names don't fit side by side, DESIGN.md Typography): `ax.barh`, categories top to bottom, vertical gridlines only.
  ```python
  ax.invert_yaxis()
  ax.grid(axis="y", visible=False)
  ```
- Stacked (parts of a whole per category): segments in series order from bottom; shares: axis fixed to whole.
  ```python
  ax.bar(x, v, bottom=below, color=color, edgecolor="white", linewidth=rcParams["grid.linewidth"])
  ax.set_ylim(0, 1)
  ```
- Win rate (pairwise win/tie/loss): one horizontal stacked bar per opponent; segments win, tie, loss from left; each bar sums to 1. Win `colors["ours"]`, tie and loss `make_shades(colors["neutral"], 2)`. 50% reference line only when paper reads win rates against it.
- Reliability diagram (calibration): one square panel (confidence histograms above: two-factor grid of square panels, DESIGN.md Grid step 0); both axes 0–1. Confidence bins on x; per-bin accuracy as touching bars in `series-1`, outlined in darker own color, never white. Paper shows gap to bin's mean confidence: second equal-terms series (DESIGN.md Colors: `series-4`, skipping ours), opaque light fill from accuracy to confidence, drawn on top. Perfect-calibration diagonal. No value labels.
  ```python
  ax.bar(edges[:-1], accuracy, width=np.diff(edges), align="edge", color=colors["series-1"],
         edgecolor=shift_lightness(colors["series-1"], -1), linewidth=rcParams["grid.linewidth"])
  ax.bar(edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence),
         width=np.diff(edges), align="edge", color=shift_lightness(colors["series-4"], 2),
         edgecolor=shift_lightness(colors["series-4"], -1), linewidth=rcParams["grid.linewidth"], label="Gap")
  ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
  ```

## Labels

- Bar values: every bar of a reported result, per DESIGN.md value table, written level; `finalize_figure` turns a panel's values upward when any overlap.
  ```python
  ax.bar_label(bars, labels=[f"{v:#.3g}" for v in values], color=shift_lightness(color, -1))
  ```
- Segment values (stacked, win rate): inside each segment; `texts` as shares (DESIGN.md Value labels). Spills out of segment: drop (Collisions step 3; each segment its own kind).
  ```python
  ax.bar_label(bars, labels=texts, label_type="center", color=text_color)  # on the segment color, DESIGN.md Typography
  ```

## Caption

- Error bars: what they show, over how many runs.
- Reliability diagram: "the diagonal marks perfect calibration; the light bars show the gap to the mean confidence"; each model's expected calibration error (ECE).
