# Area chart

Shares of a whole along a continuous x: the data mixture over training, the token share of each domain over steps, the composition of outputs over a sweep. Panel aspect 1 : 1. Read with `DESIGN.md`, whose rules all still apply. Values that are not parts of one whole are a line chart (`line-chart.md`), never unstacked areas.

- Stacked area chart: `ax.stackplot(x, ys, colors=series_colors, labels=names, edgecolor="white", linewidth=0.5)`, series in order from the bottom, the largest or most stable part at the bottom so the others read against a flat base.
- Shares that change in stages (a curriculum switching at set steps): draw the steps, `ax.stackplot(..., step="post")`, mark each switch with a dashed `neutral` vertical line (`ax.axvline(step, linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"])`), and put ticks at the switches.
- A share the takeaway cites is written inside its band at each stage, 7 pt, in `text_color(band_color)`.
- Shares: normalize each x to 1 (or 100%) and fix the axis to it, `ax.set_ylim(0, 1)`, `ax.margins(x=0)`: the whole is the space, so no margins.
- Name each band directly, at its right end beside the panel, in the stacking order, instead of a legend: `ax.annotate(name, (1, y_mid), xycoords=("axes fraction", "data"), xytext=(4, 0), textcoords="offset points", va="center")`, with `y_mid` the middle of the band at the last x; nudge labels of thin neighbouring bands apart so they don't touch.
- Gridlines: horizontal only, drawn over the areas so shares read off them: `ax.set_axisbelow(False)`, `ax.grid(axis="x", visible=False)`.
