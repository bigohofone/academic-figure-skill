# Radar chart

A few models' profiles across 5–10 benchmarks or capabilities, when the shape of the profile is the message (where each model is strong or weak). Also called a spider chart. For exact comparisons, or more than four models, draw a grouped bar chart instead (`bar-chart.md`). Read with `DESIGN.md`, whose rules all still apply.

- Polar axes: `fig, ax = plt.subplots(figsize=(width, width), subplot_kw={"projection": "polar"})`; one spoke per benchmark, evenly spaced from the top, clockwise: `angles = np.linspace(0, 2 * np.pi, n, endpoint=False)`, `ax.set_theta_offset(np.pi / 2)`, `ax.set_theta_direction(-1)`.
- Each model is a closed polygon, `ax.plot(np.r_[angles, angles[:1]], np.r_[values, values[:1]], color=color, label=name)`, filled lightly so overlaps stay visible, `ax.fill(angles, values, color=color, alpha=0.1)`; colors as in DESIGN.md: the proposed model in `colors["ours"]`, drawn last so it is on top, and the models it is compared against in `colors["neutral"]`, told apart by line style.
- One radial scale for all spokes when the benchmarks share a unit (accuracy in %): from 0, or from a stated floor when every value is far above 0, with 3–4 rings labelled 7 pt along one spoke (`ax.set_rlabel_position(0)`, `ax.set_yticks([20, 40, 60, 80])`). Benchmarks with different units: normalize each spoke to its best score (= 1) and say so in the caption.
- Benchmark names as the spoke labels, `ax.set_xticks(angles, labels=names)`, pushed off the circle so they don't sit on it, `ax.tick_params(axis="x", pad=6)`. Gridlines: the design's grid for rings and spokes; the outer circle is the panel box (`ax.spines["polar"]`).
- Value labels: only for the proposed model, its value at each spoke in 7 pt bold `darken(colors["ours"])`, just outside its vertex.
- Legend: outside above the chart, `fig.legend(loc="outside upper center", ncol=<models>, frameon=False)`.
- `fit_height` sizes the circle to the width; the `aspect` argument is ignored.
