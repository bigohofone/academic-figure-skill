"""pass@1 and pass@128 performances on extrapolative tasks under varying mid- and post-training mixture ratios. The data used in mid- and post-training is applied within the OOD-edge ranges. Different lines indicate the compute allocation strategies. Heavy-RL always improves the unseen OOD-hard tasks, while Light-RL improves best pass@1 on OOD-edge tasks."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

data = json.load(open("../data/mid-rl-split.json"))
strategies = ["Full Mid", "Full RL", "Light RL", "Heavy RL"]
panels = [(metric, title, values) for metric, by_range in data.items() for title, values in by_range.items()]

best_edge = {s: max(data["pass@1"]["OOD-edge (op=11-14)"][s]) for s in strategies}
mean_hard = {m: {s: np.mean(data[m]["OOD-hard (op=15-20)"][s]) for s in strategies} for m in data}
print("takeaway: best pass@1 on OOD-edge", best_edge)
print("takeaway: mean OOD-hard", {m: {s: f"{v:#.3g}" for s, v in by_s.items()} for m, by_s in mean_hard.items()})
assert best_edge["Light RL"] == max(best_edge.values()), "Light RL is not best at pass@1 on OOD-edge"
assert all(by_s["Heavy RL"] == max(by_s.values()) for by_s in mean_hard.values()), "Heavy RL is not best on OOD-hard"

fig, axes = plt.subplots(1, 4, figsize=(6.24, 6.24), layout="constrained")

# the takeaway names Light RL and Heavy RL; the full-budget strategies are grey and dashed
greys = make_shades(colors["neutral"], 2)
styles = {
    "Full Mid": dict(color=greys[0], linestyle="--", linewidth=paper.dashed_linewidth, marker="o"),
    "Full RL": dict(color=greys[1], linestyle=":", linewidth=paper.dashed_linewidth, marker="s"),
    "Light RL": dict(color=paper.series_colors[0], marker="^"),
    "Heavy RL": dict(color=paper.series_colors[1], marker="D"),
}
for ax, (metric, title, values) in zip(axes, panels):
    for name in strategies:
        ax.plot(values["op"], values[name], label=name, **styles[name])
    ax.set_xticks(values["op"])
    ax.set_title(f"{metric}\n{title}")
    ax.grid(True)

axes[0].set_ylabel("pass@k (%)")
fig.supxlabel("Task Difficulty")
axes[0].legend()

# original height / width 172.8 / 748.8 = 0.23, 1.44 in printed; XS gives the closest height
finalize_figure(fig, axes, height="S")
fig.savefig("../out/mid-rl-split.pdf")
