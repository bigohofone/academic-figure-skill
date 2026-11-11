# Radar chart

A few models' profiles across 5 to 10 benchmarks or capabilities, when the shape of the profile is the message (where each model is strong or weak). Also called a spider chart. For exact comparisons, or more than four models, draw a grouped bar chart instead (`bar-chart.md`). Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Axes**: polar, one spoke per benchmark, evenly spaced from the top, clockwise: `fig, ax = plt.subplots(figsize=(width, width), subplot_kw={"projection": "polar"})`, `angles = np.linspace(0, 2 * np.pi, n, endpoint=False)`, `ax.set_theta_offset(np.pi / 2)`, `ax.set_theta_direction(-1)`. `finalize_figure` sizes the chart to the width and ignores `aspect`.
- **Scale**: one radial scale for all spokes when the benchmarks share a unit (accuracy in %), fixed from 0 to the outer ring, with 3 or 4 rings plus the outer edge. Benchmarks with different units: each spoke normalized to its best score (= 1), said in the caption.
- **Grid**: an n-sided polygon grid, never circles: the circular grid and frame off, each ring and spoke drawn in the design's grid look, the outer polygon as the panel box:

  ```python
  ax.grid(False)
  ax.spines["polar"].set_visible(False)
  loop = np.r_[angles, angles[:1]]
  for r in rings:  # e.g. [25, 50, 75, 100]
      ax.plot(loop, [r] * (n + 1), color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
  for a in angles:
      ax.plot([a, a], [0, rings[-1]], color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
  ax.plot(loop, [rings[-1]] * (n + 1), color=colors["ink"], linewidth=rcParams["axes.linewidth"])
  ax.set_ylim(0, rings[-1])
  ```

- **Models**: each a closed polygon, filled lightly so overlaps stay visible, `ax.plot(loop, np.r_[values, values[:1]], color=color, linestyle=style, linewidth=1 if style == "-" else paper.dashed_width, label=name)`, `ax.fill(angles, values, color=color, alpha=0.1)`; ours in `colors["ours"]`, drawn last so it is on top, the compared models in `neutral` told apart by line style (DESIGN.md Colors).
- **Spoke names**: `ax.set_xticks(angles, labels=names)`, off the outer polygon, `ax.tick_params(axis="x", pad=6)`.
- **Ring values**: between two spokes so they sit on no line, where a polygon ring is at r·cos(π/n), not r: `ax.set_yticks([r * np.cos(np.pi / n) for r in rings[:-1]], labels=[str(r) for r in rings[:-1]])`, `ax.set_rlabel_position(180 / n)`.

## Labels

- **Values**: only ours, at each spoke, in `darken(colors["ours"])`, outside its vertex. On a side spoke the label sits beside the vertex, outward and hanging toward the horizontal axis, away from the spoke name that continues the spoke; on the top and bottom spokes it sits just beyond the vertex; on a white box where it crosses a ring line (angles clockwise from the top):

  ```python
  side = np.sin(angle) if abs(np.sin(angle)) > 0.1 else 0
  up = np.cos(angle) if side == 0 else 0
  ax.annotate(f"{v:#.3g}", (angle, v), xytext=(4 * np.sign(side), 4 * np.sign(up)), textcoords="offset points",
              ha="left" if side > 0 else "right" if side < 0 else "center",
              va=("top" if np.cos(angle) > 0 else "bottom") if side else ("bottom" if up > 0 else "top"),
              color=darken(colors["ours"]), bbox=dict(facecolor="white", edgecolor="none", pad=1), gid="value-label")
  ```

  Placements (for Collisions): as above, then the spoke names pushed out, `ax.tick_params(axis="x", pad=8)`, then 10, 12, ….
- **Legend**: outside above the chart, ours first although it is drawn last, `fig.legend(handles, labels, loc="outside upper center", ncol=len(labels), frameon=False, borderaxespad=0)`.
