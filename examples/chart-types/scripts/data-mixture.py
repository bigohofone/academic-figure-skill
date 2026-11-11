"""Figure 1: Share of pretraining tokens from each domain over training. Dashed white lines mark the mixture switches at 30K and 70K steps. Code grows from 12% to 24% and math from 6% to 18% of tokens across the three stages, while web text falls from 62% to 40%."""

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
steps = np.array(data["steps"]) / 1000  # in thousands
shares = {name: np.array(v) for name, v in data["shares"].items()}
total = sum(shares.values())
shares = {name: v / total for name, v in shares.items()}  # normalized to 1 at each step

# colors in data order; the flattest part (Wikipedia) at the bottom, the rest in data order above it
names = list(shares)
band_colors = {name: colors[f"series-{i + 1}"] for i, name in enumerate(names)}
flattest = min(names, key=lambda n: np.std(shares[n]))
stack = [flattest] + [n for n in names if n != flattest]

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.stackplot(steps, [shares[n] for n in stack], colors=[band_colors[n] for n in stack], labels=stack,
             step="post", edgecolor="white", linewidth=rcParams["grid.linewidth"])
switches = [30, 70]
for s in switches:
    ax.axvline(s, linestyle="--", linewidth=paper.dashed_width, color="white")

ax.set_ylim(0, 1)
ax.margins(x=0)
ax.set_axisbelow(False)
ax.grid(axis="x", visible=False)
ax.set_xticks([0, *switches, 100])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Training step (K)")
ax.set_ylabel("Share of tokens")

# band names at the right end, in stacking order; cited shares inside their bands at each stage
bottoms = np.cumsum([0] + [shares[n][-1] for n in stack])
for name, lo, hi in zip(stack, bottoms[:-1], bottoms[1:]):
    ax.annotate(name, (1, (lo + hi) / 2), xycoords=("axes fraction", "data"), xytext=(4, 0),
                textcoords="offset points", va="center")

stage_mid = {0: 15, 30: 50, 70: 85}
for start, x_mid in stage_mid.items():
    i = list(steps).index(start)
    bottom = 0
    for name in stack:
        v = shares[name][i]
        # math's 6% in the first stage does not fit its band; the caption gives it
        if name in ("Web", "Code", "Math") and not (name == "Math" and start == 0):
            ax.annotate(f"{v:.0%}", (x_mid, bottom + v / 2), ha="center", va="center",
                        color=text_color(band_colors[name]), gid="value-label")
        bottom += v

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/data-mixture.pdf")
fig.savefig("../outputs/data-mixture.png")
