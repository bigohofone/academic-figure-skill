"""pass@k performance on three tasks: ID (op=2-10), OOD-edge (op=11-14), OOD-hard (op(15-20)). RL is applied to four different data regimes (colors). RL on ID tasks never improves beyond the base model at pass@128. RL consistently improves pass@128 on harder tasks when applied beyond the base model's capacity."""

import json
import math
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure

colors = paper.colors

data = json.load(open("../data/rl-ext.json"))
ks = data["k"]
runs = data["pass_at_k"]
regimes = ["RL op=7-10", "RL op=9-12", "RL op=11-14", "RL op=17-20"]

final = {name: [curves[-1] for curves in runs[name]] for name in runs}
print("takeaway: pass@128 per panel", final)
assert all(final[name][0] <= final["Base"][0] for name in regimes), "RL on ID beats the base model at pass@128"
assert final["RL op=11-14"][1] > final["Base"][1] and final["RL op=11-14"][2] > final["Base"][2], "RL beyond capacity does not help"

fig, axes = plt.subplots(1, 3, figsize=(6.3, 6.3), layout="constrained", sharex=True)

# four RL regimes on equal terms, the base model as the grey reference
styles = {"Base": dict(color=colors["neutral"], linestyle="--", linewidth=paper.dashed_linewidth, marker="o")}
for name, color, marker in zip(regimes, paper.design.series_order[:4], ["s", "^", "D", "v"]):
    styles[name] = dict(color=colors[color], marker=marker)

margin = 2 ** (rcParams["axes.xmargin"] * math.log2(ks[-1] / ks[0]))
for i, (ax, title) in enumerate(zip(axes, data["panels"])):
    ax.set_xscale("log", base=2)
    for name in ["Base", *regimes]:
        ax.plot(ks, runs[name][i], label=name, **styles[name])
    ax.set_xticks(ks, labels=[str(k) for k in ks])
    ax.set_xticks([], minor=True)
    ax.set_xlim(ks[0] / margin, ks[-1] * margin)
    ax.set_title(title)
    ax.grid(True)

axes[0].set_ylabel("performance (%)")
fig.supxlabel("pass@k")
# above the panels, in one row: inside it covers curves at this height
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="outside upper center", ncol=len(labels))

finalize_figure(fig, axes, height="XS")
fig.savefig("../out/rl-ext.pdf")
