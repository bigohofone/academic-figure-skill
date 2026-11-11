# Area chart

Shares of a whole along a continuous x: the data mixture over training, the token share of each domain over steps, the composition of outputs over a sweep. Values that are not parts of one whole are a line chart (`line-chart.md`), never unstacked areas. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Areas**: `ax.stackplot(x, ys, colors=series_colors, labels=names, edgecolor="white", linewidth=rcParams["grid.linewidth"])`, panel aspect 1 : 1. the stack puts the part whose share changes least over x (the smallest std) at the bottom, so the others read against a flat base, and the rest in data order above it; every band its own color, in DESIGN.md's parts order, `series-1`, `series-4`, `series-6`, `series-5`, `series-3`, `series-2`, from the bottom up (DESIGN.md Colors, parts of one whole).
- **Axes**: shares normalized to 1 at each x, the axis fixed to the whole, `ax.set_ylim(0, 1)`, `ax.margins(x=0)`.
- **Gridlines**: horizontal only, over the areas so shares read off them, `ax.set_axisbelow(False)`, `ax.grid(axis="x", visible=False)`.

## Variants

- **Stages** (a curriculum switching at set steps): `ax.stackplot(..., step="post")`, each switch marked with a dashed white vertical line (DESIGN.md reference lines over fills), `ax.axvline(step, linestyle="--", linewidth=paper.dashed_width, color="white")`, and ticks at the switches.

## Labels

- **Band names**: a legend above the panel (DESIGN.md Legend, a filled plot), entries from the top band down.
- **Shares**: a share the takeaway cites, inside its band at each stage, written as a share (DESIGN.md Value labels) in `text_color(band_color)`; when one share of a band spills out of it, all of that band's shares go to the caption (a band's shares are one kind).

## Caption

- **Reading guide**: what the dashed lines mark.
