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
from paper import fit_height, mark_value, smooth, darken

plt.style.use(ROOT.parent / "skills/academic-figure/assets/paper.mplstyle")
ONE_HALF, DOUBLE = 5.0625, 6.75
cset = tc.colorsets["bright"]
# series colors taken from the original figures' vector paths, so each redraw matches its original
PALETTE = {"purple": "#5F16A7", "cyan": "#63C9D2", "blue": "#4D8BD7"}
data = json.load(open(OUT / "dapo.json"))


def save(fig, name):
    fig.savefig(OUT / f"{name}-after.png")
    plt.close(fig)


def shared_legend(fig, ax):
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncol=2,
               frameon=False, borderaxespad=0)


def plot_curve(ax, s, color, label=None, noisy=False):
    if noisy:
        ax.plot(s["step"], s["value"], color=color, alpha=0.25)
        ax.plot(s["step"], smooth(s["value"]), color=color, label=label)
    else:
        ax.plot(s["step"], s["value"], color=color, label=label)


def panels(rows, titles, sharex=False):
    fig, axes = plt.subplots(rows, 2, figsize=(DOUBLE, 2 * rows), sharex=sharex)
    for ax, letter, title in zip(axes.flat, "abcd", titles):
        ax.set_title(f"({letter}) {title}")
    return fig, list(axes.flat)


def ablation(name, keys, captions, ylabels, ours, other, noisy, ours_color="purple", other_color="cyan"):
    fig, axes = panels(1, captions, sharex=True)
    for ax, key, ylabel, sm in zip(axes, keys, ylabels, noisy):
        for label, color in [(other, PALETTE[other_color]), (ours, PALETTE[ours_color])]:
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
    ax.annotate("DeepSeek-R1-Zero-Qwen-32B", (10000, 47), xytext=(-6, -4), textcoords="offset points",
                ha="right", va="top", color=darken(cset.grey))
    for label, color, marker in [("DAPO avg@32", PALETTE["purple"], "o"),
                                 ("DAPO pass@32", PALETTE["cyan"], "v"),
                                 ("DAPO cons@32", PALETTE["blue"], "^")]:
        s = data["fig1"][label]
        ax.plot(s["step"], s["value"], color=color, marker=marker,
                label=label)
    avg = data["fig1"]["DAPO avg@32"]
    peak = max(avg["value"])
    best = avg["step"][avg["value"].index(peak)]
    mark_value(ax, best, peak, f"{peak:.1f}", PALETTE["purple"], star=True)
    ax.annotate("DAPO", (best, peak), xytext=(8, 0), textcoords="offset points",
                ha="left", va="center", color=darken(PALETTE["purple"]))
    mark_value(ax, 10000, 47, "47.0", cset.grey)
    ax.set_xlabel("Training steps")
    ax.set_ylabel("AIME 2024 accuracy (%)")
    ax.legend(loc="lower right", bbox_to_anchor=(9600, 0), bbox_transform=ax.get_xaxis_transform())
    fit_height(fig, ax, aspect=0.382)
    save(fig, "fig1")


def fig3():
    fig, axes = panels(1, ["Mean up-clipped probability", "Samples with an accuracy of 1"])
    for ax, key, ylabel in zip(axes, ["fig3a", "fig3b"],
                               ["Mean up-clipped probability", "Prompts with accuracy = 1"]):
        plot_curve(ax, data[key], PALETTE["blue"], noisy=True)
        ax.set_xlabel("Training steps")
        ax.set_ylabel(ylabel)
    fit_height(fig, axes)
    save(fig, "fig3")


def fig6():
    fig, ax = plt.subplots(figsize=(ONE_HALF, 2))
    ax.axhline(0.429, color=cset.grey, linestyle="--", linewidth=1, alpha=0.5, zorder=1)
    for label, color in [("w/o Dynamic Sampling", PALETTE["cyan"]),
                         ("w/ Dynamic Sampling", PALETTE["purple"])]:
        s = data["fig6"][label]
        peak = max(s["value"])
        best = s["step"][s["value"].index(peak)]
        ax.axvline(best, color=color, linestyle="--", linewidth=1, alpha=0.5, zorder=1)
        ax.plot(s["step"], s["value"], color=color, label=label)
        mark_value(ax, best, peak, f"{peak:.3f}", color)
    ax.set_xlabel("Training steps")
    ax.set_ylabel("AIME avg@32")
    ax.legend(loc="lower right", bbox_to_anchor=(5980, 0), bbox_transform=ax.get_xaxis_transform())
    fit_height(fig, ax, aspect=0.382)
    save(fig, "fig6")


def fig7():
    labels = ["Mean response length", "Reward score", "Generation entropy", "Mean probability"]
    fig, axes = panels(2, labels, sharex=True)
    for ax, key, ylabel in zip(axes, ["fig7a", "fig7b", "fig7c", "fig7d"], labels):
        ax.plot(data[key]["step"], data[key]["value"], color=PALETTE["purple"])
        ax.set_ylabel(ylabel)
    for ax in axes[2:]:
        ax.set_xlabel("Training steps")
    fit_height(fig, axes)
    save(fig, "fig7")


fig1()
ablation("fig2", ["fig2a", "fig2b"], ["Accuracy on AIME", "Entropy of actor model"],
         ["AIME avg@32", "Generation entropy"],
         "w/ Clip-Higher", "w/o Clip-Higher", noisy=(False, True))
fig3()
ablation("fig4", ["fig4a", "fig4b"],
         ["Entropy of generation probabilities", "Average response length"],
         ["Generation entropy", "Mean response length"],
         "w/ token-level loss", "w/o token-level loss", noisy=(True, True))
ablation("fig5", ["fig5a", "fig5b"], ["Performance on AIME", "Entropy of actor model"],
         ["AIME avg@32", "Generation entropy"],
         "w/ overlong filtering", "w/o overlong filtering", noisy=(False, True),
         ours_color="cyan", other_color="purple")
fig6()
fig7()
