"""Training loss and learning rate versus training steps. The loss is smoothed with a moving average over 5% of the steps; the faint line shows raw values. The learning rate warms up linearly for 1000 steps, then decays with a cosine schedule. 63% of the loss decrease happens during warmup."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import finalize_figure, moving_average

colors = paper.apply_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/loss-and-learning-rate.json") as f:
    data = json.load(f)
steps = np.array(data["steps"])
loss = np.array(data["training_loss"])
learning_rate = np.array(data["learning_rate"])

# takeaway: most of the loss decrease happens during the warmup
smoothed = np.array(moving_average(loss))
warmup_end = int(np.argmax(learning_rate))
share = (loss[0] - loss[warmup_end]) / (loss[0] - smoothed[-1])
print("takeaway:", "warmup steps", steps[warmup_end], "loss start", f"{loss[0]:#.3g}",
      "loss at warmup end", f"{loss[warmup_end]:#.3g}", "final smoothed", f"{smoothed[-1]:#.3g}",
      "share of decrease in warmup", f"{share:.0%}")
assert share > 0.5, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75))
twin = ax.twinx()

ax.plot(steps, loss, color=colors["series-1"], alpha=0.25)
ax.plot(steps, smoothed, color=colors["series-1"], label="Training loss")
ax.set_ylabel("Training loss")
ax.set_xlabel("Training step")
ax.set_xticks([0, 5000, 10000, 15000, 20000], labels=["0", "5K", "10K", "15K", "20K"])

twin.plot(steps, learning_rate * 1e4, color=colors["series-4"], linestyle="--", linewidth=paper.dashed_width, label="Learning rate")
twin.set_ylabel("Learning rate (×10⁻⁴)")
twin.grid(False)

ax.set_zorder(twin.get_zorder() + 1)
ax.patch.set_visible(False)
handles = ax.get_legend_handles_labels()[0] + twin.get_legend_handles_labels()[0]
ax.legend(handles, [h.get_label() for h in handles], loc="upper right")

finalize_figure(fig, ax)
fig.savefig("../outputs/loss-and-learning-rate.pdf")
fig.savefig("../outputs/loss-and-learning-rate.png")
