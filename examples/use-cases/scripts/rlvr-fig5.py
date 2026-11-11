"""Figure 5: Per-problem accuracy of Qwen2.5-7B on Minerva (272 problems), base model vs. its RLVR-
trained version. Bars count the problems whose accuracy falls in each interval; 0.0 and 1.0 are bins
of their own. RLVR raises the number of problems solved every time from 3 to 47 and lowers low
accuracies ((0.0, 0.1]: 52 → 33), but also raises the number never solved from 93 to 113.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig5.json") as f:
    data = json.load(f)

x = np.arange(len(data["bins"]))
width = 0.8 / 2
fig, ax = plt.subplots(figsize=(5.5, 2))
for i, (name, color) in enumerate([("Base", colors["series-1"]), ("RL", colors["series-2"])]):
    bars = ax.bar(x + (i - 0.5) * width, data[name], width, color=color, linewidth=0, label=name)
    ax.bar_label(bars, fmt="%d", color=darken(color))

ax.set_xticks(x, labels=data["bins"], rotation=45, ha="right", rotation_mode="anchor")
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Accuracy")
ax.set_ylabel("Number of problems")
ax.legend(loc="upper right")
fit_height(fig, ax, aspect=0.382)
fig.savefig("../outputs/rlvr-fig5.pdf")
fig.savefig("../outputs/rlvr-fig5.png")
