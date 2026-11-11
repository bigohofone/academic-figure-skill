# Error bar plot

Means with uncertainty, one point per method or setting. Use when values differ by < 10% (bar from 0 hides them, `bar-chart.md`), or when uncertainty is the message (gain larger than spread over seeds?). Aka dot plot with error bars; horizontal form: forest plot. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Points: hollow marker at mean; error bar in series color.
  ```python
  ax.errorbar(x, mean, yerr=err, fmt="o", color=color, capsize=2,
              elinewidth=rcParams["patch.linewidth"], capthick=rcParams["patch.linewidth"])
  ```
- Axis: methods are categories; tick marks hidden; horizontal gridlines only. Value axis: spans intervals, default margins, not from 0.

## Variants

- Forest plot (method names don't fit side by side, DESIGN.md Typography): horizontal; methods top to bottom (`ax.invert_yaxis()`); vertical gridlines only; reference line (DESIGN.md Shapes) at strongest baseline's value, or at 0 for differences.
  ```python
  ax.errorbar(mean, y, xerr=err, fmt="o", ...)
  ```
- Several series per category: points share 0.8 of category slot, like grouped bars; one legend entry per series.
  ```python
  width = 0.8 / n_series
  x_i = x + (i - (n_series - 1) / 2) * width  # series i
  ```

## Labels

- Means: beside end of error bar, `darken(color)`: above upper cap; forest plot: right of right cap.
  ```python
  ax.annotate(f"{m:#.3g}", (x, m + err), xytext=(0, 3), textcoords="offset points",
              ha="center", va="bottom", color=darken(color), gid="value-label")
  # forest plot
  ax.annotate(f"{m:#.3g}", (m + err, y), xytext=(3, 0), textcoords="offset points",
              ha="left", va="center", color=darken(color), gid="value-label")
  ```

## Caption

- Reading guide: what bars are: "error bars show ±1 std over 5 seeds" (sample std, `np.std(runs, ddof=1)`), or "95% confidence intervals over 3 seeds".
