"""t-SNE embedding of ResNet-34 penultimate-layer features on CIFAR-10 test samples, 100 per class. Each color is one class. The ten classes form separate clusters: a 5-nearest-neighbour classifier on the 2-D coordinates, computed leave-one-out, assigns 93.4% of the 1000 samples to their own class."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/t-sne.json") as f:
    classes = json.load(f)

# takeaway: the classes form separate clusters; measured by a 5-nearest-neighbour classifier
# on the 2-D coordinates, each sample labelled by its neighbours (leave-one-out)
points = np.concatenate([np.c_[c["x"], c["y"]] for c in classes.values()])
labels = np.repeat(np.arange(len(classes)), [len(c["x"]) for c in classes.values()])
dist = ((points[:, None] - points[None]) ** 2).sum(-1)
np.fill_diagonal(dist, np.inf)
neighbours = np.argsort(dist, axis=1)[:, :5]
predicted = np.array([np.bincount(labels[n], minlength=len(classes)).argmax() for n in neighbours])
knn_accuracy = 100 * (predicted == labels).mean()
print("takeaway:", {"5-NN accuracy": f"{knn_accuracy:#.3g}%", "n": f"{round(len(labels))}"})
assert knn_accuracy > 90, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
tab10 = plt.get_cmap("tab10").colors
shapes = ["o", "s", "^", "D", "v", "<", ">", "P", "X", "*"]  # with the color, each class keeps apart in grayscale
for i, (name, c) in enumerate(classes.items()):
    ax.plot(c["x"], c["y"], shapes[i], markeredgecolor=colors["ink"], markeredgewidth=paper.filled_edge_width,
            markerfacecolor=(*to_rgb(tab10[i]), 0.5), linestyle="none", label=name.replace("class_", "Class "))

ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)
# above the panel, three rows of four; matplotlib fills columns first, so reorder to read across each row
handles, names = ax.get_legend_handles_labels()
ncol = 4
order = [i for c in range(ncol) for i in range(c, len(handles), ncol)]
# a figure legend: with no tick labels, finalize_figure leaves this panel to the constrained layout, which
# moves an ax.legend anchored above the panel a little further on every draw
fig.legend([handles[i] for i in order], [names[i] for i in order], loc="outside upper center", ncol=ncol, borderaxespad=0)

finalize_figure(fig, ax, aspect=1.0)
fig.savefig("../outputs/t-sne.pdf")
fig.savefig("../outputs/t-sne.png")
