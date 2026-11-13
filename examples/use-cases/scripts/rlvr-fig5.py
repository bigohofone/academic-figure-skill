"""Number of Minerva problems per per-problem accuracy bin, for the base model and its RL-trained version. RL moves problems to the extremes: 47 problems are always solved after RL against 3 before, while the never-solved problems grow from 93 to 113."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/paper-figure/assets")
import paper  # registers the bundled Inter font
from paper import shift_lightness, finalize_figure

colors = paper.colors

with open("../data/rlvr-fig5.json") as f:
    data = json.load(f)
bins = data["bins"]
base = data["Base"]
rl = data["RL"]

print("takeaway:", {"accuracy 1.0": (base[-1], rl[-1]), "accuracy 0.0": (base[0], rl[0])})
assert rl[-1] > base[-1] and rl[0] > base[0], "the takeaway does not hold"

x = np.arange(len(bins))
width = 0.8 / 2
fig, ax = plt.subplots(figsize=(5.5, 5.5), layout="constrained")
for i, (name, counts, color) in enumerate([("Base", base, colors["neutral"]), ("RL", rl, colors["ours"])]):
    bars = ax.bar(x + (i - 0.5) * width, counts, width, color=color, linewidth=0, label=name)
    ax.bar_label(bars, labels=[f"{round(v)}" for v in counts], color=shift_lightness(color, -1))
ax.grid(axis="x", visible=False)
ax.tick_params(axis="x", length=0)
ax.set_xticks(x, labels=bins, rotation=45, ha="right", rotation_mode="anchor")
ax.set_xlabel("Per-problem accuracy")
ax.set_ylabel("Problems")
ax.legend()

finalize_figure(fig, ax)
fig.savefig("../outputs/rlvr-fig5.pdf")
fig.savefig("../outputs/rlvr-fig5.png")
