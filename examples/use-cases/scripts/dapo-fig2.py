"""Figure 2: Accuracy on AIME (avg@32) over training, with and without Clip-Higher. Dashed lines mark
each run's best accuracy. With Clip-Higher, accuracy keeps rising to a best of 0.406, while without
it stalls early at a best of 0.269.
"""

import json
import math
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")  # the skill's style files
import paper  # registers the bundled Inter font
from paper import fit_height, mark_value, smooth, darken, lighten, text_color, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/dapo.json") as f:
    data = json.load(f)["fig2a"]

fig, ax = plt.subplots(figsize=(2.75, 2))
ours, base = data["w/ Clip-Higher"], data["w/o Clip-Higher"]
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Clip-Higher")
ax.plot(base["step"], base["value"], color=colors["neutral"], label="w/o Clip-Higher")

for run, color in [(ours, colors["ours"]), (base, colors["neutral"])]:
    best = int(np.argmax(run["value"]))
    mark_value(ax, run["step"][best], run["value"][best], f"{run['value'][best]:#.3g}", color)

ax.set_xlabel("Training steps")
ax.set_ylabel("AIME avg@32")
ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))
ax.legend(loc="lower right")
fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig2.pdf")
fig.savefig("../outputs/dapo-fig2.png")
