# Pie chart

The composition of one whole with two to six parts, when the composition itself is the message: a dataset's makeup by source, domain or language. With more parts, or several wholes to compare, draw a stacked bar chart instead (`bar-chart.md`): angles are hard to compare. Read with `DESIGN.md`; its rules apply unless this file says otherwise.

## Draw

- **Donut** (a pie with its center cut out, the common form in papers): `wedges, _ = ax.pie(shares, colors=part_colors, startangle=0, counterclock=False, wedgeprops=dict(width=0.4, edgecolor="white", linewidth=rcParams["grid.linewidth"]))`. `part_colors` as DESIGN.md Colors gives them (the parts the takeaway names in color, the rest grey, or all in series order). Parts run clockwise from 3 o'clock, largest first, so the small parts end at the right side, where their outside labels stack vertically. Parts under 3% join one "Other" part, drawn last.
- **Size**: `fit_height` sizes the circle to the width and ignores `aspect`; no axes, ticks or grid (`ax.pie` hides them).

## Variants

- **Two wholes** (train and test splits): two donuts side by side, titled.

## Labels

- **Names**: outside, next to their wedges, instead of a legend: for each wedge `mid = np.deg2rad((w.theta1 + w.theta2) / 2)`, `x, y = np.cos(mid), np.sin(mid)`, `ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y), ha="left" if x > 0 else "right", va="center")`.
- **Shares**: inside the ring, on each wedge's middle, `ax.text(0.8 * x, 0.8 * y, f"{share:.0%}", ha="center", va="center", color=text_color(color))` (0.8 is the middle of a ring of width 0.4). Placements (for Collisions): inside the wedge, then joined to its name outside, `f"{name} {share:.0%}"`, with a straight leader line from the label's side, `arrowprops=dict(arrowstyle="-", color=colors["ink"], linewidth=rcParams["grid.linewidth"], relpos=(0, 0.5) if x > 0 else (1, 0.5))`; then the later of two moved outward (`xytext` at `1.35` instead of `1.12`).
- **Total**: the whole's size in the center, `ax.text(0, 0, "1.24M\nexamples", ha="center", va="center")`.
