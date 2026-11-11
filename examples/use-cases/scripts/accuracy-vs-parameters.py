"""ImageNet top-1 accuracy versus number of parameters. The solid line joins EfficientNet-B0 to B7; the dashed and dotted lines join the hand-designed and NAS models on their Pareto fronts. EfficientNet-B7 reaches 84.4% with 66M parameters, above the best baseline, AmoebaNet-C, at 83.5% with 155M, 2.35× fewer parameters."""

import json
import sys

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/accuracy-vs-parameters.json") as f:
    models = json.load(f)


def family(name):
    rows = sorted((m for m in models if m["family"] == name), key=lambda m: m["params_millions"])
    return [m["params_millions"] for m in rows], [m["top1_accuracy"] for m in rows], [m["model"] for m in rows]


ours_x, ours_y, ours_names = family("EfficientNet")
hand_x, hand_y, _ = family("hand-designed")
nas_x, nas_y, _ = family("NAS")
other_x, other_y, _ = family("other")

# takeaway: our largest model against the most accurate baseline
baselines = [m for m in models if m["family"] != "EfficientNet"]
best_base = max(baselines, key=lambda m: m["top1_accuracy"])
ours_best = max((m for m in models if m["family"] == "EfficientNet"), key=lambda m: m["top1_accuracy"])
ratio = best_base["params_millions"] / ours_best["params_millions"]
print("takeaway:", ours_best["model"], f"{ours_best['top1_accuracy']:#.3g}%", f"{ours_best['params_millions']}M;",
      best_base["model"], f"{best_base['top1_accuracy']:#.3g}%", f"{best_base['params_millions']}M;", f"{ratio:#.3g}×")
assert ours_best["top1_accuracy"] > best_base["top1_accuracy"] and ratio > 1, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
ax.grid(True)

# Pareto fronts of the baselines, under the markers
ax.plot(hand_x, hand_y, linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
ax.plot(nas_x, nas_y, linestyle=":", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
ax.plot(hand_x + nas_x + other_x, hand_y + nas_y + other_y, "o", color=colors["neutral"])
ax.plot(ours_x, ours_y, "o-", color=colors["ours"])

# cited models, named with their values
# (EfficientNet-B7 shortened to "B7": the legend names the family)
for m, name, color, xytext, ha, va in [(ours_best, "B7", colors["ours"], (-3, 3), "right", "bottom"),
                                       (best_base, "AmoebaNet-C", colors["neutral"], (-3, 3), "right", "bottom")]:
    ax.annotate(f"{name} ({m['top1_accuracy']:#.3g}%)", (m["params_millions"], m["top1_accuracy"]),
                xytext=xytext, textcoords="offset points", ha=ha, va=va, color=darken(color))

ax.set_xlabel("Parameters (M)")
ax.set_ylabel("Top-1 accuracy (%)")

handles = [
    Line2D([], [], marker="o", color=colors["ours"]),
    Line2D([], [], marker="o", linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"]),
    Line2D([], [], marker="o", linestyle=":", linewidth=paper.dashed_width, color=colors["neutral"]),
    Line2D([], [], marker="o", linestyle="none", color=colors["neutral"]),
]
ax.legend(handles, ["EfficientNet (ours)", "Hand-designed", "NAS", "Other"], loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/accuracy-vs-parameters.pdf")
fig.savefig("../outputs/accuracy-vs-parameters.png")
