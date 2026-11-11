"""Accuracy of four training methods on three benchmarks. Ours scores highest on all three, ahead of the next best method, DPO, by 0.036 on GSM8K (0.842 vs. 0.806), 0.043 on MATH (0.531 vs. 0.488) and 0.029 on HumanEval (0.701 vs. 0.672)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/grouped-bar-chart.json") as f:
    data = json.load(f)
benchmarks = data["benchmarks"]
scores = data["scores"]

# Methods in ascending order of accuracy (the same on every benchmark), so Ours ends at the right.
methods = ["Base", "SFT", "DPO", "Ours"]
for b in range(len(benchmarks)):
    assert [scores[m][b] for m in methods] == sorted(scores[m][b] for m in methods)
method_colors = dict(zip(["Base", "SFT", "DPO"], greys(3)))
method_colors["Ours"] = colors["ours"]

# Takeaway: Ours is best on every benchmark; its margin over the next best method.
for b, name in enumerate(benchmarks):
    others = {m: scores[m][b] for m in methods if m != "Ours"}
    best_other = max(others, key=others.get)
    gap = scores["Ours"][b] - others[best_other]
    print(f"takeaway: {name}: Ours {scores['Ours'][b]:.3f}, {best_other} {others[best_other]:.3f}, gap {gap:.3f}")
    assert gap > 0, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
x = np.arange(len(benchmarks))
width = 0.8 / len(methods)
for i, m in enumerate(methods):
    bars = ax.bar(x + (i - (len(methods) - 1) / 2) * width, scores[m], width,
                  color=method_colors[m], linewidth=0, label=m)
    # Given in the data: three significant figures, as the most precise value has (0.64 -> 0.640).
    ax.bar_label(bars, labels=[f"{v:.3f}" for v in scores[m]], color=darken(method_colors[m]),
                 rotation=90, padding=2)
ax.set_xticks(x, labels=benchmarks)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Accuracy")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(methods), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-bar-chart.pdf")
fig.savefig("../outputs/grouped-bar-chart.png")
