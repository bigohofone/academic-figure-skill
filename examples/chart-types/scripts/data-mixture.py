"""Figure 1: Pretraining data mixture over training under the three-stage curriculum. Dashed lines mark the stage switches at 30k and 70k steps. The share of web text falls from 62% to 40% while code grows from 12% to 24% and math from 6% to 18%."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/data-mixture.json") as f:
    data = json.load(f)
steps = np.array(data["steps"]) / 1000
shares = data["shares"]
color_of = {name: colors[f"series-{i + 1}"] for i, name in enumerate(shares)}
order = ["Wikipedia", "Web", "Books", "Code", "Math"]  # the flattest share at the bottom

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.stackplot(steps, [shares[name] for name in order], colors=[color_of[name] for name in order],
             step="post", edgecolor="white", linewidth=rcParams["grid.linewidth"])
for switch in [30, 70]:
    ax.axvline(switch, linestyle="--", linewidth=paper.dashed_width, color="white")

ax.set_xlim(0, 100)
ax.set_ylim(0, 1)
ax.set_xticks([0, 30, 70, 100])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("Training step (k)")
ax.set_ylabel("Share of tokens")
ax.set_axisbelow(False)
ax.grid(axis="x", visible=False)

bottom = np.zeros(len(steps))
for name in order:
    top = bottom + np.array(shares[name])
    ax.annotate(name, (1, (bottom[-1] + top[-1]) / 2), xycoords=("axes fraction", "data"),
                xytext=(4, 0), textcoords="offset points", va="center")
    if name in ["Web", "Code", "Math"]:
        for start, end in [(0, 30), (30, 70), (70, 100)]:
            if (name, start) == ("Math", 0):
                continue  # the band is too thin for its label; the caption gives it
            i = list(steps).index(start)
            ax.text((start + end) / 2, (bottom[i] + top[i]) / 2, f"{shares[name][i]:.0%}", ha="center", va="center",
                    color=text_color(color_of[name]))
    bottom = top

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/data-mixture.pdf")
fig.savefig("../outputs/data-mixture.png")
