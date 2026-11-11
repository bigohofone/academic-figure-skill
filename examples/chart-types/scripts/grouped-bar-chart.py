"""Figure 1: Accuracy of four training methods on GSM8K, MATH and HumanEval. Ours is the most accurate on every benchmark, ahead of the next best, DPO, by 0.036 on GSM8K, 0.043 on MATH and 0.029 on HumanEval."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/grouped-bar-chart.json"))
benchmarks = data["benchmarks"]
methods = ["Base", "SFT", "DPO", "Ours"]
method_colors = [*greys(3), colors["ours"]]

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
x = np.arange(len(benchmarks))
width = 0.8 / len(methods)
for i, (method, color) in enumerate(zip(methods, method_colors)):
    values = data["scores"][method]
    bars = ax.bar(x + (i - (len(methods) - 1) / 2) * width, values, width, color=color, linewidth=0, label=method)
    ax.bar_label(bars, labels=[f"{v:#.3g}" for v in values], rotation=90, padding=2)

ax.set_xticks(x, labels=benchmarks)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Accuracy")
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=len(methods), frameon=False)

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-bar-chart.pdf")
fig.savefig("../outputs/grouped-bar-chart.png")
