"""Figure 5: Distribution of per-problem accuracy on Minerva for the base model and its RL-trained version. RL pushes problems to the extremes: problems always solved grow from 3 to 47, but problems never solved also grow, from 93 to 113."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig5.json") as f:
    data = json.load(f)

bins = data["bins"]
x = np.arange(len(bins))
width = 0.8 / 2

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")

for i, (name, color) in enumerate([("Base", colors["series-1"]), ("RL", colors["series-2"])]):
    counts = data[name]
    ax.bar(x + (i - 0.5) * width, counts, width, color=color, linewidth=0, label=name)

ax.set_xticks(x, labels=bins, rotation=45, ha="right", rotation_mode="anchor")
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Per-problem accuracy")
ax.set_ylabel("Number of problems")
ax.legend(loc="upper center")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/rlvr-fig5.pdf")
fig.savefig("../outputs/rlvr-fig5.png")
