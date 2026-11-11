"""Figure 2: Reward model score versus human rating for 300 responses. Human ratings are 1–7 Likert
scores averaged over annotators; the line is a least-squares fit. The reward model's scores
correlate strongly with human ratings (Pearson r = 0.86, n = 300).
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

data = json.load(open("../data/correlation.json"))
rating = np.array(data["human_rating"])
score = np.array(data["reward_score"])

fig, ax = plt.subplots(figsize=(2.75, 2))
ax.scatter(rating, score, s=6.25, color=colors["series-1"], edgecolors="none", alpha=0.5)

slope, intercept = np.polyfit(rating, score, 1)
ax.plot([1, 7], [slope * 1 + intercept, slope * 7 + intercept], color=darken(colors["series-1"]))

ax.set_xticks([1, 2, 3, 4, 5, 6, 7])
ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))
ax.set_xlabel("Human rating")
ax.set_ylabel("Reward model score")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/correlation.pdf")
fig.savefig("../outputs/correlation.png")
