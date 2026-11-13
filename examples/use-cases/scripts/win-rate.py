"""Human preference between LIMA and five baselines over 300 test prompts. Each bar splits the prompts into LIMA wins, ties and LIMA losses. LIMA wins more often than it loses against Alpaca 65B (53% vs. 26%) and DaVinci003 (44% vs. 35%), and even against GPT-4 its responses are preferred or tied in 43% of prompts."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, make_shades

colors = paper.colors

with open("../data/win-rate.json") as f:
    data = json.load(f)
opponents = data["opponents"]
categories = data["categories"]  # LIMA wins, Tie, LIMA Loses
shares = {c: np.array(data[c]) / 100 for c in categories}
assert np.allclose(sum(shares.values()), 1)

# takeaway: LIMA wins more than it loses against Alpaca 65B and DaVinci003; vs. GPT-4, wins + ties
wins, ties, losses = (shares[c] for c in categories)
print("takeaway:", {o: (f"{w:.0%}", f"{l:.0%}", f"win+tie {w + t:.0%}") for o, w, t, l in zip(opponents, wins, ties, losses)})
assert wins[0] > losses[0] and wins[1] > losses[1], "the takeaway does not hold"

category_colors = [colors["ours"], *make_shades(colors["neutral"], 2)]

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
y = np.arange(len(opponents))
left = np.zeros(len(opponents))
for category, color in zip(categories, category_colors):
    values = shares[category]
    bars = ax.barh(y, values, left=left, color=color, edgecolor=colors["paper"],
                   linewidth=plt.rcParams["grid.linewidth"], label=category)
    ax.bar_label(bars, labels=[f"{v:.0%}" for v in values], label_type="center", color=colors["paper"] if np.dot(to_rgb(color), [0.299, 0.587, 0.114]) < 0.5 else colors["ink"])
    left += values

ax.set_yticks(y, labels=opponents)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlim(0, 1)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Share of test prompts")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(categories))

finalize_figure(fig, ax)
fig.savefig("../outputs/win-rate.pdf")
fig.savefig("../outputs/win-rate.png")
