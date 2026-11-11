"""Figure 1: Sources of our 1.24M instruction-tuning examples. Web forums and textbooks together supply 62% of the examples."""

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
# largest first, "Other" last
sources = sorted((kv for kv in data["sources"].items() if kv[0] != "Other"), key=lambda kv: -kv[1])
sources += [("Other", data["sources"]["Other"])]
names = [n for n, _ in sources]
shares = [s for _, s in sources]
wedge_colors = [colors[f"series-{i + 1}"] for i in range(len(names))]

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
wedges, _ = ax.pie(shares, colors=wedge_colors, startangle=0, counterclock=False,
                   wedgeprops=dict(width=0.4, edgecolor="white", linewidth=rcParams["grid.linewidth"]))

for w, name, share, color in zip(wedges, names, shares, wedge_colors):
    mid = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(mid), np.sin(mid)
    if share >= 0.1:
        ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center")
        ax.text(0.8 * x, 0.8 * y, f"{share:.0%}", ha="center", va="center", color=text_color(color))
    else:  # too narrow for its share inside: joined to its name outside, with a leader line
        ax.annotate(f"{name} {share:.0%}", (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center",
                    arrowprops=dict(arrowstyle="-", color=colors["ink"], linewidth=rcParams["grid.linewidth"],
                                    relpos=(0, 0.5) if x > 0 else (1, 0.5)))

total = data["total_examples"]
ax.text(0, 0, f"{total / 1e6:.2f}M\nexamples", ha="center", va="center")

fit_height(fig, ax)
fig.savefig("../outputs/dataset-composition.pdf")
fig.savefig("../outputs/dataset-composition.png")
