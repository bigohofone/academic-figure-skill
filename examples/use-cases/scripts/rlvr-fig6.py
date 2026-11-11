"""Figure 6: Perplexity of individual responses to an AIME24 problem under the base model (Qwen2.5-7B)
and its RLVR-trained version. PPL_M(Y_S) is model M's perplexity on responses sampled from S (16 per
model; 7 from OpenAI-o1 as Y_GT); boxes span the quartiles with the median as a line, whiskers reach
1.5× the interquartile range, and each point is one response. The base model's perplexity on RL
responses (median 1.056) falls in the lower part of its perplexity on its own responses (median
1.084), so the RL model generates responses the base model already tends to produce.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr-fig6.json") as f:
    data = json.load(f)["Problem 1"]

groups = [
    ("PPL_RL(Y_RL)", r"$\mathrm{PPL}_{\mathrm{RL}}(Y_{\mathrm{RL}})$", lighten(colors["neutral"])),
    ("PPL_Base(Y_RL)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{RL}})$", lighten(colors["series-2"])),
    ("PPL_Base(Y_Base)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{Base}})$", lighten(colors["series-1"])),
    ("PPL_Base(Y_GT)", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{GT}})$", lighten(colors["neutral"])),
]

rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(2.75, 2))
for y, (key, label, fill) in enumerate(groups):
    values = data[key]
    box = ax.boxplot(values, positions=[y], widths=0.7, orientation="horizontal", showfliers=False)
    box["boxes"][0].set_facecolor(fill)
    ax.plot(values, y + rng.uniform(-0.2, 0.2, len(values)), "o", color="black", markerfacecolor="white", linestyle="none")

ax.set_yticks(range(len(groups)), labels=[label for _, label, _ in groups])
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Perplexity")
ax.xaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))
fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/rlvr-fig6.pdf")
fig.savefig("../outputs/rlvr-fig6.png")
