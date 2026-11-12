"""Validation accuracy versus epochs on three datasets. Lines show the mean and shaded bands ±1 std over 3 seeds. Ours reaches the highest best accuracy on every dataset: 0.953 vs. 0.932 for Mixup on CIFAR-10, 0.784 vs. 0.742 on CIFAR-100 and 0.664 vs. 0.612 on Tiny-ImageNet; the baseline peaks at 0.917, 0.717 and 0.599."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/small-multiples.json") as f:
    data = json.load(f)
epochs = np.array(data["epochs"])
datasets = ["CIFAR-10", "CIFAR-100", "Tiny-ImageNet"]
runs = {name: {method: np.array(seeds) for method, seeds in data["accuracy"][name].items()} for name in datasets}

# takeaway: ours reaches the highest best mean accuracy on every dataset
for name in datasets:
    best = {method: runs[name][method].mean(axis=0).max() for method in ["Baseline", "Mixup", "Ours"]}
    print("takeaway:", name, {method: f"{v:#.3g}" for method, v in best.items()})
    assert best["Ours"] > max(best["Baseline"], best["Mixup"]), "the takeaway does not hold"

# compared series in ascending order of best accuracy: Baseline, Mixup, then ours
series = [
    ("Baseline", colors["neutral"], "--"),
    ("Mixup", colors["neutral"], ":"),
    ("Ours", colors["ours"], "-"),
]

fig, axes = plt.subplots(1, 3, figsize=(6.75, 6.75), sharex=True, sharey=True)
for ax, name in zip(axes, datasets):
    for method, color, style in series:
        mean = runs[name][method].mean(axis=0)
        std = runs[name][method].std(axis=0)
        width = paper.dashed_width if style != "-" else rcParams["lines.linewidth"]
        ax.fill_between(epochs, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)
        ax.plot(epochs, mean, color=color, linestyle=style, linewidth=width, label=method)
    ax.set_title(name)
axes[0].set_ylabel("Validation accuracy")
fig.supxlabel("Epoch")

handles, labels = axes[0].get_legend_handles_labels()
order = [2, 0, 1]  # ours first, then the grey series in line-style order
fig.legend([handles[i] for i in order], [labels[i] for i in order], loc="outside upper center", ncol=3, borderaxespad=0)

finalize_figure(fig, axes, min_width=0.7)
fig.savefig("../outputs/small-multiples.pdf")
fig.savefig("../outputs/small-multiples.png")
