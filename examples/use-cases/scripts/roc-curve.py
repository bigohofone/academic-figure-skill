"""Figure [TODO: number]: ROC curves of AI-text detectors. W/ P and W/o P are our detector with and without the golden prompt; the dashed grey diagonal marks chance, and AUC is computed from each curve with the trapezoidal rule. Ours with the golden prompt reaches an AUC of 0.987, against 0.905 without it and 0.647 for GPTZero, the best baseline."""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import Normalize, to_rgb
from matplotlib.patches import Patch
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")  # the style from DESIGN.md's tokens; colors["series-1"], colors["ours"], …

with open("../data/roc-curve.json") as f:
    methods = {m["name"]: m for m in json.load(f)["methods"]}

# ICLR, one panel: half the text width
fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")

# variants of ours in the ours color (full method solid, reduced variant dashed);
# the baselines grey, told apart by line style in ascending order of AUC
series = [
    ("Ours: W/ P", "Ours W/ P", colors["ours"], "-", "o"),
    ("Ours: W/o P", "Ours W/o P", colors["ours"], "--", "s"),
    ("OpenAI", "OpenAI", colors["neutral"], "-", "^"),
    ("GPTZero", "GPTZero", colors["neutral"], "--", "D"),
]
for key, name, color, style, marker in series:
    fpr, tpr = np.array(methods[key]["fpr"]), np.array(methods[key]["tpr"])
    auc = np.trapezoid(tpr, fpr)
    width = rcParams["lines.linewidth"] if style == "-" else paper.dashed_width
    ax.plot(fpr, tpr, linestyle=style, linewidth=width, marker=marker, markevery=max(1, len(fpr) // 10),
            color=color, label=f"{name} (AUC {auc:#.3g})")

ax.axline((0, 0), (1, 1), linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.10g}")
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}")
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.grid(True)
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/roc-curve.pdf")
fig.savefig("../outputs/roc-curve.png")
