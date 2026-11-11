"""Distribution of per-problem accuracy on Minerva for the base and RL-trained models. RL pushes problems to the extremes: the number solved in every sample rises from 3 to 47, and the number never solved from 93 to 113."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig5.json") as f:
    data = json.load(f)
bins = data["bins"]
counts = {"Base": data["Base"], "RL": data["RL"]}

print("takeaway:", {name: {"0.0": f"{c[0]}", "1.0": f"{c[-1]}"} for name, c in counts.items()})
assert counts["RL"][-1] > counts["Base"][-1] and counts["RL"][0] > counts["Base"][0], "the takeaway does not hold"

x = np.arange(len(bins))
width = 0.8 / 2
fig, ax = plt.subplots(figsize=(5.5, 5.5))
for i, (name, color) in enumerate([("Base", colors["neutral"]), ("RL", colors["ours"])]):
    bars = ax.bar(x + (i - 0.5) * width, counts[name], width, color=color, linewidth=0, label=name)
    ax.bar_label(bars, labels=[f"{round(v)}" for v in counts[name]], color=darken(color))

ax.set_xticks(x, labels=bins, rotation=45, ha="right", rotation_mode="anchor")
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Per-problem accuracy")
ax.set_ylabel("Problems")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.382)
fig.savefig("../outputs/rlvr-fig5.pdf")
fig.savefig("../outputs/rlvr-fig5.png")
