"""Human preference between LIMA and five baselines on 300 test prompts. Each bar splits the prompts into LIMA wins, ties and LIMA losses. LIMA wins or ties on 74% of prompts against Alpaca 65B and still on 43% against GPT-4."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, greys, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/win-rate.json") as f:
    data = json.load(f)
opponents = data["opponents"]  # fixed order, given by the data
categories = data["categories"]
shares = {c: np.array(data[c]) / 100 for c in categories}
assert np.allclose(sum(shares.values()), 1), "the shares of an opponent do not sum to 100%"

win_or_tie = shares["LIMA wins"] + shares["Tie"]
print("takeaway (wins + ties):", {o: f"{v:.0%}" for o, v in zip(opponents, win_or_tie)})
assert win_or_tie[0] == max(win_or_tie) and win_or_tie[-1] == min(win_or_tie), "the takeaway does not hold"

tie_color, loss_color = greys(2)
segment_colors = {"LIMA wins": colors["ours"], "Tie": tie_color, "LIMA Loses": loss_color}

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
y = np.arange(len(opponents))
left = np.zeros(len(opponents))
for category in categories:
    values = shares[category]
    color = segment_colors[category]
    bars = ax.barh(y, values, left=left, color=color, edgecolor="white",
                   linewidth=rcParams["grid.linewidth"], label=category)
    ax.bar_label(bars, labels=[f"{v:.0%}" for v in values], label_type="center", color=text_color(color))
    left += values

ax.set_yticks(y, labels=opponents)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Test prompts")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(categories), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/win-rate.pdf")
fig.savefig("../outputs/win-rate.png")
