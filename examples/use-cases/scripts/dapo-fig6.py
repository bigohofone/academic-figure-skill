"""Figure 6: Accuracy on AIME (avg@32) over training on a baseline setting, before and after applying
dynamic sampling. Dashed lines mark each run's best accuracy. With dynamic sampling, the run reaches
its best of 0.438 at step 2,320, while without it the best is 0.421, reached only at step 6,080,
2.6× more steps.
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
    data = json.load(f)["fig6"]

fig, ax = plt.subplots(figsize=(2.75, 2))
ours, base = data["w/ Dynamic Sampling"], data["w/o Dynamic Sampling"]
ax.plot(ours["step"], ours["value"], color=colors["ours"], label="w/ Dynamic Sampling")
ax.plot(base["step"], base["value"], color=colors["neutral"], label="w/o Dynamic Sampling")

for run, color in [(ours, colors["ours"]), (base, colors["neutral"])]:
    best = int(np.argmax(run["value"]))
    mark_value(ax, run["step"][best], run["value"][best], f"{run['value'][best]:#.3g}", color)

ax.set_xlabel("Training steps")
ax.set_ylabel("AIME avg@32")
ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))
ax.legend(loc="lower right")
fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/dapo-fig6.pdf")
fig.savefig("../outputs/dapo-fig6.png")
