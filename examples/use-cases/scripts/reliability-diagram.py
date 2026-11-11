"""Confidence histograms (top) and reliability diagrams (bottom) for a 5-layer LeNet and a 110-layer ResNet on CIFAR-100. In the histograms, the solid and dotted lines mark the accuracy and the average confidence over all samples; in the reliability diagrams, the diagonal marks perfect calibration and the light bars show the gap to each bin's mean confidence. ResNet has the lower test error (30.6% vs. 44.9%) but is overconfident, with an average confidence of 0.884 against an accuracy of 0.705, and its expected calibration error (ECE), computed from the binned data, is 18.2% against 4.92% for LeNet."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken, lighten

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/reliability-diagram.json") as f:
    data = json.load(f)
hist_edges = np.array(data["histogram_bin_edges"])
rel_edges = np.array(data["reliability_bin_edges"])
models = [data["models"]["lenet"], data["models"]["resnet"]]

# ECE, computed from the binned data: each reliability bin is two histogram bins, weighted by its share of samples
for m in models:
    fraction = np.array(m["fraction_of_samples_per_bin"])
    weight = fraction.reshape(len(rel_edges) - 1, -1).sum(axis=1) / fraction.sum()
    gap = np.abs(np.array(m["avg_confidence_per_bin"]) - np.array(m["accuracy_per_bin"]))
    m["ece"] = float(np.sum(weight * gap))
print("takeaway:", {m["label"]: dict(error=f"{m['error_percent']:#.3g}%",
                                       confidence=f"{m['avg_confidence_line']:.3f}",
                                       accuracy=f"{m['accuracy_line']:.3f}",
                                       ece=f"{100 * m['ece']:#.3g}%") for m in models})
lenet, resnet = models
assert resnet["error_percent"] < lenet["error_percent"], "the takeaway does not hold"
assert resnet["avg_confidence_line"] > resnet["accuracy_line"], "the takeaway does not hold"
assert resnet["ece"] > lenet["ece"], "the takeaway does not hold"

fig, axes = plt.subplots(2, 2, figsize=(2.75, 2.75), layout="constrained", sharex=True, sharey="row")
for col, m in enumerate(models):
    top, bottom = axes[0, col], axes[1, col]
    top.set_title(m["label"])

    # confidence histogram, with the mean confidence and the accuracy over all samples
    top.bar(hist_edges[:-1], m["fraction_of_samples_per_bin"], width=np.diff(hist_edges), align="edge",
            color=colors["series-1"], linewidth=0)
    top.axvline(m["accuracy_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1,
                label="Accuracy")
    top.axvline(m["avg_confidence_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1,
                linestyle=":", label="Avg. confidence")
    top.grid(axis="x", visible=False)

    # reliability diagram: accuracy per bin, the gap to the bin's mean confidence on top
    accuracy = np.array(m["accuracy_per_bin"])
    confidence = np.array(m["avg_confidence_per_bin"])
    bottom.bar(rel_edges[:-1], accuracy, width=np.diff(rel_edges), align="edge", color=colors["series-1"],
               edgecolor=darken(colors["series-1"]), linewidth=rcParams["grid.linewidth"], label="Outputs")
    bottom.bar(rel_edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence),
               width=np.diff(rel_edges), align="edge", color=lighten(colors["series-4"]),
               edgecolor=darken(colors["series-4"]), linewidth=rcParams["grid.linewidth"], label="Gap")
    bottom.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
    bottom.set_xlim(0, 1)
    bottom.set_ylim(0, 1)
    bottom.set_xticks([0, 0.5, 1])
    bottom.set_yticks([0, 0.5, 1])

axes[0, 0].yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
axes[0, 0].set_ylabel("Samples")
axes[1, 0].set_ylabel("Accuracy")
fig.supxlabel("Confidence")
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False,
           borderaxespad=0)
axes[1, 0].legend(loc="lower center", bbox_to_anchor=(0.5, 1), borderaxespad=0.5, ncol=2, frameon=False)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/reliability-diagram.pdf")
fig.savefig("../outputs/reliability-diagram.png")
