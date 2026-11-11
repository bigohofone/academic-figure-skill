"""Figure 3: Response lengths of the base model and our RL-trained model on three math benchmarks. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range, and points mark values beyond the whiskers (60 responses per box). RL training lengthens responses most on the hardest benchmark: on AIME the median grows from 872 to 1670 tokens, 1.91×."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/grouped-box-plot.json") as f:
    data = json.load(f)
datasets = data["datasets"]
lengths = data["lengths"]

series = [("Base", "Base", greys(1)[0]), ("RL (ours)", "RL (ours)", lighten(colors["ours"]))]
width = 0.8 / len(series)

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
for i, (key, name, fill) in enumerate(series):
    for x, dataset in enumerate(datasets):
        box = ax.boxplot(lengths[key][dataset], positions=[x + (i - (len(series) - 1) / 2) * width],
                         widths=0.8 * width, patch_artist=True)
        box["boxes"][0].set_facecolor(fill)
ax.set_xticks(range(len(datasets)), labels=datasets)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Length (tokens)")
ax.legend([Patch(facecolor=fill, edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"]) for _, _, fill in series],
          [name for _, name, _ in series], loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-box-plot.pdf")
fig.savefig("../outputs/grouped-box-plot.png")
