"""Median condition numbers for attention and MLP matrices at different layer depth (24 and 36 layers for 0.5B and 1B models, respectively). Models are trained for 100k iterations."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

matrices = json.load(open("../data/condition-numbers.json"))

# takeaway: GPT's attention matrices reach far higher condition numbers than nGPT's
peak = {m: {name: max(s["y"]) for name, s in series.items()} for m, series in matrices.items()}
print("takeaway: peak condition number", {m: {name: f"{v:#.3g}" for name, v in p.items()} for m, p in peak.items()})
assert all(min(peak[m]["GPT 0.5B"], peak[m]["GPT 1B"]) > 1000 * max(peak[m]["nGPT 0.5B"], peak[m]["nGPT 1B"]) for m in "QKV"), "the takeaway does not hold"

# model sizes inside each family: nGPT (ours) in shades of ours, GPT in grey shades and dashed; larger is darker
ngpt_shades, gpt_shades = make_shades(colors["ours"], 2), make_shades(colors["neutral"], 2)
styles = {
    "nGPT 0.5B": dict(color=ngpt_shades[0]),
    "nGPT 1B": dict(color=ngpt_shades[1]),
    "GPT 0.5B": dict(color=gpt_shades[0], linestyle="--", linewidth=paper.dashed_linewidth),
    "GPT 1B": dict(color=gpt_shades[1], linestyle="--", linewidth=paper.dashed_linewidth),
}

# small multiples: one panel per matrix, one condition-number scale for all (spans 1 to 10^7: log)
fig, axes = plt.subplots(2, 3, figsize=(5.5, 5.5), layout="constrained", sharex=True, sharey=True)  # the full text width, laid wide
axes[0, 0].set_yscale("log")
for ax, (matrix, series) in zip(axes.flat, matrices.items()):
    handles = {name: ax.plot(series[name]["x"], series[name]["y"], **style)[0] for name, style in styles.items()}
    ax.set_title(matrix)  # the y label names the quantity; the full original titles overlap at this width
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="both")
for row in axes:
    row[0].set_ylabel("Condition number")
fig.supxlabel("Normalized layer index")
paper.add_legend_rows(axes[0, 0], [("nGPT", [handles["nGPT 0.5B"], handles["nGPT 1B"]], ["0.5B", "1B"]),
                                   ("GPT", [handles["GPT 0.5B"], handles["GPT 1B"]], ["0.5B", "1B"])])

# square panels
finalize_figure(fig, axes, height="M", min_width=0.45)
fig.savefig("../out/condition-numbers.pdf")
