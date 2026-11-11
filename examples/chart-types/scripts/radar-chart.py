"""Accuracy (%) of 8–9B models across six benchmarks. Ours-8B scores highest on five of six benchmarks, with its largest lead on MATH (41.5 vs. 36.6 for the best baseline); Gemma-2-9B leads only on MMLU."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import darken, finalize_figure

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/radar-chart.json") as f:
    data = json.load(f)
benchmarks = data["benchmarks"]
scores = {name: np.array(v) for name, v in data["scores"].items()}
ours = "Ours-8B"
baselines = [name for name in scores if name != ours]

best_baseline = np.max([scores[b] for b in baselines], axis=0)
wins = [bm for bm, o, b in zip(benchmarks, scores[ours], best_baseline) if o > b]
lead = scores[ours] - best_baseline
k = int(np.argmax(lead))
print("takeaway:", {"wins": f"{len(wins)} of {len(benchmarks)}", "largest lead": benchmarks[k],
                    "ours": f"{scores[ours][k]:#.3g}", "best baseline": f"{best_baseline[k]:#.3g}",
                    "losses": [bm for bm in benchmarks if bm not in wins]})
assert len(wins) == 5 and benchmarks[k] == "MATH", "the takeaway does not hold"

n = len(benchmarks)
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
loop = np.r_[angles, angles[:1]]
rings = [25, 50, 75, 100]

fig, ax = plt.subplots(figsize=(2.75, 2.75), subplot_kw={"projection": "polar"})
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.grid(False)
ax.spines["polar"].set_visible(False)
for r in rings:
    ax.plot(loop, [r] * (n + 1), color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
for a in angles:
    ax.plot([a, a], [0, rings[-1]], color=colors["ink"], alpha=rcParams["grid.alpha"], linewidth=rcParams["grid.linewidth"])
ax.plot(loop, [rings[-1]] * (n + 1), color=colors["ink"], linewidth=rcParams["axes.linewidth"])
ax.set_ylim(0, rings[-1])

# Baselines in ascending order of mean accuracy, told apart by line style; ours last, on top
baselines = sorted(baselines, key=lambda b: scores[b].mean())
handles = {}
for name, style in zip(baselines, ["--", ":"]):
    (handles[name],) = ax.plot(loop, np.r_[scores[name], scores[name][:1]], color=colors["neutral"], linestyle=style,
                               linewidth=paper.dashed_width, label=name)
    ax.fill(angles, scores[name], color=colors["neutral"], alpha=0.1)
(handles[ours],) = ax.plot(loop, np.r_[scores[ours], scores[ours][:1]], color=colors["ours"], label=ours)
ax.fill(angles, scores[ours], color=colors["ours"], alpha=0.1)

ax.set_xticks(angles, labels=benchmarks)
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

labels = [ours] + baselines
fig.legend([handles[l] for l in labels], labels, loc="outside upper center", ncol=len(labels), frameon=False,
           borderaxespad=0)

finalize_figure(fig, ax)
fig.savefig("../outputs/radar-chart.pdf")
fig.savefig("../outputs/radar-chart.png")
