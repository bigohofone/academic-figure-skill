"""Confidence of our model on correct and incorrect answers. Bars show density, so the 1800 correct and 420 incorrect answers compare by shape; vertical lines mark the means. Incorrect answers get lower confidence than correct ones, 0.575 against 0.834 on average."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confidence-histogram.json") as f:
    data = json.load(f)
correct = np.array(data["correct"])
incorrect = np.array(data["incorrect"])

means = {"Correct": correct.mean(), "Incorrect": incorrect.mean()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in means.items()}, "n:", len(correct), len(incorrect))
assert means["Incorrect"] < means["Correct"], "the takeaway does not hold"

bins = np.histogram_bin_edges(np.concatenate([correct, incorrect]), bins="auto")

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for name, values, color in [("Correct", correct, colors["series-1"]),
                            ("Incorrect", incorrect, colors["series-3"])]:
    ax.hist(values, bins=bins, density=True, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)
    ax.hist(values, bins=bins, density=True, histtype="step", color=color, label=name)
    mean = values.mean()
    ax.axvline(mean, linewidth=rcParams["grid.linewidth"], color=darken(color))
    ax.annotate(f"{mean:#.3g}", (mean, 1), xycoords=("data", "axes fraction"), xytext=(0, 2),
                textcoords="offset points", ha="center", va="bottom", color=darken(color))

ax.grid(axis="x", visible=False)
ax.set_xlabel("Confidence")
ax.set_ylabel("Density")
ax.legend(loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/confidence-histogram.pdf")
fig.savefig("../outputs/confidence-histogram.png")
