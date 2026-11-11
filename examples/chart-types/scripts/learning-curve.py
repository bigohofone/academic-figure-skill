"""Validation accuracy on CIFAR-100 during training. Lines show the mean and shaded bands ±1 std over 5 seeds; circles and thin lines mark the best mean accuracy of Ours and Mixup. Ours reaches a best accuracy of 0.915, above Mixup (0.897) and Baseline (0.882)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/learning-curve.json") as f:
    data = json.load(f)
epochs = np.array(data["epochs"])
runs = {name: np.array(seeds) for name, seeds in data["accuracy"].items()}
mean = {name: r.mean(axis=0) for name, r in runs.items()}
std = {name: r.std(axis=0) for name, r in runs.items()}

best = {name: m.max() for name, m in mean.items()}
best_epoch = {name: epochs[m.argmax()] for name, m in mean.items()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()}, "at epochs", best_epoch)
assert best["Ours"] > max(v for name, v in best.items() if name != "Ours"), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))

# Ours first; grey series in ascending order of best accuracy, told apart by line style
series = [
    ("Ours", colors["ours"], "-", rcParams["lines.linewidth"]),
    ("Baseline", colors["neutral"], "--", paper.dashed_width),
    ("Mixup", colors["neutral"], ":", paper.dashed_width),
]
for name, color, style, width in series:
    ax.fill_between(epochs, mean[name] - std[name], mean[name] + std[name], color=color, alpha=0.2, linewidth=0)
    ax.plot(epochs, mean[name], linestyle=style, linewidth=width, color=color, label=name)

# three marks collide in every placement: mark ours and its closest competitor; Baseline's value is in the caption
mark_value(ax, best_epoch["Ours"], best["Ours"], f"{best['Ours']:#.3g}", colors["ours"])
mark_value(ax, best_epoch["Mixup"], best["Mixup"], f"{best['Mixup']:#.3g}", colors["neutral"], below=True)

ax.set_xlabel("Epoch")
ax.set_ylabel("Validation accuracy")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/learning-curve.pdf")
fig.savefig("../outputs/learning-curve.png")
