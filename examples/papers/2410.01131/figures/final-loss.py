"""Final validation loss (y-axis) for training runs with different computation budgets in tokens (x-axis). The training of 0.5B and 1B nGPT models is about 4x, 10x and 20x faster (in terms of tokens) on 1k, 4k and 8k context lengths, respectively."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../../skills/paper-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

runs = json.load(open("../data/final-loss.json"))

# takeaway: tokens GPT 1B needs for its final loss, over the tokens nGPT 1B needs to reach that loss
for context, series in runs.items():
    gpt, ngpt = series["GPT 1B"], series["nGPT 1B"]
    target = gpt["value"][-1]
    reached = next(t for t, v in zip(ngpt["tokens_b"], ngpt["value"]) if v <= target)
    print(f"takeaway: {context}: nGPT 1B reaches GPT 1B's final loss {target:#.3g} at {reached:.0f}B tokens, "
          f"{gpt['tokens_b'][-1] / reached:.0f}x fewer than {gpt['tokens_b'][-1]:.0f}B")
    assert reached < gpt["tokens_b"][-1], "the takeaway does not hold"

# model sizes inside each family: nGPT (ours) in shades of ours, GPT in grey shades and dashed; larger is darker
ngpt_shades, gpt_shades = make_shades(colors["ours"], 2), make_shades(colors["neutral"], 2)
styles = {
    "nGPT 0.5B": dict(marker="o", color=ngpt_shades[0]),
    "nGPT 1B": dict(marker="s", color=ngpt_shades[1]),
    "GPT 0.5B": dict(marker="^", color=gpt_shades[0], linestyle="--", linewidth=paper.dashed_linewidth),
    "GPT 1B": dict(marker="D", color=gpt_shades[1], linestyle="--", linewidth=paper.dashed_linewidth),
}

fig, axes = plt.subplots(1, 3, figsize=(5.5, 5.5), layout="constrained", sharey=True)
for ax, (context, series) in zip(axes, runs.items()):
    handles = {name: ax.plot(series[name]["tokens_b"], series[name]["value"], **style)[0] for name, style in styles.items()}
    ax.set_title(f"{context}: OpenWebText")
    ax.grid(True)
axes[0].set_ylabel("Validation loss")
fig.supxlabel("Training tokens (B)")
paper.add_legend_rows(axes[0], [("nGPT", [handles["nGPT 0.5B"], handles["nGPT 1B"]], ["0.5B", "1B"]),
                                ("GPT", [handles["GPT 0.5B"], handles["GPT 1B"]], ["0.5B", "1B"])])

finalize_figure(fig, axes)
fig.savefig("../out/final-loss.pdf")
