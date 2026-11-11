# Error bar plot

Means with their uncertainty, one point per method or setting: when the compared values differ by less than 10% of their size (a bar chart from 0 would hide them, `bar-chart.md`), or when the uncertainty itself is the message (is the gain larger than the spread over seeds?). Also called a dot plot with error bars; its horizontal form is a forest plot. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Points**: `ax.errorbar(x, mean, yerr=err, fmt="o", color=color, capsize=2, elinewidth=rcParams["patch.linewidth"], capthick=rcParams["patch.linewidth"])`: the design's hollow marker at the mean, the error bar in the series color.
- **Axis**: methods are categories: tick marks hidden, horizontal gridlines only. The value axis spans the intervals with the default margins, not from 0.

## Variants

- **Forest plot** (method names that don't fit side by side, DESIGN.md Typography): horizontal, `ax.errorbar(mean, y, xerr=err, fmt="o", ...)`, methods top to bottom (`ax.invert_yaxis()`), vertical gridlines only, and a dashed reference line at the baseline's value, or at 0 for differences.
- **Several series per category**: the points of one category share 0.8 of its slot like grouped bars, `width = 0.8 / n_series`, series `i` at `x + (i - (n_series - 1) / 2) * width`; one legend entry per series.

## Labels

- **Means**: each mean beside the end of its error bar, clear of the bar, in `darken(color)`: above the upper cap, `ax.annotate(f"{m:#.3g}", (x, m + err), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", color=darken(color))`; in a forest plot, right of the right cap, `(m + err, y)`, `xytext=(3, 0)`, `ha="left", va="center"`.

## Caption

- **Reading guide**: what the bars are: "error bars show ±1 std over 5 seeds" (the sample std, `np.std(runs, ddof=1)`), or "95% confidence intervals over 3 seeds".
