"""pass@k performance under different reward compositions. Each bar corresponds to a distinct reward-mixing strategy. Incorporating process-level information into the outcome reward consistently yields measurable performance gains across evaluation settings."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, shift_lightness

colors = paper.colors

data = json.load(open("../data/reward-mixes.json"))
rewards = data["rewards"]

gain = [[v - panel["pass_at_k"][0] for v in panel["pass_at_k"][1:]] for panel in data["panels"]]
print("takeaway: gain over 1.0 Outcome per panel", [[f"{g:+.1f}" for g in row] for row in gain])
assert all(max(row) > 0 for row in gain), "no process-aware reward beats the outcome reward"

fig, axes = plt.subplots(1, 4, figsize=(6.3, 6.3), layout="constrained")

# values differ by < 10% in three panels, so points instead of bars from 0; outcome-only reward grey, the process-aware rewards ours
styles = [dict(color=colors["neutral"], marker="D")] + [dict(color=colors["ours"], marker=m) for m in ["o", "s", "^"]]
for ax, panel in zip(axes, data["panels"]):
    base = panel["pass_at_k"][0]
    for x, (name, value, style) in enumerate(zip(rewards, panel["pass_at_k"], styles)):
        ax.plot(x, value, linestyle="none", label=name, **style)
        text = f"{value:.1f}" if x == 0 else f"{value - base:+.1f}".replace("-", "−")
        ax.annotate(text, (x, value), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                    color=shift_lightness(style["color"], -1), gid="value-label")
    ax.set_xticks([])
    ax.set_xlim(-0.5, len(rewards) - 0.5)
    ax.set_title(f"{panel['metric']}\n{panel['ops']}")
    ax.grid(axis="y")
    ax.grid(axis="x", visible=False)

axes[0].set_ylabel("pass@k (%)")
axes[0].legend()

# original height / width 185.6 / 851.3 = 0.22, 1.37 in printed; XS gives the closest height
finalize_figure(fig, axes, height="S")
fig.savefig("../out/reward-mixes.pdf")
