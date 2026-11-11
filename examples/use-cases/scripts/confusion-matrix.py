"""Figure 1: Confusion matrix of the Random Forest star-rating classifier on the Yelp test set. Values are normalized per true rating, so each row sums to 1 and the diagonal is per-class recall. Predictions are skewed towards the extremes: 1- and 5-star reviews are mostly correct (0.82 and 0.76), but 2-star reviews go to 1 star about as often as to 2 (0.38 vs 0.37), and 4-star reviews to 5 stars about as often as to 4 (0.37 vs 0.39)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confusion-matrix.json") as f:
    data = json.load(f)
labels = data["labels"]
matrix = np.array(data["matrix"])

fig, ax = plt.subplots(figsize=(2.75, 2))
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(labels)), labels=labels)
ax.set_yticks(range(len(labels)), labels=labels)
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")
for i in range(len(labels)):
    for j in range(len(labels)):
        v = matrix[i, j]
        ax.text(j, i, f"{v:.10g}", ha="center", va="center", color=text_color(im.cmap(im.norm(v))))
fig.colorbar(im, ax=ax, label="Fraction of true label")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/confusion-matrix.pdf")
fig.savefig("../outputs/confusion-matrix.png")
