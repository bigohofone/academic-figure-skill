"""Figure 2: Pass@k of base models and their RLVR-trained counterparts across mathematical benchmarks. The x axis is logarithmic. At small k the RL-trained models are ahead (Qwen2.5-7B on AIME24: 0.154 vs 0.074 pass@1), but as k grows to the tens or hundreds the base models catch up and surpass them (0.767 vs 0.633 pass@1024)."""

import json
import math
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/rlvr.json"))
benchmarks = ["AIME24", "MATH500", "Minerva", "Olympiad"]
models = ["Qwen2.5-7B", "Qwen2.5-14B", "Qwen2.5-32B", "LLaMA-3.1-8B"]
series = [("Base", colors["series-1"], "o"), ("RL", colors["series-2"], "s")]

fig, axes = plt.subplots(4, 4, figsize=(5.5, 5.5), sharex=True, sharey=True)
for r, model in enumerate(models):
    for c, benchmark in enumerate(benchmarks):
        ax = axes[r, c]
        for name, color, marker in series:
            curve = data[benchmark][model][name]
            style = "-" if len(curve["k"]) > 30 else marker + "-"
            ax.plot(curve["k"], curve["pass"], style, color=color, label=name)

ks = [1, 32, 1024]
margin = 2 ** (0.05 * math.log2(ks[-1] / ks[0]))
ax.set_xscale("log", base=2)
ax.set_xticks(ks, labels=[str(k) for k in ks])
ax.set_xticks([], minor=True)
ax.set_xlim(ks[0] / margin, ks[-1] * margin)
ax.set_ylim(0, 1)
ax.set_yticks([0, 0.5, 1], labels=["0", "0.5", "1"])

for c, benchmark in enumerate(benchmarks):
    axes[0, c].set_title(benchmark)
for r, model in enumerate(models):
    axes[r, 0].set_ylabel("Pass@k")
    axes[r, 0].annotate(model, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90,
                        fontsize=rcParams["axes.titlesize"])
fig.supxlabel("Number of samples k")
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False, borderaxespad=0)

fit_height(fig, axes, aspect=1.0, min_width=1.0)
fig.savefig("../outputs/rlvr-fig2.pdf")
fig.savefig("../outputs/rlvr-fig2.png")
