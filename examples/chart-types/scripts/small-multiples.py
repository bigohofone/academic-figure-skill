"""Validation accuracy of Ours, Mixup and the Baseline over 100 epochs on three datasets. Shaded bands show ±1 std over 3 seeds; circles and thin lines mark the best mean accuracy of Ours and Mixup. Ours reaches the highest best mean accuracy on every dataset: 0.953 vs. 0.932 for Mixup and 0.917 for the Baseline on CIFAR-10, 0.784 vs. 0.742 and 0.717 on CIFAR-100, and 0.664 vs. 0.612 and 0.599 on Tiny-ImageNet."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/small-multiples.json") as f:
    data = json.load(f)
epochs = np.array(data["epochs"])
datasets = ["CIFAR-10", "CIFAR-100", "Tiny-ImageNet"]
mean = {ds: {m: np.mean(runs, axis=0) for m, runs in data["accuracy"][ds].items()} for ds in datasets}
std = {ds: {m: np.std(runs, axis=0) for m, runs in data["accuracy"][ds].items()} for ds in datasets}

# Takeaway: Ours reaches the highest best mean accuracy on every dataset.
best = {ds: {m: mean[ds][m].max() for m in mean[ds]} for ds in datasets}
print("takeaway:", {ds: {m: f"{v:#.3g}" for m, v in b.items()} for ds, b in best.items()})
for ds in datasets:
    assert best[ds]["Ours"] > max(v for m, v in best[ds].items() if m != "Ours"), "the takeaway does not hold"

# Series in ascending order of best accuracy; grey series told apart by line style in that order.
series = [
    ("Baseline", colors["neutral"], "--"),
    ("Mixup", colors["neutral"], ":"),
    ("Ours", colors["ours"], "-"),
]

fig, axes = plt.subplots(1, 3, figsize=(6.75, 6.75), sharex=True, sharey=True, layout="constrained")
for ax, ds in zip(axes, datasets):
    for name, color, style in series:
        m, s = mean[ds][name], std[ds][name]
        width = paper.dashed_width if style != "-" else None
        ax.fill_between(epochs, m - s, m + s, color=color, alpha=0.2, linewidth=0)
        ax.plot(epochs, m, color=color, linestyle=style, linewidth=width, label=name)
    # Marks on ours and its closest competitor, Mixup (below its point); the Baseline's best is in the caption.
    for name, color, below in [("Ours", colors["ours"], False), ("Mixup", colors["neutral"], True)]:
        i = np.argmax(mean[ds][name])
        mark_value(ax, epochs[i], mean[ds][name][i], f"{mean[ds][name][i]:#.3g}", color, below=below)
    ax.set_title(ds)
    ax.grid(True)
    ax.tick_params(labelleft=True, labelbottom=True)
axes[0].set_ylabel("Accuracy")
fig.supxlabel("Epoch")

handles, labels = axes[0].get_legend_handles_labels()
order = [labels.index(n) for n in ["Ours", "Baseline", "Mixup"]]
fig.legend([handles[i] for i in order], [labels[i] for i in order], loc="outside upper center",
           ncol=3, frameon=False, borderaxespad=0)

fit_height(fig, axes, column_gap=0.25)
fig.savefig("../outputs/small-multiples.pdf")
fig.savefig("../outputs/small-multiples.png")
