"""Figure 6: AIME accuracy (avg@32) over training steps with and without Dynamic Sampling. Dashed lines mark each run's best accuracy. With Dynamic Sampling, accuracy peaks at 0.438 after 2320 steps; without it, the best is 0.421, reached only after 6080 steps."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    data = json.load(f)["fig6"]

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")

# ours first (legend order), the ablation in neutral
for name, color, below in [("w/ Dynamic Sampling", colors["ours"], False),
                           ("w/o Dynamic Sampling", colors["neutral"], False)]:
    step, value = data[name]["step"], data[name]["value"]
    ax.plot(step, value, color=color, label=name)
    best = max(range(len(value)), key=lambda i: value[i])
    mark_value(ax, step[best], value[best], f"{value[best]:#.3g}", color, below=below)

ax.set_xlabel("Training step")
ax.set_ylabel("AIME avg@32")
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig6.pdf")
fig.savefig("../outputs/dapo-fig6.png")
