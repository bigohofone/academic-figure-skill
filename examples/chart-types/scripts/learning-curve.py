"""Figure [TODO: number]: Validation accuracy on CIFAR-100 versus training epoch. Lines show the mean and shaded bands ±1 std over 5 seeds; dashed horizontal lines and circles mark the best mean accuracy of Ours and Mixup. Ours reaches a best accuracy of 0.915, above Mixup (0.897) and the Baseline (0.882)."""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import Normalize, to_rgb
from matplotlib.patches import Patch
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")  # the style from DESIGN.md's tokens; colors["series-1"], colors["ours"], …

with open("../data/learning-curve.json") as f:
    data = json.load(f)
epochs = np.array(data["epochs"])

# ICLR, one panel: half the text width
fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")

# ours in color; the baselines grey, told apart by line style in ascending order of best accuracy
series = [
    ("Ours", colors["ours"], "-"),
    ("Baseline", colors["neutral"], "-"),
    ("Mixup", colors["neutral"], "--"),
]
for name, color, style in series:
    runs = np.array(data["accuracy"][name])
    mean, std = runs.mean(axis=0), runs.std(axis=0)
    width = rcParams["lines.linewidth"] if style == "-" else paper.dashed_width
    ax.plot(epochs, mean, linestyle=style, linewidth=width, color=color, label=name)
    ax.fill_between(epochs, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)

# the comparison is not settled by the task: mark the best mean accuracy of ours and its closest
# competitor (the Baseline's label collides with theirs; its value is in the caption)
for (name, color, style), below in zip([series[0], series[2]], [False, True]):
    mean = np.array(data["accuracy"][name]).mean(axis=0)
    best = mean.argmax()
    mark_value(ax, epochs[best], mean[best], f"{mean[best]:#.3g}", color, below=below)

ax.set_xlabel("Epoch")
ax.set_ylabel("Validation accuracy")
ax.grid(True)
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/learning-curve.pdf")
fig.savefig("../outputs/learning-curve.png")
