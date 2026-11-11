"""Training loss and learning rate over training steps. The loss is smoothed with a moving average over 5% of the steps; the faint line shows raw values; the learning rate is read on the right axis. The learning rate warms up linearly to 0.0003 over the first 1000 steps, then decays with a cosine to 0.00003, while the loss falls from 11.3 to 2.01."""

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

# Takeaway: linear warmup to the peak, cosine decay after it, while the loss falls.
peak = int(np.argmax(lr))
print("takeaway:", {"peak lr": np.format_float_positional(lr[peak], 3, fractional=False, trim="-"), "warmup steps": int(steps[peak]),
                    "final lr": np.format_float_positional(lr[-1], 3, fractional=False, trim="-"), "first loss": f"{loss[0]:.3g}", "last loss": f"{loss[-1]:.3g}"})
assert np.all(np.diff(lr[:peak + 1]) > 0) and np.all(np.diff(lr[peak:]) <= 0), "the takeaway does not hold"
assert loss[-1] < loss[0], "the takeaway does not hold"

fig, ax = plt.subplots(figsize=(2.75, 2.75), layout="constrained")
right = ax.twinx()
ax.set_zorder(right.get_zorder() + 1)  # the legend on the left axis sits above the learning rate
ax.patch.set_visible(False)

ax.plot(steps, loss, color=colors["series-1"], alpha=0.25)
loss_line, = ax.plot(steps, smooth(loss), color=colors["series-1"], label="Training loss")
lr_line, = right.plot(steps, lr, color=colors["series-3"], label="Learning rate")

ax.grid(True)
ax.set_xticks([0, 5000, 10000, 15000, 20000], labels=["0", "5", "10", "15", "20"])
ax.set_xlabel("Training step (K)")
ax.set_ylabel("Training loss")
right.set_ylabel("Learning rate (×10⁻⁴)")
right.yaxis.set_major_formatter(lambda v, _: f"{v * 1e4:.10g}".replace("-", "−"))
right.set_ylim(bottom=0)

ax.legend([loss_line, lr_line], ["Training loss", "Learning rate"], loc="upper right")

fit_height(fig, ax, aspect=0.618)
fig.savefig("../outputs/loss-and-learning-rate.pdf")
fig.savefig("../outputs/loss-and-learning-rate.png")
