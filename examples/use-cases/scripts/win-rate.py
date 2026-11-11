"""Figure 1: Human preference of LIMA against five baselines on 300 test prompts. Each bar splits the prompts into LIMA wins, ties and LIMA losses. LIMA wins or ties on 74% of prompts against Alpaca 65B, and still on 43% against GPT-4 (April)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/win-rate.json") as f:
    data = json.load(f)
opponents = data["opponents"]  # the fixed order from the paper

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
y = np.arange(len(opponents))
left = np.zeros(len(opponents))
for category, color in zip(data["categories"], [colors["ours"], *greys(2)]):
    shares = np.array(data[category]) / 100
    bars = ax.barh(y, shares, left=left, color=color, edgecolor="white", linewidth=plt.rcParams["grid.linewidth"],
                   label=category)
    ax.bar_label(bars, labels=[f"{v:.0%}" for v in shares], label_type="center", color=text_color(color))
    left += shares

ax.set_yticks(y, labels=opponents)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Share of 300 test prompts")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=3, frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/win-rate.pdf")
fig.savefig("../outputs/win-rate.png")
