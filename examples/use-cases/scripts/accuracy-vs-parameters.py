"""ImageNet top-1 accuracy versus number of parameters. The solid line joins EfficientNet-B0 to B7 (ours) in size order; the dashed line joins the hand-designed models and the dotted line the NAS models on their Pareto fronts; unjoined markers are other baselines. EfficientNet-B7 reaches 84.4% top-1 with 66M parameters, above AmoebaNet-C (83.5%) with 2.35× fewer parameters."""

import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, darken

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/accuracy-vs-parameters.json") as f:
    models = json.load(f)


def family(name):
    rows = sorted((m for m in models if m["family"] == name), key=lambda m: m["params_millions"])
    return [m["params_millions"] for m in rows], [m["top1_accuracy"] for m in rows]


def pareto_front(xs, ys):
    """Models not beaten by any other model with no more parameters and higher accuracy, in x order."""
    front = [(x, y) for x, y in zip(xs, ys)
             if not any(x2 <= x and y2 > y or x2 < x and y2 >= y for x2, y2 in zip(xs, ys))]
    return [x for x, _ in front], [y for _, y in front]


eff_x, eff_y = family("EfficientNet")
hand_x, hand_y = family("hand-designed")
nas_x, nas_y = family("NAS")
other_x, other_y = family("other")

# Takeaway: the largest EfficientNet beats the most accurate baseline with fewer parameters.
baselines = [m for m in models if m["family"] != "EfficientNet"]
best_base = max(baselines, key=lambda m: m["top1_accuracy"])
b7 = max((m for m in models if m["family"] == "EfficientNet"), key=lambda m: m["params_millions"])
ratio = best_base["params_millions"] / b7["params_millions"]
print("takeaway:", b7["model"], b7["top1_accuracy"], b7["params_millions"], "|",
      best_base["model"], best_base["top1_accuracy"], best_base["params_millions"], "|", f"{ratio:#.3g}×")
assert b7["top1_accuracy"] > best_base["top1_accuracy"] and ratio > 1, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))

hand_fx, hand_fy = pareto_front(hand_x, hand_y)
nas_fx, nas_fy = pareto_front(nas_x, nas_y)
ax.plot(hand_fx, hand_fy, linestyle="--", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
ax.plot(nas_fx, nas_fy, linestyle=":", linewidth=paper.dashed_width, color=colors["neutral"], zorder=1)
ax.plot(hand_x, hand_y, "o", color=colors["neutral"], linestyle="none")
ax.plot(nas_x, nas_y, "o", color=colors["neutral"], linestyle="none")
h_other = ax.plot(other_x, other_y, "o", color=colors["neutral"], linestyle="none")[0]
h_eff = ax.plot(eff_x, eff_y, "o-", color=colors["ours"])[0]

# Legend proxies: line style plus marker for the two fronts.
p_hand = plt.Line2D([], [], color=colors["neutral"], marker="o", linestyle="--", linewidth=paper.dashed_width)
p_nas = plt.Line2D([], [], color=colors["neutral"], marker="o", linestyle=":", linewidth=paper.dashed_width)

ax.annotate(f"{b7['model'].removeprefix('EfficientNet-')} ({b7['top1_accuracy']:#.3g}%)",
            (b7["params_millions"], b7["top1_accuracy"]),
            xytext=(-3, 3), textcoords="offset points", ha="right", color=darken(colors["ours"]))
ax.annotate(f"{best_base['model']} ({best_base['top1_accuracy']:#.3g}%)",
            (best_base["params_millions"], best_base["top1_accuracy"]),
            xytext=(-3, 3), textcoords="offset points", ha="right", color=darken(colors["neutral"]))

ax.set_xlabel("Parameters (M)")
ax.set_ylabel("Top-1 accuracy (%)")
ax.grid(True)
ax.legend([h_eff, p_hand, p_nas, h_other], ["EfficientNet (ours)", "Hand-designed", "NAS", "Other"],
          loc="lower right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/accuracy-vs-parameters.pdf")
fig.savefig("../outputs/accuracy-vs-parameters.png")
