"""Attention weights of the translation model from English source words (columns) to the French target words it generates (rows). Each row is one target word's attention distribution over the source words and sums to about 1. The alignment is mostly monotonic, but reverses for the noun phrase: “zone”, “économique” and “européenne” attend to “Area”, “Economic” and “European” with weights 0.710, 0.757 and 0.973."""

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

# Takeaway: the alignment reverses for "European Economic Area" -> "zone économique européenne".
pairs = [("zone", "Area"), ("économique", "Economic"), ("européenne", "European")]
for t, s in pairs:
    i, j = target.index(t), source.index(s)
    print(f"takeaway: {t} -> {s}: {weights[i, j]:#.3g}")
    assert np.argmax(weights[i]) == j, "the takeaway does not hold"
src_cols = [source.index(s) for _, s in pairs]
assert src_cols == sorted(src_cols, reverse=True), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(5.5, 5.5))
im = ax.imshow(weights, aspect="auto", vmin=0, vmax=1)
ax.xaxis.tick_top()
ax.set_xticks(range(len(source)), labels=source, rotation=45, ha="left", rotation_mode="anchor")
ax.set_yticks(range(len(target)), labels=target)
ax.tick_params(length=0)
ax.grid(False)
fig.colorbar(im, ax=ax, label="Attention weight")

fit_height(fig, ax, aspect=weights.shape[0] / weights.shape[1])
fig.savefig("../outputs/attention-map.pdf")
fig.savefig("../outputs/attention-map.png")
