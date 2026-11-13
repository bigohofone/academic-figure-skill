# Box plot

Spread of many values per group, across groups: per-problem accuracies, per-sample perplexities, response lengths per model. No value labels. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Box: fill = series color lightened (grey series: `shift_lightness(make_shades(colors["neutral"], n)[i], 2)`); ours: full color (stays apart from pale greys in grayscale). Design draws black outline, whiskers, caps, median.
  ```python
  box = ax.boxplot(values, positions=[x], widths=0.7, patch_artist=True)
  box["boxes"][0].set_facecolor(shift_lightness(color, 2))
  ```
- Axis: groups are categories; tick marks hidden; horizontal gridlines only.
  ```python
  ax.grid(axis="x", visible=False)
  ```
- Points: ≤ 30 values per box: every value on top, jittered within box, design markers black on white, `showfliers=False`. More: only values beyond whiskers, design markers (matplotlib default fliers).
  ```python
  rng = np.random.default_rng(0)
  ax.plot(x + rng.uniform(-0.2, 0.2, len(values)), values, "o", color=colors["ink"],
          markerfacecolor="white", linestyle="none")
  ```

## Variants

- Horizontal (group names don't fit side by side, DESIGN.md Typography): groups top to bottom (`ax.invert_yaxis()`), vertical gridlines only, jitter along y.
  ```python
  ax.boxplot(values, positions=[y], widths=0.7, orientation="horizontal")
  ```
- Grouped (several series per category): boxes share 0.8 of category slot, like grouped bars; jitter within ±0.25 of box width; one legend entry per series.
  ```python
  width = 0.8 / n_series
  ax.boxplot(values, positions=[x + (i - (n_series - 1) / 2) * width], widths=0.8 * width, ...)  # box i
  Patch(facecolor=shift_lightness(color, 2), edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"], label=name)
  ```

## Caption

- Reading guide: "boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range"; what each point is (every value, or values beyond whiskers).
