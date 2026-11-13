"""Validation loss during training of 1B GPT and nGPT with 4k context length."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure

colors = paper.colors

runs = json.load(open("../data/validation-loss.json"))

final = {name: run["loss"][-1] for name, run in runs.items()}
print("takeaway: final loss", {name: f"{v:#.3g}" for name, v in final.items()})
assert final["nGPT with 20k budget"] <= final["GPT with 200k budget"], "the takeaway does not hold"

# the two nGPT runs are variants of ours (ours color, apart by line style); GPT is the compared series
styles = {
    "nGPT with 200k budget": dict(color=colors["ours"]),
    "nGPT with 20k budget": dict(color=colors["ours"], linestyle="--"),
    "GPT with 200k budget": dict(color=colors["neutral"], linestyle="--", linewidth=paper.dashed_linewidth),
}

fig, ax = plt.subplots(figsize=(5.5, 5.5), layout="constrained")
for name, style in styles.items():
    ax.plot(runs[name]["iterations_k"], runs[name]["loss"], label=name, **style)

ax.set_title("4k context: OpenWebText")
ax.set_xticks(range(0, 201, 50))  # the automatic step of 25 crowds the labels at this width
ax.set_xlabel("Iterations in thousands")
ax.set_ylabel("Loss")  # "Validation loss" is taller than the XS panel; the caption says validation
ax.grid(True)
ax.legend()

# original figure height / width 0.80 (1.50 in printed); XS keeps the printed height (1.53 in)
finalize_figure(fig, ax, height="2XS")
fig.savefig("../out/validation-loss.pdf")
