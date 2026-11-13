"""Response lengths of the base model and our RL-trained model on three math datasets. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range, and points mark values beyond the whiskers. RL training lengthens responses on every dataset, most on AIME, where the median rises from 872 to 1670 tokens (1.91×)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.patches import Patch

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, shift_lightness

colors = paper.colors

with open("../data/grouped-box-plot.json") as f:
    data = json.load(f)
datasets = data["datasets"]
lengths = data["lengths"]
models = ["Base", "RL (ours)"]
model_colors = {"Base": colors["neutral"], "RL (ours)": colors["ours"]}

medians = {m: {d: float(np.median(lengths[m][d])) for d in datasets} for m in models}
ratios = {d: medians["RL (ours)"][d] / medians["Base"][d] for d in datasets}
fmt = lambda v: f"{v:.0f}" if v >= 1000 else f"{v:#.3g}".rstrip(".")
print("takeaway:", {m: {d: fmt(v) for d, v in medians[m].items()} for m in models},
      {d: f"{r:#.3g}×" for d, r in ratios.items()})
assert all(r > 1 for r in ratios.values()), "the takeaway does not hold"
assert max(ratios, key=ratios.get) == "AIME"
all_values = np.concatenate([lengths[m][d] for m in models for d in datasets])
print("max / min:", all_values.max() / all_values.min())  # under 100, so the axis stays linear

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
width = 0.8 / len(models)
for i, model in enumerate(models):
    for x, dataset in enumerate(datasets):
        box = ax.boxplot(lengths[model][dataset], positions=[x + (i - (len(models) - 1) / 2) * width],
                         widths=0.8 * width, patch_artist=True)
        box["boxes"][0].set_facecolor(model_colors[model] if model_colors[model] == colors["ours"] else shift_lightness(model_colors[model], 2))
ax.set_xticks(range(len(datasets)), labels=datasets)
ax.set_xlim(-0.5, len(datasets) - 0.5)
ax.tick_params(axis="x", length=0)
ax.grid(axis="x", visible=False)
ax.set_ylabel("Length (tokens)")
handles = [Patch(facecolor=model_colors[m] if model_colors[m] == colors["ours"] else shift_lightness(model_colors[m], 2), edgecolor=colors["ink"], linewidth=rcParams["patch.linewidth"], label=m)
           for m in models]
ax.legend(handles=handles)

finalize_figure(fig, ax)
fig.savefig("../outputs/grouped-box-plot.pdf")
fig.savefig("../outputs/grouped-box-plot.png")
fig.savefig("../outputs/grouped-box-plot.svg")
