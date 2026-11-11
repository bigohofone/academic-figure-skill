"""Confusion matrix of a Random Forest that predicts Yelp review ratings. Each row is normalized to the fraction of reviews with that true rating, so the diagonal is the recall of each rating. The extreme ratings are recognized best, with recall 0.82 for 1 star and 0.76 for 5 stars, while 2, 3 and 4 stars reach only 0.37, 0.42 and 0.39 and are mostly confused with their neighbouring ratings."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/confusion-matrix.json") as f:
    data = json.load(f)
labels = data["labels"]
matrix = np.array(data["matrix"])  # rows: true rating, columns: predicted rating


def fmt(v):
    # Values are given with 2 significant digits and shown unchanged.
    return f"{v:#.2g}".rstrip(".")


recall = np.diag(matrix)
print("takeaway:", {r: fmt(v) for r, v in zip(labels, recall)})
assert min(recall[0], recall[-1]) > max(recall[1:-1]), "the extreme ratings are not recalled best"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=1)
# No cell text: at this width "0.0069" collides with its neighbours (Collisions step 4);
# the cited recalls are in the caption.
ax.set_xticks(range(len(labels)), labels=labels)
ax.set_yticks(range(len(labels)), labels=labels)
ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")
ax.tick_params(length=0)
ax.grid(False)
fig.colorbar(im, ax=ax, label="Recall")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/confusion-matrix.pdf")
fig.savefig("../outputs/confusion-matrix.png")
