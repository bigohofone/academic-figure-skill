# Radar chart

A few models' profiles across 5–10 benchmarks or capabilities, when the shape of the profile is the message (where each model is strong or weak). Also called a spider chart. For exact comparisons, or more than four models, draw a grouped bar chart instead (`bar-chart.md`). Read with `DESIGN.md`, whose rules all still apply.

- Polar axes: `fig, ax = plt.subplots(figsize=(width, width), subplot_kw={"projection": "polar"})`; one spoke per benchmark, evenly spaced from the top, clockwise: `angles = np.linspace(0, 2 * np.pi, n, endpoint=False)`, `ax.set_theta_offset(np.pi / 2)`, `ax.set_theta_direction(-1)`.
- Each model is a closed polygon, `ax.plot(np.r_[angles, angles[:1]], np.r_[values, values[:1]], color=color, label=name)`, filled lightly so overlaps stay visible, `ax.fill(angles, values, color=color, alpha=0.1)`; colors as in DESIGN.md: the proposed model in `colors["ours"]`, drawn last so it is on top, and the models it is compared against in `colors["neutral"]`, told apart by line style.
- One radial scale for all spokes when the benchmarks share a unit (accuracy in %): from 0, or from a stated floor when every value is far above 0, with 3–4 rings plus the outer edge. Benchmarks with different units: normalize each spoke to its best score (= 1) and say so in the caption.
- An n-sided polygon grid, never circles: turn off the circular grid and frame (`ax.grid(False)`, `ax.spines["polar"].set_visible(False)`), then draw each ring as a polygon through the spokes and the spokes themselves in the design's grid look, and the outer polygon as the panel box in `ink`, 0.5 pt:

  ```python
  loop = np.r_[angles, angles[:1]]
  for r in rings:  # 3–4 rings and the outer edge, e.g. [25, 50, 75, 100]
      ax.plot(loop, [r] * (n + 1), color=colors["ink"], alpha=0.1, linewidth=0.5)
  for a in angles:
      ax.plot([a, a], [0, rings[-1]], color=colors["ink"], alpha=0.1, linewidth=0.5)
  ax.plot(loop, [rings[-1]] * (n + 1), color=colors["ink"], linewidth=0.5)
  ax.set_ylim(0, rings[-1])
  ```
- Benchmark names as the spoke labels, `ax.set_xticks(angles, labels=names)`, pushed off the outer polygon, `ax.tick_params(axis="x", pad=6)`. Ring values labelled between two spokes so they sit on no line, where a polygon ring is at r·cos(π/n), not r: `ax.set_yticks([r * np.cos(np.pi / n) for r in rings[:-1]], labels=[str(r) for r in rings[:-1]])`, `ax.set_rlabel_position(180 / n)`.
- Value labels: only for the proposed model, its value at each spoke in 7 pt `darken(colors["ours"])`, just outside its vertex.
- Legend: outside above the chart, `fig.legend(loc="outside upper center", ncol=<models>, frameon=False)`.
- `fit_height` sizes the chart to the width; the `aspect` argument is ignored.
