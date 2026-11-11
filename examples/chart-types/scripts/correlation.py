"""Figure 1: Reward model score versus human rating for 300 responses. Human ratings are 1–7 Likert scores averaged over annotators; the line is a least-squares fit. The reward model's scores correlate strongly with human ratings (Pearson r = 0.863, n = 300)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/correlation.json"))
human = np.array(data["human_rating"])
reward = np.array(data["reward_score"])

fig, ax = plt.subplots(figsize=(2.75, 2))
color = colors["series-1"]
ax.scatter(human, reward, s=rcParams["lines.markersize"] ** 2, color=color, edgecolors="none", alpha=0.5)
slope, intercept = np.polyfit(human, reward, 1)
xs = np.array([1, 7])
ax.plot(xs, slope * xs + intercept, color=darken(color))
ax.set_xticks(range(1, 8))
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.set_xlabel("Human rating")
ax.set_ylabel("Reward score")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/correlation.pdf")
fig.savefig("../outputs/correlation.png")
