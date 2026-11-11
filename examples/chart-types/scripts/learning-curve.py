"""Validation accuracy on CIFAR-100 over training epochs. Lines show the mean over 5 seeds and shaded bands ±1 std. Ours peaks at 0.915, 0.018 above Mixup (0.897) and above Baseline (0.882)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/learning-curve.json"))
epochs = np.array(data["epochs"])
runs = {name: np.array(seeds) for name, seeds in data["accuracy"].items()}  # seeds x epochs
n_seeds = {name: len(seeds) for name, seeds in runs.items()}
mean = {name: seeds.mean(axis=0) for name, seeds in runs.items()}
std = {name: seeds.std(axis=0) for name, seeds in runs.items()}

# takeaway: each method's best mean validation accuracy
best = {name: mean[name].max() for name in runs}
best_epoch = {name: epochs[mean[name].argmax()] for name in runs}
print("seeds:", n_seeds)
print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()}, "at epochs", best_epoch)
shown = {name: float(f"{v:#.3g}") for name, v in best.items()}  # the values as written on the plot
print("ours - mixup:", f"{shown['Ours'] - shown['Mixup']:.3f}")
assert best["Ours"] > max(v for name, v in best.items() if name != "Ours"), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")

# ours in color and solid; the baselines grey, told apart by line style, in ascending order of best accuracy
styles = {
    "Ours": dict(color=colors["ours"], linestyle="-"),
    "Baseline": dict(color=colors["neutral"], linestyle="--", linewidth=paper.dashed_width),
    "Mixup": dict(color=colors["neutral"], linestyle=":", linewidth=paper.dashed_width),
}
handles = {}
for name in ["Baseline", "Mixup", "Ours"]:
    color = styles[name]["color"]
    ax.fill_between(epochs, mean[name] - std[name], mean[name] + std[name], color=color, alpha=0.2, linewidth=0)
    (handles[name],) = ax.plot(epochs, mean[name], label=name, **styles[name])

# the three best values lie within 0.04 of each other: ours and its closest competitor are marked, Baseline's is in the caption

ax.set_xlabel("Epoch")
ax.set_ylabel("Validation accuracy")
ax.grid(True)
ax.legend([handles["Ours"], handles["Baseline"], handles["Mixup"]], ["Ours", "Baseline", "Mixup"], loc="lower right")

finalize_figure(fig, ax, aspect=0.618)
fig.savefig("../outputs/learning-curve.pdf")
fig.savefig("../outputs/learning-curve.png")
