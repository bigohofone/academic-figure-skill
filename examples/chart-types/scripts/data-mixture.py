"""Pretraining data mixture over training steps. Dashed lines mark the stage switches at 30K and 70K steps. Web's share falls from 62% to 50% to 40%, while Code rises from 12% to 24% and Math from 6.0% to 18%."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, text_color_on

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/data-mixture.json") as f:
    data = json.load(f)
steps = np.array(data["steps"])
shares = {name: np.array(v) for name, v in data["shares"].items()}
assert np.allclose(sum(shares.values()), 1), "shares do not sum to 1"

# Stages: the steps where the mixture changes, plus the start
switches = [int(steps[i]) for i in range(1, len(steps)) if any(s[i] != s[i - 1] for s in shares.values())]
stage_starts = [int(steps[0])] + switches
stage_ends = switches + [int(steps[-1])]
print("switches:", switches)
assert switches == [30000, 70000], "the stages are not at 30K and 70K"


def share_text(v):
    return f"{v:.0%}" if v >= 0.1 else f"{100 * v:#.2g}%"


def stage_values(name):
    return [shares[name][list(steps).index(s)] for s in stage_starts]


print("takeaway:", {name: [share_text(v) for v in stage_values(name)] for name in ["Web", "Code", "Math"]})
assert stage_values("Web")[0] > stage_values("Web")[-1], "Web does not fall"
assert stage_values("Code")[0] < stage_values("Code")[-1] and stage_values("Math")[0] < stage_values("Math")[-1], "Code and Math do not rise"

# The flattest part at the bottom, the rest in data order above it
bottom = min(shares, key=lambda name: np.std(shares[name]))
order = [bottom] + [name for name in shares if name != bottom]
band_colors = paper.part_colors(len(order))

fig, ax = plt.subplots(figsize=(2.75, 2.75))
polys = ax.stackplot(steps, [shares[name] for name in order], colors=band_colors, labels=order, step="post",
                     edgecolor="white", linewidth=rcParams["grid.linewidth"])
for s in switches:
    ax.axvline(s, linestyle="--", linewidth=paper.dashed_width, color="white")

# Shares the takeaway cites, inside their bands at each stage
cited = ["Web", "Code", "Math"]
base = np.zeros(len(steps))
for name, color in zip(order, band_colors):
    if name in cited:
        for start, end in zip(stage_starts, stage_ends):
            i = list(steps).index(start)
            ax.text((start + end) / 2, base[i] + shares[name][i] / 2, share_text(shares[name][i]),
                    ha="center", va="center", color=text_color_on(color))
    base = base + shares[name]

ax.set_xlim(steps[0], steps[-1])
ax.margins(x=0)
ax.set_ylim(0, 1)
ax.set_xticks(stage_starts + [int(steps[-1])], labels=[f"{s // 1000}K" if s else "0" for s in stage_starts + [int(steps[-1])]])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
ax.set_axisbelow(False)
ax.grid(axis="x", visible=False)
ax.set_xlabel("Training step")
ax.set_ylabel("Share of tokens")

# Band names above the panel, from the top band down
handles, labels = ax.get_legend_handles_labels()
handles, labels = handles[::-1], labels[::-1]
ncol = 3
across = [i for c in range(ncol) for i in range(c, len(labels), ncol)]  # reads across each row
ax.legend([handles[i] for i in across], [labels[i] for i in across], loc="lower center", bbox_to_anchor=(0.5, 1),
          borderaxespad=0.5, ncol=ncol)

finalize_figure(fig, ax, aspect=1.0)
fig.savefig("../outputs/data-mixture.pdf")
fig.savefig("../outputs/data-mixture.png")
