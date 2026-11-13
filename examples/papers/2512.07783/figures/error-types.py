"""Effects of reward mixtures on reasoning correctness and structural error types."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades, shift_lightness

colors = paper.colors

data = json.load(open("../data/error-types.json"))
mixtures = data["mixtures"]
values = np.array(data["percentage"])  # rows x columns x mixtures

change = values[:, :, 1:] - values[:, :, :1]
print("takeaway: change from the base model", np.round(change, 1).tolist())
assert (change[:, 0, 1:] > change[:, 0, :1]).all(), "process rewards do not raise correctness above outcome-only RL"
assert (change[:, 1, 1:] < change[:, 1, :1]).all(), "process rewards do not cut dependency mismatches below outcome-only RL"

fig, axes = plt.subplots(2, 3, figsize=(6.3, 6.3), layout="constrained")

# the base model and outcome-only RL grey, the two process-aware rewards in ours
bar_colors = make_shades(colors["neutral"], 2) + make_shades(colors["ours"], 2)
x = np.arange(len(mixtures))
for r, row_name in enumerate(data["rows"]):
    for c, column_name in enumerate(data["columns"]):
        ax = axes[r, c]
        panel = values[r, c]
        bars = ax.bar(x, panel, color=bar_colors, linewidth=0, label=mixtures)
        texts = [f"{panel[0]:.1f}%"] + [f"{v - panel[0]:+.1f}%".replace("-", "−") for v in panel[1:]]
        for label, color in zip(ax.bar_label(bars, labels=texts), bar_colors):
            label.set_color(shift_lightness(color, -1))
        ax.set_xticks([])
        ax.grid(axis="x", visible=False)
        if r == 0:
            ax.set_title(column_name)
    axes[r, 0].set_ylabel(row_name)

fig.supylabel("Percentage (%)")

axes[0, 0].legend(axes[0, 0].containers[0], mixtures)

# original height / width 259.2 / 691.2 = 0.38, 1.89 in printed; 2XS gives the closest height
finalize_figure(fig, axes, height="XS", min_width=0.7)
fig.savefig("../out/error-types.pdf")
