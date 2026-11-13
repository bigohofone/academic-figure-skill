"""Reward-model scores of 400 responses from each policy. Violins show the kernel density of the values; inside, the bar spans the quartiles, the thin line reaches 1.5× the interquartile range, and the white dot marks the median. Ours has the highest mean reward, 1.73, against 0.728 for PPO and 0.0512 for SFT."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, shift_lightness, make_shades

colors = paper.colors

with open("../data/reward-distribution.json") as f:
    rewards = json.load(f)["rewards"]

means = {name: float(np.mean(v)) for name, v in rewards.items()}
names = sorted(rewards, key=lambda name: means[name])  # ascending, ours ends at the right
print("takeaway:", {n: f"{means[n]:#.3g}" for n in names})
assert names[-1] == "Ours", "the takeaway does not hold"

greys = make_shades(colors["neutral"], len(names) - 1)
fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for x, name in enumerate(names):
    values = rewards[name]
    color = colors["ours"] if name == "Ours" else greys[x]
    parts = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)
    body = parts["bodies"][0]
    body.set_facecolor(color if color == colors["ours"] else shift_lightness(color, 2))
    body.set_edgecolor(colors["ink"])
    body.set_linewidth(rcParams["patch.linewidth"])
    body.set_alpha(1)
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    low = min(v for v in values if v >= q1 - 1.5 * (q3 - q1))
    high = max(v for v in values if v <= q3 + 1.5 * (q3 - q1))
    ax.vlines(x, low, high, color=colors["ink"], linewidth=rcParams["grid.linewidth"])
    ax.vlines(x, q1, q3, color=colors["ink"], linewidth=4 * rcParams["grid.linewidth"])
    ax.plot(x, median, "o", color=colors["ink"], markerfacecolor="white", zorder=3)
ax.set_xticks(range(len(names)), labels=names)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Reward")

finalize_figure(fig, ax)
fig.savefig("../outputs/reward-distribution.pdf")
fig.savefig("../outputs/reward-distribution.png")
fig.savefig("../outputs/reward-distribution.svg")
