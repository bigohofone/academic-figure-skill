"""Test loss (nats per token) of Transformer language models versus model size. Both axes are logarithmic; circles are measured models and the dashed line is the fitted power law L = (N / 8.8×10¹³)^−0.076, with N the number of non-embedding parameters. Loss falls as a power law with exponent 0.076, from 5.95 nats per token at 6129 parameters to 2.35 at 1,466,000,000."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/scaling-law.json") as f:
    data = json.load(f)
n = np.array(data["non_embedding_parameters"])
loss = np.array(data["test_loss"])
n_c, alpha = data["fit"]["N_c"], data["fit"]["alpha_N"]
n_fit = np.geomspace(*data["fit"]["plotted_N_range"], 200)

predicted = (n / n_c) ** -alpha
print("takeaway: alpha", f"{alpha}", "| loss", f"{loss[0]:#.3g} at N={round(n[0]):,}", f"to {loss[-1]:#.3g} at N={round(n[-1]):,}",
      "| max relative deviation from the fit", f"{np.max(np.abs(loss / predicted - 1)):.3f}")
assert np.max(np.abs(loss / predicted - 1)) < 0.05, "the fit does not track the measurements"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.set_xscale("log")
ax.set_yscale("log")

ax.plot(n, loss, "o", color=colors["series-1"], label="Transformer")
ax.plot(n_fit, (n_fit / n_c) ** -alpha, linestyle="--", linewidth=paper.dashed_width, color=colors["series-1"],
        label=f"Fit: $L \\propto N^{{-{alpha}}}$")

ax.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9], labels=["10K", "100K", "1M", "10M", "100M", "1B"])
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_yticks([2, 3, 4, 5, 6], labels=["2", "3", "4", "5", "6"])
ax.set_yticks([], minor=True)
ax.grid(True, which="both")

ax.set_xlabel("Non-embedding parameters")
ax.set_ylabel("Test loss")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/scaling-law.pdf")
fig.savefig("../outputs/scaling-law.png")
