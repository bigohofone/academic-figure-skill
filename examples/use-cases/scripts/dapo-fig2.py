"""AIME accuracy (avg@32) over training steps, with and without Clip-Higher. Thin horizontal lines and circles mark each run's best accuracy. With Clip-Higher, the best accuracy reaches 0.406, against 0.269 without it."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, darken


def mark_best(ax, x, y, text, color, **kw):
    """The paper's figure draws each run's best as a line across the panel, so this one does too."""
    ax.axhline(y, linewidth=plt.rcParams["grid.linewidth"], color=darken(color), zorder=1)
    mark_value(ax, x, y, text, color, **kw)

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    runs = json.load(f)["fig2a"]
ours = runs["w/ Clip-Higher"]
ablation = runs["w/o Clip-Higher"]

best_ours = int(np.argmax(ours["value"]))
best_ablation = int(np.argmax(ablation["value"]))
print("takeaway:", {
    "w/ Clip-Higher": (ours["step"][best_ours], f"{ours['value'][best_ours]:#.3g}"),
    "w/o Clip-Higher": (ablation["step"][best_ablation], f"{ablation['value'][best_ablation]:#.3g}"),
})
assert ours["value"][best_ours] > ablation["value"][best_ablation], "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Clip-Higher")
ax.plot(ablation["step"], ablation["value"], color=colors["neutral"], linestyle="--",
        linewidth=paper.dashed_width, label="w/o Clip-Higher")
mark_best(ax, ours["step"][best_ours], ours["value"][best_ours],
           f"{ours['value'][best_ours]:#.3g}", colors["ours"])
mark_best(ax, ablation["step"][best_ablation], ablation["value"][best_ablation],
           f"{ablation['value'][best_ablation]:#.3g}", colors["neutral"])
ax.set_xlabel("Training step")
ax.set_ylabel("AIME accuracy")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig2.pdf")
fig.savefig("../outputs/dapo-fig2.png")
