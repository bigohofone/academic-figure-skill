# Heatmap

Values over two categorical axes: confusion matrix, attention map, a grid of results over two swept hyperparameters, per-benchmark scores of many models. Read with `DESIGN.md`, whose rules all still apply.

- `im = ax.imshow(values, aspect="auto")`, panel aspect 1 : 1 (or the matrix's shape when it is far from square), tick marks hidden (`ax.tick_params(length=0)`), no gridlines (`ax.grid(False)`), categories as text tick labels on both axes.
- **Cell text**, when the matrix is small enough to read (up to ~12 × 12) and the values matter: every cell's value, 7 pt, in `text_color(im.cmap(im.norm(v)))`, with the precision the values have. Always a colorbar, cell text or not, so the reader can read the scale: `fig.colorbar(im, ax=ax)`, labelled with the quantity ("Recall", "Accuracy", "Attention weight").
- **Axis labels**: name the quantity when the tick labels are values (learning rate, batch size); omit them when the tick labels are categories that name themselves (method names, tokens), except a confusion matrix, whose axes are always "Predicted label" (x) and "True label" (y).
- **Confusion matrix**: normalized per row (each true class sums to 1, so the diagonal is per-class recall) unless the user asks for counts; the color scale fixed to `vmin=0, vmax=1`; say in the caption how it is normalized.
- **Attention map**: tokens as tick labels, the query tokens down the y axis and the key tokens along the top (`ax.xaxis.tick_top()`), turned 90° when they don't fit side by side; no cell text; a colorbar below the panel (`location="bottom"`) so the tokens keep the width.
- **Hyperparameter grid**: the swept values in order on each axis, cell text with the metric, and the best cell outlined: `ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor="black", linewidth=1))`.

| Values | Colormap |
|---|---|
| Sequential (counts, accuracies, attention) | the design's `heatmap.colormap`, `viridis` (the default; pass nothing); few levels: `cmap=plt.get_cmap("viridis", n_levels)` |
| Sequential, lower is better (loss, error, perplexity) | reversed, `cmap="viridis_r"`, so the best values are bright; few levels: `cmap=plt.get_cmap("viridis_r", n_levels)` |
| Signed (differences, correlations) | `cmap="RdBu_r"` centered at 0 (symmetric `vmin`/`vmax`: negative blue, positive red); few levels: `cmap=plt.get_cmap("RdBu_r", n_levels)` |
