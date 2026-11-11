# Area chart

Shares of a whole along a continuous x: the data mixture over training, the token share of each domain over steps, the composition of outputs over a sweep. Values that are not parts of one whole are a line chart (`line-chart.md`), never unstacked areas. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Areas**: `ax.stackplot(x, ys, colors=series_colors, labels=names, edgecolor="white", linewidth=rcParams["grid.linewidth"])`, panel aspect 1 : 1. The part whose share changes least over x (the smallest std) at the bottom, so the others read against a flat base; the rest in series order above it.
- **Axes**: shares normalized to 1 at each x, the axis fixed to the whole, `ax.set_ylim(0, 1)`, `ax.margins(x=0)`.
- **Gridlines**: horizontal only, over the areas so shares read off them, `ax.set_axisbelow(False)`, `ax.grid(axis="x", visible=False)`.

## Variants

- **Stages** (a curriculum switching at set steps): `ax.stackplot(..., step="post")`, each switch marked with a dashed white vertical line (DESIGN.md reference lines over fills), `ax.axvline(step, linestyle="--", linewidth=paper.dashed_width, color="white")`, and ticks at the switches.

## Labels

- **Band names**: at the right end beside the panel, in stacking order, instead of a legend, `ax.annotate(name, (1, y_mid), xycoords=("axes fraction", "data"), xytext=(4, 0), textcoords="offset points", va="center")`, `y_mid` the middle of the band at the last x; when `fit_height` reports two of them overlapping, move them apart along y.
- **Shares**: a share the takeaway cites, inside its band at each stage, `f"{v:.0%}"` in `text_color(band_color)`; a label that `fit_height` reports spilling out of its band is dropped, its value in the caption.

## Caption

- **Reading guide**: what the dashed lines mark.
