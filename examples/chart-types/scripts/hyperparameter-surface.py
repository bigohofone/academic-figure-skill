"""Figure 1: Validation loss of our model over learning rate and weight decay. Both axes are log scale; colors blend between the 13 × 13 runs, and the star marks the lowest loss. The loss is lowest, 1.91, at learning rate 3.2e-4 and weight decay 5.6e-3, and stays below 2.0 in a narrow band around it."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.ticker import NullFormatter
from scipy.interpolate import RegularGridInterpolator

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/hyperparameter-surface.json") as f:
    data = json.load(f)
learning_rate = np.array(data["learning_rate"])
weight_decay = np.array(data["weight_decay"])
val_loss = np.array(data["val_loss"])  # val_loss[i][j]: weight decay i, learning rate j

fig, ax = plt.subplots(figsize=(2.75, 2.5))
ax.set_xscale("log")
ax.set_yscale("log")
X, Y = np.meshgrid(learning_rate, weight_decay)
mesh = ax.pcolormesh(X, Y, val_loss, shading="gouraud")
levels = np.arange(2.0, 5.0 + 0.25, 0.5)
lines = ax.contour(X, Y, val_loss, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])
ax.grid(False)

# level labels along the path from the minimum toward the farthest corner (lowest learning rate and weight decay)
i, j = np.unravel_index(val_loss.argmin(), val_loss.shape)
loss_at = RegularGridInterpolator((np.log10(weight_decay), np.log10(learning_rate)), val_loss)
t = np.linspace(0, 1, 2001)
path_lr = np.log10(learning_rate[j]) + t * (np.log10(learning_rate[0]) - np.log10(learning_rate[j]))
path_wd = np.log10(weight_decay[i]) + t * (np.log10(weight_decay[0]) - np.log10(weight_decay[i]))
path_loss = loss_at(np.column_stack([path_wd, path_lr]))
positions = []
for level in levels[:-1]:  # the label of 5 collides with 4.5 and is dropped
    k = np.argmax(path_loss >= level)  # first point past the level, walking out from the minimum
    positions.append((10 ** path_lr[k], 10 ** path_wd[k]))
labels = ax.clabel(lines, fmt="%.2g", manual=positions)
for label in labels:
    label.set_color(text_color(mesh.cmap(mesh.norm(float(label.get_text())))))

# the lowest loss
ax.plot(learning_rate[j], weight_decay[i], "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none")

for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_formatter(lambda v, _: f"{v:.10g}" if v >= 0.001 else f"1e{round(np.log10(v))}".replace("-", "−"))
    axis.set_minor_formatter(NullFormatter())
# the first y label collides with the first x label at the corner
ticks = [t for t in ax.get_yticks() if weight_decay[0] <= t <= weight_decay[-1]]
ax.set_yticks(ticks, labels=["", *[f"{t:.10g}" for t in ticks[1:]]])
ax.set_xlabel("Learning rate")
ax.set_ylabel("Weight decay")

cbar = fig.colorbar(mesh, ax=ax, label="Validation loss")
cbar.ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/hyperparameter-surface.pdf")
fig.savefig("../outputs/hyperparameter-surface.png")
