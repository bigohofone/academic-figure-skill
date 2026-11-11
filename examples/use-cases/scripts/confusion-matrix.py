"""Figure 1: Confusion matrix of the Random Forest that predicts Yelp review ratings. Each row is normalized to the reviews of its true rating, so the diagonal is the per-rating recall. The extreme ratings are recognized best (82% of 1-star and 76% of 5-star reviews), while the middle ratings are mostly confused with their neighbors: 2-star reviews are predicted as 1 star (38%) as often as correctly (37%)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confusion-matrix.json") as f:
    data = json.load(f)
labels = data["labels"]
matrix = np.array(data["matrix"])

fig, ax = plt.subplots(figsize=(2.75, 2.5))
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(labels)), labels=labels)
ax.set_yticks(range(len(labels)), labels=labels)
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")

# every cell's share of its row, as a whole percent
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        v = matrix[i, j]
        ax.text(j, i, f"{v:.0%}", ha="center", va="center", color=text_color(im.cmap(im.norm(v))))

cbar = fig.colorbar(im, ax=ax, label="Share of true label")
cbar.set_ticks([0, 0.5, 1], labels=["0%", "50%", "100%"])

fit_height(fig, ax, aspect=matrix.shape[0] / matrix.shape[1])
fig.savefig("../outputs/confusion-matrix.pdf")
fig.savefig("../outputs/confusion-matrix.png")
