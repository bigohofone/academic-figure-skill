"""Response lengths of the base model and our RL-trained model on three math benchmarks. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range, and points are responses beyond the whiskers; each box holds 60 responses. RL training lengthens responses on every benchmark, most on AIME, where the median grows from 872 to 1670 tokens (1.91×)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/grouped-box-plot.json") as f:
    data = json.load(f)
datasets = data["datasets"]
lengths = data["lengths"]

medians = {model: {d: np.median(lengths[model][d]) for d in datasets} for model in lengths}
ratios = {d: medians["RL (ours)"][d] / medians["Base"][d] for d in datasets}
print("takeaway: medians", {m: {d: f"{v:.0f}" if v >= 1000 else f"{v:#.3g}".rstrip(".") for d, v in x.items()}
                            for m, x in medians.items()},
      "ratios", {d: f"{r:#.3g}×" for d, r in ratios.items()})
assert all(r > 1 for r in ratios.values()), "the takeaway does not hold"
assert max(ratios, key=ratios.get) == "AIME", "the takeaway does not hold"

models = [("Base", colors["neutral"]), ("RL (ours)", colors["ours"])]
width = 0.8 / len(models)

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for i, (model, color) in enumerate(models):
    for x, d in enumerate(datasets):
        box = ax.boxplot(lengths[model][d], positions=[x + (i - (len(models) - 1) / 2) * width],
                         widths=0.8 * width, patch_artist=True)
        box["boxes"][0].set_facecolor(lighten(color))

ax.set_xticks(range(len(datasets)), labels=datasets)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Length (tokens)")
ax.legend(handles=[Patch(facecolor=lighten(color), edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"],
                         label=model) for model, color in models],
          loc="upper left")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/grouped-box-plot.pdf")
fig.savefig("../outputs/grouped-box-plot.png")
