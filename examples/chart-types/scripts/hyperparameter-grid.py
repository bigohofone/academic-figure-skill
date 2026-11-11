"""Figure 1: Validation accuracy over learning rate and batch size. The outlined cell marks the best setting. Learning rate 1e-4 with batch size 32 is best at 0.768, and accuracy drops at the largest learning rate, 3e-4, to 0.688–0.722."""

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

fig, ax = plt.subplots(figsize=(2.75, 2))
im = ax.imshow(accuracy, aspect="auto")
ax.set_xticks(range(len(batch_sizes)), labels=batch_sizes)
ax.set_yticks(range(len(learning_rates)), labels=learning_rates)
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Batch size")
ax.set_ylabel("Learning rate")
for i in range(len(learning_rates)):
    for j in range(len(batch_sizes)):
        v = accuracy[i, j]
        ax.text(j, i, f"{v:#.3g}", ha="center", va="center", color=text_color(im.cmap(im.norm(v))))
i, j = np.unravel_index(accuracy.argmax(), accuracy.shape)
ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"]))
fig.colorbar(im, ax=ax, label="Validation accuracy")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/hyperparameter-grid.pdf")
fig.savefig("../outputs/hyperparameter-grid.png")
