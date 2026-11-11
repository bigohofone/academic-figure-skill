"""Pretraining data mixture by domain over training steps. Dashed lines mark the stage switches at 30K and 70K steps. Across the three stages, Web falls from 62% to 50% to 40% of tokens while Code rises from 12% to 18% to 24% and Math from 6% to 13% to 18%."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, text_color

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/data-mixture.json") as f:
    data = json.load(f)
steps = np.array(data["steps"])
shares = {name: np.array(v) for name, v in data["shares"].items()}
assert np.allclose(sum(shares.values()), 1), "shares do not sum to 1"

switches = [30000, 70000]
stage_edges = [steps[0], *switches, steps[-1]]

# Stack: the steadiest domain at the bottom, the rest in data order above it.
bottom = min(shares, key=lambda name: shares[name].std())
names = [bottom] + [name for name in shares if name != bottom]
band_colors = [colors[f"series-{i + 1}"] for i in range(len(names))]

# Takeaway: Web's share falls while Code and Math rise, stage by stage.
cited = ["Web", "Code", "Math"]
stage_shares = {name: [shares[name][steps == s][0] for s in stage_edges[:-1]] for name in cited}
print("takeaway:", {name: [f"{v:.0%}" for v in vals] for name, vals in stage_shares.items()})
assert np.all(np.diff(stage_shares["Web"]) < 0), "Web does not fall at each stage"
assert all(np.all(np.diff(stage_shares[n]) > 0) for n in ["Code", "Math"]), "Code and Math do not rise at each stage"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.stackplot(steps, [shares[n] for n in names], colors=band_colors, labels=names, step="post",
             edgecolor="white", linewidth=rcParams["grid.linewidth"])
for s in switches:
    ax.axvline(s, linestyle="--", linewidth=paper.dashed_width, color="white")

# Shares the takeaway cites, inside their bands at each stage.
cumulative = np.cumsum([shares[n] for n in names], axis=0)
for i, name in enumerate(names):
    if name not in cited:
        continue
    for lo, hi in zip(stage_edges[:-1], stage_edges[1:]):
        k = np.flatnonzero(steps == lo)[0]
        top = cumulative[i, k]
        share = shares[name][k]
        ax.text((lo + hi) / 2, top - share / 2, f"{share:.0%}", ha="center", va="center",
                color=text_color(band_colors[i]), gid="value-label")

ax.set_xlim(steps[0], steps[-1])
ax.margins(x=0)
ax.set_ylim(0, 1)
ax.set_xticks(stage_edges, labels=[f"{s // 1000}K" if s else "0" for s in stage_edges])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
ax.set_axisbelow(False)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Training step")
ax.set_ylabel("Share of tokens")

# Legend above the panel, entries from the top band down.
handles, labels = ax.get_legend_handles_labels()
handles, labels = handles[::-1], labels[::-1]
ncol = 3
order = [i for c in range(ncol) for i in range(c, len(labels), ncol)]
ax.legend([handles[i] for i in order], [labels[i] for i in order], loc="lower center",
          bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=ncol, frameon=False)

fit_height(fig, ax, aspect=1.0)
fig.savefig("../outputs/data-mixture.pdf")
fig.savefig("../outputs/data-mixture.png")
