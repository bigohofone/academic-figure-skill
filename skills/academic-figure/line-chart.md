# Line chart

Values along a continuous x: learning curves, scaling curves, pass@k, a metric over a swept hyperparameter, ROC and precision-recall curves. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Line**: `ax.plot(x, y, color=color)`, gridlines in both directions.
- **Markers** (except ROC and PR curves, below): when every curve in the figure has 30 or fewer measured points (the longest curve decides, for all series and panels alike) shows each point as the design's hollow marker, `ax.plot(x, y, "o-", color=color)`, so the reader sees where the data is; otherwise plain lines. Each series keeps one marker shape in every panel, in series order: `"o"`, `"s"`, `"^"`, `"D"`, `"v"`, `"P"`.
- **Diagnostics**: the raw values in the series color at `alpha=0.25` without a label, then `smooth(values)` on top with the label. Reported results are drawn raw.
- **Several runs per setting** (seeds, folds): the mean as the line and ±1 std as a band, `ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)`.

## Variants

- **Log₂ x axis** (number of samples, batch size): `ax.set_xscale("log", base=2)`, no minor ticks (`ax.set_xticks([], minor=True)`). A tick and gridline at every power of 2 from the first at or below the smallest x to the first at or above the largest (`top`; in a grid sharing x, the largest over all panels), labelled as DESIGN.md's tick rule allows (every one, or every m-th with the rest blank). The axis ends at `top` with the usual 5% margin: `margin = 2 ** (0.05 * math.log2(top / ks[0]))`, `ax.set_xlim(ks[0] / margin, top * margin)`.
- **Scaling curve** (parameters, FLOPs, tokens, data size): a log x axis, as DESIGN.md's log rule gives for spans over 100×, ticks labelled with SI suffixes as plain text, `ax.set_xticks([1e8, 1e9, 1e10], labels=["100M", "1B", "10B"])`.
- **Scaling law fit**: both axes log, where a power law is a straight line. The measured points as markers without a line; the fitted law as a dashed line in the same color over the fitted range, `ax.plot(x_fit, a * x_fit ** -b, linestyle="--", linewidth=paper.dashed_width, color=color)`, its exponent in the legend entry, written by DESIGN.md's value table, `label=f"Fit: $L \\propto N^{{-{b_text}}}$"` (N, C or D for the quantity on x) (mathtext, since Inter has no ∝ glyph).
- **ROC curve**: one panel, aspect 1 : 1, both axes fixed to 0–1 (`ax.set_xlim(0, 1)`, `ax.set_ylim(0, 1)`); x "False positive rate", y "True positive rate"; the chance diagonal always, `ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)`, named in the caption. When the message is the low false-positive regime (detection at 0.1% FPR), both axes log from the smallest rate shown to 1.
- **Precision-recall curve**: as ROC, with x "Recall", y "Precision", `drawstyle="steps-post"`, and the positive rate as a horizontal reference line.
- **ROC and PR curves**: drawn as computed (a staircase through the thresholds), never smoothed; markers at the operating points the paper reports, else at 10 points evenly spaced along each curve, `markevery=max(1, len(fpr) // 10)`. The area under each curve in its legend entry, `label=f"Ours (AUC {auc:#.3g})"`; when the data gives none, compute it, `np.trapezoid(tpr, fpr)`, and say so in the caption. No `mark_value`.

## Labels

When the takeaway compares reported results across series, mark the compared values (never in a two-factor grid, DESIGN.md Layout):

- **Comparison point**: the claim decides it. "Reaches a higher score": each series' best. "Ends higher": the final values, at the last x all series share. "Ahead at the same budget": the values at that x. If the request and the paper don't settle it, ask the user; when you can't ask, compare each series' best and say so in the reply.
- **Mark**: `mark_value(ax, x, y, f"{y:#.3g}", color)` at each compared point, one per compared series: a dashed line in `darken(color)` across the panel at that value, a circle on the point, and the value above it.
- **Placements** (for Collisions): above the point, then below it (`below=True`); then mark ours and its closest competitor only, the other values in the caption.

## Caption

- **Bands**: what they are and over how many runs ("shaded bands show ±1 std over 5 seeds").
- **Diagnostics**: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- **Reference lines and log axes**: named in the reading guide ("the thin diagonal marks chance"; "both axes are logarithmic").
