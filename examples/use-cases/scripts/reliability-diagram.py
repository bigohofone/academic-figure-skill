"""Confidence histograms (top) and reliability diagrams (bottom) of a 5-layer LeNet and a 110-layer ResNet on CIFAR-100. In the histograms, the solid line marks the accuracy and the dotted line the average confidence over all samples; in the reliability diagrams, the diagonal marks perfect calibration and the light bars show the gap to the mean confidence. LeNet (44.9% error) is close to calibrated, with an average confidence of 0.500 against an accuracy of 0.541 and an expected calibration error (ECE, computed from the 10 bins) of 0.0492, while the more accurate ResNet (30.6% error) is overconfident, at 0.884 against 0.705 and an ECE of 0.182."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, lighten

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/reliability-diagram.json") as f:
    data = json.load(f)
hist_edges = np.array(data["histogram_bin_edges"])
rel_edges = np.array(data["reliability_bin_edges"])
models = [data["models"]["lenet"], data["models"]["resnet"]]

# Takeaway: LeNet is close to calibrated, ResNet is overconfident.
# ECE from the binned data: each reliability bin weighted by its share of samples
# (two 0.05-wide histogram bins make one 0.1-wide reliability bin).
assert np.allclose(hist_edges[::2], rel_edges)
ece = []
for m in models:
    weight = np.add.reduceat(np.array(m["fraction_of_samples_per_bin"]), np.arange(0, len(hist_edges) - 1, 2))
    gap = np.abs(np.array(m["accuracy_per_bin"]) - np.array(m["avg_confidence_per_bin"]))
    ece.append(np.sum(weight * gap) / np.sum(weight))
    print(f"takeaway: {m['label']}: error {m['error_percent']}%, confidence {m['avg_confidence_line']:.3f}, "
          f"accuracy {m['accuracy_line']:.3f}, ECE {ece[-1]:#.3g}")
lenet, resnet = models
assert resnet["avg_confidence_line"] - resnet["accuracy_line"] > abs(lenet["avg_confidence_line"] - lenet["accuracy_line"])
assert ece[1] > ece[0], "the takeaway does not hold"

fig, axes = plt.subplots(2, 2, figsize=(2.75, 2.75), layout="constrained", sharex=True, sharey="row")
for col, m in enumerate(models):
    # Top row: share of samples per confidence bin.
    ax = axes[0, col]
    ax.bar(hist_edges[:-1], m["fraction_of_samples_per_bin"], width=np.diff(hist_edges), align="edge",
           color=colors["series-1"], linewidth=0)
    ax.axvline(m["accuracy_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"], label="Accuracy")
    ax.axvline(m["avg_confidence_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"],
               linestyle=":", label="Avg. confidence")
    ax.grid(axis="x", visible=False)
    ax.set_title(m["label"])

    # Bottom row: accuracy per reliability bin, and the gap to the bin's mean confidence.
    ax = axes[1, col]
    accuracy = np.array(m["accuracy_per_bin"])
    confidence = np.array(m["avg_confidence_per_bin"])
    ax.bar(rel_edges[:-1], accuracy, width=np.diff(rel_edges), align="edge", color=colors["series-1"],
           edgecolor="white", linewidth=rcParams["grid.linewidth"], label="Outputs")
    ax.bar(rel_edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence),
           width=np.diff(rel_edges), align="edge", color=lighten(colors["series-3"]),
           edgecolor=colors["series-3"], linewidth=rcParams["grid.linewidth"], label="Gap")
    ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])

axes[0, 0].set_ylabel("Share of samples")
axes[0, 0].yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
axes[1, 0].set_ylabel("Accuracy")
axes[1, 0].set_yticks([0, 0.5, 1])
fig.supxlabel("Confidence")
axes[0, 0].legend(loc="upper left")
axes[1, 0].legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=2, frameon=False)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/reliability-diagram.pdf")
fig.savefig("../outputs/reliability-diagram.png")
