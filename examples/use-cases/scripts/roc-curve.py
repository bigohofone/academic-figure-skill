"""ROC curves of AI-generated-text detectors. The thin diagonal marks chance; AUC is computed from each curve with the trapezoidal rule. Ours with the golden prompt reaches an AUC of 0.987 and without it 0.905, against 0.647 for GPTZero and 0.565 for OpenAI."""

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

# Takeaway: both variants of ours have a higher AUC than either baseline.
print("takeaway (AUC):", {name: f"{v:#.3g}" for name, v in auc.items()})
assert min(auc["Ours: W/ P"], auc["Ours: W/o P"]) > max(auc["OpenAI"], auc["GPTZero"]), "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)

# Variants of ours: solid, in the ours color, told apart by marker; baselines grey, by line style,
# in ascending order of AUC (OpenAI, then GPTZero). Legend: the full method first.
style = {
    "Ours: W/ P": dict(color=colors["ours"], linestyle="-", marker="o"),
    "Ours: W/o P": dict(color=colors["ours"], linestyle="-", marker="s"),
    "OpenAI": dict(color=colors["neutral"], linestyle="--", linewidth=paper.dashed_width, marker="^"),
    "GPTZero": dict(color=colors["neutral"], linestyle=":", linewidth=paper.dashed_width, marker="D"),
}
handles = []
for name in ["Ours: W/ P", "Ours: W/o P", "OpenAI", "GPTZero"]:
    fpr, tpr = curves[name]
    (h,) = ax.plot(fpr, tpr, markevery=max(1, len(fpr) // 10), label=f"{name} (AUC {auc[name]:#.3g})", **style[name])
    handles.append(h)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.grid(True)
ax.legend(handles=handles, loc="lower right")

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/roc-curve.pdf")
fig.savefig("../outputs/roc-curve.png")
