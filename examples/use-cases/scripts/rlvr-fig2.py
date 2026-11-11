"""Pass@k of base models and their RL-trained versions over the number of samples k, for four models (rows) on four benchmarks (columns). The x axis is logarithmic (base 2). RL leads at k = 1 in all 16 panels, but the base model overtakes it as k grows and ends higher in all 16; with Qwen2.5-32B on AIME24, RL leads 0.274 to 0.0914 at k = 1 and trails 0.833 to 0.900 at k = 1024."""

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

rl_leads_at_1 = sum(data[b][m]["RL"]["pass"][0] > data[b][m]["Base"]["pass"][0] for b in benchmarks for m in models)
base_ends_higher = sum(data[b][m]["Base"]["pass"][-1] > data[b][m]["RL"]["pass"][-1] for b in benchmarks for m in models)
example = data["AIME24"]["Qwen2.5-32B"]
print("takeaway:", {
    "RL leads at k=1 (panels)": rl_leads_at_1,
    "Base ends higher (panels)": base_ends_higher,
    "AIME24 Qwen2.5-32B k=1": (f"{example['RL']['pass'][0]:#.3g}", f"{example['Base']['pass'][0]:#.3g}"),
    f"AIME24 Qwen2.5-32B k={example['RL']['k'][-1]}": (f"{example['RL']['pass'][-1]:#.3g}", f"{example['Base']['pass'][-1]:#.3g}"),
})
assert rl_leads_at_1 == 16 and base_ends_higher == 16, "the takeaway does not hold"

first_k = min(data[b][m][s]["k"][0] for b in benchmarks for m in models for s in ("RL", "Base"))
last_k = max(data[b][m][s]["k"][-1] for b in benchmarks for m in models for s in ("RL", "Base"))
top = 2 ** math.ceil(math.log2(last_k))
ticks = [2 ** i for i in range(int(math.log2(first_k)), int(math.log2(top)) + 1)]
margin = 2 ** (rcParams["axes.xmargin"] * math.log2(top / first_k))

fig, axes = plt.subplots(4, 4, figsize=(5.5, 5.5), sharex=True, sharey=True, layout="constrained")
for r, model in enumerate(models):
    for c, benchmark in enumerate(benchmarks):
        ax = axes[r, c]
        ax.set_xscale("log", base=2)
        rl = data[benchmark][model]["RL"]
        base = data[benchmark][model]["Base"]
        ax.plot(rl["k"], rl["pass"], color=colors["ours"], label="RL")
        ax.plot(base["k"], base["pass"], color=colors["neutral"], linestyle="--",
                linewidth=paper.dashed_width, label="Base")
        ax.set_xticks([], minor=True)
        ax.set_xticks(ticks, labels=[str(t) if i % 5 == 0 else "" for i, t in enumerate(ticks)])
        ax.set_xlim(first_k / margin, top * margin)
        if r == 0:
            ax.set_title(benchmark)
        if c == 0:
            ax.set_ylabel("Pass@k")

fig.supxlabel("Number of samples k")
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False, borderaxespad=0)

for r, model in enumerate(models):
    axes[r, 0].annotate(model, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90,
                        fontsize=rcParams["axes.titlesize"])

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/rlvr-fig2.pdf")
fig.savefig("../outputs/rlvr-fig2.png")
