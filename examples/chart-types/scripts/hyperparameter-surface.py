"""Validation loss of our model over learning rate and weight decay. Both axes are log scale; colors blend between the 13 × 13 runs, the lines are contours of validation loss, and the star marks the lowest loss. The loss is lowest, 1.91, at learning rate 3.16 × 10⁻⁴ and weight decay 5.62 × 10⁻³, and rises fastest toward small learning rates and the largest learning rate."""

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
val_loss = np.array(data["val_loss"])  # rows: weight decay, columns: learning rate

i_min, j_min = np.unravel_index(np.argmin(val_loss), val_loss.shape)
print("takeaway:", f"min loss {val_loss[i_min, j_min]:#.3g} at lr {learning_rate[j_min]:.2e}, wd {weight_decay[i_min]:.2e}")
assert val_loss[i_min, j_min] < np.delete(val_loss.ravel(), np.argmin(val_loss)).min(), "the takeaway does not hold"
print("span:", val_loss.max() / val_loss.min())  # under 100x, so the loss itself is contoured

lo, hi, step = 2.0, 5.5, 0.5
levels = np.arange(lo, hi + step / 2, step)

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.set_xscale("log")
ax.set_yscale("log")
X, Y = np.meshgrid(learning_rate, weight_decay)
mesh = ax.pcolormesh(X, Y, val_loss, shading="gouraud")
lines = ax.contour(X, Y, val_loss, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])
ax.plot(learning_rate[j_min], weight_decay[i_min], "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none")

# Level labels along the path from the minimum toward the farthest corner (in log coordinates).
log_lr, log_wd = np.log10(learning_rate), np.log10(weight_decay)
interp = RegularGridInterpolator((log_wd, log_lr), val_loss)
corners = [(log_lr[c], log_wd[r]) for r in (0, -1) for c in (0, -1)]
start = np.array([log_lr[j_min], log_wd[i_min]])
corner = max(corners, key=lambda c: np.hypot(c[0] - start[0], c[1] - start[1]))
t = np.linspace(0, 1, 2001)
path = start[None, :] + t[:, None] * (np.array(corner) - start)[None, :]
z = interp(path[:, ::-1])
positions = []
for level in levels[::2]:  # every second level: the labels crowd toward the corner
    k = np.argmax(z >= level)
    positions.append((10 ** path[k, 0], 10 ** path[k, 1]))
labels = ax.clabel(lines, levels=levels[::2], fmt="%.2g", manual=positions)
for label in labels:
    label.set_color(text_color(mesh.cmap(mesh.norm(float(label.get_text())))))

ax.grid(False)
ax.set_xlabel("Learning rate")
ax.set_ylabel("Weight decay")
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_formatter(lambda v, _: f"{v:.10g}" if v >= 0.001 else f"1e{round(np.log10(v))}".replace("-", "−"))
    axis.set_minor_formatter(NullFormatter())
fig.colorbar(mesh, ax=ax, label="Validation loss")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/hyperparameter-surface.pdf")
fig.savefig("../outputs/hyperparameter-surface.png")
