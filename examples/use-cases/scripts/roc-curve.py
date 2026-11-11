"""Figure 8: ROC curves for detecting GPT-3.5-turbo text completed by humans on Reddit, with DNA-GPT scoring a sliding window (each half of a text) and the baselines scoring the whole text. The dashed diagonal marks chance; AUC values are computed from the curves with the trapezoidal rule. DNA-GPT reaches an AUC of 0.987 with the golden prompt and 0.905 without it, against 0.647 for GPTZero and 0.565 for OpenAI's classifier."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

methods = {m["name"]: m for m in json.load(open("../data/roc-curve.json"))["methods"]}

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.axline((0, 0), (1, 1), linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
handles = []
for name, label, color, linestyle, marker in [
        ("Ours: W/ P", "Ours", colors["ours"], "-", "o"),
        ("Ours: W/o P", "Ours w/o prompt", colors["ours"], "--", "s"),
        ("OpenAI", "OpenAI", colors["neutral"], "-", "^"),
        ("GPTZero", "GPTZero", colors["neutral"], "--", "D")]:
    fpr, tpr = methods[name]["fpr"], methods[name]["tpr"]
    auc = np.trapezoid(tpr, fpr)
    linewidth = paper.dashed_width if linestyle != "-" else None
    (h,) = ax.plot(fpr, tpr, linestyle=linestyle, linewidth=linewidth, marker=marker, color=color,
                   markevery=max(1, len(fpr) // 10), label=f"{label} (AUC {auc:#.3g})")
    handles.append(h)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
ax.set_xticks(ticks, labels=[f"{t:,.10g}" for t in ticks])
ax.set_yticks(ticks, labels=["", *[f"{t:,.10g}" for t in ticks[1:]]])
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=1, frameon=False)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/roc-curve.pdf")
fig.savefig("../outputs/roc-curve.png")
