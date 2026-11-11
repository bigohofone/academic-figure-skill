"""Validation accuracy on CIFAR-100 versus training epochs. Lines show the mean and shaded bands ±1 std over 5 seeds; thin horizontal lines and circles mark the best mean accuracy of Ours and Mixup. Ours reaches the highest best mean accuracy, 0.915, ahead of Mixup (0.897) and Baseline (0.882)."""

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

# Takeaway: ours reaches the highest best mean validation accuracy.
best = {name: m.max() for name, m in mean.items()}
best_epoch = {name: epochs[m.argmax()] for name, m in mean.items()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()}, "at epochs", best_epoch)
assert best["Ours"] > max(v for name, v in best.items() if name != "Ours"), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")

# Baselines in ascending order of best accuracy, told apart by line style; ours solid in color.
style = {
    "Baseline": dict(color=colors["neutral"], linestyle="--", linewidth=paper.dashed_width),
    "Mixup": dict(color=colors["neutral"], linestyle=":", linewidth=paper.dashed_width),
    "Ours": dict(color=colors["ours"], linestyle="-"),
}
handles = {}
for name in ["Baseline", "Mixup", "Ours"]:
    s = style[name]
    ax.fill_between(epochs, mean[name] - std[name], mean[name] + std[name], color=s["color"], alpha=0.2, linewidth=0)
    (handles[name],) = ax.plot(epochs, mean[name], label=name, **s)

# Three marks do not fit apart, so ours and its closest competitor are marked; Baseline's value is in the caption.
for name in ["Mixup", "Ours"]:
    mark_value(ax, best_epoch[name], best[name], f"{best[name]:#.3g}", style[name]["color"], below=(name != "Ours"))

ax.set_xlabel("Epoch")
ax.set_ylabel("Validation accuracy")
ax.grid(True)
ax.legend([handles["Ours"], handles["Baseline"], handles["Mixup"]], ["Ours", "Baseline", "Mixup"], loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/learning-curve.pdf")
fig.savefig("../outputs/learning-curve.png")
