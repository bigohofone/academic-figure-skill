"""Figure 1: Accuracy (%) of three 8–9B models on six benchmarks. Ours-8B scores highest on five of six benchmarks, most clearly on MATH (41.5 vs. 36.6 for Gemma-2-9B), and trails only on MMLU (68.4 vs. 71.3)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/radar-chart.json") as f:
    data = json.load(f)
benchmarks = data["benchmarks"]
scores = {name: np.array(v) for name, v in data["scores"].items()}
n = len(benchmarks)
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
loop = np.r_[angles, angles[:1]]
rings = [25, 50, 75, 100]

fig, ax = plt.subplots(figsize=(2.75, 2.75), subplot_kw={"projection": "polar"}, layout="constrained")
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# polygon grid; the outer polygon is the panel box
ax.grid(False)
ax.spines["polar"].set_visible(False)
for r in rings:
    ax.plot(loop, [r] * (n + 1), color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
for a in angles:
    ax.plot([a, a], [0, rings[-1]], color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
ax.plot(loop, [rings[-1]] * (n + 1), color=colors["ink"], linewidth=rcParams["axes.linewidth"])
ax.set_ylim(0, rings[-1])

# baselines in grey, ascending by mean score (Gemma-2-9B, Llama-3-8B); ours last, on top
handles = {}
for name, style in [("Gemma-2-9B", "-"), ("Llama-3-8B", "--")]:
    v = scores[name]
    (handles[name],) = ax.plot(loop, np.r_[v, v[:1]], color=colors["neutral"], linestyle=style,
                               linewidth=paper.dashed_width if style != "-" else rcParams["lines.linewidth"], label=name)
    ax.fill(angles, v, color=colors["neutral"], alpha=0.1)
ours = scores["Ours-8B"]
(handles["Ours-8B"],) = ax.plot(loop, np.r_[ours, ours[:1]], color=colors["ours"], label="Ours-8B")
ax.fill(angles, ours, color=colors["ours"], alpha=0.1)

ax.set_xticks(angles, labels=benchmarks)
ax.tick_params(axis="x", pad=6)
ax.set_yticks([r * np.cos(np.pi / n) for r in rings[:-1]], labels=[str(r) for r in rings[:-1]])
ax.set_rlabel_position(180 / n)

# ours' values outside its vertices
for angle, v in zip(angles, ours):
    side = np.sin(angle) if abs(np.sin(angle)) > 0.1 else 0
    up = np.cos(angle) if side == 0 else 0
    ax.annotate(f"{v:#.3g}", (angle, v), xytext=(4 * np.sign(side), 4 * np.sign(up)), textcoords="offset points",
                ha="left" if side > 0 else "right" if side < 0 else "center",
                va=("top" if np.cos(angle) > 0 else "bottom") if side else ("bottom" if up > 0 else "top"),
                color=darken(colors["ours"]), bbox=dict(facecolor="white", edgecolor="none", pad=1))

order = ["Ours-8B", "Gemma-2-9B", "Llama-3-8B"]
fig.legend([handles[k] for k in order], order, loc="outside upper center", ncol=len(order), frameon=False, borderaxespad=0)

fit_height(fig, ax)
fig.savefig("../outputs/radar-chart.pdf")
fig.savefig("../outputs/radar-chart.png")
