"""Training loss landscape of a ResNet-56 trained on CIFAR-10, around the trained minimizer. Contour lines of the training loss along two directions α and β, every third level labelled; the star marks the trained minimizer at the origin. The minimizer sits inside a single basin, enclosed by the lowest contour at a loss of 0.1, and the loss rises to 9.6 toward the edges."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import Normalize
from matplotlib.path import Path

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/loss-landscape.json") as f:
    data = json.load(f)
levels = data["levels"]
contour_lines = data["contour_lines"]

# Takeaway: the lowest contour is a closed curve around the minimizer at (0, 0).
lowest = [c for c in contour_lines if c["level"] == min(levels)]
assert len(lowest) == 1 and Path(lowest[0]["xy"]).contains_point((0, 0)), "the minimizer is not inside the lowest contour"
print("takeaway:", f"lowest level {min(levels):.2g} encloses (0, 0); highest level {max(levels):.2g}")

cmap = plt.get_cmap("viridis")
norm = Normalize(min(levels), max(levels))

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for line in contour_lines:
    xy = np.array(line["xy"])
    ax.plot(xy[:, 0], xy[:, 1], color=cmap(norm(line["level"])), linewidth=rcParams["contour.linewidth"])

# One label per labelled level, at its first given position; every LABEL_EVERY-th level.
LABEL_EVERY = 3  # every level, then every second, collide at this width
POSITION = {7.6: 1, 9.1: 1}  # level -> index of the given position to use, when the first collides
for level in levels[::LABEL_EVERY]:
    spots = [p["xy"] for p in data["level_labels"] if p["level"] == level]
    x, y = spots[POSITION.get(level, 0)]
    ax.text(x, y, f"{level:.2g}", ha="center", va="center", gid="contour-label",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))

ax.plot(0, 0, "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none")
ax.set_xlim(data["x_range"])
ax.set_ylim(data["y_range"])
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.grid(False)
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Training loss")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/loss-landscape.pdf")
fig.savefig("../outputs/loss-landscape.png")
