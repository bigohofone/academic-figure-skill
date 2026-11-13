# Pie chart

Composition of one whole with 2–6 parts, when composition is the message: dataset makeup by source, domain or language. More parts, or several wholes to compare: stacked bar chart (`bar-chart.md`). Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Donut: each part own color, `paper.make_part_colors(n)` (DESIGN.md Colors, parts of one whole). Clockwise from 3 o'clock, largest first (small parts end at right, outside labels stack vertically). Parts < 3%: joined into one "Other", drawn last.

  ```python
  part_colors = paper.make_part_colors(n)
  wedges, _ = ax.pie(shares, colors=part_colors, startangle=0, counterclock=False,
                     wedgeprops=dict(width=0.4, edgecolor="white", linewidth=rcParams["grid.linewidth"]))
  ```

- Size: `finalize_figure` sizes circle to width, ignores `height`; no axes, ticks or grid (`ax.pie` hides them).

## Variants

- Two wholes (train and test splits): two donuts side by side, titled.

## Labels

- Names: outside, next to wedges; no legend.

  ```python
  for w, name in zip(wedges, names):
      mid = np.deg2rad((w.theta1 + w.theta2) / 2)
      x, y = np.cos(mid), np.sin(mid)
      ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y), ha="left" if x > 0 else "right", va="center")
  ```

- Shares: inside ring at wedge middle (0.8 = middle of width-0.4 ring); `share_text` per DESIGN.md value table (a share).

  ```python
  ax.text(0.8 * x, 0.8 * y, share_text, ha="center", va="center", color=text_color)  # on the wedge color, DESIGN.md Typography
  ```

  Placements (for Collisions): inside wedge; then joined to name outside, `f"{name} {share_text}"`, straight leader line from label's side (below); then later of two moved outward (`xytext` at `1.35` instead of `1.12`).

  ```python
  arrowprops = dict(arrowstyle="-", color=colors["ink"], linewidth=rcParams["grid.linewidth"], relpos=(0, 0.5) if x > 0 else (1, 0.5))
  ```

- Total: whole's size in center.

  ```python
  ax.text(0, 0, "1.24M\nexamples", ha="center", va="center")
  ```
