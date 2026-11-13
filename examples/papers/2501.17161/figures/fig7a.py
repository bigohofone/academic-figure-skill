"""Comparison of out-of-distribution performance under visual variants (GP-VL). Similar to Figures 5 and 6, we present both the performance dynamics (shown as lines) and final performance (shown as bars) for visual out-of-distribution evaluations. Detailed evaluation setups (and curve smoothing) are provided in Appendix C.3."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades, shift_lightness

colors = paper.colors

data = json.load(open("../data/fig7.json"))["GP-VL"]
final = data["final"]
methods = ["SFT", "Init", "RL"]  # ascending

# takeaway: RL raises visual OOD success above Init, SFT lowers it
print("takeaway:", {m: f"{final[m]:.1f}" for m in methods})
assert final["SFT"] < final["Init"] < final["RL"], "the takeaway does not hold"

# RL is the series the paper is about; SFT and its initialization phase are compared, in grey
series = [
    ("init", "Initialization", colors["neutral"], ":", "^"),
    ("sft", "SFT", colors["neutral"], "--", "s"),
    ("rl", "RL", colors["ours"], "-", "o"),
]
greys = make_shades(colors["neutral"], 2)
bar_colors = {"SFT": greys[0], "Init": greys[1], "RL": colors["ours"]}
text_colors = {"SFT": shift_lightness(colors["neutral"], -1), "Init": shift_lightness(colors["neutral"], -1),
               "RL": shift_lightness(colors["ours"], -1)}

fig, (ax, ax_bar) = plt.subplots(1, 2, figsize=(3.3075, 3.3075), sharey=True)
for key, name, color, style, marker in series:
    s = data["training"][key]
    gflops = np.array(s["gflops"])
    width = rcParams["lines.linewidth"] if style == "-" else paper.dashed_linewidth
    ax.fill_between(gflops, s["error_low"], s["error_high"], color=color, alpha=0.2, linewidth=0)
    ax.plot(gflops, s["raw"], marker, color=color)
    ax.plot(gflops, s["smoothed"], color=color, linestyle=style, linewidth=width)
ax.grid(True)
ax.set_title("Training")
ax.set_xlabel("GFLOPs")
ax.set_ylabel("V-OOD success (%)")

for i, m in enumerate(methods):
    bars = ax_bar.bar(i, final[m], color=bar_colors[m], linewidth=0)
    ax_bar.bar_label(bars, labels=[f"{final[m]:.1f}%"], color=text_colors[m])
ax_bar.set_xticks(range(len(methods)), labels=methods)
ax_bar.tick_params(axis="y", labelleft=True)  # a bar panel is read on its own: its values need their axis
ax_bar.tick_params(axis="x", length=0)
ax_bar.grid(axis="x", visible=False)
ax_bar.set_title("Final")

# RL first, then the grey series in line-style order
handles = [Line2D([], [], color=color, linestyle=style, marker=marker,
                  linewidth=rcParams["lines.linewidth"] if style == "-" else paper.dashed_linewidth)
           for _, _, color, style, marker in series[::-1]]
ax.legend(handles, [name for _, name, *_ in series[::-1]])

# original ratio 0.348 (height / width of the whole figure); M panels keep the page layout
finalize_figure(fig, [ax, ax_bar], height="M")
fig.savefig("../out/fig7a.pdf")
