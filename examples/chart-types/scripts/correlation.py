"""Figure 2: Reward model score versus human rating for 300 responses. Human ratings are 1–7 Likert scores averaged over annotators; the line is a least-squares fit. The reward score tracks human judgment closely, with Pearson r = 0.863 (n = 300)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy import stats

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/correlation.json") as f:
    data = json.load(f)
human = np.array(data["human_rating"])
reward = np.array(data["reward_score"])

r, _ = stats.pearsonr(human, reward)
print(f"Pearson r = {r:#.3g}, n = {len(human)}")

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
ax.grid(True)
ax.scatter(human, reward, s=rcParams["lines.markersize"] ** 2, color=colors["series-1"], edgecolors="none", alpha=0.5)

slope, intercept = np.polyfit(human, reward, 1)
ax.plot([1, 7], [slope * 1 + intercept, slope * 7 + intercept], color=darken(colors["series-1"]))

ax.set_xticks([1, 2, 3, 4, 5, 6, 7])
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.set_xlabel("Human rating")
ax.set_ylabel("Reward score")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/correlation.pdf")
fig.savefig("../outputs/correlation.png")
