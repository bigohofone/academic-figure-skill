"""Validation accuracy and training loss of Ours and the Baseline over 60 epochs on CIFAR-10 and CIFAR-100. The left two panels show validation accuracy and the right two training loss, smoothed with a moving average over 5% of the epochs, with faint lines showing raw values. Ours reaches a higher best validation accuracy than the Baseline on both datasets, 0.960 vs. 0.932 on CIFAR-10 and 0.780 vs. 0.734 on CIFAR-100, and ends at a lower training loss, 0.120 vs. 0.186 and 0.853 vs. 1.05."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, smooth

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/accuracy-and-loss.json") as f:
    data = json.load(f)
epochs = data["epochs"]
accuracy = data["validation_accuracy"]
loss = data["training_loss"]
datasets = ["CIFAR-10", "CIFAR-100"]

# Takeaway: Ours reaches a higher best validation accuracy and a lower final training loss on both datasets.
best = {ds: {m: max(accuracy[ds][m]) for m in ["Ours", "Baseline"]} for ds in datasets}
final_loss = {ds: {m: loss[ds][m][-1] for m in ["Ours", "Baseline"]} for ds in datasets}
print("takeaway best accuracy:", {ds: {m: f"{v:#.3g}" for m, v in b.items()} for ds, b in best.items()})
print("takeaway final loss:", {ds: {m: f"{v:#.3g}" for m, v in l.items()} for ds, l in final_loss.items()})
for ds in datasets:
    assert best[ds]["Ours"] > best[ds]["Baseline"], "the takeaway does not hold"
    assert final_loss[ds]["Ours"] < final_loss[ds]["Baseline"], "the takeaway does not hold"

# Two groups side by side: accuracy (CIFAR-10, CIFAR-100), then loss (CIFAR-10, CIFAR-100).
fig, axes = plt.subplots(1, 4, figsize=(5.5, 5.5), sharex=True, layout="constrained")
axes[1].sharey(axes[0])
axes[3].sharey(axes[2])

for ax, ds in zip(axes[:2], datasets):
    ax.plot(epochs, accuracy[ds]["Ours"], color=colors["ours"], label="Ours")
    ax.plot(epochs, accuracy[ds]["Baseline"], color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_width, label="Baseline")
    ax.set_title(ds)

for ax, ds in zip(axes[2:], datasets):
    ax.plot(epochs, loss[ds]["Ours"], color=colors["ours"], alpha=0.25)
    ax.plot(epochs, loss[ds]["Baseline"], color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_width, alpha=0.25)
    ax.plot(epochs, smooth(loss[ds]["Ours"]), color=colors["ours"], label="Ours")
    ax.plot(epochs, smooth(loss[ds]["Baseline"]), color=colors["neutral"], linestyle="--",
            linewidth=paper.dashed_width, label="Baseline")
    ax.set_title(ds)

for ax in axes:
    ax.grid(True)
    ax.set_xticks([0, 20, 40, 60])
axes[1].tick_params(labelleft=False)
axes[3].tick_params(labelleft=False)
axes[0].set_ylabel("Accuracy")
axes[2].set_ylabel("Training loss")
fig.supxlabel("Epoch")

fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper center", ncol=2,
           frameon=False, borderaxespad=0)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/accuracy-and-loss.pdf")
fig.savefig("../outputs/accuracy-and-loss.png")
