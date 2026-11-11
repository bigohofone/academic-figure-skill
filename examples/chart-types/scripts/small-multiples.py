"""Validation accuracy of Ours, Mixup and Baseline on CIFAR-10, CIFAR-100 and Tiny-ImageNet. Lines show the mean and shaded bands ±1 std over 3 seeds; the thin horizontal line marks the best mean accuracy of Ours. Ours reaches the highest best mean accuracy on all three datasets: 0.953 vs. 0.932 (Mixup) and 0.917 (Baseline) on CIFAR-10, 0.784 vs. 0.742 and 0.717 on CIFAR-100, and 0.664 vs. 0.612 and 0.599 on Tiny-ImageNet."""

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
accuracy = data["accuracy"]
datasets = ["CIFAR-10", "CIFAR-100", "Tiny-ImageNet"]
# grey series in ascending order of accuracy, told apart by line style; ours solid in its color
methods = [("Baseline", colors["neutral"], "--"), ("Mixup", colors["neutral"], ":"), ("Ours", colors["ours"], "-")]

mean = {d: {m: np.mean(accuracy[d][m], axis=0) for m, _, _ in methods} for d in datasets}
std = {d: {m: np.std(accuracy[d][m], axis=0) for m, _, _ in methods} for d in datasets}

# Takeaway: Ours reaches the highest best mean accuracy on every dataset.
best = {d: {m: (int(np.argmax(mean[d][m])), float(np.max(mean[d][m]))) for m, _, _ in methods} for d in datasets}
print("takeaway:", {d: {m: f"{v:#.3g}" for m, (_, v) in b.items()} for d, b in best.items()})
for d in datasets:
    assert best[d]["Ours"][1] > max(best[d]["Mixup"][1], best[d]["Baseline"][1]), "the takeaway does not hold"

fig, axes = plt.subplots(1, 3, figsize=(6.75, 6.75), sharex=True, layout="constrained")
handles = {}
for ax, d in zip(axes, datasets):
    for m, color, style in methods:
        width = paper.dashed_width if style != "-" else None
        line, = ax.plot(epochs, mean[d][m], color=color, linestyle=style, linewidth=width, label=m)
        ax.fill_between(epochs, mean[d][m] - std[d][m], mean[d][m] + std[d][m], color=color, alpha=0.2, linewidth=0)
        handles[m] = line
    # only ours is marked; the baselines' best values are in the caption (their labels collide with the curves)
    i, v = best[d]["Ours"]
    mark_value(ax, epochs[i], v, f"{v:#.3g}", colors["ours"])
    ax.set_title(d)
    ax.grid(True)
    ax.set_xticks([1, 25, 50, 75, 100])
    ax.tick_params(labelleft=True, labelbottom=True)
axes[0].set_ylabel("Validation accuracy")
fig.supxlabel("Epoch")

order = ["Ours", "Baseline", "Mixup"]
fig.legend([handles[m] for m in order], order, loc="outside upper center", ncol=3, frameon=False, borderaxespad=0)

fit_height(fig, axes, aspect=0.618)
fig.savefig("../outputs/small-multiples.pdf")
fig.savefig("../outputs/small-multiples.png")
