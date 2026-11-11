"""Figure 1: Confidence histograms (top) and reliability diagrams (bottom) for a 5-layer LeNet (left) and a 110-layer ResNet (right) on CIFAR-100. In the histograms, dashed and dotted lines mark the average confidence and the accuracy; in the reliability diagrams, the dashed diagonal marks perfect calibration and outlines show the gap to the mean confidence. LeNet is well calibrated (ECE 4.92%), while the more accurate ResNet is overconfident: its average confidence of 0.884 exceeds its accuracy of 0.705 (ECE 18.2%)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

data = json.load(open("../data/reliability-diagram.json"))
hist_edges = np.array(data["histogram_bin_edges"])
rel_edges = np.array(data["reliability_bin_edges"])

fig, axes = plt.subplots(2, 2, figsize=(2.75, 3), sharex=True, sharey="row", layout="constrained")
for col, model in enumerate(data["models"].values()):
    top, bottom = axes[0, col], axes[1, col]
    top.set_title(f"{model['label']}\n{data['dataset']}")

    top.bar(hist_edges[:-1], model["fraction_of_samples_per_bin"], width=np.diff(hist_edges), align="edge",
            color=colors["series-1"], linewidth=0)
    top.axvline(model["avg_confidence_line"], linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"],
                zorder=1, label="Avg. confidence")
    top.axvline(model["accuracy_line"], linestyle=":", linewidth=paper.dashed_width, color=colors["neutral"],
                zorder=1, label="Accuracy")
    top.grid(axis="x", visible=False)

    accuracy = np.array(model["accuracy_per_bin"])
    confidence = np.array(model["avg_confidence_per_bin"])
    bottom.bar(rel_edges[:-1], accuracy, width=np.diff(rel_edges), align="edge", color=colors["series-1"],
               edgecolor="white", linewidth=rcParams["grid.linewidth"], label="Outputs")
    bottom.bar(rel_edges[:-1], np.abs(confidence - accuracy), bottom=np.minimum(accuracy, confidence),
               width=np.diff(rel_edges), align="edge", fill=False, edgecolor=colors["ink"],
               linewidth=rcParams["patch.linewidth"], label="Gap")
    bottom.axline((0, 0), (1, 1), linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
    bottom.text(0.96, 0.04, f"Error={model['error_percent']}", transform=bottom.transAxes, ha="right", va="bottom",
                bbox=dict(facecolor="white", edgecolor="none", pad=1))
    bottom.grid(axis="x", visible=False)
    bottom.set_xlabel("Confidence")

for ax in axes.flat:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:,.10g}")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:,.10g}")
axes[0, 0].set_ylabel("% of Samples")
axes[1, 0].set_ylabel("Accuracy")
axes[0, 0].legend(loc="upper left")
axes[1, 0].legend(loc="upper left")

fit_height(fig, axes, aspect=1.0, min_width=1.0)
fig.savefig("../outputs/reliability-diagram.pdf")
fig.savefig("../outputs/reliability-diagram.png")
