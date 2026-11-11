"""Validation loss of our model over learning rate and weight decay. Both axes are log scale; filled bands step between the levels of the 13 × 13 runs, contour lines are drawn every 0.5 with every second one labelled, and the star marks the lowest loss. The loss is lowest, 1.91, at learning rate 0.000316 and weight decay 0.00562, and rises steeply toward small learning rates and small weight decay."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, text_color_on

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/hyperparameter-surface.json"))
learning_rate = np.array(data["learning_rate"])
weight_decay = np.array(data["weight_decay"])
val_loss = np.array(data["val_loss"])  # val_loss[i][j]: weight decay i, learning rate j
X, Y = np.meshgrid(learning_rate, weight_decay)

i, j = np.unravel_index(np.argmin(val_loss), val_loss.shape)
print("takeaway:", f"min {val_loss[i, j]:#.3g} at lr {learning_rate[j]:#.3g}, wd {weight_decay[i]:#.3g}",
      f"corner (smallest lr, wd) {val_loss[0, 0]:#.3g}")
assert val_loss[0, 0] == val_loss.max(), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.set_xscale("log")
ax.set_yscale("log")
step = 0.5
levels = np.arange(np.ceil(val_loss.min() / step) * step, val_loss.max(), step)  # 2 to 5.5: 8 levels
mesh = ax.contourf(X, Y, val_loss, levels=np.r_[val_loss.min(), levels, val_loss.max()])
lines = ax.contour(X, Y, val_loss, levels=levels, colors=colors["ink"], linewidths=rcParams["contour.linewidth"])

# level labels on the path from the minimum toward the farthest corner, where each level is crossed
lx, ly = np.log10(learning_rate), np.log10(weight_decay)
corners = [(0, 0), (0, -1), (-1, 0), (-1, -1)]
ci, cj = max(corners, key=lambda c: np.hypot(lx[c[1]] - lx[j], ly[c[0]] - ly[i]))
t = np.linspace(0, 1, 400)
path_i, path_j = i + t * ((ci % 13) - i), j + t * ((cj % 13) - j)
# the loss along the path, bilinear between the runs
i0, j0 = np.minimum(path_i.astype(int), 11), np.minimum(path_j.astype(int), 11)
fi, fj = path_i - i0, path_j - j0
along = (val_loss[i0, j0] * (1 - fi) * (1 - fj) + val_loss[i0 + 1, j0] * fi * (1 - fj)
         + val_loss[i0, j0 + 1] * (1 - fi) * fj + val_loss[i0 + 1, j0 + 1] * fi * fj)
positions = []
for level in levels:
    k = np.argmax(along >= level)
    positions.append((10 ** np.interp(path_j[k], np.arange(13), lx), 10 ** np.interp(path_i[k], np.arange(13), ly)))
# every second level labelled: 4.5, 5 and 5.5 crowd in the corner
labels = ax.clabel(lines, levels=levels[::2], fmt="%.2g", manual=positions[::2], fontsize=paper.contour_label_size)
for label in labels:
    label.set_color(text_color_on(mesh.cmap(mesh.norm(float(label.get_text())))))

ax.plot(learning_rate[j], weight_decay[i], "*", color=colors["ours"], markerfacecolor=colors["ours"],
        markersize=paper.highlight_size, linestyle="none")


def log_tick(v, _):
    """Powers of ten plain from 0.001, else 1e−4 with a true minus."""
    return f"{v:.10g}" if v >= 0.001 else f"1e{int(round(np.log10(v)))}".replace("-", "−")


for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_formatter(log_tick)
    axis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Learning rate")
ax.set_ylabel("Weight decay")
ax.grid(False)
fig.colorbar(mesh, ax=ax, label="Validation loss", ticks=levels)

finalize_figure(fig, ax, aspect=1.0)
fig.savefig("../outputs/hyperparameter-surface.pdf")
fig.savefig("../outputs/hyperparameter-surface.png")
