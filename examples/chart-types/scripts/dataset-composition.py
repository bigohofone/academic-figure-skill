"""Figure 2: Composition of the instruction-tuning dataset by source. The ring shows the share of the 1.24M examples from each source. Web forums (38%) and textbooks (24%) make up 62% of the data."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dataset-composition.json") as f:
    data = json.load(f)
names = list(data["sources"])
shares = list(data["sources"].values())
series_colors = [colors[f"series-{i + 1}"] for i in range(len(names))]

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
wedges, _ = ax.pie(shares, colors=series_colors, startangle=0, counterclock=False,
                   wedgeprops=dict(width=0.4, edgecolor="white", linewidth=rcParams["grid.linewidth"]))
for w, name, share, color in zip(wedges, names, shares, series_colors):
    mid = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(mid), np.sin(mid)
    if name in ["Synthetic", "Other"]:  # wedges too thin for their share inside the ring
        ax.annotate(f"{name} {share:.0%}", (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center",
                    arrowprops=dict(arrowstyle="-", color=colors["ink"], linewidth=rcParams["grid.linewidth"],
                                    relpos=(0, 0.5) if x > 0 else (1, 0.5)))
    else:
        ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y), ha="left" if x > 0 else "right", va="center")
        ax.text(0.8 * x, 0.8 * y, f"{share:.0%}", ha="center", va="center", color=text_color(color))
ax.text(0, 0, f"{data['total_examples'] / 1e6:.2f}M\nexamples", ha="center", va="center")

fit_height(fig, ax)
fig.savefig("../outputs/dataset-composition.pdf")
fig.savefig("../outputs/dataset-composition.png")
