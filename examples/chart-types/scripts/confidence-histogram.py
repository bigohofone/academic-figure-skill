"""Figure 1: Distribution of the model's confidence on correct and incorrect answers. Histograms are
normalized to density (1,800 correct and 420 incorrect answers); dashed lines mark each group's
mean. Correct answers concentrate at high confidence (mean 0.834), while incorrect ones spread
across the whole range (mean 0.575), so confidence separates the two.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confidence-histogram.json") as f:
    data = json.load(f)

series = [("Correct", data["correct"], colors["series-1"]), ("Incorrect", data["incorrect"], colors["series-2"])]
bins = np.histogram_bin_edges(np.concatenate([data["correct"], data["incorrect"]]), bins="auto")

fig, ax = plt.subplots(figsize=(2.75, 2))
for name, values, color in series:
    ax.hist(values, bins=bins, density=True, histtype="stepfilled", color=color, alpha=0.2, linewidth=0)
    ax.hist(values, bins=bins, density=True, histtype="step", color=color, label=name)
    mean = np.mean(values)
    ax.axvline(mean, linestyle="--", linewidth=paper.dashed_width, color=darken(color))
    ax.annotate(f"{mean:#.3g}", (mean, 1), xycoords=("data", "axes fraction"), xytext=(0, 2),
                textcoords="offset points", ha="center", va="bottom", color=darken(color))
ax.grid(axis="x", visible=False)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))
ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))
ax.set_xlabel("Confidence")
ax.set_ylabel("Density")
ax.legend(loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/confidence-histogram.pdf")
fig.savefig("../outputs/confidence-histogram.png")
