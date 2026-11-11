"""Training-loss landscape of a ResNet-56 trained on CIFAR-10, along two directions α and β around the trained minimizer. Lines are contours of training loss from 0.1 to 9.6 in steps of 0.5, colored by level, with every third level labelled; the star marks the trained minimizer at (0, 0). The minimizer sits in a single basin, with loss rising from 0.1 near the center to 9.6 toward the edges."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import Normalize

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/loss-landscape.json") as f:
    data = json.load(f)
levels = data["levels"]
contour_lines = data["contour_lines"]
level_labels = data["level_labels"]

lo, hi = min(levels), max(levels)
print("takeaway:", f"levels {lo:.2g} to {hi:.2g}, {len(levels)} levels, step {levels[1] - levels[0]:.2g}")
drawn = {line["level"] for line in contour_lines}
assert drawn == set(levels), "the takeaway does not hold"

cmap = plt.get_cmap("viridis")
norm = Normalize(lo, hi)

fig, ax = plt.subplots(figsize=(2.75, 2.75))
for line in contour_lines:
    xy = np.array(line["xy"])
    ax.plot(xy[:, 0], xy[:, 1], color=cmap(norm(line["level"])), linewidth=rcParams["contour.linewidth"])
ax.plot(0, 0, "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none")

# One label per level, at its first given position; every third level, as every second
# has no set of given positions that clear each other.
LABEL_EVERY = 3
POSITION = {9.1: 1, 7.6: 1}  # level -> index of the given position to use, when the first one collides
for level in levels[::LABEL_EVERY]:
    options = [p["xy"] for p in level_labels if p["level"] == level]
    x, y = options[POSITION.get(level, 0)]
    ax.text(x, y, f"{level:.2g}", ha="center", va="center", gid="contour-label",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))

ax.set_xlim(*data["x_range"])
ax.set_ylim(*data["y_range"])
ax.grid(False)
ax.set_xlabel("α")
ax.set_ylabel("β")
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Training loss")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/loss-landscape.pdf")
fig.savefig("../outputs/loss-landscape.png")
