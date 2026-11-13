"""Models trained with 4k context length. Final performance (y-axis) on a set of downstream tasks and their average value (Bottom-Right) for different computation budgets in tokens (x-axis)."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

tasks = json.load(open("../data/downstream-tasks.json"))

# takeaway: on the average, nGPT 1B is ahead of GPT 1B at every budget both trained with
average = tasks["average"]
gpt = dict(zip(average["GPT 1B"]["tokens_b"], average["GPT 1B"]["value"]))
ngpt = dict(zip(average["nGPT 1B"]["tokens_b"], average["nGPT 1B"]["value"]))
shared = [t for t in gpt if t in ngpt]
print("takeaway: average at shared budgets", {f"{t:.0f}B": (f"{ngpt[t]:#.3g}", f"{gpt[t]:#.3g}") for t in shared})
assert all(ngpt[t] > gpt[t] for t in shared), "the takeaway does not hold"

# model sizes inside each family: nGPT (ours) in shades of ours, GPT in grey shades and dashed; larger is darker
ngpt_shades, gpt_shades = make_shades(colors["ours"], 2), make_shades(colors["neutral"], 2)
styles = {
    "nGPT 0.5B": dict(marker="o", color=ngpt_shades[0]),
    "nGPT 1B": dict(marker="s", color=ngpt_shades[1]),
    "GPT 0.5B": dict(marker="^", color=gpt_shades[0], linestyle="--", linewidth=paper.dashed_linewidth),
    "GPT 1B": dict(marker="D", color=gpt_shades[1], linestyle="--", linewidth=paper.dashed_linewidth),
}

fig, axes = plt.subplots(2, 3, figsize=(5.5, 5.5), layout="constrained", sharex=True)
for ax, (task, series) in zip(axes.flat, tasks.items()):
    handles = {name: ax.plot(series[name]["tokens_b"], series[name]["value"], **style)[0] for name, style in styles.items()}
    ax.set_title(f"4K context: {task}")
    ax.grid(True)
for row in axes:
    row[0].set_ylabel("Value")
fig.supxlabel("Training tokens in billions")
paper.add_legend_rows(axes[0, 0], [("nGPT", [handles["nGPT 0.5B"], handles["nGPT 1B"]], ["0.5B", "1B"]),
                                   ("GPT", [handles["GPT 0.5B"], handles["GPT 1B"]], ["0.5B", "1B"])])

# original figure height / width 0.73 (4.00 in printed); M keeps it (3.86 in)
finalize_figure(fig, axes, height="M", min_width=0.45)
fig.savefig("../out/downstream-tasks.pdf")
