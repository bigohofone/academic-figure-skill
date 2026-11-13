"""In-distribution vs. OOD performance growth on GP-L. We record RL experiments with different number of verification iterations (VIter) as scaling up training compute (color transparency)."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure, make_shades, shift_lightness

colors = paper.colors

data = json.load(open("../data/fig10.json"))
gflops, runs = data["gflops"], data["runs"]
viters = [1, 3, 5, 10]

# takeaway: at the largest compute, OOD growth rises with the number of verification iterations
final = [runs[f"VIter {v}"]["ood_growth"][-1] for v in viters]
print("takeaway:", dict(zip(viters, final)))
assert final == sorted(final), "the takeaway does not hold"

# VIter settings on equal terms, one color each (and a marker, for black and white); compute is a sweep inside
# each, by lightness: the larger, the darker
series_colors = paper.series_colors[:4]
markers = ["o", "^", "s", "D"]
label_offsets = {1: ((3, 3), "left", "bottom"), 3: ((3, -3), "left", "top"), 5: ((3, 3), "left", "bottom"),
                 10: ((3, 3), "left", "bottom")}

fig, ax = plt.subplots(figsize=(3.25, 3.25))
for v, color, marker in zip(viters, series_colors, markers):
    run = runs[f"VIter {v}"]
    ax.plot(run["id_growth"], run["ood_growth"], color=color, zorder=1, label=f"VIter {v}")
    for x, y, shade in zip(run["id_growth"], run["ood_growth"], make_shades(color, len(gflops))):
        # the points are read on the compute gauge: the larger design size (scatter-plot.md)
        ax.plot(x, y, marker, color=shade, markersize=paper.highlight_markersize, label=f"VIter {v}")
    offset, ha, va = label_offsets[v]
    ax.annotate(f"{run['ood_growth'][-1]:#.3g}", (run["id_growth"][-1], run["ood_growth"][-1]), xytext=offset,
                textcoords="offset points", ha=ha, va=va, color=shift_lightness(color, -1), gid="value-label")
ax.set_xlabel("ID growth (%)")
ax.set_ylabel("OOD growth (%)")
ax.grid(True)

ax.legend([Line2D([], [], color=c, marker=m, markersize=paper.highlight_markersize, linestyle="none") for c, m in zip(series_colors, markers)],
          [f"VIter {v}" for v in viters])
# the gauge reads lightness as compute: the same light-to-dark steps as the shades, in grey
gauge = LinearSegmentedColormap.from_list("compute", make_shades(colors["neutral"], len(gflops)))
fig.colorbar(ScalarMappable(Normalize(min(gflops), max(gflops)), gauge), ax=ax, label="GFLOPs",
             ticks=gflops, format=lambda v, _: f"{v / 1e9:g}B")

# XS, as Figure 9 beside it
finalize_figure(fig, ax, height="XS")
fig.savefig("../out/fig10.pdf")
