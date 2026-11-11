# Violin plot

As box plot (`box-plot.md`), when spread shape matters: several modes, long tail, cluster at a bound. ≤ 30 values per group: shape unreliable; box plot with every point instead. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Body: series color lightened, full opacity (grey series: `lighten(baseline_greys(n)[i])`; ours: full color, stays apart from pale greys in grayscale); black edge.
  ```python
  parts = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)
  body = parts["bodies"][0]
  body.set_facecolor(lighten(color))
  body.set_edgecolor(colors["ink"])
  body.set_linewidth(rcParams["patch.linewidth"])
  body.set_alpha(1)
  ```
- Box inside (as seaborn `inner="box"`): whiskers thin black line to furthest values within 1.5 × IQR; IQR thick black bar; median white dot.
  ```python
  q1, median, q3 = np.percentile(values, [25, 50, 75])
  low = min(v for v in values if v >= q1 - 1.5 * (q3 - q1))
  high = max(v for v in values if v <= q3 + 1.5 * (q3 - q1))
  ax.vlines(x, low, high, color=colors["ink"], linewidth=rcParams["patch.linewidth"])
  ax.vlines(x, q1, q3, color=colors["ink"], linewidth=4 * rcParams["patch.linewidth"])
  ax.plot(x, median, "o", color=colors["ink"], markerfacecolor="white", zorder=3)
  ```
- Axis: groups are categories; tick marks hidden; horizontal gridlines only.

## Variants

- Grouped violins: placement and legend as grouped box plots (`box-plot.md`).

## Caption

- Reading guide: "violins show the kernel density of the values; inside, the bar spans the quartiles, the thin line reaches 1.5× the interquartile range, and the white dot marks the median".
