# Scatter plot

Two quantities per item against each other: accuracy vs parameters, FLOPs or latency (model comparison, often with Pareto front); one point per sample (correlation); 2-D embedding (t-SNE, UMAP). Panel: square for embeddings and one quantity against itself, else DESIGN.md Panel height. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Many points (samples, examples): design marker size, translucent; gridlines both directions.
  ```python
  ax.scatter(x, y, s=rcParams["lines.markersize"] ** 2, color=color, edgecolors="none", alpha=0.5)
  ```
- Points that carry a value in their color (a colorbar reads them: compute, step, temperature): markers at `paper.highlight_markersize`, every point. The design size marks a point on a line; a color scale needs area to be read.
- Few labelled points (models, accuracy vs cost): one marker per model. Proposed model present: ours `colors["ours"]`, all others `colors["neutral"]`. Absent: `series-1`, or one color per model family when families are the message.
  ```python
  ax.plot(x, y, "o", color=color)
  ```
- Cost axes (parameters, FLOPs, latency): log when span > 10× (not DESIGN.md's 100×; on linear axis a family's small members bunch left, names don't fit). Labels as in `line-chart.md`.

## Variants

- Trend line (takeaway is correlation): data line in `shift_lightness(color, -1)` over points; Pearson r with n in caption (Spearman ρ for ranks or ordinal ratings).
- Model family (sizes of one model, B0–B7): points joined in size order, solid data line, family color. Members are one kind: name every one by short tag (`B0` … `B7`); full names in legend or caption.
  ```python
  ax.plot(x, y, "o-", color=colors["ours"])  # our family
  ```
- Pareto front: front models joined in x order, dashed `neutral` line under markers; second front dotted (`":"`). Dominated models: markers only.
  ```python
  ax.plot(x, y, linestyle="--", linewidth=paper.dashed_linewidth, color=colors["neutral"], zorder=1)
  ```
- Embedding (t-SNE, UMAP): marker with black edge, translucent fill in class color; > 9 classes: also own marker shape (DESIGN.md Colors). One color per class (DESIGN.md Colors), legend. No ticks, tick labels, gridlines or axis labels.
  ```python
  ax.plot(x, y, shape, markeredgecolor=colors["ink"], markeredgewidth=paper.filled_markeredgewidth,
          markerfacecolor=(*to_rgb(color), 0.5), linestyle="none", label=name)
  ax.set_xticks([])
  ax.set_yticks([])
  ax.grid(False)
  ```

## Labels

- Point names: beside each labelled point, `shift_lightness(color, -1)`. Placements (for Collisions): upper right, upper left (`xytext=(-3, 3), ha="right"`), lower right, lower left (`va="top"`). `finalize_figure` grows limits up to a quarter to keep names inside; reports any beyond.
  ```python
  ax.annotate(name, (x, y), xytext=(3, 3), textcoords="offset points", color=shift_lightness(color, -1))
  ```
- Values: takeaway compares some labelled models: value joins name.
  ```python
  f"{name} ({v:#.3g}%)"
  ```

## Caption

- Correlation: coefficient and n.
- Fronts, families: what each line style joins ("the dashed line joins the NAS models on the Pareto front").
