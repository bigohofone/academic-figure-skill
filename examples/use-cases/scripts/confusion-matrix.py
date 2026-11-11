"""Confusion matrix of a Random Forest predicting Yelp review star ratings. Each row is normalized over the reviews of that true rating, so the diagonal is the per-rating recall; the colors show each fraction. The extreme ratings are recognized best (recall 0.82 for 1 star and 0.76 for 5 stars), while 2 to 4 stars reach only 0.37 to 0.42 and are mostly confused with an adjacent rating."""

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
matrix = np.array(data["matrix"])

# Takeaway: extremes have the highest recall; middle ratings are mostly confused with neighbours.
recall = np.diag(matrix)
middle = recall[1:4]
print("takeaway: recall", {lab: f"{v:#.2g}" for lab, v in zip(labels, recall)})
assert min(recall[0], recall[4]) > max(middle), "the takeaway does not hold"
for i in range(1, 4):
    adjacent = matrix[i, i - 1] + matrix[i, i + 1]
    far = matrix[i].sum() - matrix[i, i] - adjacent
    print(f"true {labels[i]}: adjacent errors {adjacent:.2f}, farther errors {far:.2f}")
    assert adjacent > far, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(labels)), labels=labels)
ax.set_yticks(range(len(labels)), labels=labels)
ax.tick_params(length=0)
ax.grid(False)
ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")
fig.colorbar(im, ax=ax, label="Fraction of true rating")

fit_height(fig, ax, aspect=matrix.shape[0] / matrix.shape[1])
fig.savefig("../outputs/confusion-matrix.pdf")
fig.savefig("../outputs/confusion-matrix.png")
