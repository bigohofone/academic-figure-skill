"""Figure 1: ImageNet top-1 accuracy versus number of parameters. The solid line joins EfficientNet-B0 to B7; the dashed and dotted lines join the hand-designed and NAS models on their Pareto fronts. EfficientNet-B7 reaches 84.4% with 66M parameters, above AmoebaNet-C's 83.5% with 155M, 2.35× fewer parameters."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/accuracy-vs-parameters.json") as f:
    models = json.load(f)

fig, ax = plt.subplots(figsize=(2.75, 2), layout="constrained")
ax.grid(True)

# Baseline Pareto fronts, dashed and dotted, under the markers
for family, linestyle in [("hand-designed", "--"), ("NAS", ":")]:
    front = sorted([m for m in models if m["family"] == family], key=lambda m: m["params_millions"])
    ax.plot([m["params_millions"] for m in front], [m["top1_accuracy"] for m in front],
            linestyle=linestyle, linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
    ax.plot([m["params_millions"] for m in front], [m["top1_accuracy"] for m in front],
            "o", color=colors["neutral"], markerfacecolor="white")

# Other baselines: markers only
others = [m for m in models if m["family"] == "other"]
ax.plot([m["params_millions"] for m in others], [m["top1_accuracy"] for m in others],
        "o", color=colors["neutral"], markerfacecolor="white")

# Ours: EfficientNet-B0 to B7, joined in size order
ours = sorted([m for m in models if m["family"] == "EfficientNet"], key=lambda m: m["params_millions"])
ax.plot([m["params_millions"] for m in ours], [m["top1_accuracy"] for m in ours],
        "o-", color=colors["ours"], markerfacecolor="white")

# Names of the two compared models, with their values
b7 = ours[-1]
amoeba_c = next(m for m in models if m["model"] == "AmoebaNet-C")
ax.annotate("EfficientNet-B7 (84.4%)", (b7["params_millions"], b7["top1_accuracy"]),
            xytext=(-3, 3), textcoords="offset points", ha="right", color=darken(colors["ours"]))
ax.annotate("AmoebaNet-C (83.5%)", (amoeba_c["params_millions"], amoeba_c["top1_accuracy"]),
            xytext=(-3, 3), textcoords="offset points", ha="right", color=darken(colors["neutral"]))

ax.set_xlabel("Parameters (M)")
ax.set_ylabel("ImageNet top-1 (%)")

handles = [
    Line2D([], [], marker="o", color=colors["ours"], markerfacecolor="white"),
    Line2D([], [], marker="o", linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], markerfacecolor="white"),
    Line2D([], [], marker="o", linestyle=":", linewidth=paper.dashed_width, color=colors["neutral"], markerfacecolor="white"),
    Line2D([], [], marker="o", linestyle="none", color=colors["neutral"], markerfacecolor="white"),
]
ax.legend(handles, ["EfficientNet (ours)", "Hand-designed", "NAS", "Other"], loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/accuracy-vs-parameters.pdf")
fig.savefig("../outputs/accuracy-vs-parameters.png")
