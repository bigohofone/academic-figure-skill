"""Validation loss of our model over learning rate and weight decay. Both axes are logarithmic; colors blend between the 13 × 13 runs, every second contour level is labelled, and the star marks the lowest loss. The loss is lowest, 1.91, at a learning rate of 3.16×10⁻⁴ and a weight decay of 0.00562, and rises toward every edge of the sweep."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/hyperparameter-surface.json") as f:
    data = json.load(f)
lr = np.array(data["learning_rate"])
wd = np.array(data["weight_decay"])
loss = np.array(data["val_loss"])  # rows: weight decay, columns: learning rate
assert loss.max() / loss.min() < 100  # under 100x: contour the loss itself, not its log

i_min, j_min = np.unravel_index(loss.argmin(), loss.shape)
sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
m, e = f"{lr[j_min]:.2e}".split("e")
print("takeaway:", f"min {loss.min():#.3g} at lr {float(m):#.3g}×10{str(int(e)).translate(sup)}, wd {wd[i_min]:#.3g}")
assert 0 < i_min < len(wd) - 1 and 0 < j_min < len(lr) - 1, "the minimum lies on the edge of the sweep"

# Levels at round values inside the data's range, 6 to 8 at half width.
step = 0.5
levels = np.arange(np.ceil(loss.min() / step) * step, loss.max(), step)
LABEL_EVERY = 2  # every level collides at the corner (Collisions step 4)

# Label positions: along the path (in log space) from the minimum to the farthest corner,
# where the loss crosses each level.
corners = [(0, 0), (0, len(lr) - 1), (len(wd) - 1, 0), (len(wd) - 1, len(lr) - 1)]
far_i, far_j = max(corners, key=lambda c: (np.hypot(c[0] - i_min, c[1] - j_min), loss[c]))
t = np.linspace(0, 1, 400)
path_i = i_min + t * (far_i - i_min)
path_j = j_min + t * (far_j - j_min)
log_wd = np.interp(path_i, np.arange(len(wd)), np.log10(wd))
log_lr = np.interp(path_j, np.arange(len(lr)), np.log10(lr))
from scipy.interpolate import RegularGridInterpolator
path_z = RegularGridInterpolator((np.log10(wd), np.log10(lr)), loss)(np.column_stack([log_wd, log_lr]))
positions = []
for level in levels[::LABEL_EVERY]:
    k = np.argmax(path_z >= level)
    if path_z[k] >= level and k > 0:
        positions.append((10 ** log_lr[k], 10 ** log_wd[k]))

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.set_xscale("log")
ax.set_yscale("log")
LR, WD = np.meshgrid(lr, wd)
mesh = ax.pcolormesh(LR, WD, loss, shading="gouraud")
lines = ax.contour(LR, WD, loss, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])
labels = ax.clabel(lines, fmt="%.2g", manual=positions)
for label in labels:
    label.set_color(text_color(mesh.cmap(mesh.norm(float(label.get_text())))))
ax.plot(lr[j_min], wd[i_min], "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none")
# Log ticks: plain powers of ten from 0.001, 1e−4 below.
log_tick = lambda v, _: f"{v:.10g}" if v >= 1e-3 else f"1e{round(np.log10(v))}".replace("-", "−")
ax.xaxis.set_major_formatter(log_tick)
ax.yaxis.set_major_formatter(log_tick)
ax.xaxis.set_minor_formatter(NullFormatter())
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Learning rate")
ax.set_ylabel("Weight decay")
ax.grid(False)
fig.colorbar(mesh, ax=ax, label="Validation loss")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/hyperparameter-surface.pdf")
fig.savefig("../outputs/hyperparameter-surface.png")
