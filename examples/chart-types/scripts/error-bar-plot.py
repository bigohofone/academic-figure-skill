"""Figure 1: GLUE accuracy of five fine-tuning methods. Error bars show ±1 std over 5 seeds. Ours reaches 0.879, 0.0138 above full fine-tuning (0.865), about three times the seed std of either (≤0.0046)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, lighten, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

runs = json.load(open("../data/error-bar-plot.json"))["accuracy_per_seed"]
methods = sorted(runs, key=lambda m: np.mean(runs[m]))

fig, ax = plt.subplots(figsize=(2.75, 2))
for x, method in enumerate(methods):
    color = colors["ours"] if method == "Ours" else colors["neutral"]
    mean, err = np.mean(runs[method]), np.std(runs[method], ddof=1)
    ax.errorbar(x, mean, yerr=err, fmt="o", color=color, capsize=2,
                elinewidth=rcParams["patch.linewidth"], capthick=rcParams["patch.linewidth"])
    ax.annotate(f"{mean:#.3g}", (x, mean + err), xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", color=darken(color), gid="value-label")
ax.set_xticks(range(len(methods)), labels=methods)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("GLUE accuracy")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/error-bar-plot.pdf")
fig.savefig("../outputs/error-bar-plot.png")
