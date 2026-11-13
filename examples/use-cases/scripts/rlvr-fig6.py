"""Perplexity of individual responses to Problem 1, under the base and RL models. Boxes span the quartiles with the median as a line; whiskers reach 1.5× the interquartile range; points show every response. The base model finds RL responses as likely as its own (median perplexity 1.06 against 1.08), far more likely than ground-truth responses (1.21)."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, shift_lightness

colors = paper.colors

with open("../data/rlvr-fig6.json") as f:
    groups = json.load(f)["Problem 1"]
names = ["PPL_Base(Y_Base)", "PPL_Base(Y_RL)", "PPL_RL(Y_RL)", "PPL_Base(Y_GT)"]
labels = [r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{Base}})$", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{RL}})$",
          r"$\mathrm{PPL}_{\mathrm{RL}}(Y_{\mathrm{RL}})$", r"$\mathrm{PPL}_{\mathrm{Base}}(Y_{\mathrm{GT}})$"]

medians = {name: float(np.median(groups[name])) for name in names}
print("takeaway:", {name: f"{v:#.3g}" for name, v in medians.items()})
assert medians["PPL_Base(Y_RL)"] <= medians["PPL_Base(Y_Base)"] < medians["PPL_Base(Y_GT)"], "the takeaway does not hold"

rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
for y, name in enumerate(names):
    values = groups[name]
    box = ax.boxplot(values, positions=[y], widths=0.7, patch_artist=True, showfliers=False, orientation="horizontal")
    box["boxes"][0].set_facecolor(shift_lightness(colors["series-1"], 2))
    ax.plot(values, y + rng.uniform(-0.2, 0.2, len(values)), "o", color=colors["ink"], linestyle="none")
ax.set_yticks(range(len(names)), labels=labels)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.grid(axis="y", visible=False)
ax.set_xlabel("Perplexity")

finalize_figure(fig, ax)
fig.savefig("../outputs/rlvr-fig6.pdf")
fig.savefig("../outputs/rlvr-fig6.png")
