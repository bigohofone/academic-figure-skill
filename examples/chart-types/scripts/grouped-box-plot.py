"""Figure 1: Response lengths of the base model and our RL-trained model on three datasets. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range, and points mark values beyond them. RL training lengthens responses on every dataset, most on AIME, where the median grows 1.9× from 873 to 1,670 tokens."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, lighten, greys

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/grouped-box-plot.json"))
datasets = data["datasets"]
series = [("Base", colors["neutral"]), ("RL (ours)", colors["ours"])]
width = 0.8 / len(series)

fig, ax = plt.subplots(figsize=(2.75, 2))
for i, (name, color) in enumerate(series):
    for x, dataset in enumerate(datasets):
        box = ax.boxplot(data["lengths"][name][dataset], positions=[x + (i - (len(series) - 1) / 2) * width],
                         widths=0.8 * width)
        box["boxes"][0].set_facecolor(lighten(color))
ax.set_xticks(range(len(datasets)), labels=datasets)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.10g}".replace("-", "−"))
ax.set_ylabel("Length (tokens)")
ax.legend(handles=[Patch(facecolor=lighten(color), edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"], label=name)
                   for name, color in series], loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-box-plot.pdf")
fig.savefig("../outputs/grouped-box-plot.png")
