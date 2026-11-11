"""Figure 5: Per-problem accuracy of Qwen2.5-7B on Minerva (272 problems) before and after RLVR. RLVR raises the number of problems solved every time from 3 to 47 and lowers the counts at low accuracies (52 to 33 in (0.0, 0.1]), but it also raises the number of problems never solved from 93 to 113."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/rlvr-fig5.json"))
bins = data["bins"]

fig, ax = plt.subplots(figsize=(5.5, 2))
x = np.arange(len(bins))
width = 0.8 / 2
for i, (name, color) in enumerate([("Base", colors["series-1"]), ("RL", colors["series-2"])]):
    counts = data[name]
    bars = ax.bar(x + (i - 0.5) * width, counts, width, color=color, linewidth=0, label=name)
    ax.bar_label(bars, labels=[f"{c}" for c in counts], color=paper.darken(color), rotation=90, padding=2)

ax.set_xticks(x, labels=bins, rotation=45, ha="right", rotation_mode="anchor")
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Accuracy")
ax.set_ylabel("Count")
ax.legend(loc="upper center")

fit_height(fig, ax, aspect=0.382)
fig.savefig("../outputs/rlvr-fig5.pdf")
fig.savefig("../outputs/rlvr-fig5.png")
