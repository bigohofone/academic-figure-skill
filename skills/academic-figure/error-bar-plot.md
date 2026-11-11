# Error bar plot

Means with their uncertainty, one point per method or setting: when the differences are small next to the values (a bar chart from 0 would hide them), or when the uncertainty itself is the message (is the gain larger than the spread over seeds?). Also called a dot plot with error bars; the horizontal form with many methods is a forest plot. Read with `DESIGN.md`, whose rules all still apply.

- `ax.errorbar(x, mean, yerr=err, fmt="o", color=color, capsize=2, elinewidth=0.75, capthick=0.75)`: the design's hollow marker at the mean, the error bar in the series color. Methods are categories on the x-axis: hide their tick marks, horizontal gridlines only.
- The axis does not start at 0: it spans the intervals with the default margins.
- Value labels: write each mean beside the end of its error bar, clear of the bar: `ax.annotate(f"{m:#.3g}", (x, m + err), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", color=darken(color))` above the upper cap; in a forest plot, right of the right cap, `(m + err, y)`, `xytext=(3, 0)`, `ha="left", va="center"`.
- Several series per category (methods on several benchmarks): offset the points of one category like grouped bars, `x + (i - (n_series - 1) / 2) * 0.2`, one legend entry per series.
- **Forest plot** (method names that don't fit side by side, as in DESIGN.md Typography): horizontal, `ax.errorbar(mean, y, xerr=err, fmt="o", ...)`, methods top to bottom in reading order (`ax.invert_yaxis()`), vertical gridlines only, and a dashed reference line at the baseline's value or at 0 for differences.
- The caption says what the bars are: "error bars show ±1 std over 5 seeds" (the sample std, `np.std(runs, ddof=1)`) or "95% confidence intervals over 3 seeds".
