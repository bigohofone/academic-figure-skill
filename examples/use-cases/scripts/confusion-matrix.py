"""Figure 2: Confusion matrix of the Random Forest (500 trees, TF-IDF features) predicting Yelp star
ratings on the test set. Each row is normalized over the reviews with that true rating, so the
diagonal is per-class recall. Predictions skew to the extremes: 1- and 5-star reviews are mostly
correct (0.82 and 0.76), but 2-star reviews are predicted as 1-star as often as correctly (0.38 vs.
0.37), and 4-star reviews as 5-star (0.37 vs. 0.39).
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confusion-matrix.json") as f:
    data = json.load(f)
matrix = np.array(data["matrix"])
labels = data["labels"]

fig, ax = plt.subplots(figsize=(2.75, 3))
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=1)
for i in range(len(labels)):
    for j in range(len(labels)):
        v = matrix[i, j]
        ax.text(j, i, f"{v:.2g}", ha="center", va="center", color=text_color(im.cmap(im.norm(v))))
ax.set_xticks(range(len(labels)), labels=labels)
ax.set_yticks(range(len(labels)), labels=labels)
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")
fig.colorbar(im, ax=ax, label="Fraction of true label")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/confusion-matrix.pdf")
fig.savefig("../outputs/confusion-matrix.png")
