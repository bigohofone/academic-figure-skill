"""Figure 2: AIME accuracy (avg@32) over training with and without Clip-Higher. With Clip-Higher, accuracy keeps rising to a best of 0.406, while without it, it plateaus at 0.269."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/dapo.json"))["fig2a"]

fig, ax = plt.subplots(figsize=(2.75, 2))
series = [
    ("w/ Clip-Higher", colors["ours"]),
    ("w/o Clip-Higher", colors["neutral"]),
]
for name, color in series:
    curve = data[name]
    ax.plot(curve["step"], curve["value"], color=color, label=name)
for name, color in series:
    curve = data[name]
    best = max(curve["value"])
    mark_value(ax, curve["step"][curve["value"].index(best)], best, f"{best:#.3g}", color)

ax.set_xlabel("Training steps")
ax.set_ylabel("AIME avg@32")
ax.xaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
ax.legend(loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig2.pdf")
fig.savefig("../outputs/dapo-fig2.png")
