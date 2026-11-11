"""Figure 1: Attention weights of the French translation (rows) on the English source sentence (columns). Each row is the attention distribution of one generated word and sums to 1. The alignment is mostly monotonic but reverses for the noun phrase: “zone économique européenne” attends to “European Economic Area” in reverse order, with “européenne” putting 0.97 of its weight on “European”."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/attention-map.json") as f:
    data = json.load(f)
source_tokens = data["source_tokens"]
target_tokens = data["target_tokens"]
weights = np.array(data["weights"])  # weights[i][j]: target word i on source word j

fig, ax = plt.subplots(figsize=(2.75, 2.75))
im = ax.imshow(weights, aspect="auto", vmin=0, vmax=1)
ax.xaxis.tick_top()
ax.set_xticks(range(len(source_tokens)), labels=source_tokens, rotation=90, ha="center")
ax.set_yticks(range(len(target_tokens)), labels=target_tokens)
ax.tick_params(length=0)
ax.grid(False)

cbar = fig.colorbar(im, ax=ax, label="Attention weight", location="bottom")
cbar.set_ticks([0, 0.5, 1], labels=["0", "0.5", "1"])

fit_height(fig, ax, aspect=weights.shape[0] / weights.shape[1])
fig.savefig("../outputs/attention-map.pdf")
fig.savefig("../outputs/attention-map.png")
