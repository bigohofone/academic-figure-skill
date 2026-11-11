"""Figure 1: Training loss landscape around a ResNet-56 trained on CIFAR-10. Contour lines are colored by training loss in steps of 0.5; the star marks the trained minimizer at (0, 0). The minimizer sits in one wide, nearly convex basin: the training loss stays below 2.1 within about 0.4 of it along both directions."""

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

fig, ax = plt.subplots(figsize=(2.75, 2.5))
cmap = plt.get_cmap("viridis")
norm = Normalize(min(levels), max(levels))
lines = []  # to cut the gaps for the labels
for line in data["contour_lines"]:
    xy = np.array(line["xy"])
    # the same polyline with extra points every 0.005 along it, so a label's gap can be cut cleanly
    along = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]
    s = np.union1d(along, np.arange(0, along[-1], 0.005))
    x, y = np.interp(s, along, xy[:, 0]), np.interp(s, along, xy[:, 1])
    (handle,) = ax.plot(x, y, color=cmap(norm(line["level"])), linewidth=rcParams["contour.linewidth"])
    lines.append(handle)
ax.set_xlim(data["x_range"])
ax.set_ylim(data["y_range"])
ax.grid(False)

# one label per level, at the first given position that does not collide with an earlier label
# (5.6 to 9.1 take a later position; 9.6 collides at every position and is dropped)
position = {5.6: 1, 6.6: 1, 7.6: 3, 8.1: 3, 8.6: 1, 9.1: 1}
for level in levels:
    if level == 9.6:
        continue
    x, y = [label["xy"] for label in data["level_labels"] if label["level"] == level][position.get(level, 0)]
    ax.text(x, y, f"{level:.2g}", ha="center", va="center", gid="contour-label")

# the trained minimizer
ax.plot(0, 0, "*", color=colors["ours"], markerfacecolor=colors["ours"], markersize=paper.highlight_size,
        linestyle="none")

ax.set_xlabel("Direction 1")
ax.set_ylabel("Direction 2")
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ticks = [t for t in ax.get_yticks() if -1 <= t <= 1]
ax.set_yticks(ticks, labels=["", *[f"{t:.10g}".replace("-", "−") for t in ticks[1:]]])

fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="Training loss")

fit_height(fig, ax, aspect=1.0)

# cut a gap in the lines under each label, as ax.clabel does (the given positions are not always on their own level's line)
fig.canvas.draw()
for text in ax.texts:
    box = text.get_window_extent().padded(fig.dpi / 72).transformed(ax.transData.inverted())
    for line in lines:
        x, y = line.get_data()
        inside = (box.x0 < x) & (x < box.x1) & (box.y0 < y) & (y < box.y1)
        line.set_data(np.where(inside, np.nan, x), np.where(inside, np.nan, y))

fig.savefig("../outputs/loss-landscape.pdf")
fig.savefig("../outputs/loss-landscape.png")
