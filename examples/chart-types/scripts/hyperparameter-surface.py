"""Figure 1: Validation loss over learning rate and weight decay. Both axes are log scale; colors blend between the 13 × 13 runs, and the star marks the lowest loss. The loss is lowest, 1.91, at learning rate 3e-4 and weight decay 6e-3, and rises to 3.76–4.55 at the largest learning rate, 1e-2, where training diverges."""

import json
import math
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
val_loss = np.array(data["val_loss"])
X, Y = np.meshgrid(learning_rate, weight_decay)
levels = np.arange(2.0, 4.5 + 0.25, 0.5)

# label positions: where the loss crosses each level on the straight path (in log space)
# from the minimum to the farthest corner, where the lines are farthest apart
i_min, j_min = np.unravel_index(val_loss.argmin(), val_loss.shape)
n = len(weight_decay) - 1
corners = [(0, 0), (0, n), (n, 0), (n, n)]
i_far, j_far = max(corners, key=lambda c: math.hypot(c[0] - i_min, c[1] - j_min))
t = np.linspace(0, 1, 1000)
path_i, path_j = i_min + t * (i_far - i_min), j_min + t * (j_far - j_min)
loss_on_path = RegularGridInterpolator((np.arange(n + 1), np.arange(n + 1)), val_loss)(np.column_stack([path_i, path_j]))
positions = []
for level in levels:
    k = np.argmax(loss_on_path >= level)
    lr = np.interp(path_j[k], np.arange(n + 1), np.log10(learning_rate))
    wd = np.interp(path_i[k], np.arange(n + 1), np.log10(weight_decay))
    positions.append((10**lr, 10**wd))

fig, ax = plt.subplots(figsize=(2.75, 2))
ax.set_xscale("log")
ax.set_yscale("log")
mesh = ax.pcolormesh(X, Y, val_loss, shading="gouraud")
lines = ax.contour(X, Y, val_loss, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])
labels = ax.clabel(lines, fmt="%.2g", manual=positions)
for label in labels:
    label.set_color(text_color(mesh.cmap(mesh.norm(float(label.get_text())))))
ax.plot(learning_rate[j_min], weight_decay[i_min], "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none", label="Lowest loss")
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_formatter(lambda v, _: f"{v:g}" if v >= 1e-3 else f"1e{round(math.log10(v))}")
    axis.set_minor_formatter(NullFormatter())
ax.grid(False)
ax.set_xlabel("Learning rate")
ax.set_ylabel("Weight decay")
lo, hi = ax.get_ylim()
ticks = [t for t in ax.get_yticks() if lo <= t <= hi]
ax.set_yticks(ticks, labels=["", *[f"{t:g}" if t >= 1e-3 else f"1e{round(math.log10(t))}" for t in ticks[1:]]])
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=1, frameon=False)
fig.colorbar(mesh, ax=ax, label="Validation loss")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/hyperparameter-surface.pdf")
fig.savefig("../outputs/hyperparameter-surface.png")
