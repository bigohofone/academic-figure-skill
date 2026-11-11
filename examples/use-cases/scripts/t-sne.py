"""Figure 1: t-SNE embedding of penultimate-layer features of a ResNet-34 trained on CIFAR-10, for CIFAR-10 test samples. Each color is one of the ten classes, 100 samples each, numbered in the original paper's order. All ten classes form separate clusters, consistent with class-conditional Gaussian features."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/t-sne.json"))

fig, ax = plt.subplots(figsize=(2.75, 2.75))
for i, color in enumerate(plt.get_cmap("tab10").colors, start=1):
    points = data[f"class_{i}"]
    ax.plot(points["x"], points["y"], "o", markeredgecolor=colors["ink"], markeredgewidth=paper.filled_edge_width, markerfacecolor=(*to_rgb(color), 0.5),
            linestyle="none", label=f"Class {i}")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=4, frameon=False)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/t-sne.pdf")
fig.savefig("../outputs/t-sne.png")
