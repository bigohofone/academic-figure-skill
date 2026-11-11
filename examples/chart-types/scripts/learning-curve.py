"""Figure 1: Validation accuracy on CIFAR-100 during training for our augmentation, Mixup and the baseline. Lines show the mean and shaded bands ±1 std over 5 seeds; dashed lines mark the final mean accuracy of ours and Mixup. Ours ends at 91.2%, 1.7 points above Mixup (89.5%) and 3.5 points above the baseline (87.8%)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/learning-curve.json"))
epochs = np.array(data["epochs"])

fig, ax = plt.subplots(figsize=(2.75, 2))
handles = {}
for name, color, linestyle in [("Baseline", colors["neutral"], "-"),
                               ("Mixup", colors["neutral"], "--"),
                               ("Ours", colors["ours"], "-")]:
    runs = np.array(data["accuracy"][name]) * 100
    mean, std = runs.mean(axis=0), runs.std(axis=0)
    linewidth = paper.dashed_width if linestyle != "-" else None
    (handles[name],) = ax.plot(epochs, mean, linestyle=linestyle, linewidth=linewidth, color=color, label=name)
    ax.fill_between(epochs, mean - std, mean + std, color=color, alpha=0.2, linewidth=0)
    if name != "Baseline":
        mark_value(ax, epochs[-1], mean[-1], f"{mean[-1]:#.3g}", color, below=name == "Mixup")

ax.set_xlabel("Epoch")
ax.set_ylabel("Validation accuracy (%)")
ax.legend([handles["Ours"], handles["Baseline"], handles["Mixup"]], ["Ours", "Baseline", "Mixup"], loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/learning-curve.pdf")
fig.savefig("../outputs/learning-curve.png")
