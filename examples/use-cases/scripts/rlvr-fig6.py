"""Perplexity of individual responses to Problem 1 under the base and RL models. Boxes span the quartiles with the median as a line, and whiskers reach 1.5× the interquartile range. Points show every response. Under the base model, RL responses have a median perplexity of 1.06, within the range of the base model's own responses (median 1.08). Ground-truth responses have the highest median (1.21), and the RL model's own perplexity on its responses has the lowest (1.01).
"""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig6.json") as f:
    groups = json.load(f)["Problem 1"]
names = ["PPL_Base(Y_Base)", "PPL_Base(Y_RL)", "PPL_RL(Y_RL)", "PPL_Base(Y_GT)"]
labels = [r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{Base}})$", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{RL}})$",
          r"$\mathrm{PPL}_{\mathrm{RL}}(Y_{\mathrm{RL}})$", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{GT}})$"]

medians = {name: float(np.median(groups[name])) for name in names}
print("takeaway:", {name: f"{v:#.3g}" for name, v in medians.items()})
base_y = groups["PPL_Base(Y_Base)"]
assert min(base_y) <= medians["PPL_Base(Y_RL)"] <= max(base_y), "the takeaway does not hold"
assert medians["PPL_Base(Y_GT)"] == max(medians.values()) and medians["PPL_RL(Y_RL)"] == min(medians.values())

rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for y, name in enumerate(names):
    values = groups[name]
    box = ax.boxplot(values, positions=[y], widths=0.7, orientation="horizontal", patch_artist=True,
                     showfliers=False)
    box["boxes"][0].set_facecolor(lighten(colors["series-1"]))
    ax.plot(values, y + rng.uniform(-0.2, 0.2, len(values)), "o", color=colors["ink"], markerfacecolor="white",
            linestyle="none")

ax.set_yticks(range(len(names)), labels=labels)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Perplexity")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/rlvr-fig6.pdf")
fig.savefig("../outputs/rlvr-fig6.png")
