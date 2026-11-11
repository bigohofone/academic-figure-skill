"""Figure 1: Distribution of our model's confidence on correct and incorrect answers. Histograms show density; dashed lines mark the means. Our model is 0.834 confident on correct answers on average, against 0.575 on incorrect ones."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confidence-histogram.json") as f:
    data = json.load(f)
correct = np.array(data["correct"])
incorrect = np.array(data["incorrect"])

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
bins = np.histogram_bin_edges(np.concatenate([correct, incorrect]), bins="auto")
for values, name, color in [(correct, "Correct", colors["series-1"]), (incorrect, "Incorrect", colors["series-2"])]:
    ax.hist(values, bins=bins, density=True, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)
    ax.hist(values, bins=bins, density=True, histtype="step", color=color, label=name)
    mean = values.mean()
    ax.axvline(mean, linestyle="--", linewidth=paper.dashed_width, color=darken(color))
    ax.annotate(f"{mean:#.3g}", (mean, 1), xycoords=("data", "axes fraction"), xytext=(0, 2),
                textcoords="offset points", ha="center", va="bottom", color=darken(color))
ax.grid(axis="x", visible=False)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.set_xlabel("Confidence")
ax.set_ylabel("Density")
ax.legend(loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/confidence-histogram.pdf")
fig.savefig("../outputs/confidence-histogram.png")
