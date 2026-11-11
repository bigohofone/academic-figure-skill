"""Composition of the instruction-tuning data by source. Web forums and textbooks together make up 62% of the 1.24M examples."""

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
total = data["total_examples"]
sources = data["sources"]
assert np.isclose(sum(sources.values()), 1), "shares do not sum to 1"

# Largest first, clockwise from 3 o'clock; "Other" last.
names = sorted((n for n in sources if n != "Other"), key=lambda n: -sources[n])
if "Other" in sources:
    names.append("Other")
shares = [sources[n] for n in names]
part_colors = [colors[f"series-{i + 1}"] for i in range(len(names))]

# Takeaway: the two largest sources make up most of the data.
top_two = sources["Web forums"] + sources["Textbooks"]
print("takeaway:", f"Web forums + Textbooks = {top_two:.0%}", f"total = {total / 1e6:.3g}M")
assert top_two > 0.5 and set(names[:2]) == {"Web forums", "Textbooks"}, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
wedges, _ = ax.pie(shares, colors=part_colors, startangle=0, counterclock=False,
                   wedgeprops=dict(width=0.4, edgecolor="white", linewidth=rcParams["grid.linewidth"]))

for name, share, color, w in zip(names, shares, part_colors, wedges):
    share_text = f"{share:.0%}" if share >= 0.1 else f"{100 * share:#.2g}%"
    mid = np.deg2rad((w.theta1 + w.theta2) / 2)
    x, y = np.cos(mid), np.sin(mid)
    if name in ("Synthetic", "Other"):  # too thin for its share inside: joined to its name, with a leader line
        ax.annotate(f"{name} {share_text}", (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center",
                    arrowprops=dict(arrowstyle="-", color=colors["ink"], linewidth=rcParams["grid.linewidth"],
                                    relpos=(0, 0.5) if x > 0 else (1, 0.5)))
    else:
        ax.annotate(name, (1.02 * x, 1.02 * y), xytext=(1.12 * x, 1.12 * y),
                    ha="left" if x > 0 else "right", va="center")
        ax.text(0.8 * x, 0.8 * y, share_text, ha="center", va="center", color=text_color(color))

ax.text(0, 0, f"{total / 1e6:.3g}M\nexamples", ha="center", va="center")

fit_height(fig, ax)
fig.savefig("../outputs/dataset-composition.pdf")
fig.savefig("../outputs/dataset-composition.png")
