"""Accuracy of four training methods on three reasoning and coding benchmarks. Ours scores highest on all three, ahead of the best baseline, DPO, by 0.036 on GSM8K, 0.043 on MATH and 0.029 on HumanEval."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/grouped-bar-chart.json") as f:
    data = json.load(f)
benchmarks = data["benchmarks"]
scores = data["scores"]

# Methods left to right in ascending order of mean accuracy, so Ours ends at the right.
methods = sorted(scores, key=lambda m: np.mean(scores[m]))
assert methods[-1] == "Ours", "the takeaway does not hold"
baseline_colors = greys(len(methods) - 1)
method_colors = {m: baseline_colors[i] for i, m in enumerate(methods[:-1])}
method_colors["Ours"] = colors["ours"]

# Takeaway: Ours beats the best baseline on every benchmark.
best_baseline = max((m for m in methods if m != "Ours"), key=lambda m: np.mean(scores[m]))
gaps = [o - b for o, b in zip(scores["Ours"], scores[best_baseline])]
print("takeaway: best baseline", best_baseline, {b: f"{g:.3f}" for b, g in zip(benchmarks, gaps)})
for i in range(len(benchmarks)):
    assert all(scores["Ours"][i] > scores[m][i] for m in methods if m != "Ours"), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
x = np.arange(len(benchmarks))
width = 0.8 / len(methods)
for i, method in enumerate(methods):
    values = scores[method]
    bars = ax.bar(x + (i - (len(methods) - 1) / 2) * width, values, width,
                  color=method_colors[method], linewidth=0, label=method)
    ax.bar_label(bars, labels=[f"{v:.3f}" for v in values], color=darken(method_colors[method]),
                 rotation=90, padding=2)

ax.set_xticks(x, labels=benchmarks)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Accuracy")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(methods), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-bar-chart.pdf")
fig.savefig("../outputs/grouped-bar-chart.png")
