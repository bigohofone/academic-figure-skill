"""ROC curves of AI-text detectors. The thin diagonal marks chance; the area under each curve (AUC), in the legend, is computed from the curve by the trapezoidal rule. Ours with the golden prompt reaches an AUC of 0.987, ahead of Ours without it (0.905), GPTZero (0.647) and OpenAI (0.565)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/roc-curve.json") as f:
    data = json.load(f)
curves = {m["name"]: (np.array(m["fpr"]), np.array(m["tpr"])) for m in data["methods"]}
auc = {name: np.trapezoid(tpr, fpr) for name, (fpr, tpr) in curves.items()}

print("takeaway:", {name: f"{v:#.3g}" for name, v in auc.items()})
assert auc["Ours: W/ P"] > max(v for name, v in auc.items() if name != "Ours: W/ P"), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))

ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)

# variants of ours: ours color, solid, told apart by marker; baselines grey, by line style,
# in ascending order of AUC
baselines = sorted(["OpenAI", "GPTZero"], key=lambda name: auc[name])
series = [
    ("Ours: W/ P", colors["ours"], "-", rcParams["lines.linewidth"], "o"),
    ("Ours: W/o P", colors["ours"], "-", rcParams["lines.linewidth"], "s"),
    (baselines[0], colors["neutral"], "--", paper.dashed_width, "^"),
    (baselines[1], colors["neutral"], ":", paper.dashed_width, "D"),
]
for name, color, style, width, marker in series:
    fpr, tpr = curves[name]
    ax.plot(fpr, tpr, linestyle=style, linewidth=width, marker=marker, markevery=max(1, len(fpr) // 10),
            color=color, label=f"{name} (AUC {auc[name]:#.3g})")

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/roc-curve.pdf")
fig.savefig("../outputs/roc-curve.png")
