"""pass@1 and pass@128 performances on extrapolative tasks under varying mid- and post-training mixture ratios. The data used in mid- and post-training is applied within the OOD-edge ranges. Different lines indicate the compute allocation strategies. Heavy-RL always improves the unseen OOD-hard tasks, while Light-RL improves best pass@1 on OOD-edge tasks."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

data = json.load(open("../data/mid-rl-split.json"))
strategies = ["Full Mid", "Full RL", "Light RL", "Heavy RL"]
split = "OOD-hard (op=15-20)"  # (b) of Figure 6, split from the 1 x 4 original so each part is one range of tasks

mean = {m: {s: np.mean(data[m][split][s]) for s in strategies} for m in data}
print("takeaway: mean OOD-hard", {m: {s: f"{v:#.3g}" for s, v in by_s.items()} for m, by_s in mean.items()})
assert all(by_s["Heavy RL"] == max(by_s.values()) for by_s in mean.values()), "Heavy RL is not best on OOD-hard"

fig, axes = plt.subplots(1, 2, figsize=(3.087, 3.087), layout="constrained")

# the takeaway names Light RL and Heavy RL; the full-budget strategies are grey and dashed
greys = make_shades(colors["neutral"], 2)
styles = {
    "Full Mid": dict(color=greys[0], linestyle="--", linewidth=paper.dashed_linewidth, marker="o"),
    "Full RL": dict(color=greys[1], linestyle=":", linewidth=paper.dashed_linewidth, marker="s"),
    "Light RL": dict(color=paper.series_colors[0], marker="^"),
    "Heavy RL": dict(color=paper.series_colors[1], marker="D"),
}
for ax, metric in zip(axes, data):
    values = data[metric][split]
    for name in strategies:
        ax.plot(values["op"], values[name], label=name, **styles[name])
    ax.set_xticks(values["op"])
    ax.set_title(metric)
    ax.grid(True)
axes[0].set_ylabel("pass@k (%)")
fig.supxlabel("Task Difficulty")
# no legend: (a) beside it carries the one legend for both parts

finalize_figure(fig, axes, height="XS")
fig.savefig("../out/mid-rl-split-b.pdf")
