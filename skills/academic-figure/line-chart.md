# Line chart

Values along a continuous x: learning curves (training curves), scaling curves, pass@k, a metric over a swept hyperparameter, ROC and precision-recall curves. Read with `DESIGN.md`, whose rules all still apply.

## Lines

- `ax.plot(x, y, color=color)`; gridlines in both directions.
- A curve through a few measured points (up to ~30: model sizes, sweep values, numbers of samples, classifier thresholds) shows every measured point as the design's hollow marker on the line, `ax.plot(x, y, "o-", color=color)`, so the reader sees where the data is and where the line only connects it. Densely logged curves (training steps, epochs) are plain lines. With markers, each series gets its own marker shape, in series order: `"o"`, `"s"`, `"^"`, `"D"`, `"v"`, `"P"`, the same shape for a series in every panel.
- Diagnostics, however often they were logged: draw the raw values in the series color at `alpha=0.25` without a label, then `smooth(values)` on top with the label, and add to the caption: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- Reported results are drawn raw.
- Several runs per setting (seeds, folds, trials): draw the mean as the line and a band of ±1 std with `ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)`, and say in the caption what the band is and over how many runs.

## Axes

- Log₂ axes (number of samples, batch size): `ax.set_xscale("log", base=2)`, ticks as DESIGN.md sets for log axes (`b = 2`, `e0 = 0`, `top = 2 ** e1` the first power at or above the largest x), `ax.set_xticks(ks, labels=[str(k) for k in ks])`, and no minor ticks (`ax.set_xticks([], minor=True)`). The axis ends at `top` with the usual 5% margin, so every panel ends on a labelled tick: `margin = 2 ** (0.05 * math.log2(top))`, `ax.set_xlim(1 / margin, top * margin)`.
- Scaling curves (parameters, FLOPs, tokens, data size): `ax.set_xscale("log")`, ticks at the powers of 10 in range, labelled with SI suffixes as plain text (`ax.set_xticks([1e8, 1e9, 1e10], labels=["100M", "1B", "10B"])`), minor ticks and gridlines kept without labels, as in DESIGN.md. A scaling law (loss against compute) also takes a log y axis.
- Scaling law fits: the measured points as markers without a line, and the fitted power law as a dashed line in the same color over the fitted range, `ax.plot(x_fit, a * x_fit ** -b, linestyle="--", linewidth=paper.dashed_width, color=color)`; the fitted exponent goes in the legend entry, `label=f"Ours (fit: $L \\propto C^{{-{b:.3f}}}$)"` (mathtext, since Inter has no ∝ glyph), or in the caption.

## ROC and precision-recall curves

- One panel, aspect 1 : 1, both axes from 0 to 1 (`ax.set_xlim(0, 1)`, `ax.set_ylim(0, 1)`, the one place limits are fixed, since the unit square is the space). When the message is the low false-positive regime (membership inference, detection at 0.1% FPR), both axes on a log scale from the smallest rate shown to 1, the chance line still the diagonal.
- The curve is computed from a finite test set, so it is a staircase through the thresholds: draw it as computed (`drawstyle="steps-post"` for precision-recall), never smoothed, with markers at the operating points the paper reports, or else at ~10 points evenly spaced along each curve (`markevery=max(1, len(fpr) // 10)`).
- ROC: x "False positive rate", y "True positive rate", and the chance diagonal as a reference line, named in the caption rather than the legend (`ax.axline((0, 0), (1, 1), linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)`). Precision-recall: x "Recall", y "Precision", and the positive rate as a horizontal reference line.
- The area under each curve goes in its legend entry, three significant figures: `label=f"Ours (AUC {auc:.3f})"`; when the data gives none, compute it from the curve (`np.trapezoid(tpr, fpr)`) and say so in the caption. The chance diagonal is drawn even when the paper left it out. No `mark_value`.

## Value labels

When the takeaway compares reported results across series, mark the compared values on the curves:

- Find the point where the paper makes the comparison: the claim decides it. "Ours reaches a higher score" compares each series' best; "ours ends higher" compares final values (at the last x all series share, when they end at different x); "ours is ahead at the same budget" compares values at that shared x. The value is the plotted metric at that point.
- If the request and the paper don't settle the comparison point, ask the user. When you can't ask, compare each series' best and say so in the reply.
- Mark each value there with `mark_value(ax, x, y, "0.438", color)`: a dashed line in `darken(color)` across the whole panel at that value, under the curves; a circle on the point; and the value just above it. One per compared series, in the panels the takeaway is about. The lines let the reader compare heights anywhere in the panel.
- If a label above the point covers a curve, put it below with `below=True`.
- When the compared values sit too close for every label to stand clear (curves a few points apart at the comparison point), mark ours and its closest competitor only, and give the other values in the caption.
- A two-factor grid (models × benchmarks) carries no value marks: it shows a pattern across many panels, and a mark in one panel singles it out. The compared numbers go in the caption.
