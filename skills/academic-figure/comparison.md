# Comparison: reported results across categories

Methods, ablations or settings compared on one or more benchmarks, one value each. Read with `SKILL.md`, whose rules all still apply.

- **Bar** (one bar per category on the x-axis): `bars = ax.bar(x, values, width, color=color, linewidth=0)`, grouped bars sharing 0.8 of each slot (`width = 0.8 / n_series`), every bar labelled with its value, `ax.bar_label(bars, fontweight="bold")`. Horizontal gridlines only: `ax.grid(axis="x", visible=False)`. For several groups (benchmarks, datasets), one panel per group, named by its subcaption. Over several runs, error bars of ±1 std, named in the caption: `ax.bar(..., yerr=std, capsize=2, error_kw=dict(elinewidth=0.75, capthick=0.75, ecolor="black"))`.
- **Horizontal bar**: only for unordered categories with long names. As bars, with `ax.barh` and vertical gridlines only: `ax.grid(axis="y", visible=False)`.
- **Stacked bar** (parts of a whole per category): segments in series order from the bottom with white 0.5 pt seams, `ax.bar(x, v, bottom=below, color=color, edgecolor="white", linewidth=0.5)`; horizontal gridlines only.
- **Pie chart**: draw a bar chart instead.
