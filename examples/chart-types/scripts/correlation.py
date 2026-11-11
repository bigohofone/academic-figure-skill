"""Reward model score versus human rating for 300 responses. Human ratings are 1–7 Likert scores averaged over annotators; the line is a least-squares fit. The reward score tracks human judgement closely, with Spearman ρ = 0.875 (n = 300)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy import stats

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import darken, fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/correlation.json") as f:
    data = json.load(f)
human = np.array(data["human_rating"])
reward = np.array(data["reward_score"])

# takeaway: the reward model ranks responses as humans do; ratings are ordinal, so Spearman's rho
rho = stats.spearmanr(human, reward).statistic
print("takeaway:", {"rho": f"{rho:#.3g}", "n": f"{round(len(human))}"})
assert rho > 0.8, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.scatter(human, reward, s=rcParams["lines.markersize"] ** 2, color=colors["series-1"], edgecolors="none", alpha=0.5)

# trend line: least-squares fit over the rated range
slope, intercept = np.polyfit(human, reward, 1)
x_fit = np.array([human.min(), human.max()])
ax.plot(x_fit, slope * x_fit + intercept, color=darken(colors["series-1"]))

ax.set_xticks(range(1, 8))
ax.set_xlabel("Human rating")
ax.set_ylabel("Reward score")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/correlation.pdf")
fig.savefig("../outputs/correlation.png")
