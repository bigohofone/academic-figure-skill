"""Validation accuracy over a grid of learning rates and batch sizes. The outlined cell marks the best setting. Accuracy peaks at 0.768 with learning rate 1e−4 and batch size 32, and falls off toward the largest learning rate and batch size."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/hyperparameter-grid.json") as f:
    data = json.load(f)
learning_rates = data["learning_rates"]
batch_sizes = data["batch_sizes"]
accuracy = np.array(data["accuracy"])

best_i, best_j = np.unravel_index(np.argmax(accuracy), accuracy.shape)
print("takeaway:", f"best {accuracy[best_i, best_j]:#.3g} at lr {learning_rates[best_i]}, batch size {batch_sizes[best_j]}")
assert accuracy[best_i, best_j] == accuracy.max() and (accuracy == accuracy.max()).sum() == 1, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
im = ax.imshow(accuracy, aspect="auto", origin="lower")
ax.set_xticks(range(len(batch_sizes)), labels=[str(b) for b in batch_sizes])
ax.set_yticks(range(len(learning_rates)), labels=[lr.replace("-", "−") for lr in learning_rates])
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Batch size")
ax.set_ylabel("Learning rate")
for i in range(accuracy.shape[0]):
    for j in range(accuracy.shape[1]):
        v = accuracy[i, j]
        ax.text(j, i, f"{v:#.3g}", ha="center", va="center", color=text_color(im.cmap(im.norm(v))))
ax.add_patch(plt.Rectangle((best_j - 0.5, best_i - 0.5), 1, 1, fill=False,
                           edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"]))
fig.colorbar(im, ax=ax, label="Validation accuracy")

fit_height(fig, ax, aspect=accuracy.shape[0] / accuracy.shape[1])
fig.savefig("../outputs/hyperparameter-grid.pdf")
fig.savefig("../outputs/hyperparameter-grid.png")
