"""Validation accuracy and training loss of Ours and Baseline on CIFAR-10 and CIFAR-100. Training loss is smoothed with a moving average over 5% of the epochs; faint lines show raw values. Ours reaches a higher best validation accuracy on both datasets (0.960 vs. 0.932 on CIFAR-10, 0.780 vs. 0.734 on CIFAR-100) and ends with a lower smoothed training loss (0.124 vs. 0.201 and 0.876 vs. 1.07)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, smooth

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/accuracy-and-loss.json") as f:
    data = json.load(f)
epochs = np.array(data["epochs"])
accuracy = data["validation_accuracy"]
loss = data["training_loss"]
datasets = ["CIFAR-10", "CIFAR-100"]

# Takeaway: Ours reaches the higher best validation accuracy on both datasets, and ends with lower loss.
best = {d: {m: max(accuracy[d][m]) for m in ("Ours", "Baseline")} for d in datasets}
final_loss = {d: {m: smooth(loss[d][m])[-1] for m in ("Ours", "Baseline")} for d in datasets}
print("takeaway best accuracy:", {d: {m: f"{v:#.3g}" for m, v in b.items()} for d, b in best.items()})
print("takeaway final smoothed loss:", {d: {m: f"{v:#.3g}" for m, v in b.items()} for d, b in final_loss.items()})
for d in datasets:
    assert best[d]["Ours"] > best[d]["Baseline"], "the takeaway does not hold"
    assert final_loss[d]["Ours"] < final_loss[d]["Baseline"], "the takeaway does not hold"

fig, axes = plt.subplots(1, 4, figsize=(5.5, 5.5), sharex=True, layout="constrained")
axes[1].sharey(axes[0])
axes[3].sharey(axes[2])

for ax, d in zip(axes[:2], datasets):
    ax.plot(epochs, accuracy[d]["Baseline"], color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_width, label="Baseline")
    ax.plot(epochs, accuracy[d]["Ours"], color=colors["ours"], label="Ours")
    ax.set_title(d)

for ax, d in zip(axes[2:], datasets):
    ax.plot(epochs, loss[d]["Baseline"], color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_width, alpha=0.25)
    ax.plot(epochs, smooth(loss[d]["Baseline"]), color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_width, label="Baseline")
    ax.plot(epochs, loss[d]["Ours"], color=colors["ours"], alpha=0.25)
    ax.plot(epochs, smooth(loss[d]["Ours"]), color=colors["ours"], label="Ours")
    ax.set_title(d)

for ax in axes:
    ax.grid(True)
    ax.set_xticks([1, 20, 40, 60])
axes[0].set_ylabel("Val. accuracy")
axes[2].set_ylabel("Train loss")
axes[1].tick_params(labelleft=False)
axes[3].tick_params(labelleft=False)
fig.supxlabel("Epoch")

handles, labels = axes[0].get_legend_handles_labels()
order = [labels.index("Ours"), labels.index("Baseline")]
fig.legend([handles[i] for i in order], [labels[i] for i in order], loc="outside upper center",
           ncol=2, frameon=False, borderaxespad=0)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/accuracy-and-loss.pdf")
fig.savefig("../outputs/accuracy-and-loss.png")
