# Heatmap: values over two categorical axes

Heatmaps, confusion matrices, attention maps, grids of results over two swept settings. Read with `SKILL.md`, whose rules all still apply.

- `ax.imshow(..., aspect="auto")`, panel aspect 1 : 1, tick marks hidden, no gridlines (`ax.grid(False)`), a colorbar for continuous values; cell text 7 pt in `"white" if np.dot(im.cmap(im.norm(v))[:3], [0.299, 0.587, 0.114]) < 0.5 else "black"`.
- Category axes carry no axis labels when the tick labels name them.

| Values | Colormap |
|---|---|
| Sequential | `cmap="tol.iridescent"`; few levels: `tol.YlOrBr_discrete` |
| Signed | `cmap="tol.sunset"` centered at 0 (symmetric `vmin`/`vmax`); few levels: `tol.sunset_discrete` |
