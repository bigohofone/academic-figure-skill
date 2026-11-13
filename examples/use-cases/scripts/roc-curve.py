"""ROC curves of AI-text detectors. W/ P and W/o P are Ours with and without the golden prompt; the thin diagonal marks chance; the AUC in each legend entry is computed from the curve with the trapezoidal rule. With the golden prompt, Ours reaches an AUC of 0.987, against 0.905 without it and 0.647 for GPTZero, the best baseline."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/paper-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure

colors = paper.colors

data = json.load(open("../data/roc-curve.json"))
curves = {m["name"]: (np.array(m["fpr"]), np.array(m["tpr"])) for m in data["methods"]}

# the data gives no AUC: computed from each curve
auc = {name: np.trapezoid(tpr, fpr) for name, (fpr, tpr) in curves.items()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in auc.items()})
assert auc["Ours: W/ P"] > max(v for name, v in auc.items() if name != "Ours: W/ P"), "the takeaway does not hold"
assert auc["Ours: W/o P"] > max(auc["OpenAI"], auc["GPTZero"]), "ours without the prompt does not beat the baselines"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")

# variants of ours in the ours color, told apart by line style; baselines grey, in ascending order of AUC
styles = {
    "Ours: W/ P": dict(color=colors["ours"], linestyle="-"),
    "Ours: W/o P": dict(color=colors["ours"], linestyle="--", linewidth=paper.dashed_linewidth),
    "OpenAI": dict(color=colors["neutral"], linestyle="--", linewidth=paper.dashed_linewidth),
    "GPTZero": dict(color=colors["neutral"], linestyle=":", linewidth=paper.dashed_linewidth),
}
ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
for name in ["OpenAI", "GPTZero", "Ours: W/o P", "Ours: W/ P"]:
    fpr, tpr = curves[name]
    ax.plot(fpr, tpr, label=f"{name} (AUC {auc[name]:#.3g})", **styles[name])

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.grid(True)
handles, labels = ax.get_legend_handles_labels()
order = [3, 2, 0, 1]  # the full method first, then its variant, then the baselines
ax.legend([handles[i] for i in order], [labels[i] for i in order])

finalize_figure(fig, ax)
fig.savefig("../outputs/roc-curve.pdf")
fig.savefig("../outputs/roc-curve.png")
