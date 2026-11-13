# Histogram

Spread of one quantity: scores, confidences, lengths, per-problem accuracies. Shape is the message: raw-value bars carry no value labels (named bins with counts: labelled as bars, below). Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Bars: raw values as touching bars; all series share bins computed from all values together; horizontal gridlines only.

  ```python
  bins = np.histogram_bin_edges(np.concatenate(all_values), bins="auto")
  ax.hist(values, bins=bins, color=color, linewidth=0)
  ```

- y axis: "Count"; "Density" (`density=True`) when series differ in size.

## Variants

- Overlaid (2–3 series, one axis): each a translucent fill with outline on top; outline carries legend entry. > 3 series: one panel each, sharing both axes.

  ```python
  ax.hist(values, bins=bins, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)
  ax.hist(values, bins=bins, histtype="step", color=color, label=name)
  ```

- Precomputed counts per bin: continuous-quantity bins as touching bars on numeric axis (below). Named bins (intervals, length buckets): grouped bars (`bar-chart.md`), in order on x, text tick labels, labelled as in bar-chart.md: every bar or none.

  ```python
  ax.bar(edges[:-1], counts, width=np.diff(edges), align="edge", linewidth=0)
  ```

- Density curve (KDE): only on request; data line in series color, filled under at `alpha=0.2`.

  ```python
  density = scipy.stats.gaussian_kde(values)(xs)
  ```

## Labels

- Means (when takeaway compares series' centers): thin solid vertical reference line in `shift_lightness(color, -1)`; value just above panel at the line.

  ```python
  ax.axvline(mean, linewidth=rcParams["grid.linewidth"], color=shift_lightness(color, -1))
  ax.annotate(f"{mean:#.3g}", (mean, 1), xycoords=("data", "axes fraction"), xytext=(0, 2), textcoords="offset points",
              ha="center", va="bottom", color=shift_lightness(color, -1))
  ```

## Caption

- Reading guide: "vertical lines mark the means"; "a kernel density estimate" for density curve; "density" when series normalized.
