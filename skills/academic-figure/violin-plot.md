# Violin plot

As a box plot (`box-plot.md`), when the shape of the spread matters: several modes, a long tail, a cluster at a bound. With few values per group (under ~20) the estimated shape is unreliable; draw a box plot with every point instead. Read with `DESIGN.md`, whose rules all still apply.

- `parts = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)`; fill the body with its series color lightened, at full opacity, with a black 0.75 pt edge (`body = parts["bodies"][0]`, `body.set_facecolor(lighten(color))`, `body.set_edgecolor("black")`, `body.set_linewidth(0.75)`, `body.set_alpha(1)`), and draw a box plot inside it, as seaborn's `inner="box"`, so the quartiles stay readable next to the shape: the whiskers as a thin black line to the furthest values within 1.5 × IQR, the interquartile range as a thick black bar, the median as a white dot on it:

  ```python
  q1, median, q3 = np.percentile(values, [25, 50, 75])
  low = min(v for v in values if v >= q1 - 1.5 * (q3 - q1))
  high = max(v for v in values if v <= q3 + 1.5 * (q3 - q1))
  ax.vlines(x, low, high, color=colors["ink"], linewidth=rcParams["patch.linewidth"])
  ax.vlines(x, q1, q3, color=colors["ink"], linewidth=4 * rcParams["patch.linewidth"])
  ax.plot(x, median, "o", color=colors["ink"], markerfacecolor="white", zorder=3)
  ```
- Groups on the x-axis are categories: hide their tick marks, horizontal gridlines only.
- Grouped violins and legend entries as grouped box plots in `box-plot.md`.
- Caption: "violins show the kernel density of the values; inside, the bar spans the quartiles, the thin line reaches 1.5× the interquartile range, and the white dot marks the median".
