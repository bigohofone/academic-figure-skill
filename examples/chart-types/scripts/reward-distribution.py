"""Reward-model scores of responses from three policies. Violins show the kernel density of the 400 scores per policy; inside, the bar spans the quartiles, the thin line reaches 1.5× the interquartile range, and the white dot marks the median. Ours shifts the whole distribution up, to a median reward of 1.86 against 1.02 for PPO and −0.231 for SFT."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/reward-distribution.json") as f:
    rewards = json.load(f)["rewards"]

medians = {name: np.median(v) for name, v in rewards.items()}
policies = sorted(rewards, key=lambda name: medians[name])  # ascending, so Ours ends at the right
print("takeaway: medians", {name: f"{medians[name]:#.3g}".replace("-", "−") for name in policies},
      "n:", {name: len(rewards[name]) for name in policies})
assert policies[-1] == "Ours", "the takeaway does not hold"

baselines = [name for name in policies if name != "Ours"]
fill = dict(zip(baselines, greys(len(baselines))), Ours=colors["ours"])

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for x, name in enumerate(policies):
    values = rewards[name]
    parts = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)
    body = parts["bodies"][0]
    body.set_facecolor(lighten(fill[name]))
    body.set_edgecolor(colors["ink"])
    body.set_linewidth(rcParams["patch.linewidth"])
    body.set_alpha(1)

    q1, median, q3 = np.percentile(values, [25, 50, 75])
    low = min(v for v in values if v >= q1 - 1.5 * (q3 - q1))
    high = max(v for v in values if v <= q3 + 1.5 * (q3 - q1))
    ax.vlines(x, low, high, color=colors["ink"], linewidth=rcParams["patch.linewidth"])
    ax.vlines(x, q1, q3, color=colors["ink"], linewidth=4 * rcParams["patch.linewidth"])
    ax.plot(x, median, "o", color=colors["ink"], markerfacecolor="white", zorder=3)

ax.set_xticks(range(len(policies)), labels=policies)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Reward")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/reward-distribution.pdf")
fig.savefig("../outputs/reward-distribution.png")
