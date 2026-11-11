# Histogram

How one quantity's values are spread: scores, confidences, lengths, per-problem accuracies. The shape is the message, so no value labels. Read with `DESIGN.md`, whose rules all still apply.

- **Histogram**: raw values as touching bars, `ax.hist(values, bins=bins, color=color, linewidth=0)`, with bins from all series together so every series shares them: `bins = np.histogram_bin_edges(np.concatenate(all_values), bins="auto")`. Horizontal gridlines only. y label "Count", or "Density" with `density=True` when the series have different sizes.
- **Overlaid histograms** (two or three series on one axis): outlines, `ax.hist(values, bins=bins, histtype="step", linewidth=1, color=color, label=name)`, so every series stays visible. More than three series: one panel each, sharing both axes.
- **Counts per bin** already computed (accuracy intervals, length buckets): grouped bars as in `bar-chart.md`, the bins in order on the x-axis with text tick labels, never horizontal bars; bar labels only when the takeaway compares specific bins.
- **Density plot** (a smooth curve, KDE), only when the user asks: `scipy.stats.gaussian_kde(values)(xs)` drawn as a 1 pt line in the series color, filled under with `alpha=0.2`; say in the caption it is a kernel density estimate.
