"""Redraw every figure of the DAPO paper (arXiv:2503.14476) with academic-figure.

The data in academic-figure/dapo.json was read from the vector paths of the paper's PDF.
Run from the repo root: uv run -p 3.12 --with matplotlib --with tol-colors python examples/academic-figure.py
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import tol_colors as tc

ROOT = Path(__file__).parent
OUT = ROOT / "academic-figure"
sys.path.insert(0, str(ROOT.parent / "skills/academic-figure/assets"))
from paper import fit_height

plt.style.use(ROOT.parent / "skills/academic-figure/assets/paper.mplstyle")
ONE_HALF, DOUBLE = 5.0625, 6.75
cset = tc.colorsets["bright"]
data = json.load(open(OUT / "dapo.json"))


def save(fig, name):
    fig.savefig(OUT / f"{name}-after.png")
    plt.close(fig)


def shared_legend(fig, ax):
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=2,
               frameon=False, borderaxespad=0, fontsize=8)


def moving_average(values):
    half = max(1, len(values) // 40)
    return [sum(w) / len(w) for w in (values[max(0, i - half):i + half + 1] for i in range(len(values)))]


def plot_curve(ax, s, color, label=None, smooth=False):
    if smooth:
        ax.plot(s["step"], s["value"], color=color, alpha=0.25)
        ax.plot(s["step"], moving_average(s["value"]), color=color, label=label)
    else:
        ax.plot(s["step"], s["value"], color=color, label=label)


def panels(rows, titles, sharex=False):
    fig, axes = plt.subplots(rows, 2, figsize=(DOUBLE, 2 * rows), sharex=sharex)
    for ax, letter, title in zip(axes.flat, "abcd", titles):
        ax.set_title(f"({letter}) {title}")
    return fig, list(axes.flat)


def ablation(name, keys, captions, ylabels, ours, other, smooth):
    fig, axes = panels(1, captions, sharex=True)
    for ax, key, ylabel, sm in zip(axes, keys, ylabels, smooth):
        for label, color in [(other, cset.blue), (ours, cset.red)]:
            plot_curve(ax, data[key][label], color, label, sm)
        ax.set_xlabel("Training steps")
        ax.set_ylabel(ylabel)
    shared_legend(fig, axes[0])
    fit_height(fig, axes)
    save(fig, name)


def fig1():
    fig, ax = plt.subplots(figsize=(DOUBLE, 2))
    ax.axhline(47, color=cset.grey, linestyle="--", linewidth=1, alpha=0.5, zorder=1)
    ax.axvline(10000, color=cset.grey, linestyle="--", linewidth=1, alpha=0.5, zorder=1)
    ax.plot(10000, 47, "o", color=cset.grey)
    ax.annotate("DeepSeek-R1-Zero-Qwen-32B", (10000, 47), xytext=(-6, -4), textcoords="offset points",
                ha="right", va="top", fontsize=7, color=tc.colorsets["dark"].dark_grey)
    for label, color, marker in [("DAPO avg@32", cset.red, "o"), ("DAPO pass@32", cset.blue, "v"),
                                 ("DAPO cons@32", cset.green, "^")]:
        s = data["fig1"][label]
        ax.plot(s["step"], s["value"], color=color, marker=marker,
                label=label)
    ax.set_xlabel("Training steps")
    ax.set_ylabel("AIME 2024 accuracy (%)")
    ax.legend(loc="lower right", bbox_to_anchor=(9600, 0), bbox_transform=ax.get_xaxis_transform())
    fit_height(fig, ax, aspect=1 / 3)
    save(fig, "fig1")


def fig3():
    fig, axes = panels(1, ["Mean up-clipped probability", "Samples with an accuracy of 1"])
    for ax, key, ylabel in zip(axes, ["fig3a", "fig3b"],
                               ["Mean up-clipped probability", "Prompts with accuracy = 1"]):
        plot_curve(ax, data[key], cset.blue, smooth=True)
        ax.set_xlabel("Training steps")
        ax.set_ylabel(ylabel)
    fit_height(fig, axes)
    save(fig, "fig3")


def fig6():
    fig, ax = plt.subplots(figsize=(ONE_HALF, 2))
    ax.axhline(0.429, color=cset.grey, linestyle="--", linewidth=1, alpha=0.5, zorder=1)
    for label, color in [("w/o Dynamic Sampling", cset.blue), ("w/ Dynamic Sampling", cset.red)]:
        s = data["fig6"][label]
        best = s["step"][s["value"].index(max(s["value"]))]
        ax.axvline(best, color=color, linestyle="--", linewidth=1, alpha=0.5, zorder=1)
        ax.plot(s["step"], s["value"], color=color, label=label)
    ax.set_xlabel("Training steps")
    ax.set_ylabel("AIME avg@32")
    ax.legend(loc="lower right")
    fit_height(fig, ax, aspect=1 / 3)
    save(fig, "fig6")


def fig7():
    labels = ["Mean response length", "Reward score", "Generation entropy", "Mean probability"]
    fig, axes = panels(2, labels, sharex=True)
    for ax, key, ylabel in zip(axes, ["fig7a", "fig7b", "fig7c", "fig7d"], labels):
        ax.plot(data[key]["step"], data[key]["value"], color=cset.blue)
        ax.set_ylabel(ylabel)
    for ax in axes[2:]:
        ax.set_xlabel("Training steps")
    fit_height(fig, axes)
    save(fig, "fig7")


fig1()
ablation("fig2", ["fig2a", "fig2b"], ["Accuracy on AIME", "Entropy of actor model"],
         ["AIME avg@32", "Generation entropy"],
         "w/ Clip-Higher", "w/o Clip-Higher", smooth=(False, True))
fig3()
ablation("fig4", ["fig4a", "fig4b"],
         ["Entropy of generation probabilities", "Average response length"],
         ["Generation entropy", "Mean response length"],
         "w/ token-level loss", "w/o token-level loss", smooth=(True, True))
ablation("fig5", ["fig5a", "fig5b"], ["Performance on AIME", "Entropy of actor model"],
         ["AIME avg@32", "Generation entropy"],
         "w/ overlong filtering", "w/o overlong filtering", smooth=(False, True))
fig6()
fig7()
