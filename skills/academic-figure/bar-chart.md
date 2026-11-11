# Bar chart

Reported results compared across categories, one value each: methods, ablations or settings on one or more benchmarks. When the compared values differ by less than 10% of their size (`(max - min) / max < 0.1`), a bar from 0 hides the differences: draw an error bar plot instead (`error-bar-plot.md`). Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Bars**: `bars = ax.bar(x, values, width, color=color, linewidth=0)`, horizontal gridlines only, `ax.grid(axis="x", visible=False)`. The y axis starts at 0 (matplotlib's default for bars): a bar's length is its value.
- **Error bars** (several runs): ±1 std, `ax.bar(..., yerr=std, capsize=2, error_kw=dict(elinewidth=rcParams["patch.linewidth"], capthick=rcParams["patch.linewidth"], ecolor=colors["ink"]))`.

## Variants

- **Grouped bar chart** (several series per category): the series of one category share 0.8 of its slot, `width = 0.8 / n_series`, series `i` at `x + (i - (n_series - 1) / 2) * width`; one legend entry per series. Groups of categories in different units or ranges (one group's largest value below half of another group's largest) go in one panel each, titled with the group.
- **Horizontal bar chart** (category names that don't fit side by side, DESIGN.md Typography): `ax.barh`, categories top to bottom (`ax.invert_yaxis()`), vertical gridlines only, `ax.grid(axis="y", visible=False)`.
- **Stacked bar chart** (parts of a whole per category): segments in series order from the bottom, `ax.bar(x, v, bottom=below, color=color, edgecolor="white", linewidth=rcParams["grid.linewidth"])`; shares fix the axis to the whole, `ax.set_ylim(0, 1)`.
- **Win rate chart** (pairwise judgments of win, tie or loss): one horizontal stacked bar per opponent, segments win, tie, loss from the left, each bar summing to 1; win in `colors["ours"]`, tie and loss in `greys(2)`; a reference line at 50% only when the paper reads win rates against it.
- **Reliability diagram** (calibration): one square panel, both axes fixed to 0–1; confidence bins on x, each bin's accuracy as a bar touching its neighbours in `series-1`, `ax.bar(edges[:-1], accuracy, width=np.diff(edges), align="edge", color=colors["series-1"], edgecolor="white", linewidth=rcParams["grid.linewidth"])`; when the paper shows the gap to the bin's mean confidence, it is the second series of equal terms (DESIGN.md Colors: `series-3`, skipping ours), an opaque light fill from the accuracy to the confidence, drawn on top so it never mixes with the accuracy bar, `ax.bar(edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence), width=np.diff(edges), align="edge", color=lighten(colors["series-3"]), edgecolor=colors["series-3"], linewidth=rcParams["grid.linewidth"], label="Gap")`; the perfect-calibration diagonal, `ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)`. No value labels: the gap to the diagonal is the message.

## Labels

- **Bar values**: every bar of a reported result, `ax.bar_label(bars, labels=[f"{v:#.3g}" for v in values], color=darken(color))`, written by DESIGN.md's value table. Placements (for Collisions): horizontal, then turned to read upward, `rotation=90, padding=2`.
- **Values on segments** (stacked, win rate): each segment's value inside it, `ax.bar_label(bars, labels=texts, label_type="center", color=text_color(color))`, `texts` written as shares (DESIGN.md Value labels); a label that spills out of its segment is dropped (Collisions step 3; for segments, each segment is its own kind).

## Caption

- **Error bars**: what they show and over how many runs.
- **Reliability diagram**: "the diagonal marks perfect calibration; the light bars show the gap to the mean confidence", and the expected calibration error (ECE) of each model.
