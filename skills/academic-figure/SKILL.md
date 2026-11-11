---
name: academic-figure
description: Makes publication-ready figures for academic papers with matplotlib or seaborn, following a DESIGN.md design system (print sizes, typography, color-blind-safe colors, chart-type rules for line, bar, scatter, box, heatmap, histogram, error bar, area, contour, radar, pie and violin charts) - delivered as cells in `figures/figures.ipynb` in the user's project, with a paper-style caption. Use it whenever creating or editing any figure, plot, graph, chart, heatmap or visualization for a paper, even if no venue (ICML, CVPR, ACL, NeurIPS, ICLR) is mentioned and even if the user asks only for the plotting code.
---

# Paper Figures

Goal: a figure that reads well printed in the paper, where the reader gets its one message at a glance. How figures look is set by the design system, `DESIGN.md`: its tokens (colors, type sizes, line widths) and its rules (layout, legends, chart types). This file is the workflow. Apply every rule unless the user says otherwise. A figure is delivered when its cell is in the notebook with its caption and has run.

Steps, in order:

1. **Set up** `figures/` (Notebook below), then read `figures/DESIGN.md`: the project's copy is the design, and the user may have changed it.
2. **Takeaway**: work out what the paper uses this figure to show (from the user's request, the paper text or caption, the figure's role), then write it as one sentence with a number from the data. It decides the value labels and becomes the caption's takeaway.
3. **Chart type**: pick it from DESIGN.md's Components table and read its file (`{skill-dir}/line-chart.md`, …), every one the figure uses.
4. **Draw** by DESIGN.md: width, grid, aspect and height (Layout), colors, legend, value labels, and the chart type's file.
5. **Save, caption, notebook**, then **check**.

## What is plotted

Every plotted quantity is one of two kinds; decide which before drawing:

- **Reported results**: the numbers the paper claims, measured once per setting (accuracy, F1, latency, throughput, error rate, a score per method). Readers compare them exactly, so when the takeaway compares them, their values are written on the plot.
- **Diagnostics**: quantities logged along a process to show its behavior (loss, gradient norm, entropy, temperature, queue length per iteration). Readers read their trend and shape, so they carry no value labels.

## Save and caption

- Save `{id}.pdf` and `{id}.png` (kebab-case id) into `figures/` with relative paths. The design embeds fonts as TrueType, which venues accept; keep text as text.
- LaTeX line for the reply: single column → `figure`, `width=\columnwidth`; 1.5 column → `figure*`, `width=0.75\textwidth`; double → `figure*`, `width=\textwidth`.

The caption is written as it appears under the figure in the paper, in the paper's language (default English), and stands alone:

| Part | Content |
|---|---|
| Lead (bold) | what the figure shows, one short sentence |
| Reading guide | encodings the axes and legend don't explain: bands (±1 std over N seeds), dashed lines, sub-figures by letter, log scale |
| Takeaway | the takeaway from step 2, with its number |

- One sentence per part (skip the reading guide when there is nothing to explain), present tense, plain text with Unicode (±, ×, α).
- Unknown details become `[TODO: …]` and go in the reply.

> **Figure 1: Test accuracy versus training steps on CIFAR-10.** Shaded bands show ±1 std over 3 seeds; the dashed line marks the best baseline's final accuracy. Ours reaches it after 12k steps, 2.1× faster.

## Notebook (required)

All figure work happens in `figures/` at the root of the user's project, even for one figure or a script-only request. The user runs, edits and re-exports figures there, without this skill, so each cell is plain, readable code.

```
figures/
├── DESIGN.md                      # the design system; edit it to change how every figure looks
├── paper.py, paper.mplstyle, Inter-*.ttf, Inter-LICENSE.txt
├── figures.ipynb
└── {id}.pdf, {id}.png
```

- `{skill-dir}` is this skill's base directory. Copy with `cp -n {skill-dir}/assets/{DESIGN.md,paper.py,paper.mplstyle,Inter-*} figures/`, which keeps copies already there, so a design the user changed stays. The notebook uses only these copies.
- It needs `tol-colors` and `pyyaml` (Python 3.10+). If they are missing, tell the user and ask before installing them.

| Cell | Content |
|---|---|
| First (code, once) | `%matplotlib inline`, `%config InlineBackend.print_figure_kwargs = {"bbox_inches": None}`, `%config InlineBackend.figure_formats = ["retina"]`, then the setup below |
| Per figure (markdown) | `## {id}`, then the caption |
| Per figure (code) | everything for that figure: load data, plot, `fit_height`, save PDF + PNG, `plt.show()` |

```python
import json

import matplotlib.pyplot as plt
import numpy as np
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten

colors = paper.use_design()  # the style from DESIGN.md's tokens; colors["series-1"], colors["ours"], …
```

- Each figure cell runs on its own after the setup cell.
- Load data from the project's result files (paths relative to `figures/`); write numbers inline only when there is no file.
- Write the notebook yourself, top to bottom, the way a person would: create `figures/figures.ipynb` with `Write` as an empty notebook, then add each cell with `NotebookEdit` (insert after the last cell), and fix a cell by replacing it with `NotebookEdit`. The same `id` replaces its two cells; a new id appends two cells. If `NotebookEdit` is a deferred tool, load it first.

  ```json
  {"cells": [], "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "nbformat": 4, "nbformat_minor": 5}
  ```

- Write each code cell as a person would write it by hand: top to bottom, plain matplotlib calls, data and labels spelled out where they are used. Use the `paper` helpers and write everything else inline in the cell; a loop over the series being plotted is as far as abstraction goes.
- Run it with the project's Python: `jupyter nbconvert --to notebook --execute --inplace figures/figures.ipynb`. If jupyter is missing, tell the user and ask before installing it.
- **Reply**: changes, LaTeX line, any `[TODO]`.

## Check

After the notebook has run:

1. Read each cell's output. `fit_height` warns about a panel narrower than 1.2 in, text cut off or overlapping (rotated labels included), a value label or legend covering a curve, a legend covering a bar or box, and a font other than the design's. Fix the cell until it runs without warnings.
2. Look at each PNG for what code can't see: the takeaway reads at a glance; value marks sit on reported results at the comparison points; legend entries follow DESIGN.md's order; colors follow its roles; the chart type's file is followed; the caption matches the figure.
3. PDF fonts are embedded TrueType: `pdffonts {id}.pdf` shows `CID TrueType`, emb `yes` (without pdffonts: `grep -ac /Type3 {id}.pdf` prints 0).
