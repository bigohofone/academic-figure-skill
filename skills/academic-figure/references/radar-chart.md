# Radar chart

A few models' profiles across 5–10 benchmarks or capabilities, when profile shape is the message (where each model is strong or weak). Also: spider chart. Exact comparisons or > 4 models: grouped bar chart (`bar-chart.md`). Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Axes: polar; one spoke per benchmark, evenly spaced, clockwise from top. `finalize_figure` sizes chart to width, ignores `height`.

  ```python
  fig, ax = plt.subplots(figsize=(width, width), subplot_kw={"projection": "polar"})
  angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
  ax.set_theta_offset(np.pi / 2)
  ax.set_theta_direction(-1)
  ```

- Scale: shared unit (accuracy in %): one radial scale, 0 to outer ring, 3–4 rings plus outer edge. Different units: each spoke normalized to its best score (= 1); say so in caption.
- Grid: n-sided polygons, never circles. Circular grid and frame off; rings and spokes in design grid look; outer polygon = panel box.

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

- Models: closed, lightly filled polygons. Ours: `colors["ours"]`, drawn last (on top). Compared: `neutral`, distinguished by line style (DESIGN.md Colors).

  ```python
  ax.plot(loop, np.r_[values, values[:1]], color=color, linestyle=style,
          linewidth=1 if style == "-" else paper.dashed_linewidth, label=name)
  ax.fill(angles, values, color=color, alpha=0.1)
  ```

- Spoke names: off outer polygon.

  ```python
  ax.set_xticks(angles, labels=names)
  ax.tick_params(axis="x", pad=6)
  ```

- Ring values: between two spokes (on no line); polygon ring at r·cos(π/n), not r.

  ```python
  ax.set_yticks([r * np.cos(np.pi / n) for r in rings[:-1]], labels=[str(r) for r in rings[:-1]])
  ax.set_rlabel_position(180 / n)
  ```

## Labels

- Values: ours only, at each spoke, in `shift_lightness(colors["ours"], -1)`, outside vertex (angles clockwise from top):
  - Side spokes: beside vertex, outward, hanging toward horizontal axis, away from spoke name.
  - Top and bottom spokes: just beyond vertex.
  - Crossing a ring line: white box.

  ```python
  side = np.sin(angle) if abs(np.sin(angle)) > 0.1 else 0
  up = np.cos(angle) if side == 0 else 0
  ax.annotate(f"{v:#.3g}", (angle, v), xytext=(4 * np.sign(side), 4 * np.sign(up)), textcoords="offset points",
              ha="left" if side > 0 else "right" if side < 0 else "center",
              va=("top" if np.cos(angle) > 0 else "bottom") if side else ("bottom" if up > 0 else "top"),
              color=shift_lightness(colors["ours"], -1), bbox=dict(facecolor=colors["paper"], edgecolor="none", pad=1), gid="value-label")
  ```

  Placements (for Collisions): as above; then spoke names pushed out (`pad=8`, then 10, 12, …).
- Legend: outside, above chart; ours first though drawn last.

  ```python
  fig.legend(handles, labels, loc="outside upper center", ncol=len(labels), borderaxespad=0)
  ```
