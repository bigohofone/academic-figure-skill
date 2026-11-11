"""Figure 1: Loss landscape of ResNet-56 (5.89% test error) on CIFAR-10, redrawn from Li et al. (2018), Figure 5(b). Contour lines show the training loss L(θ* + αδ + βη) along two random filter-normalized directions; the star marks the trained minimizer θ* at the origin. Lines are drawn every 0.5 from 0.1 to 9.6. With skip connections, the minimizer sits in a wide, nearly convex basin: the contours around it are smooth, nested and roughly elliptical up to a loss of about 3."""

import json
import sys
import warnings

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

cmap = plt.get_cmap("viridis")
norm = Normalize(min(levels), max(levels))

fig, ax = plt.subplots(figsize=(2.75, 2))
for line in data["contour_lines"]:
    x, y = np.array(line["xy"]).T
    ax.plot(x, y, color=cmap(norm(line["level"])), linewidth=rcParams["contour.linewidth"])
level_labels = []
for label in data["level_labels"]:
    x, y = label["xy"]
    level_labels.append(ax.text(x, y, f"{label['level']:.2g}", ha="center", va="center", gid="contour-label"))
ax.plot(0, 0, "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none", label="Trained minimizer")
ax.set_xlim(data["x_range"])
ax.set_ylim(data["y_range"])
ax.set_xticks([-1, -0.5, 0, 0.5, 1], labels=["−1", "−0.5", "0", "0.5", "1"])
ax.set_yticks([-1, -0.5, 0, 0.5, 1], labels=["", "−0.5", "0", "0.5", "1"])
ax.grid(False)
ax.set_xlabel("Direction 1")
ax.set_ylabel("Direction 2")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=1, frameon=False)
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Training loss")

# measure the labels at the printed size, then drop each one that overlaps a kept label or leaves the panel
with warnings.catch_warnings(action="ignore"):
    fit_height(fig, ax, aspect=1.0)
fig.canvas.draw()
panel = ax.get_window_extent()
kept = []
for t in level_labels:
    box = t.get_window_extent().padded(fig.dpi / 72)
    inside = panel.x0 <= box.x0 and box.x1 <= panel.x1 and panel.y0 <= box.y0 and box.y1 <= panel.y1
    if inside and not any(box.overlaps(k) for k in kept):
        kept.append(box)
    else:
        t.remove()

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/loss-landscape.pdf")
fig.savefig("../outputs/loss-landscape.png")
