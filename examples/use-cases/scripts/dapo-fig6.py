"""AIME accuracy (avg@32, 0–1) over training steps with and without Dynamic Sampling. Thin horizontal lines mark each run's best accuracy. With Dynamic Sampling, training reaches the best accuracy of the run without it (0.421, at step 6080) by step 2160, 2.81× fewer steps, and peaks at 0.438."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    runs = json.load(f)["fig6"]
ours = runs["w/ Dynamic Sampling"]
ablation = runs["w/o Dynamic Sampling"]

best = {name: max(run["value"]) for name, run in runs.items()}
ablation_best_step = ablation["step"][ablation["value"].index(best["w/o Dynamic Sampling"])]
ours_reaches_step = next(s for s, v in zip(ours["step"], ours["value"]) if v >= best["w/o Dynamic Sampling"])
speedup = ablation_best_step / ours_reaches_step
print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()},
      f"ablation best at step {ablation_best_step:.0f}, ours reaches it at step {ours_reaches_step:.0f}, {speedup:#.3g}x")
assert best["w/ Dynamic Sampling"] > best["w/o Dynamic Sampling"] and speedup > 1, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Dynamic Sampling")
ax.plot(ablation["step"], ablation["value"], linestyle="--", linewidth=paper.dashed_width,
        color=colors["neutral"], label="w/o Dynamic Sampling")

for run, color in [(ours, colors["ours"]), (ablation, colors["neutral"])]:
    i = run["value"].index(max(run["value"]))
    mark_value(ax, run["step"][i], run["value"][i], f"{run['value'][i]:#.3g}", color)

ax.set_xlabel("Training step")
ax.set_ylabel("AIME accuracy")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig6.pdf")
fig.savefig("../outputs/dapo-fig6.png")
