"""Figure 1: Distribution of the model's confidence on correct and incorrect answers. Histograms are normalized to density. 67% of correct answers have confidence above 0.8, against 13% of incorrect ones, which spread across the whole range."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, lighten, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/confidence-histogram.json"))
series = [("Correct", data["correct"], colors["series-1"]), ("Incorrect", data["incorrect"], colors["series-2"])]
bins = np.histogram_bin_edges(np.concatenate([values for _, values, _ in series]), bins="auto")

fig, ax = plt.subplots(figsize=(2.75, 2))
for name, values, color in series:
    ax.hist(values, bins=bins, density=True, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)
    ax.hist(values, bins=bins, density=True, histtype="step", color=color, label=name)
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
lo, hi = ax.get_ylim()
ticks = [t for t in ax.get_yticks() if lo <= t <= hi]
ax.set_yticks(ticks, labels=["", *[f"{t:.10g}" for t in ticks[1:]]])
ax.grid(axis="x", visible=False)
ax.set_xlabel("Confidence")
ax.set_ylabel("Density")
ax.legend(loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/confidence-histogram.pdf")
fig.savefig("../outputs/confidence-histogram.png")
