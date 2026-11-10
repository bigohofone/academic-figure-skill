import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TEXT_WIDTH = 6.75
COLUMN_WIDTH = 3.25

plt.rcParams.update({
    "font.size": 8,
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "legend.fontsize": 7,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "lines.linewidth": 1.2,
})

data = json.load(open("dapo.json"))


def plot_panel(ax, curves, title, ylabel):
    if "step" in curves:
        curves = {None: curves}
    for label, c in curves.items():
        ax.plot(c["step"], c["value"], label=label)
    ax.set_title(title)
    ax.set_xlabel("Training steps")
    ax.set_ylabel(ylabel)
    if None not in curves:
        ax.legend()


def save_panels(name, panels, width=TEXT_WIDTH, height=2.2):
    fig, axes = plt.subplots(1, len(panels), figsize=(width, height))
    axes = [axes] if len(panels) == 1 else axes
    for ax, (key, title, ylabel) in zip(axes, panels):
        plot_panel(ax, data[key], title, ylabel)
    fig.tight_layout()
    fig.savefig(name, dpi=300)
    plt.close(fig)


fig, ax = plt.subplots(figsize=(TEXT_WIDTH, 2.6))
ax.axhline(47, color="gray", linestyle="--", linewidth=1, label="DeepSeek-R1-Zero-Qwen-32B (10k steps)")
plot_panel(ax, data["fig1"], "AIME 2024 (Qwen2.5-32B base)", "Score")
ax.axvline(5000, color="gray", linestyle=":", linewidth=1)
ax.text(4950, 5, "50% of steps", ha="right", color="gray", fontsize=7)
fig.tight_layout()
fig.savefig("fig1.png", dpi=300)
plt.close(fig)

save_panels("fig2.png", [
    ("fig2a", "(a) Accuracy on AIME", "avg@32"),
    ("fig2b", "(b) Entropy of actor model", "Entropy"),
])
save_panels("fig3.png", [
    ("fig3a", "(a) Mean up-clipped probability", "Probability"),
    ("fig3b", "(b) Proportion of samples with accuracy 1", "Proportion"),
])
save_panels("fig4.png", [
    ("fig4a", "(a) Entropy of generation probabilities", "Entropy"),
    ("fig4b", "(b) Average response length", "Length (tokens)"),
])
save_panels("fig5.png", [
    ("fig5a", "(a) Performance on AIME", "avg@32"),
    ("fig5b", "(b) Entropy of actor model", "Entropy"),
])
save_panels("fig6.png", [
    ("fig6", "AIME (avg@32) with and without dynamic sampling", "avg@32"),
], width=1.5 * COLUMN_WIDTH, height=2.4)
save_panels("fig7.png", [
    ("fig7a", "(a) Mean response length", "Length (tokens)"),
    ("fig7b", "(b) Reward score", "Reward"),
    ("fig7c", "(c) Generation entropy", "Entropy"),
    ("fig7d", "(d) Mean probability", "Probability"),
], height=1.9)
