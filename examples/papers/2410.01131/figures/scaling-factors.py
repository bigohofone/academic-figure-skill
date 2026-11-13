"""(Left): Eigen learning rates of Attention and MLP blocks. (Middle): Scaling factors applied to the intermediate states of MLP. (Right): Scaling factors applied before the QK dot product; distribution of per-vector scalings applied to logits. Models are trained for 100k iterations."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

factors = json.load(open("../data/scaling-factors.json"))

# takeaway (paper text): the mean eigen learning rate drops from the 0.5B to the 1B network, in both blocks
mean = {block: {name: np.mean(s["y"]) for name, s in factors[block].items()} for block in ["alpha_A", "alpha_M"]}
print("takeaway: mean eigen learning rate", {b: {n: f"{v:#.2g}" for n, v in m.items()} for b, m in mean.items()})
assert all(m["nGPT 1B"] < m["nGPT 0.5B"] for m in mean.values()), "the takeaway does not hold"

# both series are nGPT (ours): model sizes in shades of ours, the larger darker
shades = dict(zip(["nGPT 0.5B", "nGPT 1B"], make_shades(colors["ours"], 2)))

# short titles and labels: the original ones ("Eigen learning rates of Attention", "mean(abs(Value))", ...) overlap
# at this width; the caption names each panel
panels = {
    "alpha_A": (r"$\alpha_A$, Attention", "Layer"),
    "s_u": (r"$s_u$, MLP", "Layer"),
    "s_qk": (r"$s_{qk}$, QK dot product", "Layer"),
    "alpha_M": (r"$\alpha_M$, MLP", "Layer"),
    "s_nu": (r"$s_\nu$, MLP", "Layer"),
    "s_z_density": (r"$s_z$, 32k embeddings", "Value"),
}

# the full text width, laid wide as in the original: the left and middle columns plot the same quantity
# over the same layers in both rows, so they share axes down the column
fig, axes = plt.subplots(2, 3, figsize=(5.5, 5.5), layout="constrained")
for c in [0, 1]:
    axes[0, c].sharex(axes[1, c])
    axes[0, c].sharey(axes[1, c])
    axes[0, c].tick_params(labelbottom=False)
for ax, (key, (title, xlabel)) in zip(axes.flat, panels.items()):
    handles = [ax.plot(factors[key][name]["x"], factors[key][name]["y"], color=color)[0] for name, color in shades.items()]
    ax.set_title(title)
    if ax not in axes[0, :2]:
        ax.set_xlabel(xlabel)
    ax.grid(True)
for row in axes:
    row[0].set_ylabel("Mean |value|")
axes[1, 2].set_ylabel("Density")
paper.add_legend_rows(axes[0, 0], [("nGPT", handles, ["0.5B", "1B"])])

# square panels
finalize_figure(fig, axes, height="M")
fig.savefig("../out/scaling-factors.pdf")
