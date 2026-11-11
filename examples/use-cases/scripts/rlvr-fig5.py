"""Distribution of per-problem accuracy on Minerva for the base and RL models. After RL, 47 problems are always solved, against 3 for the base model, and 113 are never solved, against 93.
"""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import darken, fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig5.json") as f:
    data = json.load(f)
bins = data["bins"]
base, rl = data["Base"], data["RL"]

print("takeaway:", f"accuracy 1.0: Base {base[-1]}, RL {rl[-1]}; accuracy 0.0: Base {base[0]}, RL {rl[0]}")
assert rl[-1] > base[-1] and rl[0] > base[0], "the takeaway does not hold"

x = np.arange(len(bins))
width = 0.8 / 2
fig, ax = plt.subplots(figsize=(5.5, 5.5), layout="constrained")
for i, (name, counts, color) in enumerate((("Base", base, colors["neutral"]), ("RL", rl, colors["ours"]))):
    bars = ax.bar(x + (i - 0.5) * width, counts, width, color=color, linewidth=0, label=name)
    ax.bar_label(bars, labels=[f"{round(v)}" for v in counts], color=darken(color))

ax.grid(axis="x", visible=False)
ax.tick_params(axis="x", length=0)
ax.set_xticks(x, labels=bins, rotation=45, ha="right", rotation_mode="anchor")
ax.set_xlabel("Per-problem accuracy")
ax.set_ylabel("Number of problems")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.382)
fig.savefig("../outputs/rlvr-fig5.pdf")
fig.savefig("../outputs/rlvr-fig5.png")
