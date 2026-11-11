"""Confidence histograms (top) and reliability diagrams (bottom) of a 5-layer LeNet and a 110-layer ResNet on CIFAR-100. In the histograms, the solid and dotted vertical lines mark the accuracy and the average confidence over all test samples; in the reliability diagrams, the diagonal marks perfect calibration and the light bars show the gap to each bin's mean confidence. The ResNet has the lower test error (30.6% vs. 44.9%) but is overconfident: its average confidence is 0.884 against an accuracy of 0.705, while the LeNet's 0.500 sits close to its 0.541; the expected calibration error (ECE), computed from the 10 bins, is 0.182 for the ResNet and 0.0492 for the LeNet."""

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

# ECE from the binned data: each reliability bin weighted by its share of samples (two histogram bins each).
per_rel_bin = len(hist_edges[:-1]) // len(rel_edges[:-1])
ece = []
for m in models:
    weights = np.array(m["fraction_of_samples_per_bin"]).reshape(-1, per_rel_bin).sum(axis=1)
    gap = np.abs(np.array(m["accuracy_per_bin"]) - np.array(m["avg_confidence_per_bin"]))
    ece.append(np.sum(weights * gap) / weights.sum())
print("takeaway:", {m["label"]: dict(error=f"{m['error_percent']:#.3g}%", conf=f"{m['avg_confidence_line']:.3f}",
                                      acc=f"{m['accuracy_line']:.3f}", ece=f"{e:#.3g}") for m, e in zip(models, ece)})
lenet, resnet = models
assert resnet["error_percent"] < lenet["error_percent"], "the takeaway does not hold"
assert resnet["avg_confidence_line"] - resnet["accuracy_line"] > abs(lenet["avg_confidence_line"] - lenet["accuracy_line"])
assert ece[1] > ece[0], "the takeaway does not hold"

fig, axes = plt.subplots(2, 2, figsize=(2.75, 2.75), sharex=True, sharey="row")
for col, m in enumerate(models):
    hist_ax, rel_ax = axes[0, col], axes[1, col]
    hist_ax.set_title(m["label"])

    # Confidence histogram: share of samples per confidence bin.
    hist_ax.bar(hist_edges[:-1], m["fraction_of_samples_per_bin"], width=np.diff(hist_edges), align="edge",
                color=colors["series-1"], linewidth=0)
    hist_ax.grid(axis="x", visible=False)
    hist_ax.axvline(m["accuracy_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"],
                    zorder=1, label="Accuracy")
    hist_ax.axvline(m["avg_confidence_line"], color=colors["neutral"], linewidth=rcParams["grid.linewidth"],
                    linestyle=":", zorder=1, label="Avg. confidence")

    # Reliability diagram: accuracy per confidence bin, and the gap to the bin's mean confidence.
    accuracy = np.array(m["accuracy_per_bin"])
    confidence = np.array(m["avg_confidence_per_bin"])
    rel_ax.bar(rel_edges[:-1], accuracy, width=np.diff(rel_edges), align="edge", color=colors["series-1"],
               edgecolor="white", linewidth=rcParams["grid.linewidth"], label="Bin accuracy")
    rel_ax.bar(rel_edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence),
               width=np.diff(rel_edges), align="edge", color=lighten(colors["series-3"]),
               edgecolor=colors["series-3"], linewidth=rcParams["grid.linewidth"], label="Gap")
    rel_ax.axline((0, 0), (1, 1), color=colors["neutral"], linewidth=rcParams["grid.linewidth"], zorder=1)
    rel_ax.set_xlim(0, 1)
    rel_ax.set_ylim(0, 1)

axes[0, 0].yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
axes[0, 0].set_ylabel("Samples")
axes[1, 0].set_ylabel("Accuracy")
fig.supxlabel("Confidence")
# Each row's legend sits above that row: no inside spot of the 0.9 in panels holds it.
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False,
           borderaxespad=0)
axes[1, 0].legend(loc="lower left", bbox_to_anchor=(0, 1), borderaxespad=0.5, ncol=2, frameon=False)

fit_height(fig, axes, aspect=1.0, min_width=0.9)
fig.savefig("../outputs/reliability-diagram.pdf")
fig.savefig("../outputs/reliability-diagram.png")
