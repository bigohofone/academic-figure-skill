"""The landing page's layout card, before: the same three figures as a model writes them without the skill.

Plain matplotlib, each figure sized by its own guess and saved with a tight bounding box, so stacked at one width
their panels neither line up nor share a text size.

Run from anywhere: python examples/layouts/without.py
Writes docs/layouts/img/without/.
"""

from pathlib import Path

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[2] / "docs/layouts/img/without"
steps = np.arange(0, 2600, 50)


def curves(ax, gap):
    ours = 0.9 - 0.7 * np.exp(-steps / 500)
    ax.plot(steps, ours, label="Ours")
    ax.plot(steps, ours - gap, label="Baseline")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


OUT.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 2.6))
curves(ax, 0.08)
ax.set_xlabel("Training step")
ax.set_ylabel("Accuracy")
ax.legend()
save(fig, "one-panel-full-width-xs")

for n, size in ((3, (15, 4)), (6, (18, 3.2))):
    fig, axes = plt.subplots(1, n, figsize=size)
    for i, ax in enumerate(axes):
        curves(ax, 0.03 * (i + 1))
        ax.set_title(f"Dataset {i + 1}")
        ax.set_xlabel("Training step")
        ax.set_ylabel("Accuracy")
        ax.legend()
    save(fig, "row-of-3" if n == 3 else "row-of-6-sq")
