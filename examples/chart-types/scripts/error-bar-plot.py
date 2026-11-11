"""GLUE accuracy of five fine-tuning methods. Error bars show ±1 std over 5 seeds; the vertical line marks the best baseline, full fine-tuning, at 0.865. Ours reaches 0.879, 0.014 above it."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, darken

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/error-bar-plot.json") as f:
    runs = json.load(f)["accuracy_per_seed"]

means = {name: float(np.mean(v)) for name, v in runs.items()}
stds = {name: float(np.std(v, ddof=1)) for name, v in runs.items()}
names = sorted(runs, key=lambda name: means[name])  # ascending top to bottom, ours ends at the bottom
best_baseline = max((n for n in names if n != "Ours"), key=lambda n: means[n])
gap = round(means["Ours"], 3) - round(means[best_baseline], 3)
print("takeaway:", {n: f"{means[n]:#.3g}" for n in names}, "best baseline:", best_baseline, f"gap: {gap:.3f}")
assert names[-1] == "Ours", "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.axvline(means[best_baseline], color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
for y, name in enumerate(names):
    color = colors["ours"] if name == "Ours" else colors["neutral"]
    ax.errorbar(means[name], y, xerr=stds[name], fmt="o", color=color, capsize=2,
                elinewidth=rcParams["patch.linewidth"], capthick=rcParams["patch.linewidth"])
    ax.annotate(f"{means[name]:#.3g}", (means[name] + stds[name], y), xytext=(3, 0), textcoords="offset points",
                ha="left", va="center", color=darken(color), gid="value-label")
ax.set_yticks(range(len(names)), labels=names)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlabel("GLUE accuracy")

finalize_figure(fig, ax, aspect=0.618)
fig.savefig("../outputs/error-bar-plot.pdf")
fig.savefig("../outputs/error-bar-plot.png")
