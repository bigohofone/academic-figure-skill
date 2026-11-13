"""Validation accuracy over a grid of learning rates and batch sizes. Accuracy peaks at 0.768 with learning rate 1e−4 and batch size 32, and drops at the largest learning rate and batch size."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.colors

data = json.load(open("../data/hyperparameter-grid.json"))
learning_rates = data["learning_rates"]
batch_sizes = data["batch_sizes"]
accuracy = np.array(data["accuracy"])  # accuracy[i][j]: learning rate i, batch size j

bi, bj = np.unravel_index(np.argmax(accuracy), accuracy.shape)
print("takeaway:", f"best {accuracy[bi, bj]:#.3g} at lr {learning_rates[bi]}, batch size {batch_sizes[bj]}")
assert accuracy[bi, bj] == accuracy.max(), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
im = ax.imshow(accuracy, aspect="auto", origin="lower")
for i in range(len(learning_rates)):
    for j in range(len(batch_sizes)):
        v = accuracy[i, j]
        ax.text(j, i, f"{v:#.3g}", ha="center", va="center", color=colors["paper"] if np.dot(to_rgb(im.cmap(im.norm(v))), [0.299, 0.587, 0.114]) < 0.5 else colors["ink"])
ax.set_xticks(range(len(batch_sizes)), labels=[str(b) for b in batch_sizes])
ax.set_yticks(range(len(learning_rates)), labels=[lr.replace("-", "−") for lr in learning_rates])
ax.set_xlabel("Batch size")
ax.set_ylabel("Learning rate")
ax.tick_params(length=0)
ax.grid(False)

finalize_figure(fig, ax)
fig.savefig("../outputs/hyperparameter-grid.pdf")
fig.savefig("../outputs/hyperparameter-grid.png")
fig.savefig("../outputs/hyperparameter-grid.svg")
