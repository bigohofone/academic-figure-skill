---
name: academic-figure
description: Makes publication-ready figures for academic papers with matplotlib or seaborn, following a DESIGN.md design system (venue widths, print-size type, color-blind-safe colors, chart-type rules) - one script per figure with a paper-style caption. Use it when creating or editing a figure, plot or chart meant for a paper (ICML, CVPR, ACL, NeurIPS, ICLR or any paper), even if only the plotting code is asked for. Not for quick exploratory plots, notebooks, dashboards or slides.
---

# Paper Figures

Goal: figure that reads well printed, one message at a glance. `DESIGN.md`: how figures look (tokens, rules). This file: workflow. Every rule applies unless the user says otherwise. Done: script with caption in the figures folder, runs without warnings.

## Steps

1. Set up the figures folder (Files); read its `DESIGN.md` once (the project's copy is the design; user may have changed it).
2. Takeaway: one sentence on what the figure shows (from request, paper text, figure's role), with a number from the data if any. Decides value labels; becomes the caption's takeaway.
3. Kind of data: each plotted quantity is a reported result or a diagnostic (below).
4. Chart type: from DESIGN.md's chart type table; read its file in `{skill-dir}/references/`, one per type used. Several panels, sub-figures or a second y axis: also `references/multi-panel.md`.
5. Draw by DESIGN.md and the chart files.
6. Save, caption, check.

## How to work

Few turns, each finishing a step. Typical figure: 5-6 turns.

1. First turn, all at once: setup commands, a printout of the data's structure, and Read of `figures/DESIGN.md` and the chart files. The files to read are named above; don't list or explore the skill folder, don't read the `paper` code.
2. Read each file whole with the Read tool, once. Not `cat`: long output gets cut, then read twice.
3. Data: one Python call printing the takeaway's numbers.
4. Write the whole script once, rules applied up front. Leave placement to `finalize_figure`: panel legends without `loc`, bar values level (it turns crowded ones upward).
5. Run the script and the font check in one command.
6. Warnings: fix all of them in one edit, then rerun. No trial loops over placements, no temp scripts.
7. Look at the PNG once, at the end.

## Kind of data

| Kind | What | On the plot |
|---|---|---|
| Reported result | number the paper claims, once per setting (accuracy, F1, latency) | value written when the takeaway compares it |
| Diagnostic | quantity logged along a process (loss, gradient norm, entropy per step) | trend and shape; no value labels |

Metric logged along training (validation accuracy per epoch): reported result at the compared point, diagnostic elsewhere.

## Files

One folder for all work: the one the user names, else `figures/` in the working directory. User reruns and edits scripts there without this skill: plain, readable code.

```
figures/
├── {id}.py      # one script per figure, caption as docstring
├── DESIGN.md    # the design; edit to restyle every figure
├── style/paper/ # helpers, style, fonts (copied from the skill)
└── outputs/     # {id}.pdf, {id}.png
```

- Setup (`{skill-dir}`: this skill's base directory; `-n` keeps a design the user changed):

  ```bash
  mkdir -p figures/style figures/outputs
  cp -n {skill-dir}/assets/DESIGN.md figures/
  cp -Rn {skill-dir}/assets/paper figures/style/
  ```

- Requirements: Python 3.10+, matplotlib 3.10+, numpy 2+, pyyaml; scipy for density curves. Missing one: ask before installing.
- Script `figures/{id}.py` (kebab-case id), self-contained: caption docstring, setup, data, plot, `finalize_figure`, save.

  ```python
  """Test accuracy versus training steps on CIFAR-10. Shaded bands show ±1 std over 3 seeds; ..."""

  import json
  import sys

  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib import rcParams

  sys.path.insert(0, "style")
  import paper
  from paper import finalize_figure, baseline_greys, darken

  colors = paper.apply_design("DESIGN.md")  # colors["series-1"], colors["ours"], ...
  ```

- Helpers in `paper`:

  | Helper | Use |
  |---|---|
  | `apply_design(path)` | style from DESIGN.md; returns colors by name |
  | `finalize_figure(fig, axes, aspect=0.618, min_width=0.9, column_gap=0)` | call last: height, layout, warnings |
  | `set_group_label(axes, text, axis="x")` | one axis label for a group of panels |
  | `baseline_greys(n)` | grey fills for n compared series |
  | `part_colors(n)` | colors for parts of one whole |
  | `ramp(color, n)` | n shades of one hue, light to dark, for a sweep (depths, sizes) |
  | `darken(color)` / `lighten(color)` | series text and edges / box and violin fills |
  | `text_color_on(fill)` | black or white, whichever reads on the fill |
  | `moving_average(values)` | smooth a logged curve |
  | `mark_value(ax, x, y, text, color, below=False)` | circle and write a compared value |
  | `paper.dashed_width`, `highlight_size`, `filled_edge_width`, `bar_label_size`, `contour_label_size` | token values |

- Data: from the project's result files (paths relative to `figures/`, e.g. `../results/run.json`); inline numbers only when no file.
- Numbers: every number on plot and caption computed from loaded data; every given point drawn. Script prints the takeaway's numbers and asserts the claim; caption written from that printout, in DESIGN.md value formats. Data doesn't support the claim: tell the user, don't draw around it.

  ```python
  best = {name: max(curve) for name, curve in runs.items()}
  print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()})
  assert best["Ours"] > max(v for name, v in best.items() if name != "Ours"), "the takeaway does not hold"
  ```

- Code style: top to bottom, as written by hand; plain matplotlib calls; data and labels where used. Abstraction: at most a loop over series.
- Run from the figures folder with the project's Python:

  ```bash
  cd figures && python {id}.py
  ```

## Save and caption

- Save:

  ```python
  fig.savefig("outputs/{id}.pdf")
  fig.savefig("outputs/{id}.png")
  ```

- LaTeX line for the reply:

  | Venue | Width | LaTeX |
  |---|---|---|
  | Single-column (ICLR, NeurIPS) | full / half | `figure`, `width=\textwidth` / `width=0.5\textwidth` |
  | Two-column | single column | `figure`, `width=\columnwidth` |
  | Two-column | 1.5 column | `figure*`, `width=0.75\textwidth` |
  | Two-column | double | `figure*`, `width=\textwidth` |

- Caption: text of `\caption{}`; paper's language (default English); stands alone; one sentence per part; present tense; plain text with Unicode (±, ×, α). Unknown details: `[TODO: …]`, listed in the reply.

  | Part | Content |
  |---|---|
  | Lead (bold in the paper) | what the figure shows, one short sentence |
  | Reading guide | what axes and legend don't explain: bands, dashed lines, outlines, sub-figure letters, log axes; skip if none |
  | Takeaway | step 2's takeaway with its number |

  > Test accuracy versus training steps on CIFAR-10. Shaded bands show ±1 std over 3 seeds; the dashed line marks the best baseline's final accuracy. Ours reaches it after 12k steps, 2.1× faster.

- Reply: what changed, LaTeX line, any `[TODO]`.

## Check

After each run:

1. Warnings: each `finalize_figure` warning names the problem; fix by DESIGN.md until clean.
2. Numbers: caption matches the printed takeaway exactly; assert passed. Derived numbers (ECE, AUC): named as computed in the caption.
3. Look at the PNG at printed size (pixel width / 300 in), not zoomed: takeaway at a glance; value labels at compared points; legend order and colors per DESIGN.md; chart file followed; caption matches.
4. Fonts embedded as TrueType: `pdffonts` shows `CID TrueType`, emb `yes`; without pdffonts, the `grep` prints 0.

   ```bash
   pdffonts outputs/{id}.pdf
   grep -ac /Type3 outputs/{id}.pdf
   ```
