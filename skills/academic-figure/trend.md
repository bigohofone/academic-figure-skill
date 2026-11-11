# Trend: values along a continuous x

Training curves, scaling with model or data size, pass@k over the number of samples, a metric over a swept hyperparameter. Read with `SKILL.md`, whose rules all still apply.

## Lines

- `ax.plot(x, y, color=color)`; gridlines in both directions (style).
- Curves are plain lines; add markers (the style's hollow markers) only when the user asks. Then each series gets its own marker shape, in series order: `"o"`, `"s"`, `"^"`, `"D"`, `"v"`, `"P"`, the same shape for a series in every panel.
- Diagnostics, however often they were logged: draw the raw values in the series color at `alpha=0.25` without a label, then `smooth(values)` on top with the label, and add to the caption: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- Reported results are drawn raw.
- Several runs per setting (seeds, folds, trials): draw the mean as the line and a band of ±1 std with `ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)`, and say in the caption what the band is and over how many runs.
- Log₂ axes (number of samples, batch size, model size): `ax.set_xscale("log", base=2)`, a tick at every power of 2 up to the first one at or above the largest x (`top`) with `ax.set_xticks(ks, labels=[str(k) for k in ks])`, and no minor ticks (`ax.set_xticks([], minor=True)`). The axis ends at `top` with the usual 5% margin, so every panel ends on a labelled tick: `margin = 2 ** (0.05 * math.log2(top))`, `ax.set_xlim(1 / margin, top * margin)`. Where those labels overlap, step by 4 (`1, 4, 16, 64`).

## Value labels

When the takeaway compares reported results across series, mark the compared values on the curves:

- Find the point where the paper makes the comparison: the claim decides it. "Ours reaches a higher score" compares each series' best; "ours ends higher" compares final values (at the last x all series share, when they end at different x); "ours is ahead at the same budget" compares values at that shared x. The value is the plotted metric at that point.
- If the request and the paper don't settle the comparison point, ask the user. When you can't ask, compare each series' best and say so in the reply.
- Write each value with three significant figures.
- Mark each value there with `mark_value(ax, x, y, "0.438", color)`: a 0.75 pt dashed line in `darken(color)` across the whole panel at that value, under the curves; a circle on the point; and the value in bold just above it. One per compared series, in the panels the takeaway is about. The lines let the reader compare heights anywhere in the panel.
- If a label above the point covers a curve, put it below with `below=True`.
