"""Figure 2: Pass@k of base models and their RLVR-trained counterparts across mathematical benchmarks.
Rows are models and columns are benchmarks; the x axis is on a log₂ scale. RL-trained models lead at
small k (Qwen2.5-7B on AIME24: 0.154 vs. 0.0738 at k = 1), but base models catch up as k grows to
the tens or hundreds and end ahead in every panel (0.767 vs. 0.633 at k = 1024).
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

with open("../data/rlvr.json") as f:
    data = json.load(f)

benchmarks = ["AIME24", "MATH500", "Minerva", "Olympiad"]
models = ["Qwen2.5-7B", "Qwen2.5-14B", "Qwen2.5-32B", "LLaMA-3.1-8B"]

fig, axes = plt.subplots(4, 4, figsize=(5.5, 5.5), sharex=True, sharey=True)
for r, model in enumerate(models):
    for c, benchmark in enumerate(benchmarks):
        ax = axes[r, c]
        for name, marker, color in [("Base", "o", colors["series-1"]), ("RL", "s", colors["series-2"])]:
            curve = data[benchmark][model][name]
            ax.plot(curve["k"], curve["pass"], marker + "-", color=color, label=name)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}".replace("-", "−"))

top = 2 ** math.ceil(math.log2(max(data[b][m]["Base"]["k"][-1] for b in benchmarks for m in models)))
ks = [2 ** e for e in range(0, int(math.log2(top)) + 1, 5)]
axes[0, 0].set_xscale("log", base=2)
axes[0, 0].set_xticks(ks, labels=[str(k) for k in ks])
axes[0, 0].set_xticks([], minor=True)
margin = 2 ** (0.05 * math.log2(top))
axes[0, 0].set_xlim(1 / margin, top * margin)
for c, benchmark in enumerate(benchmarks):
    axes[0, c].set_title(benchmark)

for r, model in enumerate(models):
    axes[r, 0].set_ylabel("Pass@k")
    axes[r, 0].annotate(model, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90, fontsize=11)

fig.supxlabel("Number of samples k")
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False, borderaxespad=0)
fit_height(fig, axes, aspect=1.0, min_width=1.0)
fig.savefig("../outputs/rlvr-fig2.pdf")
fig.savefig("../outputs/rlvr-fig2.png")
