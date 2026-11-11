# Several panels

How panels share a figure: grid, shared axes, axis labels, second y axis, panel names. DESIGN.md's other rules apply to every panel.

## Grid

| Width | Max columns |
|---|---|
| Half text width (2.75 in) | 1 |
| Single column (3–3.25 in) | 2 |
| Full width, single-column venue (5.5 in) | 3 |
| 1.5 column | 3 |
| Double column | 4 |

0. Two-factor grid (models × benchmarks, methods × datasets; also rows of different plots over same columns: plot type = row factor, named by each row's y label): one factor per row, other per column, ignoring column limit; 4 models × 4 benchmarks = 4 × 4. Layout the user or task asks for (e.g. all panels in one row) wins; each factor's groups then = Grouped axes of step 6.
   - Axis with same quantity in every panel: one range across grid (`sharex=True` / `sharey=True`). Quantity changes between columns or rows: share only down column (`sharex="col"`) or across row (`sharey="row"`).
   - Tick numbers only on left column and bottom row (step 5 does not apply); panels may be as narrow as 0.9 in (two columns fit half text width). Still narrower: factor with fewer levels on columns; never reflow.
   - No value marks or emphasis singling out one panel; compared numbers in caption.
   ```python
   finalize_figure(fig, axes, min_width=0.9)
   ```
1. Start: all panels in one row, up to column limit.
2. Render: `finalize_figure` warns when a panel's data area < `min_width` (1.2 in), or text is cut off or overlaps.
3. On warning, first free room within row: share y when panels plot same quantity (step 5); Typography text tick rule; shorten labels. Panel still too narrow: add a row, columns = ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 2 × 3); render again. No row limit.
4. Unused cells: off (5 panels in 2 × 3: the last).
5. Shared axes: panels plot same quantity over same range: share. Tick numbers once (matplotlib default): y on leftmost panel of each row, x on bottom row. `finalize_figure` sets gaps (panels close). Unshared axis: own tick numbers.
   ```python
   fig, axes = plt.subplots(..., sharex=True, sharey=True)
   ```
6. Axis labels: each quantity named once, in one or two words when panels are narrow (Accuracy, Loss; detail in the caption).
   - Side by side, same x quantity: one `fig.supxlabel` under row; none on panels.
   - Stacked, same y quantity: y label on leftmost panel of each row only (or `fig.supylabel` once down column).
   - Side by side, same y quantity, shared or not: y label on leftmost panel only.
   - Inside sub-figures (`supxlabel` is subcaption): each panel keeps own.
   - Panel with different quantity: own label.

   Grouped axes: columns in groups, each its own quantity (two panels accuracy, then two loss): first column of each group carries group's y label and tick numbers; `sharey` within group; `labelleft=False` on rest. x label same rule: one `fig.supxlabel` when all groups share x quantity, else one label centred under each group (`axis="y"` for a group of rows, passing its left panels). `finalize_figure` sets gaps: columns within group close, groups apart.
   ```python
   paper.set_group_label(bottom_panels_of_group, "Step")
   ```
   Right y axis (`ax.twinx()`, second quantity on same x): mirrors left: four-character tick labels, label line, in right margin; panel narrows, keeps standard height. Equal terms (Colors: `series-1` left, `series-4` right, unless one is ours); right one also dashed (black-and-white). Gridlines from left axis only. One legend for both, on left axes raised above twin. Set schedule (learning rate, warmup): drawn as given, never smoothed.
   ```python
   twin.grid(False)
   ax.set_zorder(twin.get_zorder() + 1)
   ax.patch.set_visible(False)
   ```

## Panel names

No figure title; caption names it. First row that fits:

| Panels | Names |
|---|---|
| Two-factor grid | Headers: each column once above top row; each row once left of first column's y label (rows of different plots: y labels name them). Code A |
| Sub-figures side by side, each a panel group with own message and legend | Lettered subcaption below each; its panels titled per next row. Only sub-figures get letters. Code B |
| Several panels reader must tell apart | Title above each, `ax.set_title` |
| One panel | None |

```python
# A: two-factor grid headers
ax.set_title(col_name)
axes[r, 0].annotate(row_name, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                    textcoords="offset points", ha="right", va="center", rotation=90,
                    fontsize=rcParams["axes.titlesize"])

# B: sub-figures (width ratios = panel counts)
left, right = fig.subfigures(1, 2, width_ratios=[3, 2])
panels = left.subplots(1, 3)
left.supxlabel("(a) Reward gating ablation")

# Several panels
ax.set_title("Response length")
```
