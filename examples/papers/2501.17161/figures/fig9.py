"""RL experiments on GP-L without SFT initialization. All trials fail due to poor instruction following capability of the base model."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

sys.path.insert(0, "../../../../skills/academic-figure/assets")
import paper
from paper import finalize_figure, make_shades

colors = paper.colors

runs = json.load(open("../data/fig9.json"))["runs"]
rates = ["5e-7", "1e-6", "2e-6"]  # the learning rate sweep, smallest first

# takeaway: every learning rate ends at zero success
final = {rate: runs[rate]["raw"][-1] for rate in rates}
print("takeaway:", final)
assert all(v == 0 for v in final.values()), "the takeaway does not hold"

shades = make_shades(colors["ours"], len(rates))  # RL, ours in every figure of the paper

fig, ax = plt.subplots(figsize=(3.25, 3.25))
for rate, color, marker in zip(rates, shades, ["o", "s", "^"]):
    run = runs[rate]
    gflops = np.array(run["gflops"])
    ax.fill_between(gflops, run["error_low"], run["error_high"], color=color, alpha=0.2, linewidth=0)
    ax.plot(gflops, run["raw"], marker, color=color, label=rate)
    # a success rate is never below 0; the original smoothing dips under it (to −0.024), so it is clipped there
    ax.plot(gflops, np.clip(run["smoothed"], 0, None), color=color, label=rate)
ax.set_xlabel("Computation (GFLOPs)")
ax.set_ylabel("Success rate (%)")
ax.grid(True)
ax.legend([Line2D([], [], color=color, marker=marker) for color, marker in zip(shades, ["o", "s", "^"])],
          [rate.replace("-", "−") for rate in rates])

# XS, as Figure 10 beside it
finalize_figure(fig, ax, height="XS")
fig.savefig("../out/fig9.pdf")
