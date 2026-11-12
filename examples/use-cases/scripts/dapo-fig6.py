"""AIME accuracy (avg@32) over training steps, with and without dynamic sampling. Thin horizontal lines and circles mark each run's best accuracy. With dynamic sampling, accuracy passes the ablation's best (0.421, at step 6080) at step 2160, 2.81× fewer steps, and peaks higher, at 0.438."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, mark_value, darken


def mark_best(ax, x, y, text, color, **kw):
    """The paper's figure draws each run's best as a line across the panel, so this one does too."""
    ax.axhline(y, linewidth=plt.rcParams["grid.linewidth"], color=darken(color), zorder=1)
    mark_value(ax, x, y, text, color, **kw)

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    runs = json.load(f)["fig6"]
ours = runs["w/ Dynamic Sampling"]
ablation = runs["w/o Dynamic Sampling"]

best_ours = int(np.argmax(ours["value"]))
best_ablation = int(np.argmax(ablation["value"]))
ablation_best = ablation["value"][best_ablation]
ablation_best_step = ablation["step"][best_ablation]
ours_reaches = next(s for s, v in zip(ours["step"], ours["value"]) if v >= ablation_best)
speedup = ablation_best_step / ours_reaches
print("takeaway:", {
    "w/ best": f"{ours['value'][best_ours]:#.3g}",
    "w/o best": f"{ablation_best:#.3g}",
    "w/o best step": f"{ablation_best_step:.0f}",
    "w/ reaches it at": f"{ours_reaches:.0f}",
    "speedup": f"{speedup:#.3g}×",
})
assert ours["value"][best_ours] > ablation_best and ours_reaches < ablation_best_step, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Dynamic Sampling")
ax.plot(ablation["step"], ablation["value"], color=colors["neutral"], linestyle="--",
        linewidth=paper.dashed_width, label="w/o Dynamic Sampling")
mark_best(ax, ours["step"][best_ours], ours["value"][best_ours],
           f"{ours['value'][best_ours]:#.3g}", colors["ours"])
mark_best(ax, ablation_best_step, ablation_best, f"{ablation_best:#.3g}", colors["neutral"])
ax.set_xlabel("Training step")
ax.set_ylabel("AIME accuracy")
ax.legend()

finalize_figure(fig, ax)
fig.savefig("../outputs/dapo-fig6.pdf")
fig.savefig("../outputs/dapo-fig6.png")
