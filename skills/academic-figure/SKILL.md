---
name: academic-figure
description: Makes publication-ready figures for academic papers with matplotlib or seaborn, following a DESIGN.md design system (print sizes, typography, color-blind-safe colors, chart-type rules for line, bar, scatter, box, heatmap, histogram, error bar, area, contour, radar, pie and violin charts) - delivered as one script per figure, `{id}.py` in the folder the user names or else `figures/`, with a paper-style caption. Use it whenever creating or editing any figure, plot, graph, chart, heatmap or visualization for a paper, even if no venue (ICML, CVPR, ACL, NeurIPS, ICLR) is mentioned and even if the user asks only for the plotting code.
---

# Paper Figures

Goal: a figure that reads well printed in the paper, where the reader gets its one message at a glance. How figures look is set by the design system, `DESIGN.md`: its tokens (colors, type sizes, line widths) and its rules (layout, legends, chart types). This file is the workflow. Apply every rule unless the user says otherwise. A figure is delivered when its script, with its caption, is in the figures folder and has run without warnings.

## Steps

1. **Set up** the figures folder (Files), then read its `DESIGN.md`: the project's copy is the design, and the user may have changed it.
2. **Takeaway**: work out what the paper uses this figure to show (the user's request, the paper text or caption, the figure's role), then write it as one sentence with a number from the data. It decides the value labels and becomes the caption's takeaway.
3. **Kind of data**: decide for every plotted quantity whether it is a reported result or a diagnostic (below).
4. **Chart type**: pick it from DESIGN.md's Components table and read its file (`{skill-dir}/line-chart.md`, …), every one the figure uses.
5. **Draw** by DESIGN.md (width, grid, aspect, colors, legend, value labels) and the chart type's file.
6. **Save and caption**, then **check**.

## Kind of data

| Kind | What it is | On the plot |
|---|---|---|
| Reported result | a number the paper claims, measured once per setting (accuracy, F1, latency, a score per method) | when the takeaway compares it, its value is written on the plot |
| Diagnostic | a quantity logged along a process to show its behavior (loss, gradient norm, entropy per step) | its trend and shape; no value labels |

## Files

All figure work happens in one folder, even for one figure or a code-only request: the folder the user names ("put it in `paper/plots/`"), else `figures/` in the current working directory. Below, `figures/` stands for that folder. The user runs, edits and re-exports figures there without this skill, so each script is plain, readable code.

```
figures/
├── {id}.py           # one script per figure, its caption on top
├── DESIGN.md         # the design system; edit it to restyle every figure
├── style/            # paper.py, paper.mplstyle, Inter fonts, copied from the skill; not edited by hand
└── outputs/          # {id}.pdf and {id}.png
```

- **Setup**: `{skill-dir}` is this skill's base directory. `mkdir -p figures/style figures/outputs`, `cp -n {skill-dir}/assets/DESIGN.md figures/`, `cp -n {skill-dir}/assets/{paper.py,paper.mplstyle,Inter-*} figures/style/`; `-n` keeps copies already there, so a design the user changed stays.
- **Requirements**: Python 3.10+, `matplotlib` 3.10+, `numpy` 2+, `pyyaml`, and `scipy` for density curves. If one is missing, tell the user and ask before installing it.
- **Script**: `figures/{id}.py` (kebab-case id) runs on its own: the caption as its docstring, the setup below, then everything for that figure: load data, plot, `fit_height`, save PDF and PNG.

  ```python
  """Figure 1: Test accuracy versus training steps on CIFAR-10. Shaded bands show ±1 std over 3 seeds; ..."""

  import json
  import math
  import sys

  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib import rcParams
  from matplotlib.colors import ListedColormap, Normalize, to_rgb
  from matplotlib.patches import Patch
  from matplotlib.ticker import NullFormatter

  sys.path.insert(0, "style")
  import paper  # registers the bundled Inter font
  from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

  colors = paper.use_design("DESIGN.md")  # the style from DESIGN.md's tokens; colors["series-1"], colors["ours"], …
  ```

- **Data**: loaded from the project's result files (paths relative to `figures/`); numbers inline only when there is no file.
- **Code style**: top to bottom as a person would write it by hand: plain matplotlib calls, data and labels spelled out where they are used, the `paper` helpers for the rest; a loop over the plotted series is as far as abstraction goes.
- **Run**: from the figures folder with the project's Python, `cd figures && python {id}.py`.

## Save and caption

- **Files**: `fig.savefig("outputs/{id}.pdf")` and `fig.savefig("outputs/{id}.png")`. The design embeds fonts as TrueType, which venues accept; text stays text.
- **LaTeX line** for the reply: single-column venue (ICLR, NeurIPS): `figure`, `width=\textwidth` at full width, `width=0.5\textwidth` at half; two-column venue: single column `figure`, `width=\columnwidth`; 1.5 column `figure*`, `width=0.75\textwidth`; double `figure*`, `width=\textwidth`.
- **Caption**: as it appears under the figure in the paper, in the paper's language (default English), standing alone; one sentence per part, present tense, plain text with Unicode (±, ×, α); unknown details become `[TODO: …]` and go in the reply.

  | Part | Content |
  |---|---|
  | Lead (bold in the paper) | what the figure shows, one short sentence |
  | Reading guide | what the axes and legend don't explain: bands, dashed lines, outlines, sub-figure letters, log axes (skip when there is nothing) |
  | Takeaway | the takeaway from step 2, with its number, written by DESIGN.md's value table |

  > **Figure 1: Test accuracy versus training steps on CIFAR-10.** Shaded bands show ±1 std over 3 seeds; the dashed line marks the best baseline's final accuracy. Ours reaches it after 12k steps, 2.1× faster.

- **Reply**: what changed, the LaTeX line, any `[TODO]`.

## Check

After each script has run:

1. **Warnings**: read its output. `fit_height` warns about a panel narrower than `min_width`; text cut off, overlapping, sticking out of its panel or spilling out of its fill; a value label, point name or legend covering a curve or data points; a legend over text or with more than a tenth of its area over filled marks; a font other than the design's. Each rule says what to do on its warning; fix the script until it runs without warnings.
2. **Look** at the PNG for what code can't see: the takeaway reads at a glance; value marks sit on reported results at the comparison points; legend entries follow DESIGN.md's order; colors follow its roles; the chart type's file is followed; the caption matches the figure.
3. **Fonts**: embedded TrueType: `pdffonts outputs/{id}.pdf` shows `CID TrueType`, emb `yes` (without pdffonts: `grep -ac /Type3 outputs/{id}.pdf` prints 0).
