"""Figure 3: t-SNE embedding of ResNet-34 penultimate-layer features for CIFAR-10 test samples. Each point is one sample, 100 per class, colored by class. The classes form well-separated clusters: a 5-nearest-neighbour classifier on the 2-D embedding (leave-one-out, computed here) labels 93.4% of samples correctly."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from scipy.spatial import cKDTree

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/t-sne.json") as f:
    data = json.load(f)

# Takeaway number: leave-one-out 5-NN accuracy in the embedding
points = np.concatenate([np.c_[data[f"class_{i}"]["x"], data[f"class_{i}"]["y"]] for i in range(1, 11)])
labels = np.repeat(np.arange(10), 100)
_, neighbours = cKDTree(points).query(points, k=6)
votes = labels[neighbours[:, 1:]]
predicted = np.array([np.bincount(v, minlength=10).argmax() for v in votes])
print(f"5-NN accuracy = {(predicted == labels).mean():.1%}")

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
palette = plt.get_cmap("tab10").colors
for i in range(1, 11):
    ax.plot(data[f"class_{i}"]["x"], data[f"class_{i}"]["y"], "o",
            markeredgecolor=colors["ink"], markeredgewidth=paper.filled_edge_width,
            markerfacecolor=(*to_rgb(palette[i - 1]), 0.5), linestyle="none", label=f"Class {i}")

ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=4, frameon=False)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/t-sne.pdf")
fig.savefig("../outputs/t-sne.png")
