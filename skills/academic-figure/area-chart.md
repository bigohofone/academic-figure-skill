# Area chart

Shares of a whole along a continuous x: the data mixture over training, the token share of each domain over steps, the composition of outputs over a sweep. Read with `DESIGN.md`, whose rules all still apply. Values that are not parts of one whole are a line chart (`line-chart.md`), never unstacked areas.

- Stacked area chart: `ax.stackplot(x, ys, colors=series_colors, labels=names, edgecolor="white", linewidth=0.5)`, series in order from the bottom, the largest or most stable part at the bottom so the others read against a flat base.
- Shares: normalize each x to 1 (or 100%) and fix the axis to it, `ax.set_ylim(0, 1)`, `ax.margins(x=0)`: the whole is the space, so no margins.
- Legend entries in the stacking order from the top, so they read like the chart: `handles, labels = ax.get_legend_handles_labels()`, `ax.legend(handles[::-1], labels[::-1], ...)`, outside to the right when the areas fill the panel, `ax.legend(..., loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)`.
- Gridlines: horizontal only, drawn over the areas so shares read off them: `ax.set_axisbelow(False)`, `ax.grid(axis="x", visible=False)`.
