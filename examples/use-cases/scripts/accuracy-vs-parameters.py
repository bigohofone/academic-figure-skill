"""Figure 1: ImageNet top-1 accuracy versus number of parameters. The solid line joins EfficientNet-B0 to B7; the dashed line joins the NAS models and the dotted line the hand-designed models on their Pareto fronts. EfficientNet-B7 reaches 84.4% top-1 accuracy with 66M parameters, above AmoebaNet-C (83.5%) with 2.35× fewer parameters."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

models = json.load(open("../data/accuracy-vs-parameters.json"))
by_name = {m["model"]: m for m in models}

fig, ax = plt.subplots(figsize=(2.75, 2))

for family, linestyle in [("hand-designed (dotted gray front)", ":"), ("NAS (dashed blue front)", "--")]:
    front = sorted((m for m in models if m["family"] == family), key=lambda m: m["params_millions"])
    ax.plot([m["params_millions"] for m in front], [m["top1_accuracy"] for m in front],
            linestyle=linestyle, linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)

others = [m for m in models if m["family"] != "EfficientNet"]
ax.plot([m["params_millions"] for m in others], [m["top1_accuracy"] for m in others], "o", color=colors["neutral"])
ours = [m for m in models if m["family"] == "EfficientNet"]
ax.plot([m["params_millions"] for m in ours], [m["top1_accuracy"] for m in ours], "o-", color=colors["ours"])

# (model, label, offset in points, horizontal alignment, vertical alignment)
labels = [
    ("EfficientNet-B0", "B0", (2, -3), "right", "top"),
    ("EfficientNet-B3", "B3", (-3, 0), "right", "center"),
    ("EfficientNet-B4", "B4", (-3, 0), "right", "center"),
    ("EfficientNet-B5", "B5", (-2, 1), "right", "bottom"),
    ("EfficientNet-B6", "B6", (0, -3), "center", "top"),
    ("EfficientNet-B7", "B7 (84.4%)", (3, 0), "left", "center"),
    ("Inception-v2", "Inception-v2", (5, 3.7), "left", "center"),
    ("DenseNet-201", "DenseNet-201", (3, -1), "left", "center"),
    ("Xception", "Xception", (3, -3.5), "left", "center"),
    ("Inception-ResNet-v2", "Inception-ResNet-v2", (3, -2.5), "left", "top"),
    ("ResNeXt-101", "ResNeXt-101", (3, -0.2), "left", "top"),
    ("SENet", "SENet", (0, -5), "center", "top"),
    ("NASNet-A (mobile)", "NASNet-A", (3, 2), "left", "center"),
    ("AmoebaNet-C", "AmoebaNet-C", (5, 1), "right", "bottom"),
    ("NASNet-A (large)", "NASNet-A", (-3, 1), "right", "bottom"),
    ("ResNet-34", "ResNet-34", (3, -0.5), "left", "center"),
    ("ResNet-50", "ResNet-50", (3, 2.5), "left", "center"),
    ("ResNet-152", "ResNet-152", (3, 4.5), "left", "center"),
]
for name, text, offset, ha, va in labels:
    m = by_name[name]
    color = colors["ours"] if m["family"] == "EfficientNet" else colors["neutral"]
    ax.annotate(text, (m["params_millions"], m["top1_accuracy"]), xytext=offset, textcoords="offset points",
                ha=ha, va=va, color=darken(color))

ax.set_xlabel("Parameters (millions)")
ax.set_ylabel("Top-1 accuracy (%)")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/accuracy-vs-parameters.pdf")
fig.savefig("../outputs/accuracy-vs-parameters.png")
