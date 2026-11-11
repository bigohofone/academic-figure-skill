# Contour plot

A function of two continuous variables: a loss landscape, a decision boundary, an objective over two hyperparameters, a density in 2-D. Read with `DESIGN.md`, whose rules all still apply. A 3D surface plot is drawn as a contour plot instead: in print, a surface hides its own far side and its heights can't be read.

- Filled contours with lines on them: `cs = ax.contourf(X, Y, Z, levels=10)` in the design's colormap (`Blues`; signed values: `RdBu_r` centered at 0, as in `heatmap.md`), then `ax.contour(X, Y, Z, levels=cs.levels, colors="black", linewidths=0.5, alpha=0.5)`; a colorbar labelled with the quantity, `fig.colorbar(cs, ax=ax)`. Contour labels on the lines only when there is no colorbar: `ax.clabel(lines, fontsize=7, fmt="%.2g")`, then `fontweight` bold on each returned label.
- Panel aspect 1 : 1, no gridlines (`ax.grid(False)`), both axes labelled with their variables. A loss landscape's axes are the two directions in weight space, "Direction 1" and "Direction 2", with the trained solution at (0, 0).
- Points of interest on top: a minimum or the trained solution as the design's marker in `colors["ours"]`, a training trajectory as a data line in the series color with markers at its ends; named in a legend.
- A loss with a large range: contour its logarithm and say so in the colorbar label ("log loss").
