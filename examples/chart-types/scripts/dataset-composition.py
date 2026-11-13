"""Sources of our 1.24M instruction-tuning examples. Web forums and textbooks together make up 62% of the data."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.colors

with open("../data/dataset-composition.json") as f:
    data = json.load(f)
total = data["total_examples"]
sources = data["sources"]
assert abs(sum(sources.values()) - 1) < 1e-9, "shares do not sum to 1"

# Largest first; parts under 3% join one "Other" part, drawn last
main = {name: v for name, v in sorted(sources.items(), key=lambda kv: -kv[1]) if v >= 0.03 and name != "Other"}
other = sum(v for name, v in sources.items() if name not in main)
parts = {**main, "Other": other} if other > 0 else main
names, values = list(parts), list(parts.values())


def share_text(v):
    return f"{v:.0%}" if v >= 0.1 else f"{100 * v:#.2g}%"


top_two = values[0] + values[1]
print("takeaway:", {"total": f"{total / 1e6:.3g}M", f"{names[0]} + {names[1]}": share_text(top_two),
                    **{n: share_text(v) for n, v in parts.items()}})
assert top_two > 0.5, "the two largest sources are not a majority"

part_colors = paper.make_part_colors(len(names))

fig, ax = plt.subplots(figsize=(2.75, 2.75))
wedges, _ = ax.pie(values, colors=part_colors, startangle=0, counterclock=False,
                   wedgeprops=dict(width=0.4, edgecolor="white", linewidth=rcParams["grid.linewidth"]))

# Shares inside their wedges; those too small for their wedge join the name outside, with a leader line
outside = ["Synthetic", "Other"]
for w, name, v, color in zip(wedges, names, values, part_colors):
    mid = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(mid), np.sin(mid)
    if name in outside:
        ax.annotate(f"{name} {share_text(v)}", (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center",
                    arrowprops=dict(arrowstyle="-", color=colors["ink"], linewidth=rcParams["grid.linewidth"],
                                    relpos=(0, 0.5) if x > 0 else (1, 0.5)))
    else:
        ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y), ha="left" if x > 0 else "right", va="center")
        ax.text(0.8 * x, 0.8 * y, share_text(v), ha="center", va="center", color="white" if np.dot(to_rgb(color), [0.299, 0.587, 0.114]) < 0.5 else "black")

ax.text(0, 0, f"{total / 1e6:.3g}M\nexamples", ha="center", va="center")

finalize_figure(fig, ax)
fig.savefig("../outputs/dataset-composition.pdf")
fig.savefig("../outputs/dataset-composition.png")
fig.savefig("../outputs/dataset-composition.svg")
