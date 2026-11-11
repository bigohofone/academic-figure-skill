"""Confidence histograms (top) and reliability diagrams (bottom) for a 5-layer LeNet and a 110-layer ResNet on CIFAR-100. In the histograms, the solid line marks the accuracy and the dotted line the average confidence over all samples; in the reliability diagrams, the diagonal marks perfect calibration and the light bars show the gap to the mean confidence. The ResNet has the lower test error (30.6% vs. 44.9%) but is overconfident, with an average confidence of 0.884 against an accuracy of 0.705 and an expected calibration error (ECE, computed from the binned data) of 0.182 against 0.0492 for LeNet."""

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

# ECE = sum over reliability bins of (share of samples) * |accuracy - confidence|; each reliability
# bin (width 0.1) holds two histogram bins (width 0.05), so its share is the sum of their fractions
for m in models:
    weights = np.add.reduceat(np.array(m["fraction_of_samples_per_bin"]),
                              np.searchsorted(hist_edges, rel_edges[:-1]))
    gaps = np.abs(np.array(m["avg_confidence_per_bin"]) - np.array(m["accuracy_per_bin"]))
    m["ece"] = np.sum(weights * gaps) / np.sum(weights)
print("takeaway:", {m["label"]: dict(error=m["error_percent"], conf=f"{m['avg_confidence_line']:#.3g}",
                                     acc=f"{m['accuracy_line']:#.3g}", ece=f"{m['ece']:#.3g}") for m in models})
lenet, resnet = models
assert resnet["error_percent"] < lenet["error_percent"], "the takeaway does not hold"
assert resnet["avg_confidence_line"] - resnet["accuracy_line"] > lenet["avg_confidence_line"] - lenet["accuracy_line"]
assert resnet["ece"] > lenet["ece"], "the takeaway does not hold"

fig, axes = plt.subplots(2, 2, figsize=(2.75, 2.75), layout="constrained", sharex=True, sharey="row")
for col, m in enumerate(models):
    # top row: confidence histogram, with the accuracy and the average confidence over all samples
    ax = axes[0, col]
    ax.bar(hist_edges[:-1], m["fraction_of_samples_per_bin"], width=np.diff(hist_edges), align="edge",
           color=colors["series-1"], linewidth=0)
    ax.axvline(m["accuracy_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"],
               label="Accuracy")
    ax.axvline(m["avg_confidence_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"],
               linestyle=":", label="Avg. confidence")
    ax.grid(axis="x", visible=False)
    ax.set_title(m["label"])

    # bottom row: reliability diagram
    ax = axes[1, col]
    accuracy = np.array(m["accuracy_per_bin"])
    confidence = np.array(m["avg_confidence_per_bin"])
    ax.bar(rel_edges[:-1], accuracy, width=np.diff(rel_edges), align="edge", color=colors["series-1"],
           edgecolor="white", linewidth=rcParams["grid.linewidth"], label="Accuracy")
    ax.bar(rel_edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence),
           width=np.diff(rel_edges), align="edge", color=lighten(colors["series-3"]),
           edgecolor=colors["series-3"], linewidth=rcParams["grid.linewidth"], label="Gap")
    ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

percent = lambda v, _: f"{v:.0%}"
axes[0, 0].yaxis.set_major_formatter(percent)
axes[0, 0].set_ylabel("Samples")
axes[1, 0].set_ylabel("Accuracy")
fig.supxlabel("Confidence")
for ax in axes[1]:
    ax.set_xticks([0, 0.5, 1])
axes[0, 0].legend(loc="upper left")
# no inside spot of the bottom row clears the bars, so its legend goes above its first panel
axes[1, 0].legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=2, frameon=False)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/reliability-diagram.pdf")
fig.savefig("../outputs/reliability-diagram.png")
