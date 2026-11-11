"""Human preference between LIMA and five baselines on 300 test prompts. Each bar splits the prompts into those where LIMA's response is preferred, both are judged equivalent, or the baseline's is preferred. LIMA wins outright against Alpaca 65B (53%) and DaVinci003 (44%), and even against GPT-4 it wins or ties on 43% of prompts."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/win-rate.json") as f:
    data = json.load(f)
opponents = data["opponents"]
categories = data["categories"]
shares = {c: np.array(data[c]) / 100 for c in categories}
assert np.allclose(sum(shares.values()), 1)

# Takeaway: LIMA beats the weaker baselines outright, and wins or ties against GPT-4 on 43% of prompts.
win, tie, loss = (shares[c] for c in categories)
print("takeaway: wins", {o: f"{w:.0%}" for o, w in zip(opponents, win)},
      "win or tie vs GPT-4:", f"{win[-1] + tie[-1]:.0%}")
assert win[0] > loss[0] and win[1] > loss[1], "the takeaway does not hold"

segment_colors = [colors["ours"], *greys(2)]

fig, ax = plt.subplots(figsize=(2.75, 2.75))
y = np.arange(len(opponents))
left = np.zeros(len(opponents))
for category, color in zip(categories, segment_colors):
    values = shares[category]
    bars = ax.barh(y, values, left=left, color=color, edgecolor="white",
                   linewidth=rcParams["grid.linewidth"], label=category)
    ax.bar_label(bars, labels=[f"{v:.0%}" for v in values], label_type="center", color=text_color(color))
    left += values

ax.set_yticks(y, labels=opponents)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Share of test prompts")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(categories), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/win-rate.pdf")
fig.savefig("../outputs/win-rate.png")
