# Heatmap

Values over two categorical axes: confusion matrix, attention map, grid over two swept hyperparameters, per-benchmark scores of many models. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Cells: square: `finalize_figure(..., aspect=n_rows / n_cols)`; no tick marks, no gridlines; categories as text tick labels on both axes.

  ```python
  im = ax.imshow(values, aspect="auto")
  ax.tick_params(length=0)
  ax.grid(False)
  ```

- Colormap:

  | Values | Colormap |
  |---|---|
  | Sequential (counts, accuracies, attention) | design's `heatmap.colormap`, `viridis` (pass nothing); `n` discrete levels: below |
  | Signed (differences, correlations) | `"RdBu_r"`, symmetric around 0 (negative blue, positive red): below |

  ```python
  cmap = plt.get_cmap("viridis", n)                       # n discrete levels
  im = ax.imshow(values, cmap="RdBu_r", vmin=-m, vmax=m)  # signed
  ```

- Colorbar: always; labelled with quantity ("Recall", "Attention weight"); placed per DESIGN.md Axes.

  ```python
  fig.colorbar(im, ax=ax, label=...)
  ```

- Axis labels: quantity when tick labels are values (learning rate, batch size); none when self-naming categories (methods, tokens).

## Variants

- Confusion matrix: normalized per row (each true class sums to 1) unless user asks for counts; `vmin=0, vmax=1`; axes always "Predicted label" (x), "True label" (y).
- Attention map: query tokens down y, key tokens along top, as text tick labels; no cell text.

  ```python
  ax.xaxis.tick_top()
  ```

- Hyperparameter grid: swept values increase rightward and upward (`origin="lower"`); cell text; best cell outlined.

  ```python
  ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"]))
  ```

## Labels

- Cell text: every cell when ≤ 12 × 12, in DESIGN.md value formats, text color per cell; larger: none.

  ```python
  ax.text(j, i, label, ha="center", va="center", color=text_color_on(im.cmap(im.norm(v))))
  ```

## Caption

- Normalization: per row, per column, or counts.
