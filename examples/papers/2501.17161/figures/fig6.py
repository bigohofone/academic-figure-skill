"""Comparison of out-of-distribution performance under rule variants. We report the success rate for GeneralPoints and per-step-accuracy for V-IRL. For each subplot, RL and SFT are trained with equal computation, and their shared initial checkpoint (marked as Init) is set as baseline. Detailed setups are provided in Appendix C.3."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure, make_shades, shift_lightness

colors = paper.colors

data = json.load(open("../data/fig6.json"))
tasks = data["tasks"]
methods = ["SFT", "Init", "RL"]  # ascending on every task, left to right

# takeaway: RL raises OOD success above Init on every task, SFT lowers it
for task in tasks:
    v = data["success"][task]
    print("takeaway:", task, {m: f"{v[m]:.1f}" for m in methods}, f"RL {v['RL'] - v['Init']:+.1f}", f"SFT {v['SFT'] - v['Init']:+.1f}")
    assert v["SFT"] < v["Init"] < v["RL"], "the takeaway does not hold"

greys = make_shades(colors["neutral"], 2)
bar_colors = {"SFT": greys[0], "Init": greys[1], "RL": colors["ours"]}
text_colors = {"SFT": shift_lightness(colors["neutral"], -1), "Init": shift_lightness(colors["neutral"], -1),
               "RL": shift_lightness(colors["ours"], -1)}

fig, axes = plt.subplots(1, 4, figsize=(6.75, 6.75))  # both columns of the page
for ax, task in zip(axes, tasks):
    for i, m in enumerate(methods):
        value = data["success"][task][m]
        bars = ax.bar(i, value, color=bar_colors[m], linewidth=0)
        ax.bar_label(bars, labels=[f"{value:.1f}%"], color=text_colors[m])
    ax.set_title(task)
    # the caption: GeneralPoints reports episode success, V-IRL per-step accuracy
    ax.set_ylabel("Success rate (%)" if task.startswith("GP") else "Per-step accuracy (%)")
    ax.set_xticks(range(len(methods)), labels=methods)
    ax.grid(axis="x", visible=False)
    ax.tick_params(axis="x", length=0)

# original ratio 0.257 (height / width): S is closest, but with S this figure moves up beside Figure 5; M keeps the page layout
finalize_figure(fig, axes, height="M")
fig.savefig("../out/fig6.pdf")
