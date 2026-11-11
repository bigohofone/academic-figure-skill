"""Figure 5: Training-loss landscape of ResNet-56 (5.89% test error) on CIFAR-10 around its trained
minimizer. Contours show L(θ* + αδ + βη) along two random filter-normalized directions δ (Direction
1) and η (Direction 2), redrawn from Li et al. (2018), Figure 5(b); the star marks the minimizer θ*.
With skip connections, the minimizer sits in a wide, nearly convex basin: the loss rises smoothly
from 0.1 at the center through roughly elliptical contours to 9.6 at the edges.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, Normalize

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/loss-landscape.json") as f:
    data = json.load(f)
levels = data["levels"]
cmap = ListedColormap(plt.get_cmap("viridis")(np.linspace(0, 0.85, 256)))
norm = Normalize(levels[0], levels[-1])

fig, ax = plt.subplots(figsize=(2.75, 2.4))
for line in data["contour_lines"]:
    xy = np.array(line["xy"])
    ax.plot(xy[:, 0], xy[:, 1], color=cmap(norm(line["level"])), linewidth=plt.rcParams["contour.linewidth"])
ax.plot(0, 0, "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=2 * plt.rcParams["lines.markersize"], linestyle="none", label="Trained minimizer")

ticks = [-1, -0.5, 0, 0.5, 1]
tick_labels = [f"{v:g}".replace("-", "−") for v in ticks]
ax.set_xlim(data["x_range"])
ax.set_ylim(data["y_range"])
ax.set_xticks(ticks, labels=tick_labels)
ax.set_yticks(ticks, labels=["", *tick_labels[1:]])
ax.grid(False)
ax.set_xlabel("Direction 1")
ax.set_ylabel("Direction 2")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=1, frameon=False)
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Training loss")

# keep the first of each group of level labels that would overlap at print size
fig.canvas.draw()
kept = []
for label in data["level_labels"]:
    t = ax.text(*label["xy"], f"{label['level']:.2g}", ha="center", va="center")
    box = t.get_window_extent().padded(fig.dpi / 72)  # the 1 pt gap fit_height asks for
    if any(box.overlaps(other) for other in kept):
        t.remove()
    else:
        kept.append(box)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/loss-landscape.pdf")
fig.savefig("../outputs/loss-landscape.png")
