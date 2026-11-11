"""Figure 6: Perplexity of individual responses to Problem 1 under the base and RL models. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range; points show every response. The base model finds the RL model's responses likely (median perplexity 1.06), within the range of its own responses (median 1.09)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig6.json") as f:
    data = json.load(f)["Problem 1"]

# ascending median, top to bottom
groups = [
    ("PPL_RL(Y_RL)", r"$\mathrm{PPL}_{\mathrm{RL}}(Y_{\mathrm{RL}})$"),
    ("PPL_Base(Y_RL)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{RL}})$"),
    ("PPL_Base(Y_Base)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{Base}})$"),
    ("PPL_Base(Y_GT)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{GT}})$"),
]
rng = np.random.default_rng(0)

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")

for y, (key, _) in enumerate(groups):
    values = data[key]
    box = ax.boxplot(values, positions=[y], widths=0.7, orientation="horizontal", patch_artist=True,
                     showfliers=False)
    box["boxes"][0].set_facecolor(lighten(colors["series-1"]))
    ax.plot(values, y + rng.uniform(-0.2, 0.2, len(values)), "o", color=colors["ink"], markerfacecolor="white",
            linestyle="none")

ax.set_yticks(range(len(groups)), labels=[label for _, label in groups])
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Perplexity")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/rlvr-fig6.pdf")
fig.savefig("../outputs/rlvr-fig6.png")
