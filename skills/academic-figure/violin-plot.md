# Violin plot

As a box plot (`box-plot.md`), when the shape of the spread matters: several modes, a long tail, a cluster at a bound. With few values per group (under ~20) the estimated shape is unreliable; draw a box plot with every point instead. Read with `DESIGN.md`, whose rules all still apply.

- `parts = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)`; fill the body with its series color lightened, at full opacity, with a black 0.75 pt edge (`body = parts["bodies"][0]`, `body.set_facecolor(lighten(color))`, `body.set_edgecolor("black")`, `body.set_linewidth(0.75)`, `body.set_alpha(1)`), and draw the median as a black 1 pt line across it: `ax.hlines(np.median(values), x - 0.15, x + 0.15, color="black", linewidth=1)`.
- Groups on the x-axis are categories: hide their tick marks, horizontal gridlines only.
- Grouped violins and legend entries as grouped box plots in `box-plot.md`.
- Caption: "violins show the kernel density of the values; the line marks the median".
