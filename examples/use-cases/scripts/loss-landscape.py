"""Training-loss landscape of ResNet-56 on CIFAR-10 around the trained minimizer. Contour lines are drawn every 0.5 in loss, colored by level, with every second level labelled; the star marks the trained minimizer at (0, 0). The levels from 0.1 to 3.1 form single nested rings around the minimizer, while from 3.6 up the surface breaks into several separate regions."""

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

data = json.load(open("../data/loss-landscape.json"))
levels = data["levels"]
contour_lines = data["contour_lines"]
level_labels = data["level_labels"]

# takeaway: up to which level each level is one line around the minimizer
pieces = {lv: [np.array(c["xy"]) for c in contour_lines if c["level"] == lv] for lv in levels}
rings = [lv for lv in levels if len(pieces[lv]) == 1 and Path(pieces[lv][0]).contains_point((0, 0))]
first_split = min(lv for lv in levels if len(pieces[lv]) > 1)
print("takeaway:", f"single rings {rings[0]:.2g} to {rings[-1]:.2g}; split from {first_split:.2g}")
assert rings == [lv for lv in levels if lv < first_split], "the takeaway does not hold"

cmap = plt.get_cmap("viridis")
norm = Normalize(min(levels), max(levels))

fig, ax = plt.subplots(figsize=(2.75, 2.75))
for c in contour_lines:
    xy = np.array(c["xy"])
    ax.plot(xy[:, 0], xy[:, 1], color=cmap(norm(c["level"])), linewidth=rcParams["contour.linewidth"])

# every second level labelled (9.1 and 9.6 have no free position), once, at its first given position,
# turned along its line
label_every = 2
moved = {8.1: 1, 9.1: 1}  # level: index of its given position, for a label moved off a collision
for lv in levels[::label_every]:
    x, y = [p["xy"] for p in level_labels if p["level"] == lv][moved.get(lv, 0)]
    line = min(pieces[lv], key=lambda xy: np.hypot(*(xy - (x, y)).T).min())
    k = int(np.argmin(np.hypot(*(line - (x, y)).T)))
    k = min(max(k, 1), len(line) - 2)
    angle = (np.degrees(np.arctan2(line[k + 1, 1] - line[k - 1, 1], line[k + 1, 0] - line[k - 1, 0])) + 90) % 180 - 90
    ax.text(x, y, f"{lv:.2g}", ha="center", va="center", rotation=angle, rotation_mode="anchor",
            transform_rotates_text=True, fontsize=paper.contour_label_size, gid="contour-label",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))

ax.plot(0, 0, "*", color=colors["ours"], markerfacecolor=colors["ours"], markersize=paper.highlight_size,
        linestyle="none")
ax.set_xlim(*data["x_range"])
ax.set_ylim(*data["y_range"])
ax.set_xlabel("α")
ax.set_ylabel("β")
ax.grid(False)
fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Training loss")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/loss-landscape.pdf")
fig.savefig("../outputs/loss-landscape.png")
