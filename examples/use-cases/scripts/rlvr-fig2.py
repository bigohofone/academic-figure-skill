"""Pass@k of base models and their RL-trained versions on four benchmarks. The x axis is logarithmic. In all 16 model–benchmark pairs, the RL model has the higher pass@1 and the base model has the higher pass@k at the largest k.
"""

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

rl_first = sum(data[b][m]["RL"]["pass"][0] > data[b][m]["Base"]["pass"][0] for b in benchmarks for m in models)
base_last = sum(data[b][m]["Base"]["pass"][-1] > data[b][m]["RL"]["pass"][-1] for b in benchmarks for m in models)
print("takeaway:", f"RL higher pass@1 in {rl_first}/16; Base higher at largest k in {base_last}/16")
assert rl_first == 16 and base_last == 16, "the takeaway does not hold"

k_min = min(data[b][m][s]["k"][0] for b in benchmarks for m in models for s in ("Base", "RL"))
k_max = max(data[b][m][s]["k"][-1] for b in benchmarks for m in models for s in ("Base", "RL"))
top = 2 ** math.ceil(math.log2(k_max))
ticks = [2 ** i for i in range(int(math.log2(k_min)), int(math.log2(top)) + 1)]
margin = 2 ** (rcParams["axes.xmargin"] * math.log2(top / k_min))

fig, axes = plt.subplots(4, 4, figsize=(5.5, 5.5), sharex=True, sharey=True, layout="constrained")
for r, model in enumerate(models):
    for c, benchmark in enumerate(benchmarks):
        ax = axes[r, c]
        ax.set_xscale("log", base=2)
        rl, base = data[benchmark][model]["RL"], data[benchmark][model]["Base"]
        ax.plot(rl["k"], rl["pass"], color=colors["ours"], label="RL")
        ax.plot(base["k"], base["pass"], "--", linewidth=paper.dashed_width, color=colors["neutral"], label="Base")
        ax.set_xticks([], minor=True)
        ax.set_xticks(ticks, labels=[str(t) if i % 5 == 0 else "" for i, t in enumerate(ticks)])
        ax.set_xlim(k_min / margin, top * margin)
    axes[r, 0].set_ylabel("pass@k")
for c, benchmark in enumerate(benchmarks):
    axes[0, c].set_title(benchmark)

fig.supxlabel("Number of samples k")
fig.legend(*axes.flat[0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False,
           borderaxespad=0)
fig.canvas.draw()  # place the y labels, which the row names are anchored to
for r, model in enumerate(models):
    axes[r, 0].annotate(model, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90,
                        fontsize=rcParams["axes.titlesize"])

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/rlvr-fig2.pdf")
fig.savefig("../outputs/rlvr-fig2.png")
