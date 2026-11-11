"""Accuracy of four training methods on three benchmarks. Ours is the most accurate on every benchmark, 0.036, 0.043 and 0.029 above the best baseline, DPO, on GSM8K, MATH and HumanEval."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, darken, baseline_greys

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/grouped-bar-chart.json") as f:
    data = json.load(f)
benchmarks = data["benchmarks"]
scores = data["scores"]

# takeaway: Ours beats every baseline on every benchmark
baselines = [m for m in scores if m != "Ours"]
best_baseline = [max(baselines, key=lambda m: scores[m][j]) for j in range(len(benchmarks))]
margins = [scores["Ours"][j] - scores[best_baseline[j]][j] for j in range(len(benchmarks))]
print("takeaway:", {b: (bb, f"{m:.3f}") for b, bb, m in zip(benchmarks, best_baseline, margins)})
assert all(m > 0 for m in margins), "the takeaway does not hold"

# methods left to right in ascending order of mean accuracy, so Ours ends at the right
methods = sorted(scores, key=lambda m: np.mean(scores[m]))
assert methods[-1] == "Ours"
method_colors = dict(zip(methods[:-1], baseline_greys(len(methods) - 1)))
method_colors["Ours"] = colors["ours"]

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
x = np.arange(len(benchmarks))
width = 0.8 / len(methods)
for i, method in enumerate(methods):
    values = scores[method]
    bars = ax.bar(x + (i - (len(methods) - 1) / 2) * width, values, width,
                  color=method_colors[method], linewidth=0, label=method)
    label_color = darken(colors["ours"] if method == "Ours" else colors["neutral"])  # one text grey for grey series
    ax.bar_label(bars, fontsize=paper.bar_label_size, labels=[f"{v:.3f}" for v in values], color=label_color,
                 rotation=90, padding=2)

ax.set_xticks(x, labels=benchmarks)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Accuracy")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(methods))

finalize_figure(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-bar-chart.pdf")
fig.savefig("../outputs/grouped-bar-chart.png")
