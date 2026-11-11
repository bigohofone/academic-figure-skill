"""Test loss of Transformer language models versus non-embedding parameter count. Test loss is in nats per token, and both axes are logarithmic; circles are measured models and the dashed line is the fitted power law L = (N / N_c)^−α_N. Loss follows the power law with α_N = 0.076 across a 239,000× range of model sizes, every model within 1.95% of the fit."""

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
N = np.array(data["non_embedding_parameters"])
loss = np.array(data["test_loss"])
N_c = data["fit"]["N_c"]
alpha = data["fit"]["alpha_N"]
N_fit = np.geomspace(*data["fit"]["plotted_N_range"], 200)

# Takeaway: the measured losses follow the given power law over the whole range of sizes.
span = N.max() / N.min()
max_dev = np.max(np.abs(loss / (N / N_c) ** -alpha - 1))
print("takeaway:", {"alpha_N": f"{alpha}", "span": f"{float(f'{span:.3g}'):,.0f}×", "max relative deviation": f"{100 * max_dev:#.3g}%"})
assert max_dev < 0.05, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.set_xscale("log")
ax.set_yscale("log")

ax.plot(N, loss, "o", color=colors["series-1"], label="Transformer LMs")
ax.plot(N_fit, (N_fit / N_c) ** -alpha, linestyle="--", linewidth=paper.dashed_width, color=colors["series-1"],
        label=f"Fit: $L \\propto N^{{-{alpha}}}$")

ax.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9], labels=["10K", "100K", "1M", "10M", "100M", "1B"])
ax.xaxis.set_minor_formatter(NullFormatter())
# The loss spans less than one power of ten, so its log axis is ticked at whole nats.
ax.set_yticks([2, 3, 4, 5, 6], labels=["2", "3", "4", "5", "6"])
ax.set_yticks([], minor=True)
ax.set_xlabel("Non-embedding parameters")
ax.set_ylabel("Test loss (nats)")
ax.grid(True, which="both")
ax.legend(loc="upper right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/scaling-law.pdf")
fig.savefig("../outputs/scaling-law.png")
