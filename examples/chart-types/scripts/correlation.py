"""Reward model score versus human rating for 300 responses. Each point is one response, its human rating averaged over annotators on a 1–7 Likert scale; the line is a least-squares fit. The reward score agrees with human judgment, Spearman ρ = 0.875 (n = 300)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy.stats import spearmanr

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/correlation.json") as f:
    data = json.load(f)
human = np.array(data["human_rating"])
reward = np.array(data["reward_score"])

rho = spearmanr(human, reward).statistic
print("takeaway:", f"rho = {rho:#.3g}", f"n = {len(human)}")
assert rho > 0.5, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.grid(True)
color = colors["series-1"]
ax.scatter(human, reward, s=rcParams["lines.markersize"] ** 2, color=color, edgecolors="none", alpha=0.5)

slope, intercept = np.polyfit(human, reward, 1)
line_x = np.array([human.min(), human.max()])
ax.plot(line_x, slope * line_x + intercept, color=darken(color))

ax.set_xticks(range(1, 8))
ax.set_xlabel("Human rating")
ax.set_ylabel("Reward score")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/correlation.pdf")
fig.savefig("../outputs/correlation.png")
