# Area chart

Shares of a whole along continuous x: data mixture over training, each domain's token share over steps, output composition over a sweep. Values not parts of one whole: line chart (`line-chart.md`), never unstacked areas. Read with `DESIGN.md`; its rules apply unless overridden here.

## Draw

- Areas: panel aspect 1 : 1. Bottom: part whose share changes least over x (smallest std), giving others a flat base; rest above in data order. Each band own color, `paper.part_colors(n)` (DESIGN.md Colors, parts of one whole), bottom up.

  ```python
  ax.stackplot(x, ys, colors=series_colors, labels=names, edgecolor="white", linewidth=rcParams["grid.linewidth"])
  ```

- Axes: shares normalized to 1 at each x; y fixed to the whole; no x margins.

  ```python
  ax.set_ylim(0, 1)
  ax.margins(x=0)
  ```

- Gridlines: horizontal only, over the areas.

  ```python
  ax.set_axisbelow(False)
  ax.grid(axis="x", visible=False)
  ```

## Variants

- Stages (curriculum switching at set steps): stepped areas; each switch a dashed white vertical line (DESIGN.md reference lines over fills); ticks at switches.

  ```python
  ax.stackplot(..., step="post")
  ax.axvline(step, linestyle="--", linewidth=paper.dashed_width, color="white")
  ```

## Labels

- Band names: legend above panel (DESIGN.md Legend, a filled plot), entries from top band down.
- Shares: shares the takeaway cites, inside band at each stage, as shares (DESIGN.md Value labels), in `text_color_on(band_color)`; if one share of a band spills out: all that band's shares to caption.

## Caption

- Reading guide: what dashed lines mark.
