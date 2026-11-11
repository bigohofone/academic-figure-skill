"""Figure 6: AIME accuracy (avg@32) over training of a baseline setting with and without dynamic sampling. With dynamic sampling, accuracy peaks at 0.438 after 2,320 steps, above the 0.421 that the run without it reaches only after 6,080 steps."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/dapo.json"))["fig6"]

fig, ax = plt.subplots(figsize=(2.75, 2))
series = [
    ("w/ Dynamic Sampling", colors["ours"]),
    ("w/o Dynamic Sampling", colors["neutral"]),
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
fig.savefig("../outputs/dapo-fig6.pdf")
fig.savefig("../outputs/dapo-fig6.png")
