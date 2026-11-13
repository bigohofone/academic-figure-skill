# Heatmap

Values over two categorical axes: confusion matrix, attention map, grid over two swept hyperparameters, per-benchmark scores of many models. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Cells: square, always: `finalize_figure` sets the panel's shape from the grid's rows and columns (no `height` needed); no tick marks, no gridlines; categories as text tick labels on both axes.

  ```python
  im = ax.imshow(values, aspect="auto")
  ax.tick_params(length=0)
  ax.grid(False)
  ```

- Colormap:

  | Values | Colormap |
  |---|---|
  | Sequential (counts, accuracies, attention) | design's `"paper"`, low light, high dark (pass nothing); `n` discrete levels: below |
  | Signed (differences, correlations) | `"paper-diverging"`, symmetric around 0 (negative orange, positive blue, as Tableau's Orange-Blue): below |

  ```python
  cmap = plt.get_cmap("paper", n)                                  # n discrete levels
  im = ax.imshow(values, cmap="paper-diverging", vmin=-m, vmax=m)  # signed
  ```

- Colorbar: labelled with quantity ("Recall", "Attention weight"); placed per DESIGN.md Axes. None when every cell's value is written (Labels): the values carry the numbers, the colors only the pattern; the caption names the quantity.

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

- Hyperparameter grid: swept values increase rightward and upward (`origin="lower"`); cell text.
- No mark on single cells (no outline, star or box on the best or worst cell): the cell values show them, the caption names them.

## Labels

- Cell text: every cell when ≤ 12 × 12, in DESIGN.md value formats, text color per cell; larger: none. `finalize_figure` sets all of them to one size that fits every cell, down to 4 pt; still crowded: drop them (DESIGN.md Collisions step 4).
- Row and column names: every one written (no every-m-th labelling); `finalize_figure` sets them to one size that fits the cells, down to 4 pt.

  ```python
  fill = im.cmap(im.norm(v))
  ax.text(j, i, label, ha="center", va="center",
          color=colors["paper"] if np.dot(fill[:3], [0.299, 0.587, 0.114]) < 0.5 else colors["ink"])
  ```

## Caption

- Normalization: per row, per column, or counts.
