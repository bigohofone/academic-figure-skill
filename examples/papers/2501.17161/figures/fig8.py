"""Recognition vs. success rate for RL and SFT under different variants in GP-VL. We report both in-distribution (red) and OOD (blue) performance of recognition (y-axis) and episode success rate (x-axis). We denote the training compute of each data point via transparency (color bar) while connected (★-○) pairs are evaluated using same checkpoints. As scaling up post-training compute, RL improves both recognition and overall accuracy, while SFT shows opposite effect."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

data = json.load(open("../data/fig8.json"))["panels"]

# takeaway: from least to most compute, RL gains OOD recognition and success, SFT loses both
for panel, runs in data.items():
    for method, sign in (("RL", 1), ("SFT", -1)):
        first, last = runs[method][0], runs[method][-1]
        print("takeaway:", panel, method, f"recognition {first['ood_recognition']:#.3g} -> {last['ood_recognition']:#.3g}",
              f"success {first['ood_success']:#.3g} -> {last['ood_success']:#.3g}")
        assert sign * (last["ood_recognition"] - first["ood_recognition"]) > 0, "the takeaway does not hold"
        assert sign * (last["ood_success"] - first["ood_success"]) > 0, "the takeaway does not hold"

# the points are the data and their color is read on the gauge: markers at the larger design size (scatter-plot.md)
# compute is a sweep inside each method: one hue per method (RL ours, SFT grey), light to dark with compute
all_gflops = [r["gflops"] for runs in data.values() for rs in runs.values() for r in rs]
norm = Normalize(min(all_gflops), max(all_gflops))
cmaps = {
    "RL": LinearSegmentedColormap.from_list("rl", make_shades(colors["ours"], 2)),
    "SFT": LinearSegmentedColormap.from_list("sft", make_shades(colors["neutral"], 2)),
}
cmaps["Init"] = cmaps["SFT"]  # the shared starting checkpoint, at the least compute
# lightness is taken by compute, so the three methods differ by line style, as in Figures 5 and 7
styles = {"RL": "-", "SFT": "--", "Init": ":"}

fig, axes = plt.subplots(1, 2, figsize=(6.75, 6.75), sharex=True, sharey=True)
for ax, (panel, runs) in zip(axes, data.items()):
    for method, rows in runs.items():
        for r in rows:
            color = cmaps[method](norm(r["gflops"]))
            ax.plot([r["ood_success"], r["id_success"]], [r["ood_recognition"], r["id_recognition"]],
                    color=color, linestyle=styles[method], zorder=1, label=method)
            ax.plot(r["ood_success"], r["ood_recognition"], "o", color=color, markersize=paper.highlight_markersize, label=method)
            ax.plot(r["id_success"], r["id_recognition"], "*", color=color, markeredgecolor=color, markersize=paper.highlight_markersize,
                    label=method)
    ax.set_title(panel)
    ax.grid(True)
axes[0].set_ylabel("Recognition (%)")
fig.supxlabel("GP-VL success rate (%)")

# what tells the points apart: line style and color the method, marker the split
handles = [Line2D([], [], color=cmaps["RL"](0.8), linestyle=styles["RL"]),
           Line2D([], [], color=cmaps["SFT"](0.8), linestyle=styles["SFT"]),
           Line2D([], [], color=cmaps["SFT"](0.3), linestyle=styles["Init"]),
           Line2D([], [], color=colors["ink"], marker="o", markersize=paper.highlight_markersize, linestyle="none"),
           Line2D([], [], color=colors["ink"], marker="*", markeredgecolor=colors["ink"], markersize=paper.highlight_markersize, linestyle="none")]
fig.legend(handles, ["RL", "SFT", "Init", "Out-of-distribution", "In-distribution"], loc="outside upper center", ncol=5, borderaxespad=0)

# one gauge for compute: the SFT scale and the RL scale side by side in one bar, its ticks and label once
bar = fig.colorbar(ScalarMappable(norm, cmaps["RL"]), ax=axes, label="GFLOPs (SFT | RL)")
bar.ax.imshow(np.linspace(1, 0, 256)[:, None], cmap=cmaps["SFT"], aspect="auto", extent=(0, 0.5, *norm.inverse([0, 1])), zorder=2)
bar.ax.set_xlim(0, 1)  # the strip would shrink the bar to its own half

# original ratio 0.335 (height / width); S panels keep the page layout
finalize_figure(fig, axes, height="XS")
fig.savefig("../out/fig8.pdf")
