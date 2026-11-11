"""Confidence of our model on correct and incorrect answers. Histograms are normalized to density; vertical lines mark the means. Correct answers get a mean confidence of 0.834, against 0.575 for incorrect ones."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, darken

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confidence-histogram.json") as f:
    data = json.load(f)
series = {"Correct": data["correct"], "Incorrect": data["incorrect"]}
series_colors = {"Correct": colors["series-1"], "Incorrect": colors["series-4"]}

means = {name: float(np.mean(values)) for name, values in series.items()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in means.items()})
assert means["Correct"] > means["Incorrect"], "the takeaway does not hold"

bins = np.histogram_bin_edges(np.concatenate(list(series.values())), bins="auto")

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for name, values in series.items():
    color = series_colors[name]
    ax.hist(values, bins=bins, density=True, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)
    ax.hist(values, bins=bins, density=True, histtype="step", color=color, label=name)
    ax.axvline(means[name], linewidth=rcParams["grid.linewidth"], color=darken(color))
    ax.annotate(f"{means[name]:#.3g}", (means[name], 1), xycoords=("data", "axes fraction"),
                xytext=(0, 2), textcoords="offset points", ha="center", va="bottom", color=darken(color))
ax.grid(axis="x", visible=False)
ax.set_xlabel("Confidence")
ax.set_ylabel("Density")
ax.legend()

finalize_figure(fig, ax, aspect=0.618)
fig.savefig("../outputs/confidence-histogram.pdf")
fig.savefig("../outputs/confidence-histogram.png")
