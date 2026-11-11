# Box plot

The spread of many values per group, compared across groups: per-problem accuracies, per-sample perplexities, response lengths per model. The shape is the message, so no value labels. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Box**: `box = ax.boxplot(values, positions=[x], widths=0.7)`, filled with its series color lightened so the black median and the points on it stay readable, `box["boxes"][0].set_facecolor(lighten(color))`; the design draws the black outline, whiskers, caps and median.
- **Axis**: groups are categories: tick marks hidden, horizontal gridlines only, `ax.grid(axis="x", visible=False)`.
- **Points**: with 30 or fewer values per box, every value on top, jittered within the box as the design's markers in black on white, `ax.plot(x + rng.uniform(-0.2, 0.2, len(values)), values, "o", color=colors["ink"], markerfacecolor="white", linestyle="none")` with `rng = np.random.default_rng(0)`, and `showfliers=False`, since the points already show the values beyond the whiskers. With more values, only the values beyond the whiskers, as the design's markers (matplotlib's default fliers).

## Variants

- **Horizontal box plot** (group names that don't fit side by side, DESIGN.md Typography): `ax.boxplot(values, positions=[y], widths=0.7, orientation="horizontal")`, groups top to bottom (`ax.invert_yaxis()`), vertical gridlines only, jitter along y.
- **Grouped box plot** (several series per category): the boxes of one category share 0.8 of its slot like grouped bars, `width = 0.8 / n_series`, box `i` with `widths=0.8 * width` at `x + (i - (n_series - 1) / 2) * width`, jitter within ±0.25 of the box width; one legend entry per series, `Patch(facecolor=lighten(color), edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"], label=name)`.

## Caption

- **Reading guide**: "boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range", and what each point is (every value, or values beyond the whiskers).
