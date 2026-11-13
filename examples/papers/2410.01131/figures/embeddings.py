"""Left: Distribution of norms of vectors from input (Top line) and output (Bottom line) embedding matrices. Middle: Distribution of eigenvalues divided by its median value. Right: Pairwise distribution of dot products between embeddings. Models are trained for 100k iterations."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

embeddings = json.load(open("../data/embeddings.json"))

# takeaway: nGPT keeps every embedding at norm 1 while GPT's norms spread
for side in ["input", "output"]:
    norms = embeddings["norms"][side]
    print(f"takeaway: {side} norm range", {name: f"{min(s['y']):#.3g}-{max(s['y']):#.3g}" for name, s in norms.items()})
    assert all(abs(v - 1) < 0.01 for name in ["nGPT 0.5B", "nGPT 1B"] for v in norms[name]["y"]), "the takeaway does not hold"

# model sizes inside each family: nGPT (ours) in shades of ours, GPT in grey shades and dashed; larger is darker
ngpt_shades, gpt_shades = make_shades(colors["ours"], 2), make_shades(colors["neutral"], 2)
styles = {
    "nGPT 0.5B": dict(color=ngpt_shades[0]),
    "nGPT 1B": dict(color=ngpt_shades[1]),
    "GPT 0.5B": dict(color=gpt_shades[0], linestyle="--", linewidth=paper.dashed_linewidth),
    "GPT 1B": dict(color=gpt_shades[1], linestyle="--", linewidth=paper.dashed_linewidth),
}
columns = {"norms": ("Norm", "Norm value"), "eigenvalues": ("Eigenvalue", "Eigenvalue / median"),
           "dot-products": ("Dot product", "Value")}  # y labels: the panel is too short for the full names

# the full text width, laid wide: rows input and output embeddings, columns the three statistics
fig, axes = plt.subplots(2, 3, figsize=(5.5, 5.5), layout="constrained", sharex=True)
# eigenvalues over their median run from below 0.1 to above 10 (the original clips both ends): log
for ax in axes[:, 1]:
    ax.set_yscale("log")
for c, (kind, (title, ylabel)) in enumerate(columns.items()):
    for r, side in enumerate(["input", "output"]):
        ax = axes[r, c]
        series = embeddings[kind][side]
        handles = {name: ax.plot(series[name]["x"], series[name]["y"], **style)[0] for name, style in styles.items()}
        ax.grid(True)
    axes[0, c].set_title(title)
for ax in axes[:, 1]:
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="both")
for r, side in enumerate(["Input", "Output"]):
    axes[r, 0].set_ylabel(side)
fig.supxlabel("Normalized rank")
paper.add_legend_rows(axes[0, 0], [("nGPT", [handles["nGPT 0.5B"], handles["nGPT 1B"]], ["0.5B", "1B"]),
                                   ("GPT", [handles["GPT 0.5B"], handles["GPT 1B"]], ["0.5B", "1B"])])

# square panels
finalize_figure(fig, axes, height="M")
fig.savefig("../out/embeddings.pdf")
