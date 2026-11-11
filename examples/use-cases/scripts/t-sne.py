"""t-SNE embedding of ResNet-34 penultimate-layer features for CIFAR-10 test samples. Each point is one sample (100 per class), colored by its class. The classes form separate clusters: a 5-nearest-neighbour majority vote in the embedding, computed here, recovers the class of 93.4% of the 1000 samples."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/t-sne.json") as f:
    classes = json.load(f)

# Takeaway: classes separate in the embedding, measured by leave-one-out 5-NN accuracy in 2-D.
points = np.concatenate([np.column_stack([c["x"], c["y"]]) for c in classes.values()])
labels = np.repeat(np.arange(len(classes)), [len(c["x"]) for c in classes.values()])
dist = np.linalg.norm(points[:, None] - points[None], axis=-1)
np.fill_diagonal(dist, np.inf)
neighbours = labels[np.argsort(dist, axis=1)[:, :5]]
votes = np.array([np.bincount(row, minlength=len(classes)).argmax() for row in neighbours])
knn_acc = (votes == labels).mean()
print("takeaway:", f"5-NN accuracy = {100 * knn_acc:#.3g}%", f"n = {len(labels)}")
assert knn_acc > 0.5, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))

palette = plt.get_cmap("tab10").colors
for i, (name, c) in enumerate(classes.items()):
    ax.plot(c["x"], c["y"], "o", markeredgecolor=colors["ink"], markeredgewidth=paper.filled_edge_width,
            markerfacecolor=(*to_rgb(palette[i]), 0.5), linestyle="none", label=f"Class {i + 1}")

ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)

handles, names = ax.get_legend_handles_labels()
ncol = 4
order = [i for c in range(ncol) for i in range(c, len(names), ncol)]
ax.legend([handles[i] for i in order], [names[i] for i in order], loc="lower center", bbox_to_anchor=(0.5, 1),
          borderaxespad=0.5, ncol=ncol, frameon=False)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/t-sne.pdf")
fig.savefig("../outputs/t-sne.png")
