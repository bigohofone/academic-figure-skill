# Contour plot

A function of two continuous variables: a loss landscape, a decision boundary, an objective over two hyperparameters, a density in 2-D. A 3D surface is drawn as a contour plot instead: in print, a surface hides its own far side and its heights can't be read. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Panel**: aspect 1 : 1, no gridlines (`ax.grid(False)`), both axes labelled with their variables.
- **Values**: when they span over 100×, contour their logarithm (DESIGN.md's log rule) and say "contours of log loss" in the caption.
- **Filled contours with lines**: `cs = ax.contourf(X, Y, Z, levels=levels)` in the design's colormap (`viridis`, low values dark; signed values `RdBu_r` centered at 0, as in `heatmap.md`), then `lines = ax.contour(X, Y, Z, levels=cs.levels, colors=colors["ink"], alpha=0.1)` at the design's `contour` width (pass no `linewidths`): as faint as the grid, so the fill carries the values. 6 to 8 levels at half width, 10 at full width: `levels = np.linspace(lo, hi, 7)` over round `lo`, `hi`.
- **Colorbar**: always, labelled with the quantity, `fig.colorbar(cs, ax=ax, label="Validation loss")`.
- **Measured grid** (a sweep of runs, fewer than 50 values per side): contour a smoothing spline of it, so the lines follow the surface, not the grid's straight segments or the run-to-run noise: `fine = RectBivariateSpline(y, x, Z, s=Z.size * noise ** 2)(y_fine, x_fine)` (`from scipy.interpolate import RectBivariateSpline`), on 200 points per axis (`np.linspace` of the data coordinates; `np.log10` of a log axis, then back with `10 **`), where `noise` is the run-to-run spread: the std over seeds when the data has it, else `0.02 * np.ptp(Z)`.

## Variants

- **Contour lines only** (as many papers draw them): `lines = ax.contour(X, Y, Z, levels=levels, cmap=cmap)`, colored by level from the design's colormap without its lightest end, so no line vanishes on white, `cmap = ListedColormap(plt.get_cmap("viridis")(np.linspace(0, 0.85, 256)))`; a colorbar for the line colors, `fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(lo, hi), cmap=cmap), ax=ax, label=...)`.
- **Lines given as polylines** (each with its level, not a grid): each drawn with `ax.plot(x, y, color=cmap(norm(level)), linewidth=rcParams["contour.linewidth"])`.
- **Loss landscape**: axes "Direction 1" and "Direction 2", the trained solution at (0, 0).

## Labels

- **Level labels**: one label per level, black or white for the fill at its level, at full opacity (labels inherit the lines' alpha). Place them along the path from the minimum toward the farthest corner, where the lines are farthest apart: `positions` holds, for each level, the point on that path where Z crosses it.

  ```python
  labels = ax.clabel(lines, fmt="%.2g", manual=positions)
  for t in labels:
      t.set_alpha(1)
      t.set_color(text_color(cs.cmap(cs.norm(float(t.get_text())))))
  ```

  For polylines, write each level at its given label position, `ax.text(x, y, f"{level:.2g}", ha="center", va="center", gid="contour-label")`; when `fit_height` reports two of them overlapping, drop the later one.
- **Points of interest**: a minimum or the trained solution as a filled star in `colors["ours"]` at the design's highlight size, `ax.plot(x, y, "*", color=colors["ours"], markerfacecolor=colors["ours"], markersize=paper.highlight_size, linestyle="none", label=...)`, at a measured run; a training trajectory as a data line with markers at its ends; named in a legend (outside, DESIGN.md Legend).

## Caption

- **Reading guide**: "smoothed from the N × M runs" for a measured grid; what the star marks.
