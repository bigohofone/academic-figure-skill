"""Figure 1: Soft alignment found by RNNsearch-50 when translating an English sentence (columns) into French (rows). Each cell is the attention weight αᵢⱼ of target word i on source word j; each row sums to 1. The alignment is mostly monotonic along the diagonal, but the model aligns "zone" with "Area" (0.97), jumping over "European" and "Economic", and then looks one word back at a time to finish "zone économique européenne"."""

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
source = data["source_tokens"]
target = data["target_tokens"]
weights = np.array(data["weights"])

fig, ax = plt.subplots(figsize=(2.75, 2))
im = ax.imshow(weights, aspect="auto", vmin=0, vmax=1)
ax.xaxis.tick_top()
ax.set_xticks(range(len(source)), labels=source, rotation=90, ha="center")
ax.set_yticks(range(len(target)), labels=target)
ax.tick_params(length=0)
ax.grid(False)
fig.colorbar(im, ax=ax, label="Attention weight", location="bottom")

fit_height(fig, ax, aspect=len(target) / len(source))
fig.savefig("../outputs/attention-map.pdf")
fig.savefig("../outputs/attention-map.png")
