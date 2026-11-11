"""GLUE accuracy of five fine-tuning methods. Points mark the mean and error bars show ±1 std over 5 seeds; the vertical line marks the best baseline's mean. Ours reaches 0.879, 0.014 above the best baseline, full fine-tuning (0.865)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/error-bar-plot.json") as f:
    runs = json.load(f)["accuracy_per_seed"]

mean = {name: np.mean(acc) for name, acc in runs.items()}
std = {name: np.std(acc, ddof=1) for name, acc in runs.items()}
methods = sorted(runs, key=lambda name: mean[name])  # ascending top to bottom, so Ours ends at the bottom
best_baseline = max((name for name in methods if name != "Ours"), key=lambda name: mean[name])
gap = float(f"{mean['Ours']:#.3g}") - float(f"{mean[best_baseline]:#.3g}")
print("takeaway:", {name: f"{mean[name]:#.3g} ± {std[name]:.4f}" for name in methods},
      "best baseline:", best_baseline, "gap:", f"{gap:.3f}", "seeds:", len(runs["Ours"]))
assert mean["Ours"] > mean[best_baseline], "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for y, name in enumerate(methods):
    color = colors["ours"] if name == "Ours" else colors["neutral"]
    ax.errorbar(mean[name], y, xerr=std[name], fmt="o", color=color, capsize=2,
                elinewidth=rcParams["patch.linewidth"], capthick=rcParams["patch.linewidth"])
    ax.annotate(f"{mean[name]:#.3g}", (mean[name] + std[name], y), xytext=(3, 0), textcoords="offset points",
                ha="left", va="center", color=darken(color), gid="value-label")
ax.axvline(mean[best_baseline], color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)

ax.set_yticks(range(len(methods)), labels=methods)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlabel("GLUE accuracy")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/error-bar-plot.pdf")
fig.savefig("../outputs/error-bar-plot.png")
