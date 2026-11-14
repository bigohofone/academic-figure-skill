# Pie chart

Composition of one whole with 2–6 parts, when composition is the message: dataset makeup by source, domain or language. More parts, or several wholes to compare: stacked bar chart (`bar-chart.md`). Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Donut: each part own color, `paper.make_part_colors(n)` (DESIGN.md Colors, parts of one whole): the legend is read by color. Clockwise from 12 o'clock, largest first. Parts < 3%: joined into one "Other", drawn last.

  ```python
  part_colors = paper.make_part_colors(n)
  wedges, _ = ax.pie(shares, colors=part_colors, startangle=90, counterclock=False,
                     wedgeprops=dict(width=0.4, edgecolor=colors["paper"], linewidth=rcParams["grid.linewidth"]))
  ```

- Size: `finalize_figure` sizes circle to width, ignores `height`; no axes, ticks or grid (`ax.pie` hides them).

## Variants

- Two wholes (train and test splits): two donuts side by side, titled, one legend for both.

## Labels

- Names and shares: in a legend right of the donut, one entry per part in wedge order, `f"{name} {share_text}"` (`share_text` per DESIGN.md value table, a share); nothing written on or beside the wedges, so small parts read like large ones. Right of a round panel is free (overrides DESIGN.md Layout, right of panels).

  ```python
  fig.legend(wedges, [f"{name} {share_text}" for name, share_text in ...], loc="outside right center")
  ```

- Total: whole's size in center.

  ```python
  ax.text(0, 0, "1.24M\nexamples", ha="center", va="center")
  ```
