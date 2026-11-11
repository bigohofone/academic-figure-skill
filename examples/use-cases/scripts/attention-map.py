"""Attention weights of an English-to-French translation model. Each row is a generated French word and shows its attention over the English source words, top. The model aligns each French word with its English counterpart and reverses the word order of "European Economic Area" into "zone économique européenne", with weights of 0.710, 0.757 and 0.973 on "Area", "Economic" and "European"."""

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
weights = np.array(data["weights"])  # rows: target words, columns: source words

# Takeaway: the reversed phrase "European Economic Area" -> "zone économique européenne".
pairs = [("zone", "Area"), ("économique", "Economic"), ("européenne", "European")]
reversed_weights = []
for fr, en in pairs:
    i, j = target.index(fr), source.index(en)
    assert weights[i].argmax() == j, f"{fr} does not attend most to {en}"
    reversed_weights.append(weights[i, j])
print("takeaway:", {fr: f"{w:#.3g}" for (fr, _), w in zip(pairs, reversed_weights)})

fig, ax = plt.subplots(figsize=(5.5, 5.5), layout="constrained")
im = ax.imshow(weights, aspect="auto")
ax.xaxis.tick_top()
ax.set_xticks(range(len(source)), labels=source, rotation=45, ha="left", rotation_mode="anchor")
ax.set_yticks(range(len(target)), labels=target)
ax.tick_params(length=0)
ax.grid(False)
fig.colorbar(im, ax=ax, label="Attention weight")

fit_height(fig, ax, aspect=len(target) / len(source))
fig.savefig("../outputs/attention-map.pdf")
fig.savefig("../outputs/attention-map.png")
