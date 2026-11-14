"""Distribution of topological similarity between generated correct context B and gold context A graphs."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

data = json.load(open("../data/graph-similarity.json"))
edges = np.array(data["edges"])
centers = (edges[:-1] + edges[1:]) / 2
ranges = ["op=2-10", "op=11-14", "op=15-20"]
range_colors = dict(zip(ranges, make_shades(colors["series-1"], 3)))  # task difficulty is a sweep: light to dark

mean = [{name: np.average(centers, weights=p) for name, p in panel.items()} for panel in data["probability"]]
print("takeaway: mean similarity from bin centers", [{k: f"{v:#.3g}" for k, v in m.items()} for m in mean])
assert all(m["op=2-10"] > m["op=11-14"] > m["op=15-20"] for m in mean[1:]), "harder tasks are not less similar"

fig, axes = plt.subplots(1, 3, figsize=(6.3, 6.3), layout="constrained", sharex=True, sharey=True)

for ax, title, panel in zip(axes, data["panels"], data["probability"]):
    for name in ranges:
        if name not in panel:
            continue
        ax.hist(centers, bins=edges, weights=panel[name], histtype="stepfilled", color=range_colors[name], alpha=0.2, linewidth=0)
        ax.hist(centers, bins=edges, weights=panel[name], histtype="step", color=range_colors[name], label=name)
    ax.set_title(title)
    ax.grid(axis="y")
    ax.grid(axis="x", visible=False)

axes[0].set_ylabel("probability (%)")
fig.supxlabel("similarity")
# above the panels, in one row: inside it covers curves at this height
handles, labels = axes[1].get_legend_handles_labels()
fig.legend(handles, labels, loc="outside upper center", ncol=len(labels))

finalize_figure(fig, axes, height="XS")
fig.savefig("../out/graph-similarity.pdf")
