"""Figure 6: Perplexity of individual responses to an AIME24 problem, under the base model (Qwen2.5-7B) and the RL-trained model. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range; points show every response (16 per group; 7 o1 responses, as one of the 8 could not be recovered). The base model's perplexity on RL responses (median 1.056) matches the lower part of its perplexity on its own responses (median 1.084): the RL model's responses are ones the base model already tends to generate."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/rlvr-fig6.json"))["Problem 1"]
groups = [
    ("PPL_RL(Y_RL)", r"$\mathrm{PPL}_{\mathrm{RL}}(Y_{\mathrm{RL}})$"),
    ("PPL_Base(Y_RL)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{RL}})$"),
    ("PPL_Base(Y_Base)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{Base}})$"),
    ("PPL_Base(Y_GT)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{GT}})$"),
]

fig, ax = plt.subplots(figsize=(2.75, 2))
rng = np.random.default_rng(0)
for y, (key, _) in enumerate(groups):
    values = data[key]
    box = ax.boxplot(values, positions=[y], widths=0.7, showfliers=False, orientation="horizontal")
    box["boxes"][0].set_facecolor(lighten(colors["series-1"]))
    ax.plot(values, y + rng.uniform(-0.2, 0.2, len(values)), "o", color=colors["ink"],
            markerfacecolor="white", linestyle="none")

ax.set_yticks(range(len(groups)), labels=[label for _, label in groups])
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:,.10g}".replace("-", "−"))
ax.set_xlabel("Perplexity")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/rlvr-fig6.pdf")
fig.savefig("../outputs/rlvr-fig6.png")
