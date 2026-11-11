"""Figure 1: Test loss of Transformer language models on WebText2 against model size. Both axes are logarithmic; markers show models trained to near convergence and the dashed line the power-law fit L = (N / 8.8·10¹³)^−0.076. Loss falls smoothly from 5.95 to 2.34 nats per token as non-embedding parameters grow from 6K to 1.5B, with no deviation from the power law at the largest models."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/scaling-law.json"))
n = np.array(data["non_embedding_parameters"])
loss = np.array(data["test_loss"])
n_c, alpha = data["fit"]["N_c"], data["fit"]["alpha_N"]
n_fit = np.geomspace(*data["fit"]["plotted_N_range"], 200)

fig, ax = plt.subplots(figsize=(2.75, 2))
ax.plot(n, loss, "o", color=colors["series-1"], label="Test loss")
ax.plot(n_fit, (n_fit / n_c) ** -alpha, linestyle="--", linewidth=paper.dashed_width, color=colors["series-1"],
        label=f"Fit: $L \\propto N^{{-{alpha}}}$")

ax.set_xscale("log")
ax.set_yscale("log")
ax.grid(True, which="both")
ax.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9], labels=["10K", "100K", "1M", "10M", "100M", "1B"])
ax.xaxis.set_minor_formatter(NullFormatter())
y_ticks = data["axes"]["y_ticks"]
ax.set_yticks(y_ticks, labels=[f"{t:,.10g}" for t in y_ticks])
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Parameters (non-embedding)")
ax.set_ylabel("Test loss (nats/token)")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/scaling-law.pdf")
fig.savefig("../outputs/scaling-law.png")
