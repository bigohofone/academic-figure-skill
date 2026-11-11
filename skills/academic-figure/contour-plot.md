# Contour plot

A function of two continuous variables: a loss landscape, a decision boundary, an objective over two hyperparameters, a density in 2-D. A 3D surface is drawn as a contour plot instead: in print, a surface hides its own far side and its heights can't be read. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Panel**: aspect 1 : 1, no gridlines (`ax.grid(False)`), both axes labelled with their variables.
- **Values**: when they span over 100×, contour their logarithm (DESIGN.md's log rule) and say "contours of log loss" in the caption.
- **Gradient with lines**: the values as a continuous gradient in the design's colormap (`viridis`, low values dark; signed values `RdBu_r` centered at 0, as in `heatmap.md`), exact at each data point and blended smoothly between them, `mesh = ax.pcolormesh(X, Y, Z, shading="gouraud")`; on it, the contour lines of the data itself, never of a smoothed copy, so each line marks exactly where the values cross its level, `lines = ax.contour(X, Y, Z, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])`. 6 to 8 levels at half width, 10 at full width, at round values inside the data's range: `levels = np.arange(lo, hi + step / 2, step)`.
- **Colorbar**: always, labelled with the quantity, `fig.colorbar(mesh, ax=ax, label="Validation loss")`.

## Variants

- **Contour lines only** (as many papers draw them): `lines = ax.contour(X, Y, Z, levels=levels, cmap=cmap)`, colored by level from the design's whole colormap, `cmap = plt.get_cmap("viridis")`, the same scale as everywhere else; a colorbar for the line colors, `fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(lo, hi), cmap=cmap), ax=ax, label=...)`.
- **Lines given as polylines** (each with its level, not a grid): each drawn with `ax.plot(x, y, color=cmap(norm(level)), linewidth=rcParams["contour.linewidth"])`.
- **Loss landscape**: axes named as the data names the two directions (α, β), else "Direction 1" and "Direction 2"; the trained solution at (0, 0).

## Labels

- **Level labels**: one label per level, black or white for the color at its level (black on a lines-only plot). Place them along the path from the minimum toward the farthest corner, where the lines are farthest apart: `positions` holds, for each level, the point on that path where Z crosses it.

  ```python
  labels = ax.clabel(lines, fmt="%.2g", manual=positions)
  for t in labels:
      t.set_color(text_color(mesh.cmap(mesh.norm(float(t.get_text())))))
  ```

  For polylines, write each level once, at the first of its given label positions that does not collide (Collisions step 1), on a white box since no gap is cut for it: `ax.text(x, y, f"{level:.2g}", ha="center", va="center", gid="contour-label", bbox=dict(facecolor="white", edgecolor="none", pad=1))`; a level with no free position goes unlabelled.
- **Points of interest**: a minimum or the trained solution as a filled star in `colors["ours"]` at the design's highlight size, `ax.plot(x, y, "*", color=colors["ours"], markerfacecolor=colors["ours"], markersize=paper.highlight_size, linestyle="none", label=...)`; a training trajectory as a data line with markers at its ends; named in a legend when there are two or more of them, else in the caption (DESIGN.md Legend).

## Caption

- **Reading guide**: "colors blend between the N × M runs" for a measured grid; what the star marks.
