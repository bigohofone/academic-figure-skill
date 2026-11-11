"""Figure [TODO: number]: Test loss of Transformer language models versus non-embedding parameter count. Both axes are logarithmic; the dashed line is the power-law fit L = (N / 8.8×10¹³)^−0.076. Loss falls from 5.95 to 2.34 nats per token as models grow from 6.1K to 1.5B parameters, following a single power law with exponent 0.076."""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.colors import Normalize, to_rgb
from matplotlib.patches import Patch
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")  # the style from DESIGN.md's tokens; colors["series-1"], colors["ours"], …

with open("../data/scaling-law.json") as f:
    data = json.load(f)
n = np.array(data["non_embedding_parameters"])
loss = np.array(data["test_loss"])
n_c, alpha = data["fit"]["N_c"], data["fit"]["alpha_N"]

# ICLR, one panel: half the text width
fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
ax.set_xscale("log")
ax.set_yscale("log")

color = colors["series-1"]
ax.plot(n, loss, "o", color=color, label="Transformer")
n_fit = np.geomspace(*data["fit"]["plotted_N_range"], 200)
ax.plot(n_fit, (n_fit / n_c) ** -alpha, linestyle="--", linewidth=paper.dashed_width, color=color,
        label=f"Fit: $L \\propto N^{{-{alpha}}}$")

ax.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9], labels=["10K", "100K", "1M", "10M", "100M", "1B"])
ax.xaxis.set_minor_formatter(NullFormatter())
# the loss spans less than a power of ten: plain ticks at whole nats, no minor ticks
ax.set_yticks([2, 3, 4, 5, 6], labels=["2", "3", "4", "5", "6"])
ax.set_yticks([], minor=True)
ax.set_xlabel("Non-embedding parameters")
ax.set_ylabel("Test loss (nats/token)")
ax.grid(True, which="both")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/scaling-law.pdf")
fig.savefig("../outputs/scaling-law.png")
