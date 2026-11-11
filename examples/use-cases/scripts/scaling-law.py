"""Figure 3: Test loss of Transformer language models on WebText2 against model size. Both axes are log
scales; markers show models trained to near convergence, and the dashed line is the power-law fit L
= (N / 8.8·10¹³)^−0.076 over N non-embedding parameters. Loss falls smoothly from 5.95 to 2.34 nats
per token as N grows from 6.1K to 1.5B, following the power law with α_N = 0.076 over six orders of
magnitude, so doubling N cuts the loss by a factor of 0.95.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/scaling-law.json") as f:
    data = json.load(f)
n = np.array(data["non_embedding_parameters"])
loss = np.array(data["test_loss"])
n_c, alpha = data["fit"]["N_c"], data["fit"]["alpha_N"]
n_fit = np.geomspace(*data["fit"]["plotted_N_range"], 200)

fig, ax = plt.subplots(figsize=(2.75, 2))
color = colors["series-1"]
ax.plot(n, loss, "o", color=color, label="Measured")
ax.plot(n_fit, (n_fit / n_c) ** -alpha, linestyle="--", linewidth=paper.dashed_width, color=color,
        label=r"Fit: $L = (N / 8.8 \cdot 10^{13})^{-0.076}$")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9], labels=["10K", "100K", "1M", "10M", "100M", "1B"])
ax.xaxis.set_minor_formatter(NullFormatter())
y_ticks = data["axes"]["y_ticks"]
ax.set_yticks(y_ticks, labels=[f"{t:g}" for t in y_ticks])
ax.set_yticks([], minor=True)
ax.grid(True, which="both")
ax.set_xlabel("Parameters (non-embedding)")
ax.set_ylabel("Test loss (nats/token)")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/scaling-law.pdf")
fig.savefig("../outputs/scaling-law.png")
