# Line chart

Values along continuous x: learning curves, scaling curves, pass@k, metric over swept hyperparameter, ROC and precision-recall curves. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Line: gridlines both directions.
  ```python
  ax.plot(x, y, color=color)
  ```
- Markers (not ROC/PR): when the longest curve in the figure has ≤ 30 measured points, hollow marker at each point, all series and panels; else plain lines. One shape per series in every panel, in series order: `"o"`, `"s"`, `"^"`, `"D"`, `"v"`, `"P"`.
  ```python
  ax.plot(x, y, "o-", color=color)
  ```
- Diagnostics: raw values in series color, `alpha=0.25`, unlabelled; centered moving average over 5% of the points on top, labelled.
  ```python
  w = max(1, len(y) // 40) * 2 + 1
  smooth = np.convolve(y, np.ones(w) / w, mode="valid")
  ax.plot(x[w // 2 : len(x) - w // 2], smooth, color=color, label=name)
  ```
  Reported results: raw.
- Several runs per setting (seeds, folds): mean as line, ±1 std as band.
  ```python
  ax.fill_between(x, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)
  ```

## Variants

- Log₂ x (number of samples, batch size): no minor ticks. Tick and gridline at every power of 2, from first ≤ smallest x to first ≥ largest x (`top`; in a grid sharing x, largest over all panels). Every power labelled; too crowded: every second power as the tick step. Axis ends at `top` plus design data margin.
  ```python
  ax.set_xscale("log", base=2)
  ax.set_xticks([], minor=True)
  margin = 2 ** (rcParams["axes.xmargin"] * math.log2(top / ks[0]))
  ax.set_xlim(ks[0] / margin, top * margin)
  ```
- Scaling curve (parameters, FLOPs, tokens, data size): log x (DESIGN.md log rule, span > 100×); ticks with SI suffixes as plain text.
  ```python
  ax.set_xticks([1e8, 1e9, 1e10], labels=["100M", "1B", "10B"])
  ```
- Scaling law fit: both axes log. Measured points: markers, no line. Fitted law: dashed, same color, over fitted range; exponent in legend entry, per DESIGN.md value table; N, C or D for the x quantity; mathtext (Inter has no ∝ glyph).
  ```python
  ax.plot(x_fit, a * x_fit ** -b, linestyle="--", linewidth=paper.dashed_linewidth, color=color,
          label=f"Fit: $L \\propto N^{{-{b_text}}}$")
  ```
- ROC curve: one panel, both axes 0–1 (square, set by `finalize_figure`); x "False positive rate", y "True positive rate"; chance diagonal always, named in caption. Message is low-FPR regime (detection at 0.1% FPR): both axes log, smallest rate shown to 1.
  ```python
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
  ```
- Precision-recall curve: as ROC; x "Recall", y "Precision", `drawstyle="steps-post"`; positive rate as horizontal reference line.
- ROC and PR curves: as computed (staircase through thresholds), never smoothed. No markers, except operating points the paper reports. Variants of ours: by line style, full method solid, others dashed, all ours color (DESIGN.md Colors). AUC in each legend entry; data gives none: compute it, say so in caption.
  ```python
  auc = np.trapezoid(tpr, fpr)
  label = f"Ours (AUC {auc:#.3g})"
  ```

## Labels

No value marks on curves. Takeaway compares reported results across series: compared values in caption, at the point the claim implies:

- "Reaches a higher score": each series' best.
- "Ends higher": final values, at last x all series share.
- "Ahead at the same budget": values at that x.
- Request and paper don't settle it: ask user; can't ask: each series' best, say so in reply.

## Caption

- Bands: what and over how many runs ("shaded bands show ±1 std over 5 seeds").
- Diagnostics: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- Reference lines, log axes: named in reading guide ("the thin diagonal marks chance"; "both axes are logarithmic").
