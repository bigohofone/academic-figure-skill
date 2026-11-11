"""Human preference judgments of LIMA against five baselines on 300 test prompts. Each bar splits the prompts into LIMA wins, ties and LIMA losses. LIMA wins or ties on 74% of prompts against Alpaca 65B and on 65% against DaVinci003, and still on 43% against GPT-4 (April)."""

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
opponents = data["opponents"]  # fixed order, given by the data
categories = data["categories"]  # "LIMA wins", "Tie", "LIMA Loses"
shares = {c: np.array(data[c]) / 100 for c in categories}
assert np.allclose(sum(shares.values()), 1)
segment_colors = [colors["ours"], *greys(2)]

# Takeaway: LIMA wins or ties against each opponent on this share of prompts.
win_or_tie = shares["LIMA wins"] + shares["Tie"]
print("takeaway:", {o: f"{v:.0%}" for o, v in zip(opponents, win_or_tie)})
assert win_or_tie[0] > 0.5 and win_or_tie[1] > 0.5, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
y = np.arange(len(opponents))
left = np.zeros(len(opponents))
for c, color in zip(categories, segment_colors):
    v = shares[c]
    bars = ax.barh(y, v, left=left, color=color, edgecolor="white",
                   linewidth=plt.rcParams["grid.linewidth"], label=c)
    ax.bar_label(bars, labels=[f"{s:.0%}" for s in v], label_type="center", color=text_color(color))
    left += v
ax.set_yticks(y, labels=opponents)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Share of prompts")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(categories), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/win-rate.pdf")
fig.savefig("../outputs/win-rate.png")
