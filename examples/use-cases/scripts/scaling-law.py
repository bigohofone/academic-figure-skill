"""Test loss of Transformer language models versus model size. Both axes are logarithmic; the dashed line is the fitted power law L = (N / 8.8×10¹³)^−0.076. From 6129 to 1.47B non-embedding parameters, test loss falls from 5.95 to 2.35 nats per token, following the power law with exponent 0.076."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/scaling-law.json"))
n = np.array(data["non_embedding_parameters"])
loss = np.array(data["test_loss"])
n_c, alpha = data["fit"]["N_c"], data["fit"]["alpha_N"]
n_fit = np.geomspace(*data["fit"]["plotted_N_range"], 200)
loss_fit = (n_fit / n_c) ** -alpha

# takeaway: loss falls as a power law in N, from the smallest to the largest model
smallest, largest = n.argmin(), n.argmax()
residual = np.abs(np.log(loss) - np.log((n / n_c) ** -alpha))
print("takeaway:", f"alpha_N={alpha}", f"N {round(n[smallest])} -> {n[largest] / 1e9:#.3g}B",
      f"loss {loss[smallest]:#.3g} -> {loss[largest]:#.3g}", f"max |log residual|={residual.max():.3f}")
assert np.corrcoef(np.log(n), np.log(loss))[0, 1] < -0.99, "loss does not follow a power law in N"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.set_xscale("log")
ax.set_yscale("log")

color = colors["series-1"]
ax.plot(n, loss, "o", color=color, label="Transformer LMs")
ax.plot(n_fit, loss_fit, linestyle="--", linewidth=paper.dashed_width, color=color,
        label=f"Fit: $L \\propto N^{{-{alpha}}}$")

ax.set_xticks([1e4, 1e5, 1e6, 1e7, 1e8, 1e9], labels=["10K", "100K", "1M", "10M", "100M", "1B"])
ax.xaxis.set_minor_formatter(NullFormatter())
yticks = [2, 3, 4, 5, 6]
ax.set_yticks(yticks, labels=[str(t) for t in yticks])
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Non-embedding parameters")
ax.set_ylabel("Test loss (nats/token)")
ax.grid(True, which="both")
ax.legend()

finalize_figure(fig, ax)
fig.savefig("../outputs/scaling-law.pdf")
fig.savefig("../outputs/scaling-law.png")
