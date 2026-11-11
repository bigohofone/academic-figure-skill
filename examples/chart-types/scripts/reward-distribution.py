"""Figure 1: Reward-model scores of responses from three policies. Violins show the kernel density of the values; inside, the bar spans the quartiles, the thin line reaches 1.5× the interquartile range, and the white dot marks the median. Scores fall into a low and a high mode; ours puts 92% of responses above 0, against 67% for PPO and 45% for SFT."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, lighten, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

rewards = json.load(open("../data/reward-distribution.json"))["rewards"]
grey_sft, grey_ppo = greys(2)
series = [("SFT", grey_sft), ("PPO", grey_ppo), ("Ours", colors["ours"])]

fig, ax = plt.subplots(figsize=(2.75, 2))
for x, (name, color) in enumerate(series):
    values = rewards[name]
    body = ax.violinplot(values, positions=[x], widths=0.8, showextrema=False)["bodies"][0]
    body.set_facecolor(lighten(color))
    body.set_edgecolor(colors["ink"])
    body.set_linewidth(rcParams["patch.linewidth"])
    body.set_alpha(1)
    q1, median, q3 = np.percentile(values, [25, 50, 75])
    low = min(v for v in values if v >= q1 - 1.5 * (q3 - q1))
    high = max(v for v in values if v <= q3 + 1.5 * (q3 - q1))
    ax.vlines(x, low, high, color=colors["ink"], linewidth=rcParams["patch.linewidth"])
    ax.vlines(x, q1, q3, color=colors["ink"], linewidth=4 * rcParams["patch.linewidth"])
    ax.plot(x, median, "o", color=colors["ink"], markerfacecolor="white", zorder=3)
ax.set_xticks(range(len(series)), labels=[name for name, _ in series])
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.set_ylabel("Reward")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/reward-distribution.pdf")
fig.savefig("../outputs/reward-distribution.png")
