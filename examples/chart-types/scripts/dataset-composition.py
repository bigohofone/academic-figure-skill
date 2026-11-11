"""Figure 2: Composition of our instruction-tuning dataset by source. Web forums and textbooks together
make up 62% of the 1.24M examples.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/dataset-composition.json"))
names = list(data["sources"])
shares = list(data["sources"].values())
wedge_colors = [colors[f"series-{i + 1}"] for i in range(len(names))]

fig, ax = plt.subplots(figsize=(2.75, 2.75))
wedges, _ = ax.pie(shares, colors=wedge_colors, startangle=0, counterclock=False,
                   wedgeprops=dict(width=0.4, edgecolor="white", linewidth=0.5))
for w, name, share, color in zip(wedges, names, shares, wedge_colors):
    mid = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(mid), np.sin(mid)
    if share >= 0.06:
        ax.text(0.8 * x, 0.8 * y, f"{share:.0%}", ha="center", va="center", color=text_color(color))
        ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center")
    else:
        ax.annotate(f"{name} {share:.0%}", (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center",
                    arrowprops=dict(arrowstyle="-", color=colors["ink"], linewidth=0.5,
                                    relpos=(0, 0.5) if x > 0 else (1, 0.5)))
ax.text(0, 0, f"{data['total_examples'] / 1e6:.2f}M\nexamples", ha="center", va="center")

fit_height(fig, ax)
fig.savefig("../outputs/dataset-composition.pdf")
fig.savefig("../outputs/dataset-composition.png")
