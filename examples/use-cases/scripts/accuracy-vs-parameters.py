"""ImageNet top-1 accuracy versus number of parameters. The x axis is logarithmic; the solid line joins EfficientNet-B0 to B7 (ours), the dashed line the hand-designed models and the dotted line the NAS models on their Pareto fronts. EfficientNet-B7 reaches 84.4% top-1 accuracy with 66.0M parameters, above the best baseline, AmoebaNet-C (83.5% with 155M), with 2.35× fewer parameters."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import shift_lightness, finalize_figure

colors = paper.colors

with open("../data/accuracy-vs-parameters.json") as f:
    models = json.load(f)

ours = sorted([m for m in models if m["family"] == "EfficientNet"], key=lambda m: m["params_millions"])
hand = sorted([m for m in models if m["family"] == "hand-designed"], key=lambda m: m["params_millions"])
nas = sorted([m for m in models if m["family"] == "NAS"], key=lambda m: m["params_millions"])
other = [m for m in models if m["family"] == "other"]
baselines = hand + nas + other

# takeaway: the largest EfficientNet beats every baseline with fewer parameters than the best one
b7 = ours[-1]
best = max(baselines, key=lambda m: m["top1_accuracy"])
ratio = best["params_millions"] / b7["params_millions"]
print("takeaway:", {"B7": (f"{b7['top1_accuracy']:#.3g}%", f"{b7['params_millions']:#.3g}M".replace(".M", "M")),
                    best["model"]: (f"{best['top1_accuracy']:#.3g}%", f"{best['params_millions']:#.3g}M".replace(".M", "M")),
                    "ratio": f"{ratio:#.3g}×"})
assert b7["top1_accuracy"] > best["top1_accuracy"] and b7["params_millions"] < best["params_millions"], "the takeaway does not hold"
# each baseline group is a Pareto front: accuracy rises with parameters
for front in (hand, nas):
    assert all(a["top1_accuracy"] < b["top1_accuracy"] for a, b in zip(front, front[1:])), "not a Pareto front"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
ax.set_xscale("log")

# baselines: the two Pareto fronts, dashed and dotted, under the markers; every baseline a grey marker
ax.plot([m["params_millions"] for m in hand], [m["top1_accuracy"] for m in hand],
        linestyle="--", linewidth=paper.dashed_linewidth, color=colors["neutral"], zorder=1)
ax.plot([m["params_millions"] for m in nas], [m["top1_accuracy"] for m in nas],
        linestyle=":", linewidth=paper.dashed_linewidth, color=colors["neutral"], zorder=1)
ax.plot([m["params_millions"] for m in baselines], [m["top1_accuracy"] for m in baselines],
        "o", color=colors["neutral"])

# ours: B0 to B7 joined in size order
ax.plot([m["params_millions"] for m in ours], [m["top1_accuracy"] for m in ours], "o-", color=colors["ours"])

# point names: every EfficientNet by its tag, upper left of its point, above the curve; the compared
# accuracies have no free spot beside the crowded top right, so they are given in the caption
for m in ours:
    tag = m["model"].removeprefix("EfficientNet-")
    # B1 sits too close to B2 for both to be named above: it takes the next placement, left of its point
    left = tag == "B1"
    ax.annotate(tag, (m["params_millions"], m["top1_accuracy"]), xytext=(-4, 0) if left else (-3, 3),
                textcoords="offset points", ha="right", va="center_baseline" if left else "baseline",
                color=shift_lightness(colors["ours"], -1))

ax.set_xticks([10, 100], labels=["10", "100"])
ax.xaxis.set_minor_formatter(NullFormatter())
ax.grid(True, which="both")
ax.set_xlabel("Parameters (M)")
ax.set_ylabel("Top-1 accuracy (%)")

handles = [
    Line2D([], [], marker="o", linestyle="-", color=colors["ours"]),
    Line2D([], [], marker="o", linestyle="--", linewidth=paper.dashed_linewidth, color=colors["neutral"]),
    Line2D([], [], marker="o", linestyle=":", linewidth=paper.dashed_linewidth, color=colors["neutral"]),
    Line2D([], [], marker="o", linestyle="none", color=colors["neutral"]),
]
# no corner inside the panel is free of data, so the legend goes above it, two entries per row
labels = ["EfficientNet (ours)", "Hand-designed", "NAS", "Other"]
order = [0, 2, 1, 3]  # matplotlib fills columns first; this reads across each row
ax.legend([handles[i] for i in order], [labels[i] for i in order], loc="lower center", bbox_to_anchor=(0.5, 1),
          borderaxespad=0.5, ncol=2)

finalize_figure(fig, ax)
fig.savefig("../outputs/accuracy-vs-parameters.pdf")
fig.savefig("../outputs/accuracy-vs-parameters.png")
