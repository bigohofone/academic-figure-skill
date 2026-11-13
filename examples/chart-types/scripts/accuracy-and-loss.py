"""Validation accuracy and training loss versus epochs on CIFAR-10 and CIFAR-100. Training loss is smoothed with a moving average over 5% of the epochs; faint lines show raw values. Ours reaches a higher best validation accuracy than the baseline on both datasets, 0.960 vs. 0.932 on CIFAR-10 and 0.780 vs. 0.734 on CIFAR-100, and ends at a lower training loss, 0.120 vs. 0.186 and 0.853 vs. 1.05."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.colors

with open("../data/accuracy-and-loss.json") as f:
    data = json.load(f)
epochs = data["epochs"]
accuracy = data["validation_accuracy"]
loss = data["training_loss"]
datasets = ["CIFAR-10", "CIFAR-100"]

# takeaway: ours reaches the higher best accuracy and ends at the lower loss on both datasets
for name in datasets:
    best = {method: max(accuracy[name][method]) for method in ["Ours", "Baseline"]}
    final = {method: loss[name][method][-1] for method in ["Ours", "Baseline"]}
    print("takeaway:", name, "best accuracy", {m: f"{v:#.3g}" for m, v in best.items()},
          "final loss", {m: f"{v:#.3g}" for m, v in final.items()})
    assert best["Ours"] > best["Baseline"], "the takeaway does not hold"
    assert final["Ours"] < final["Baseline"], "the takeaway does not hold"

# metric x dataset, laid out side by side as the task asks: two groups of two panels
fig, axes = plt.subplots(1, 4, figsize=(5.5, 5.5), sharex=True)
axes[1].sharey(axes[0])
axes[3].sharey(axes[2])
axes[1].tick_params(labelleft=False)
axes[3].tick_params(labelleft=False)

for ax, name in zip(axes[:2], datasets):
    ax.plot(epochs, accuracy[name]["Baseline"], color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_linewidth, label="Baseline")
    ax.plot(epochs, accuracy[name]["Ours"], color=colors["ours"], label="Ours")
    ax.set_title(name)
axes[0].set_ylabel("Accuracy")

for ax, name in zip(axes[2:], datasets):
    ax.plot(epochs, loss[name]["Baseline"], color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_linewidth, alpha=0.25)
    ax.plot(epochs, loss[name]["Ours"], color=colors["ours"], alpha=0.25)
    w = max(1, len(epochs) // 40) * 2 + 1
    smoothed_epochs = epochs[w // 2 : len(epochs) - w // 2]
    ax.plot(smoothed_epochs, np.convolve(loss[name]["Baseline"], np.ones(w) / w, mode="valid"), color=colors["neutral"],
            linestyle="--", linewidth=paper.dashed_linewidth, label="Baseline")
    ax.plot(smoothed_epochs, np.convolve(loss[name]["Ours"], np.ones(w) / w, mode="valid"), color=colors["ours"], label="Ours")
    ax.set_title(name)
axes[2].set_ylabel("Training loss")

for ax in axes:
    ax.set_xticks([0, 20, 40, 60])
fig.supxlabel("Epoch")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles[::-1], labels[::-1], loc="outside upper center", ncol=2, borderaxespad=0)

finalize_figure(fig, axes, height="M", min_width=0.9)
fig.savefig("../outputs/accuracy-and-loss.pdf")
fig.savefig("../outputs/accuracy-and-loss.png")
fig.savefig("../outputs/accuracy-and-loss.svg")
