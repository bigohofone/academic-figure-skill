"""t-SNE embedding of ResNet-34 penultimate-layer features for CIFAR-10 test samples. Each point is one of 100 samples per class, colored by its class. The ten classes form separate clusters: a 5-nearest-neighbour classifier in the 2-D embedding, computed leave-one-out, labels 93% of the samples correctly."""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/t-sne.json") as f:
    data = json.load(f)
names = [f"class_{i}" for i in range(1, 11)]
class_colors = plt.get_cmap("tab10").colors

# takeaway: leave-one-out 5-NN accuracy in the embedding
points = np.concatenate([np.column_stack([data[n]["x"], data[n]["y"]]) for n in names])
labels = np.concatenate([[i] * len(data[n]["x"]) for i, n in enumerate(names)])
dist = np.linalg.norm(points[:, None] - points[None], axis=-1)
np.fill_diagonal(dist, np.inf)
neighbours = labels[np.argsort(dist, axis=1)[:, :5]]
predicted = np.array([np.bincount(row, minlength=10).argmax() for row in neighbours])
knn_accuracy = np.mean(predicted == labels)
print("takeaway:", f"5-NN accuracy {knn_accuracy:.0%}", f"n = {len(labels)}")
assert knn_accuracy > 0.8, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for i, name in enumerate(names):
    ax.plot(data[name]["x"], data[name]["y"], "o", markeredgecolor=colors["ink"],
            markeredgewidth=paper.filled_edge_width, markerfacecolor=(*to_rgb(class_colors[i]), 0.5),
            linestyle="none", label=f"Class {i + 1}")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)

ncol = math.ceil(len(names) / 3)
handles, labels_ = ax.get_legend_handles_labels()
order = [i for c in range(ncol) for i in range(c, len(names), ncol)]
ax.legend([handles[i] for i in order], [labels_[i] for i in order], loc="lower center", bbox_to_anchor=(0.5, 1),
          borderaxespad=0.5, ncol=ncol, frameon=False)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/t-sne.pdf")
fig.savefig("../outputs/t-sne.png")
