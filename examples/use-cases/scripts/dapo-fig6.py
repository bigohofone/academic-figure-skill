"""AIME accuracy with and without Dynamic Sampling over training steps. Accuracy is avg@32. Thin horizontal lines mark each run's best accuracy. With Dynamic Sampling, training reaches the best accuracy of the run without it (0.421) after 2160 steps instead of 6080, 2.81× fewer.
"""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    runs = json.load(f)["fig6"]
ours = runs["w/ Dynamic Sampling"]
ablation = runs["w/o Dynamic Sampling"]

ablation_best = max(ablation["value"])
ablation_step = ablation["step"][int(np.argmax(ablation["value"]))]
ours_step = next(s for s, v in zip(ours["step"], ours["value"]) if v >= ablation_best)
print("takeaway:", f"w/o best {ablation_best:#.3g} at step {ablation_step:.0f}; w/ reaches it at step {ours_step:.0f};",
      f"{ablation_step / ours_step:#.3g}x fewer steps; w/ best {max(ours['value']):#.3g}")
assert ours_step < ablation_step, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Dynamic Sampling")
ax.plot(ablation["step"], ablation["value"], "--", linewidth=paper.dashed_width, color=colors["neutral"],
        label="w/o Dynamic Sampling")

for run, color in ((ours, colors["ours"]), (ablation, colors["neutral"])):
    i = int(np.argmax(run["value"]))
    mark_value(ax, run["step"][i], run["value"][i], f"{run['value'][i]:#.3g}", color)

ax.set_xlabel("Training step")
ax.set_ylabel("AIME accuracy")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig6.pdf")
fig.savefig("../outputs/dapo-fig6.png")
