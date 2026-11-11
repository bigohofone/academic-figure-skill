"""AIME accuracy (avg@32, 0–1) over training steps with and without Clip-Higher. Thin horizontal lines mark each run's best accuracy. With Clip-Higher, accuracy peaks at 0.406, against 0.269 without it."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    runs = json.load(f)["fig2a"]
ours = runs["w/ Clip-Higher"]
ablation = runs["w/o Clip-Higher"]

best = {name: max(run["value"]) for name, run in runs.items()}
print("takeaway:", {name: f"{v:#.3g}" for name, v in best.items()})
assert best["w/ Clip-Higher"] > best["w/o Clip-Higher"], "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Clip-Higher")
ax.plot(ablation["step"], ablation["value"], linestyle="--", linewidth=paper.dashed_width,
        color=colors["neutral"], label="w/o Clip-Higher")

for run, color in [(ours, colors["ours"]), (ablation, colors["neutral"])]:
    i = run["value"].index(max(run["value"]))
    mark_value(ax, run["step"][i], run["value"][i], f"{run['value'][i]:#.3g}", color)

ax.set_xlabel("Training step")
ax.set_ylabel("AIME accuracy")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig2.pdf")
fig.savefig("../outputs/dapo-fig2.png")
