"""Training loss and learning rate over training steps. The loss is smoothed with a moving average over 5% of the steps; the faint line shows raw values. The learning rate warms up linearly to its peak at step 1000, then decays along a cosine; the loss falls from 11.3 to 2.01 and covers 90% of that drop by step 3200."""

import json
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "../../../skills/academic-figure/assets")
import paper  # registers the bundled Inter font
from paper import fit_height, smooth

colors = paper.use_design("../../../skills/academic-figure/assets/DESIGN.md")

with open("../data/loss-and-learning-rate.json") as f:
    data = json.load(f)
steps = np.array(data["steps"])
loss = np.array(data["training_loss"])
lr = np.array(data["learning_rate"])

# Takeaway: the loss drops early, around warmup, and flattens as the learning rate decays.
smoothed = np.array(smooth(loss))
peak_step = steps[np.argmax(lr)]
drop = smoothed[0] - smoothed[-1]
step_90 = steps[np.argmax(smoothed <= smoothed[0] - 0.9 * drop)]
print("takeaway:", {"first loss": f"{loss[0]:#.3g}", "last loss": f"{loss[-1]:#.3g}",
                    "lr peak step": int(peak_step), "90% of drop by step": int(step_90)})
assert step_90 < steps[-1] / 4, "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
twin = ax.twinx()

ax.plot(steps, loss, color=colors["series-1"], alpha=0.25)
ax.plot(steps, smoothed, color=colors["series-1"], label="Training loss")
twin.plot(steps, lr * 1e4, color=colors["series-3"], label="Learning rate")

ax.grid(True)
twin.grid(False)
ax.set_xticks([0, 5000, 10000, 15000, 20000], labels=["0", "5K", "10K", "15K", "20K"])
ax.set_xlabel("Training step")
ax.set_ylabel("Training loss")
twin.set_ylabel("Learning rate (×10⁻⁴)")

ax.set_zorder(twin.get_zorder() + 1)
ax.patch.set_visible(False)
handles = ax.get_legend_handles_labels()[0] + twin.get_legend_handles_labels()[0]
ax.legend(handles, [h.get_label() for h in handles], loc="upper right")

fit_height(fig, ax)
fig.savefig("../outputs/loss-and-learning-rate.pdf")
fig.savefig("../outputs/loss-and-learning-rate.png")
