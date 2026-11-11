"""Pass@k of base models and their RL-trained versions on four math benchmarks. The x axis (number of samples k) is logarithmic. In all 16 model–benchmark pairs, the RL model has the higher pass@1 but the base model has the higher pass@k at the largest k; on AIME24, Qwen2.5-32B goes from 0.0914 (base) to 0.274 (RL) at k = 1, while at k = 1024 the base model reaches 0.900 against 0.833 for RL."""

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
    results = json.load(f)
benchmarks = ["AIME24", "MATH500", "Minerva", "Olympiad"]
models = ["Qwen2.5-7B", "Qwen2.5-14B", "Qwen2.5-32B", "LLaMA-3.1-8B"]

# takeaway: RL wins at k = 1, the base model wins at the largest k, in every panel
for benchmark in benchmarks:
    for model in models:
        rl, base = results[benchmark][model]["RL"], results[benchmark][model]["Base"]
        assert rl["pass"][0] > base["pass"][0], f"RL does not lead at k=1 on {benchmark}/{model}"
        assert base["pass"][-1] > rl["pass"][-1], f"base does not lead at the largest k on {benchmark}/{model}"
cited = results["AIME24"]["Qwen2.5-32B"]
print("takeaway: AIME24 Qwen2.5-32B",
      f"k={cited['Base']['k'][0]}: base {cited['Base']['pass'][0]:#.3g}, RL {cited['RL']['pass'][0]:#.3g};",
      f"k={cited['Base']['k'][-1]}: base {cited['Base']['pass'][-1]:#.3g}, RL {cited['RL']['pass'][-1]:#.3g}")

all_k = [k for b in benchmarks for m in models for s in ("RL", "Base") for k in results[b][m][s]["k"]]
low, top = 2 ** math.floor(math.log2(min(all_k))), 2 ** math.ceil(math.log2(max(all_k)))
ticks = [2 ** e for e in range(int(math.log2(low)), int(math.log2(top)) + 1)]

fig, axes = plt.subplots(len(models), len(benchmarks), figsize=(5.5, 5.5), sharex=True, sharey=True)
for r, model in enumerate(models):
    for c, benchmark in enumerate(benchmarks):
        ax = axes[r, c]
        ax.set_xscale("log", base=2)
        rl, base = results[benchmark][model]["RL"], results[benchmark][model]["Base"]
        ax.plot(rl["k"], rl["pass"], color=colors["ours"], label="RL")
        ax.plot(base["k"], base["pass"], linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"],
                label="Base")
        ax.set_xticks(ticks, labels=[str(t) if i % 5 == 0 else "" for i, t in enumerate(ticks)])
        ax.set_xticks([], minor=True)

margin = 2 ** (rcParams["axes.xmargin"] * math.log2(top / low))
axes[0, 0].set_xlim(low / margin, top * margin)

for c, benchmark in enumerate(benchmarks):
    axes[0, c].set_title(benchmark)
for r, model in enumerate(models):
    axes[r, 0].set_ylabel("pass@k")
    axes[r, 0].annotate(model, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90,
                        fontsize=rcParams["axes.titlesize"])
fig.supxlabel("Number of samples k")
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False,
           borderaxespad=0)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/rlvr-fig2.pdf")
fig.savefig("../outputs/rlvr-fig2.png")
