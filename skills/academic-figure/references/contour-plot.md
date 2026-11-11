# Contour plot

Function of two continuous variables: loss landscape, decision boundary, objective over two hyperparameters, 2-D density. 3D surface: draw as contour plot instead (in print a surface hides its far side; heights unreadable). Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Panel: aspect 1 : 1; no gridlines (`ax.grid(False)`); both axes labelled with their variables.
- Values spanning > 100×: contour their log (DESIGN.md log rule); caption says "contours of log loss".
- Bands with lines: filled bands between levels in design colormap (`viridis`, low = dark; signed: `"RdBu_r"` centered at 0, as in `heatmap.md`); one flat color per band, never smooth gradient. On top: ink contour lines of the data itself, never of a smoothed copy. Levels: 6–8 at half width, 10 at full width, round values inside data range.

  ```python
  levels = np.arange(lo, hi + step / 2, step)
  mesh = ax.contourf(X, Y, Z, levels=np.r_[Z.min(), levels, Z.max()])
  lines = ax.contour(X, Y, Z, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])
  ```

- Colorbar: always; labelled with quantity; ticks at levels only (not data ends).

  ```python
  fig.colorbar(mesh, ax=ax, label="Validation loss", ticks=levels)
  ```

## Variants

- Lines only: each line colored by level from whole `viridis` colormap; colorbar for line colors.

  ```python
  cmap = plt.get_cmap("viridis")
  lines = ax.contour(X, Y, Z, levels=levels, cmap=cmap)
  fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(lo, hi), cmap=cmap), ax=ax, label=...)
  ```

- Lines given as polylines (each with its level, no grid): each a line in its level's color.

  ```python
  ax.plot(x, y, color=cmap(norm(level)), linewidth=rcParams["contour.linewidth"])
  ```

- Loss landscape: axes named as data names the two directions (α, β), else "Direction 1", "Direction 2"; trained solution at (0, 0).

## Labels

- Level labels: one per level; black or white for color at its level (black on lines-only plot). Placed along path from minimum toward farthest corner (lines farthest apart): `positions` = per level, point on that path where Z crosses it.

  ```python
  labels = ax.clabel(lines, fmt="%.2g", manual=positions, fontsize=paper.contour_label_size)  # inline, turned along each line
  for t in labels:
      t.set_color(text_color_on(mesh.cmap(mesh.norm(float(t.get_text())))))
  ```

  - Polylines: each level once, at its first given label position, turned along line like `clabel`'s, on white box (no gap cut).
  - `finalize_figure` reports collision: move to level's next given position, render again (Collisions step 1).
  - Angle: line direction in data coordinates at vertex `k` nearest position, kept upright; `transform_rotates_text=True` adapts it to panel's final shape.
  - No free position for a level: label every 2nd level, then every 3rd, … (Collisions step 4), keeping labelled levels evenly spaced.

  ```python
  angle = (np.degrees(np.arctan2(ys[k + 1] - ys[k - 1], xs[k + 1] - xs[k - 1])) + 90) % 180 - 90
  ax.text(x, y, f"{level:.2g}", ha="center", va="center", rotation=angle, rotation_mode="anchor",
          transform_rotates_text=True, fontsize=paper.contour_label_size, gid="contour-label",
          bbox=dict(facecolor="white", edgecolor="none", pad=1))
  ```

- Points of interest: minimum or trained solution: filled star in `colors["ours"]`, highlight size; training trajectory: data line, markers at ends. ≥ 2: named in legend; else in caption (DESIGN.md Legend).

  ```python
  ax.plot(x, y, "*", color=colors["ours"], markerfacecolor=colors["ours"], markersize=paper.highlight_size, linestyle="none", label=...)
  ```

## Caption

- Reading guide: "each band spans one level step" for filled bands; what the star marks.
