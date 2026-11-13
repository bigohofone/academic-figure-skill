"""Success rate (%) - GFLOPs trendlines for RL and SFT on GeneralPoints and V-IRL. The top row shows in-distribution performance, while the bottom row shows out-of-distribution performance. Results are presented for both pure language (-L) and vision-language (-VL) variants of each task. For GeneralPoints, we report the episode success rate, while for V-IRL, we report per-step accuracy with overall success rate in Figures 1 and 18. Detailed evaluation setups (and curve smoothing) are provided in Appendix C.3."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure

colors = paper.colors

data = json.load(open("../data/fig5.json"))
tasks = ["GP-VL", "V-IRL-VL"]  # (b) with vision
splits = ["In-distribution", "Out-of-distribution"]
panels = {(p["split"], p["task"]): p for p in data["panels"]}

# takeaway: at the end of training RL is above SFT out of distribution on every task
for task in tasks:
    ood = panels["Out-of-distribution", task]
    final = {name: ood[name]["raw"][-1] for name in ("sft", "rl")}
    print("takeaway:", task, {name: f"{v:#.3g}" for name, v in final.items()})
    assert final["rl"] > final["sft"], "the takeaway does not hold"

# RL is the series the paper is about; SFT and its initialization phase are compared, in grey
series = [
    ("init", "Initialization", colors["neutral"], ":", "^"),
    ("sft", "SFT", colors["neutral"], "--", "s"),
    ("rl", "RL", colors["ours"], "-", "o"),
]

fig, axes = plt.subplots(2, 2, figsize=(3.3075, 3.3075), sharex="col")
for r, split in enumerate(splits):
    for c, task in enumerate(tasks):
        ax = axes[r, c]
        panel = panels[split, task]
        for key, name, color, style, marker in series:
            s = panel[key]
            gflops = np.array(s["gflops"])
            width = rcParams["lines.linewidth"] if style == "-" else paper.dashed_linewidth
            ax.fill_between(gflops, s["error_low"], s["error_high"], color=color, alpha=0.2, linewidth=0)
            ax.plot(gflops, s["raw"], marker, color=color)
            ax.plot(gflops, s["smoothed"], color=color, linestyle=style, linewidth=width)
        ax.grid(True)
        if r == 0:
            ax.set_title(task)
    # the caption names the quantity; the row headers name the split
    axes[r, 0].annotate(split, xy=(0, 0.5), xycoords=axes[r, 0].yaxis.label, xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", rotation=90,
                        fontsize=rcParams["axes.titlesize"])
fig.supxlabel("Training computation (GFLOPs)")

# RL first, then the grey series in line-style order
handles = [Line2D([], [], color=color, linestyle=style, marker=marker,
                  linewidth=rcParams["lines.linewidth"] if style == "-" else paper.dashed_linewidth)
           for _, _, color, style, marker in series[::-1]]
fig.legend(handles, [name for _, name, *_ in series[::-1]], loc="outside upper center", ncol=3, borderaxespad=0)

# (b) of Figure 5, split from the 2 x 4 original (ratio 0.541) so each half carries one takeaway; square panels
finalize_figure(fig, axes, height="M", min_width=0.7)
fig.savefig("../out/fig5b.pdf")
