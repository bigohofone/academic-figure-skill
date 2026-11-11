# Histogram

How one quantity's values are spread: scores, confidences, lengths, per-problem accuracies. The shape is the message, so the bars carry no value labels. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Bars**: raw values as touching bars, `ax.hist(values, bins=bins, color=color, linewidth=0)`, with bins from all series together so every series shares them, `bins = np.histogram_bin_edges(np.concatenate(all_values), bins="auto")`; horizontal gridlines only.
- **y axis**: "Count", or "Density" with `density=True` when the series have different sizes.

## Variants

- **Overlaid histograms** (two or three series on one axis): each as a translucent fill with its outline on top, so every series stays visible where they overlap, `ax.hist(values, bins=bins, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)`, then `ax.hist(values, bins=bins, histtype="step", color=color, label=name)` (the outline carries the legend entry). More than three series: one panel each, sharing both axes.
- **Counts per bin** (already computed): bins of a continuous quantity as touching bars on a numeric axis, `ax.bar(edges[:-1], counts, width=np.diff(edges), align="edge", linewidth=0)`; named bins (intervals, length buckets) as grouped bars (`bar-chart.md`), in order on x with text tick labels, labelled as bar-chart.md labels bars: every bar or none.
- **Density curve** (KDE), only when the user asks: `scipy.stats.gaussian_kde(values)(xs)` as a data line in the series color, filled under at `alpha=0.2`.

## Labels

- **Means** (when the takeaway compares the series' centers): each mean as a dashed vertical line in `darken(color)`, `ax.axvline(mean, linestyle="--", linewidth=paper.dashed_width, color=darken(color))`, its value just above the panel at the line, `ax.annotate(f"{mean:#.3g}", (mean, 1), xycoords=("data", "axes fraction"), xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", color=darken(color))`.

## Caption

- **Reading guide**: "dashed lines mark the means"; "a kernel density estimate" for a density curve; "density" when the series are normalized.
