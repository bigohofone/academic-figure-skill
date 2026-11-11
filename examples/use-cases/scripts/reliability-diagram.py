"""Figure 1: Confidence histograms (top) and reliability diagrams (bottom) for a 5-layer LeNet and a 110-layer ResNet on CIFAR-100. In the histograms, the dashed line marks the overall accuracy and the dotted line the average confidence; in the reliability diagrams, the dashed diagonal marks perfect calibration and the light bars show the gap to each bin's mean confidence. The ResNet has lower test error than LeNet (30.6% vs. 44.9%) but is overconfident: its average confidence of 0.884 exceeds its accuracy of 0.705, raising the expected calibration error (ECE) from 0.0492 for LeNet to 0.182 (computed from the 10 binned values)."""

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

fig, axes = plt.subplots(2, 2, figsize=(5.5, 5), layout="constrained", sharex=True, sharey="row")
for col, model in enumerate(models):
    # Top row: share of samples per confidence bin, with the overall accuracy and average confidence.
    ax = axes[0, col]
    fractions = np.array(model["fraction_of_samples_per_bin"])
    ax.bar(hist_edges[:-1], fractions, width=np.diff(hist_edges), align="edge", color=colors["series-1"], linewidth=0)
    ax.axvline(model["accuracy_line"], linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"],
               label="Accuracy")
    ax.axvline(model["avg_confidence_line"], linestyle=":", linewidth=paper.dashed_width, color=colors["neutral"],
               label="Avg. confidence")
    ax.grid(axis="x", visible=False)
    ax.set_title(model["label"])

    # Bottom row: accuracy per confidence bin, the gap to its mean confidence, and the diagonal.
    ax = axes[1, col]
    accuracy = np.array(model["accuracy_per_bin"])
    confidence = np.array(model["avg_confidence_per_bin"])
    filled = (accuracy > 0) | (confidence > 0)  # an empty bin is stored as 0 and drawn as nothing
    ax.bar(rel_edges[:-1][filled], accuracy[filled], width=np.diff(rel_edges)[filled], align="edge",
           color=colors["series-1"], edgecolor="white", linewidth=rcParams["grid.linewidth"], label="Outputs")
    ax.bar(rel_edges[:-1][filled], np.abs(confidence - accuracy)[filled],
           bottom=np.minimum(accuracy, confidence)[filled], width=np.diff(rel_edges)[filled], align="edge",
           color=lighten(colors["series-2"]), edgecolor=colors["series-2"], linewidth=rcParams["grid.linewidth"],
           label="Gap")
    ax.axline((0, 0), (1, 1), linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
    ax.grid(axis="x", visible=False)
    ax.set_xlabel("Confidence")

for ax in axes.flat:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], labels=["0", "0.25", "0.5", "0.75", "1"])
axes[0, 0].set_yticks([0, 0.25, 0.5, 0.75, 1], labels=["0%", "25%", "50%", "75%", "100%"])
axes[1, 0].set_yticks([0, 0.25, 0.5, 0.75, 1], labels=["0", "0.25", "0.5", "0.75", "1"])
axes[0, 0].set_ylabel("Share of samples")
axes[1, 0].set_ylabel("Accuracy")

axes[0, 0].legend(loc="upper left")
axes[1, 0].legend(loc="upper left")

fit_height(fig, axes, aspect=1.0, min_width=1.0)
fig.savefig("../outputs/reliability-diagram.pdf")
fig.savefig("../outputs/reliability-diagram.png")
