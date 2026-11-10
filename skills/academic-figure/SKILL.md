---
name: academic-figure
description: Style rules for academic paper figures made with matplotlib or seaborn (size, fonts, colors, axes, legends, saving), plus a required delivery step - a `figures/` folder in the user's project holds a copy of the style files and `figures.ipynb`, where every figure is one self-contained cell, with a paper-style caption above it, so the user can run, edit, and re-export it (PDF/PNG) themselves. Always use this skill when creating or editing any figure, plot, graph, chart, heatmap, or visualization intended for a paper, even if no venue (ICML, CVPR, ACL, NeurIPS, ICLR) is mentioned, and even if the user asks only for the plotting code.
---

# Paper Figure Rules

Goal: a figure that reads well printed in the paper, where the reader gets its one message at a glance. Apply every rule unless the user says otherwise. A figure is delivered when its cell is in the notebook with its caption and has run.

Steps, in order:

1. **Takeaway**: work out what the paper uses this figure to show (from the user's request, the paper text or caption, the figure's role), then write it as one sentence with a number from the data. It sets the value labels (§3) and becomes the caption's takeaway (§7).
2. **Size**: width, grid and aspect (§1).
3. **Draw**: base style (§2), lines and text (§3), plot type (§4), color (§5), legend (§6).
4. **Save, caption, notebook** (§7, §8), then **check** (§9).

## 1. Size

### Width

| Venue | Single column | 1.5 column | Double column |
|---|---|---|---|
| ICML | 3.25 in | 5.0625 in | 6.75 in |
| CVPR | 3.25 in | 5.15625 in | 6.875 in |
| ACL (ARR) | 3 in | 4.6875 in | 6.25 in |
| NeurIPS | – | – | 5.5 in |
| ICLR | – | – | 5.5 in |

- Use the width the user names. Otherwise: the venue's single column (NeurIPS/ICLR: 5.5 in); with no venue, ICML single column.
- 1.5 column (0.75 × double) is a `figure*` narrower than the text: use it when the user asks, or when single column is too narrow and double column leaves the content sparse.

### Grid

| Width | Max cols | Max rows | More panels |
|---|---|---|---|
| Single column | 2 | 3 | double column |
| 1.5 column | 3 | 1 | double column |
| Double column | 4 | 2 | split into two figures |

1. Start with the most columns the limits allow.
2. Render and check every panel:
   - its data area (inside the spines) is at least 1.2 in wide;
   - its tick labels, title and axis labels are all shown in full, each on one line.
3. If a panel fails, add a row and set the columns to ⌈panels / rows⌉ (4 panels: 1 × 4 → 2 × 2; 5 panels: 1 × 4 → 2 × 3), then render again. When the rows are at their limit, move to the next wider width.
4. Turn off unused cells (5 panels in 2 × 3: the last cell).
5. When panels plot the same quantity over the same range on an axis, share it (`plt.subplots(..., sharex=True, sharey=True)`); the axis label then goes on the outer panels only.
6. Every panel has a y-axis label (with `sharey`, the outer panels carry it).

### Panel aspect

The aspect (width : height) is per panel. Use one of these, golden ratio φ : 1 by default:

| Aspect | `aspect=` | Fit |
|---|---|---|
| φ² : 1 | 0.382 | a single panel at 1.5- or double-column width |
| φ : 1 | 0.618 | curves, bars, histograms (default) |
| 1 : 1 | 1.0 | heatmap, confusion matrix, embedding |
| 1 : φ | 1.618 | content taller than wide (many horizontal bars) |

Slopes and gaps between curves need height, many x categories need width, matrices need square cells. If curves look flat after rendering, pick a taller aspect.

### Height

Let `fit_height` set it. Create the figure at the target width with any height, draw everything (labels, legend, colorbar), call `fit_height` last, then save with plain `fig.savefig`:

```python
fig, axes = plt.subplots(2, 1, figsize=(3.25, 2), sharex=True)
...  # plot, labels, legend, colorbar
fit_height(fig, axes, aspect=0.618)
fig.savefig("{id}.pdf")
```

- `ax` may be one Axes, an array, a list, or the `subplot_mosaic` dict; hidden cells and colorbars are skipped.
- `fit_height` also keeps every `mark_value` label inside its panel: it raises the y-limit to make room, and turns labels at a side edge inward.
- On `ValueError` (fixed aspect), draw images with `imshow(..., aspect="auto")`.
- On the "different widths" warning, give all panels the same width (plain grid, equal columns).

## 2. Base style

Start every figure with the bundled style, copied into the project's `figures/` (§8). In the notebook, which runs from `figures/`:

```python
import tol_colors as tc
from paper import fit_height, mark_value, smooth, darken  # importing paper registers the bundled Inter font
plt.style.use("paper.mplstyle")
```

It needs `tol-colors` (Python 3.10+). If it is missing, tell the user and ask before installing it.

| The style sets | |
|---|---|
| Text | Inter for all text and math; titles 9 pt, ticks 7 pt, everything else 8 pt |
| Axes | left and bottom spines, black, 0.75 pt; ticks 0.75 pt, 3 pt long (minor 2 pt) |
| Grid | horizontal, #DDDDDD, 0.75 pt, behind the data |
| Lines, markers | lines 1.25 pt; hollow markers, size 4 |
| Color | Paul Tol `bright` cycle, `tol.iridescent` colormap |
| Layout | constrained layout, 0.16 in between panels side by side, 0.08 in stacked |
| Output | 300 dpi; `pdf.fonttype: 42` (text stays text, Inter embedded) |

- Keep these values as they are; the style is tuned for print.
- Name panels with axes titles: in reading order, prefix each with its letter, `"(a) Accuracy on AIME"`, `"(b) …"`. A single panel has no title unless it needs one (dataset, setting). The figure itself has no title; the caption names it.
- Keep matplotlib's default axis limits and margins; `fit_height` makes room for value labels (§1, Height).
- Category axes (bar charts, text tick labels): hide the tick marks on that axis with `ax.tick_params(axis="x", length=0)` (`axis="y"` for horizontal bars), on every panel.

## 3. Lines and text

### Lines

- Curves are plain lines; add markers (the style's hollow markers) only when the user asks.
- Training statistics logged during training (loss, reward, entropy, response length, probabilities): draw the raw values in the series color at `alpha=0.25` without a label, then `smooth(values)` on top with the label, and add to the caption: "smoothed with a moving average over 5% of the steps; faint lines show raw values".
- Evaluation results (accuracy, scores on a benchmark) are drawn raw.
- Reference lines (a baseline's score, a threshold): `ax.axhline(..., linestyle="--", linewidth=1, zorder=1)` in #BBBBBB, fully opaque. Compared values get their lines from `mark_value` (§3, Value labels).

### Value labels

Evaluation results (accuracy, benchmark scores) are the numbers a paper claims, so when the takeaway compares them across series, write them on the plot so the reader can read them exactly. Training statistics (loss, reward, entropy, length, probabilities) show trends, which the curves already show; their panels carry no marks.

- Find the point where the paper makes the comparison: the claim decides it. "Ours reaches higher accuracy" compares each run's best; "ours ends higher" compares final values; "ours is ahead at the same budget" compares values at that shared step. When runs end at different steps, "ends higher" compares values at the last step they share. The value is the plotted metric at that point.
- Mark each value there with `mark_value(ax, x, y, "0.438", color)`: a 1 pt dashed line in `darken(color)` across the whole panel at that value, under the curves; a circle on the point; and the value in bold just above it. One per compared series, in the panels the takeaway is about. The lines let the reader compare heights anywhere in the panel.
- If a label above the point covers a curve, put it below with `below=True`.
- When the user names one headline value, mark it with `star=True` (a filled star).
- Bar charts: label every bar with `ax.bar_label(bars, fontweight="bold")`.

### Other text

- Text that belongs to one series (labels, annotations) uses `darken(series_color)`. Titles, axis labels, ticks and legend text are black.

## 4. Plot type

| Plot type | Frame | Gridlines | Other |
|---|---|---|---|
| Line | Base | Horizontal | – |
| Vertical bar, histogram | Base | Horizontal | `linewidth=0` |
| Horizontal bar | Base | Vertical | `linewidth=0` |
| Scatter | Full | Horizontal | `edgecolors="none"`, `alpha=0.5` |
| Embedding (t-SNE, UMAP) | Full | None | ticks hidden; markers as scatter |
| Heatmap, confusion matrix | Full | None | tick marks hidden; cell text `"white" if np.dot(im.cmap(im.norm(v))[:3], [0.299, 0.587, 0.114]) < 0.5 else "black"` |

- Bar charts: name the bars on the x-axis. For several groups (benchmarks, datasets), use one panel per group, titled with the group.

## 5. Color

Paul Tol's color-blind-safe schemes from `tol_colors` (`tc`): colors by name from a set (`cset = tc.colorsets["bright"]`, then `cset.red`), colormaps by `cmap="tol.<name>"`.

| Set | Colors (in order) | Use |
|---|---|---|
| `bright` | blue, red, green, yellow, cyan, purple, grey | default |
| `vibrant` | orange, blue, cyan, magenta, red, teal, grey | when the user prefers it |
| `muted` | rose, indigo, sand, green, cyan, wine, teal, olive, purple | 7–9 series |
| `high_contrast` | blue, yellow, red | ≤ 3 series that must survive grayscale printing |
| `medium_contrast` | light/dark blue, yellow, red | paired series, e.g. train/test per method |

| Case | Color |
|---|---|
| Single series | the set's first color (`bright`: blue) |
| Categorical | the set's colors in the order above |
| "Ours" (the proposed method among baselines or ablations) | the set's red (`muted`: rose); the others take the rest in order. Without such a series, use the categorical order. |
| Neutral, baselines, reference lines | `tc.colorsets["bright"].grey` (#BBBBBB) |
| Grouped (sizes, sweeps) | one set color per group; within a group blend with white at 40 / 70 / 100 %, light → dark |
| Sequential | `tol.iridescent`; also `tol.YlOrBr`, `tol.WhOrBr`, `tol.incandescent` |
| Signed | `tol.sunset` centered at 0 (symmetric `vmin`/`vmax`); also `tol.BuRd`, `tol.PRGn` |

- One set per figure, the same set across the paper.
- Few levels (e.g. a 5-step heatmap): the `_discrete` map (`tol.sunset_discrete`).
- Grey lines, series and bands are #BBBBBB (`tc.colorsets["bright"].grey`) at full opacity; grey text is `darken("#BBBBBB")`.
- Series that color alone can't separate (grayscale, many series): also vary line style.
- Series are told apart by color, solid fills.
- Emphasis, when the user names a series to emphasize: that series is the set's red, every other series #BBBBBB (bands and markers too), told apart by line style.
- Custom colors (hex codes, a brand palette, "match the original"): use them for the data series, defined once in the setup cell as a dict (`PALETTE = {"ours": "#5F16A7", "base": "#63C9D2"}`); everything else keeps the style. If some are very light (cyan, yellow), tell the user they read weakly on white.

## 6. Legend

| Case | Legend |
|---|---|
| Single panel | inside, at an explicit `loc` where it covers no data |
| Panels with the same series | one `fig.legend(loc="outside upper center", ncol=<entries>, frameon=False, borderaxespad=0)` above the panels |
| Panels with different series | one per panel above its title: `ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=2, frameon=False)` |
| Grouped series | rows = groups, columns = variants |
| One series per panel | none; the title names it |

## 7. Save and caption

- Save `{id}.pdf` and `{id}.png` (kebab-case id) into `figures/` with relative paths. The style embeds fonts as TrueType, which venues accept; keep text as text.
- LaTeX line for the reply: single column → `figure`, `width=\columnwidth`; 1.5 column → `figure*`, `width=0.75\textwidth`; double → `figure*`, `width=\textwidth`.

The caption is written as it appears under the figure in the paper, in the paper's language (default English), and stands alone:

| Part | Content |
|---|---|
| Lead (bold) | what the figure shows, one short sentence |
| Reading guide | encodings the axes and legend don't explain: bands (±1 std over N seeds), dashed lines, panels by letter, log scale |
| Takeaway | the takeaway from step 1, with its number |

- One sentence per part (skip the reading guide when there is nothing to explain), present tense, plain text with Unicode (±, ×, α).
- Unknown details become `[TODO: …]` and go in the reply.

> **Figure 1: Test accuracy versus training steps on CIFAR-10.** Shaded bands show ±1 std over 3 seeds; the dashed line marks the best baseline's final accuracy. Ours reaches it after 12k steps, 2.1× faster.

## 8. Notebook (required)

All figure work happens in `figures/` at the root of the user's project, even for one figure or a script-only request. The user runs, edits and re-exports figures there, without this skill, so each cell is plain, readable code.

```
figures/
├── paper.py, paper.mplstyle, Inter-*.ttf, Inter-LICENSE.txt   # copied from {skill-dir}/assets/
├── figures.ipynb
└── {id}.pdf, {id}.png
```

- `{skill-dir}` is this skill's base directory. Copy with `cp -n {skill-dir}/assets/{paper.py,paper.mplstyle,Inter-*} figures/`, which keeps copies already there. The notebook uses only these copies.

| Cell | Content |
|---|---|
| First (code, once) | `%matplotlib inline`, `%config InlineBackend.print_figure_kwargs = {"bbox_inches": None}`, `%config InlineBackend.figure_formats = ["retina"]`, imports, the §2 setup |
| Per figure (markdown) | `## {id}`, then the caption |
| Per figure (code) | everything for that figure: load data, plot, `fit_height`, save PDF + PNG, `plt.show()` |

- Each figure cell runs on its own after the setup cell.
- Load data from the project's result files (paths relative to `figures/`); write numbers inline only when there is no file.
- The same `id` replaces its two cells; a new id appends two cells. Edit with `NotebookEdit`; create the notebook with `Write`.
- Run it with the project's Python: `jupyter nbconvert --to notebook --execute --inplace figures/figures.ipynb`. If jupyter is missing, tell the user and ask before installing it.
- **Reply**: changes, LaTeX line, any `[TODO]`.

## 9. Check

After the notebook has run, look at each PNG and fix and re-run until all hold:

- Width equals the target; `fit_height` gave no warning.
- Every panel passes the grid check (§1).
- All text is Inter, shown in full, and overlaps no other text, curve or legend.
- Value marks sit on evaluation results, at the points where the takeaway makes its comparison.
- Colors follow §5.
- PDF fonts are embedded TrueType: `pdffonts {id}.pdf` shows `CID TrueType`, emb `yes` (without pdffonts: `grep -ac /Type3 {id}.pdf` prints 0).
- The caption matches the figure.
