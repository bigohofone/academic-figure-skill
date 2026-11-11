"""Reward model score versus human rating for 300 responses. Each dot is one response, its human rating the mean 1–7 Likert score over annotators; the line is a least-squares fit. Reward scores rise with human ratings (Spearman ρ = 0.875, n = 300)."""

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
rating = np.array(data["human_rating"])
score = np.array(data["reward_score"])

# Takeaway: the reward model's scores agree with human ratings (ratings are ordinal, so Spearman).
rho, p = spearmanr(rating, score)
print("takeaway:", f"Spearman rho = {rho:#.3g}", f"p = {p:.2e}", f"n = {len(rating)}")
assert rho > 0 and p < 0.05, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))

color = colors["series-1"]
ax.scatter(rating, score, s=rcParams["lines.markersize"] ** 2, color=color, edgecolors="none", alpha=0.5)
slope, intercept = np.polyfit(rating, score, 1)
fit_x = np.array([rating.min(), rating.max()])
ax.plot(fit_x, slope * fit_x + intercept, color=darken(color))

ax.set_xticks(range(1, 8))
ax.set_xlabel("Human rating")
ax.set_ylabel("Reward score")
ax.grid(True)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/correlation.pdf")
fig.savefig("../outputs/correlation.png")
