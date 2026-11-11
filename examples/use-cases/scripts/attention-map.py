"""Attention weights of the translation model for one English–French sentence pair. Each row is a generated French word and its weights over the English source words; rows sum to about 1. Attention follows the word order except where French reverses it: "zone économique européenne" attends to "Area", "Economic" and "European" in reverse order, with weights of 0.710, 0.757 and 0.973."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/attention-map.json"))
source = data["source_tokens"]
target = data["target_tokens"]
weights = np.array(data["weights"])  # rows: target words (queries), columns: source words (keys)

# takeaway: the French noun phrase reverses the English one, and attention follows it
rows = [target.index(w) for w in ("zone", "économique", "européenne")]
focus = [source[int(np.argmax(weights[i]))] for i in rows]
print("takeaway:", {target[i]: (f, f"{weights[i].max():#.3g}") for i, f in zip(rows, focus)})
assert focus == ["Area", "Economic", "European"], "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(5.5, 5.5))
im = ax.imshow(weights, aspect="auto", vmin=0, vmax=1)
ax.xaxis.tick_top()
ax.set_xticks(range(len(source)), labels=source, rotation=45, ha="left", rotation_mode="anchor")
ax.set_yticks(range(len(target)), labels=target)
ax.tick_params(length=0)
ax.grid(False)
cbar = fig.colorbar(im, ax=ax, label="Attention weight")

fit_height(fig, ax, aspect=len(target) / len(source))
# the colorbar keeps its default 20:1 shape, half the panel height at full width; let it span the panel as fit_height placed it
cbar.ax.set_axes_locator(None)
cbar.ax.set_box_aspect(None)
fig.savefig("../outputs/attention-map.pdf")
fig.savefig("../outputs/attention-map.png")
