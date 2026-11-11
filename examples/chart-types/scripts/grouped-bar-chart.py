"""Accuracy of four training methods on three benchmarks. Ours is the most accurate on all three, ahead of DPO by 0.036 on GSM8K, 0.043 on MATH and 0.029 on HumanEval."""

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

# methods in ascending order of mean accuracy, so Ours ends at the right
methods = sorted(scores, key=lambda m: np.mean(scores[m]))
print("order:", methods)

margins = {b: scores["Ours"][i] - max(scores[m][i] for m in scores if m != "Ours")
           for i, b in enumerate(benchmarks)}
runner_up = {b: max((m for m in scores if m != "Ours"), key=lambda m: scores[m][i])
             for i, b in enumerate(benchmarks)}
print("takeaway:", {b: f"{runner_up[b]} +{v:.3f}" for b, v in margins.items()})
assert all(v > 0 for v in margins.values()), "the takeaway does not hold"

baseline_colors = greys(len(methods) - 1)
method_colors = {m: baseline_colors[i] for i, m in enumerate(m for m in methods if m != "Ours")}
method_colors["Ours"] = colors["ours"]

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
x = np.arange(len(benchmarks))
width = 0.8 / len(methods)
for i, method in enumerate(methods):
    values = scores[method]
    bars = ax.bar(x + (i - (len(methods) - 1) / 2) * width, values, width,
                  color=method_colors[method], linewidth=0, label=method)
    ax.bar_label(bars, labels=[f"{v:#.3g}" for v in values], color=darken(colors["ours"] if method == "Ours" else colors["neutral"]),
                 rotation=90, padding=2)

ax.set_xticks(x, labels=benchmarks)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Accuracy")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(methods), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-bar-chart.pdf")
fig.savefig("../outputs/grouped-bar-chart.png")
