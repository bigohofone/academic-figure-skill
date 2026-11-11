# Scatter plot

Two quantities per item plotted against each other: accuracy against parameters, FLOPs or latency (a model comparison, often with a Pareto front), one point per sample to show a correlation, or a 2-D embedding (t-SNE, UMAP). Panel aspect 1 : 1: both axes are data and matter equally. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Many points** (samples, examples): dots of the design's marker size, translucent so dense regions read darker, `ax.scatter(x, y, s=rcParams["lines.markersize"] ** 2, color=color, edgecolors="none", alpha=0.5)`, gridlines in both directions.
- **Few labelled points** (models compared on accuracy against cost): one hollow marker per model, `ax.plot(x, y, "o", color=color)`. With a proposed model, ours in `colors["ours"]` and every other model in `colors["neutral"]`; without one, `series-1`, or one color per model family when families are the message.
- **Cost axes** (parameters, FLOPs, latency): log when they span over 10× (an order of magnitude), lower than DESIGN.md's 100×, because model sizes grow by factors and on a linear axis the small members of a family bunch at the left where their names cannot fit; labelled as in `line-chart.md`.

## Variants

- **Trend line** (the takeaway is a correlation): a data line in `darken(color)` over the points; Pearson r with n in the caption (Spearman ρ when the data are ranks or ordinal ratings).
- **Model family** (sizes of one model, B0–B7): its points joined in size order with a solid data line in the family's color, `ax.plot(x, y, "o-", color=colors["ours"])` for ours; its members are one kind, so every one is named, by its short tag (`B0` … `B7`), the full names in the legend or caption.
- **Pareto front**: the models on the front joined in x order with a dashed `neutral` line under the markers, `ax.plot(x, y, linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)`; a second front dotted, `":"`. Dominated models stay as markers.
- **Embedding** (t-SNE, UMAP): each point as a marker with a black edge and a translucent fill in its class color, past six classes also its own marker shape (DESIGN.md Colors), `ax.plot(x, y, shape, markeredgecolor=colors["ink"], markeredgewidth=paper.filled_edge_width, markerfacecolor=(*to_rgb(color), 0.5), linestyle="none", label=name)`; one color per class (DESIGN.md Colors) with a legend; no ticks, tick labels, gridlines or axis labels (`ax.set_xticks([])`, `ax.set_yticks([])`, `ax.grid(False)`): the axes of an embedding mean nothing.

## Labels

- **Point names**: next to each labelled point in `darken(color)`, `ax.annotate(name, (x, y), xytext=(3, 3), textcoords="offset points", color=darken(color))`. Placements (for Collisions): upper right, upper left (`xytext=(-3, 3), ha="right"`), lower right and lower left (`va="top"`). `finalize_figure` grows the limits by up to a quarter to keep names inside; beyond that it reports them.
- **Values**: when the takeaway compares some labelled models, their values join their names, `f"{name} ({v:#.3g}%)"`.

## Caption

- **Correlation**: the coefficient and n.
- **Fronts and families**: what each line style joins ("the dashed line joins the NAS models on the Pareto front").
