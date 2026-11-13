"""Confusion matrix of the Random Forest that predicts Yelp review star ratings. Each row is normalized over the reviews of its true rating, so the diagonal is the per-rating recall. The extreme ratings are recognized best (recall 0.82 for 1 star and 0.76 for 5 stars), while the middle ratings reach only 0.37 to 0.42, and 2-star reviews are predicted as 1 star (0.38) as often as correctly."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.colors

data = json.load(open("../data/confusion-matrix.json"))
labels = data["labels"]
matrix = np.array(data["matrix"])  # rows: true rating, columns: predicted rating, each row sums to about 1

recall = np.diag(matrix)
print("takeaway:", {f"{l} star": f"{r:#.2g}" for l, r in zip(labels, recall)}, "2 as 1:", f"{matrix[1, 0]:#.2g}")
assert min(recall[0], recall[4]) > max(recall[1:4]), "the takeaway does not hold"
assert matrix[1, 0] >= matrix[1, 1], "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
im = ax.imshow(matrix, aspect="auto", vmin=0, vmax=1)
ax.set_xticks(range(len(labels)), labels=labels)
ax.set_yticks(range(len(labels)), labels=labels)
ax.set_xlabel("Predicted label")
ax.set_ylabel("True label")
ax.tick_params(length=0)
ax.grid(False)
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        v = matrix[i, j]
        ax.text(j, i, f"{v:#.2g}", ha="center", va="center",
                color=colors["paper"] if np.dot(to_rgb(im.cmap(im.norm(v))), [0.299, 0.587, 0.114]) < 0.5 else colors["ink"])

finalize_figure(fig, ax)
fig.savefig("../outputs/confusion-matrix.pdf")
fig.savefig("../outputs/confusion-matrix.png")
