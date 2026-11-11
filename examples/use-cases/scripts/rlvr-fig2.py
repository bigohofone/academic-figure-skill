"""Figure 2: Pass@k of base models and their RL-trained versions on four math benchmarks. The x axis (number of samples k) is logarithmic. RL leads at small k, but the base model overtakes it at large k in every panel: on AIME24, Qwen2.5-32B reaches 0.900 pass@1024 as a base model against 0.833 after RL."""

import json
import math
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/rlvr.json") as f:
    data = json.load(f)

benchmarks = ["AIME24", "MATH500", "Minerva", "Olympiad"]
models = ["Qwen2.5-7B", "Qwen2.5-14B", "Qwen2.5-32B", "LLaMA-3.1-8B"]

fig, axes = plt.subplots(4, 4, figsize=(5.5, 5.5), sharex=True, sharey=True, layout="constrained")

# log2 x axis: one tick and gridline per power of 2 from 1 to 1024, every fifth labelled
ticks = [2**i for i in range(11)]
top = ticks[-1]
margin = 2 ** (0.05 * math.log2(top / 1))

for r, model in enumerate(models):
    for c, bench in enumerate(benchmarks):
        ax = axes[r, c]
        ax.set_xscale("log", base=2)
        for name, color in [("Base", colors["series-1"]), ("RL", colors["series-2"])]:
            curve = data[bench][model][name]
            ax.plot(curve["k"], curve["pass"], color=color, label=name)
        ax.set_xticks([], minor=True)
        ax.set_xticks(ticks, labels=[str(t) if i % 5 == 0 else "" for i, t in enumerate(ticks)])
        ax.set_xlim(1 / margin, top * margin)
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:.10g}".replace("-", "−"))
        if r == 0:
            ax.set_title(bench)
        if r == 3:
            ax.set_xlabel("k")
        if c == 0:
            ax.set_ylabel("Pass@k")

for r, model in enumerate(models):
    axes[r, 0].annotate(model, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90,
                        fontsize=rcParams["axes.titlesize"])

fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False,
           borderaxespad=0)

fit_height(fig, axes, aspect=1.0, min_width=1.0)
fig.savefig("../outputs/rlvr-fig2.pdf")
fig.savefig("../outputs/rlvr-fig2.png")
