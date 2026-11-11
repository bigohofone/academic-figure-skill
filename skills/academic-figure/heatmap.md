# Heatmap

Values over two categorical axes: confusion matrix, attention map, a grid of results over two swept hyperparameters, per-benchmark scores of many models. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Cells**: `im = ax.imshow(values, aspect="auto")`, panel aspect = rows / columns of the matrix (square cells), tick marks hidden (`ax.tick_params(length=0)`), no gridlines (`ax.grid(False)`), categories as text tick labels on both axes.
- **Colormap**:

  | Values | Colormap |
  |---|---|
  | Sequential (counts, accuracies, attention) | the design's `heatmap.colormap`, `viridis` (pass nothing); `n` discrete levels: `cmap=plt.get_cmap("viridis", n)` |
  | Signed (differences, correlations) | `cmap="RdBu_r"` with symmetric `vmin=-m, vmax=m` (negative blue, positive red) |

- **Colorbar**: always, labelled with the quantity ("Recall", "Attention weight"), as DESIGN.md Axes places it, `fig.colorbar(im, ax=ax, label=...)`.
- **Axis labels**: the quantity when the tick labels are values (learning rate, batch size); none when they are categories that name themselves (methods, tokens).

## Variants

- **Confusion matrix**: normalized per row (each true class sums to 1, so the diagonal is per-class recall) unless the user asks for counts; scale fixed to `vmin=0, vmax=1`; axes always "Predicted label" (x) and "True label" (y).
- **Attention map**: query tokens down the y axis, key tokens along the top (`ax.xaxis.tick_top()`), as text tick labels; no cell text.
- **Hyperparameter grid**: the swept values in order on each axis, cell text, and the best cell outlined, `ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"]))`.

## Labels

- **Cell text**: with at most 12 rows and 12 columns, every cell's value, written by DESIGN.md's value table, in `text_color(im.cmap(im.norm(v)))`, `ax.text(j, i, label, ha="center", va="center", color=...)`. Larger matrices carry none.

## Caption

- **Normalization**: how the values are normalized (per row, per column, counts).
