"""Accuracy of 8–9B models across six benchmarks. Ours-8B leads on five of the six benchmarks, with its largest margin on MATH (41.5 vs. 36.6 for the next best model)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/radar-chart.json") as f:
    data = json.load(f)
names = data["benchmarks"]
scores = {model: np.array(v) for model, v in data["scores"].items()}
ours = "Ours-8B"
n = len(names)

# Takeaway: ours leads on most benchmarks, by the most on one of them.
others = np.max([v for m, v in scores.items() if m != ours], axis=0)
leads = scores[ours] > others
margin = scores[ours] - others
k = int(np.argmax(margin))
print("takeaway:", f"leads on {leads.sum()} of {n}", f"largest margin on {names[k]}: {scores[ours][k]:#.3g} vs. {others[k]:#.3g}")
assert leads.sum() == 5 and names[k] == "MATH", "the takeaway does not hold"

# Compared models in ascending order of mean accuracy, told apart by line style.
baselines = sorted((m for m in scores if m != ours), key=lambda m: scores[m].mean())
styles = dict(zip(baselines, ["--", ":"]))

fig, ax = plt.subplots(figsize=(2.75, 2.75), subplot_kw={"projection": "polar"})
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

rings = [25, 50, 75, 100]
ax.grid(False)
ax.spines["polar"].set_visible(False)
loop = np.r_[angles, angles[:1]]
for r in rings:
    ax.plot(loop, [r] * (n + 1), color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
for a in angles:
    ax.plot([a, a], [0, rings[-1]], color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
ax.plot(loop, [rings[-1]] * (n + 1), color=colors["ink"], linewidth=rcParams["axes.linewidth"])
ax.set_ylim(0, rings[-1])

handles = {}
for model in baselines + [ours]:
    values = scores[model]
    color = colors["ours"] if model == ours else colors["neutral"]
    style = "-" if model == ours else styles[model]
    (handles[model],) = ax.plot(loop, np.r_[values, values[:1]], color=color, linestyle=style,
                                linewidth=1 if style == "-" else paper.dashed_width, label=model)
    ax.fill(angles, values, color=color, alpha=0.1)

ax.set_xticks(angles, labels=names)
ax.tick_params(axis="x", pad=6)
ax.set_yticks([r * np.cos(np.pi / n) for r in rings[:-1]], labels=[str(r) for r in rings[:-1]])
ax.set_rlabel_position(180 / n)

for angle, v in zip(angles, scores[ours]):
    side = np.sin(angle) if abs(np.sin(angle)) > 0.1 else 0
    up = np.cos(angle) if side == 0 else 0
    ax.annotate(f"{v:#.3g}", (angle, v), xytext=(4 * np.sign(side), 4 * np.sign(up)), textcoords="offset points",
                ha="left" if side > 0 else "right" if side < 0 else "center",
                va=("top" if np.cos(angle) > 0 else "bottom") if side else ("bottom" if up > 0 else "top"),
                color=darken(colors["ours"]), bbox=dict(facecolor="white", edgecolor="none", pad=1), gid="value-label")

order = [ours] + baselines
fig.legend([handles[m] for m in order], order, loc="outside upper center", ncol=len(order),
           frameon=False, borderaxespad=0)

fit_height(fig, ax)
fig.savefig("../outputs/radar-chart.pdf")
fig.savefig("../outputs/radar-chart.png")
