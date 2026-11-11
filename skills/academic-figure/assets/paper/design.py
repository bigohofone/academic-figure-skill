"""The design: reads DESIGN.md's tokens into matplotlib's style and holds the values the other modules use."""
from pathlib import Path

import matplotlib
import matplotlib.style
import yaml
from cycler import cycler
from matplotlib import font_manager, rcParams

# Inter ships with the skill because no environment has it installed; DESIGN.md names it.
for _font in Path(__file__).parent.glob("Inter-*.ttf"):
    font_manager.fontManager.addfont(str(_font))


dashed_width = 0.75  # the dashed-line token, set by use_design(); pass it to dashed and dotted lines
highlight_size = 5  # the marker highlight-size token, set by use_design(); for a point of interest
filled_edge_width = 0.25  # the marker filled-edge-width token, set by use_design(); for filled markers
canvas_pad = 0.1  # the canvas-pad token, in inches, set by use_design(): free space at the left and right edges
contour_label_size = 6.0  # the contour-label token, in points, set by use_design()
bar_label_size = 6.0  # the bar-label token, in points, set by use_design()
_ours = "#EE6677"  # the ours token, set by use_design()
_palette = {}  # the colors tokens, set by use_design()
colorbar_width, colorbar_gap = 0.1, 0.06  # the colorbar tokens, in inches, set by use_design()


def _resolve(value, tokens):
    """Replace token references such as "{colors.series-2}" with the value they point to."""
    if isinstance(value, dict):
        return {k: _resolve(v, tokens) for k, v in value.items()}
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        target = tokens
        for key in value[1:-1].split("."):
            target = target[key]
        return _resolve(target, tokens)
    return value


def _number(value):
    """A token dimension such as "0.5pt" or "0.02in" as a number in its unit."""
    return float(str(value).rstrip("ptin"))


def use_design(path="DESIGN.md"):
    """Set matplotlib's style from paper.mplstyle and the tokens in the front matter of `path`, a DESIGN.md.
    Returns the colors by name, e.g. colors["series-1"], colors["ours"]."""
    global dashed_width, highlight_size, filled_edge_width, canvas_pad, colorbar_width, colorbar_gap, contour_label_size, bar_label_size, _greys, _ours, _palette
    # one renderer everywhere: screen backends measure text differently, so fit_height's layout and
    # checks would differ from what Agg saves; the scripts write files and never open a window
    matplotlib.use("agg", force=True)
    tokens = yaml.safe_load(Path(path).read_text().split("---")[1])
    tokens = _resolve(tokens, tokens)
    c, t, s, k = tokens["colors"], tokens["typography"], tokens["spacing"], tokens["components"]
    _greys = c["neutral"], c["neutral-light"], c["neutral-dark"]
    _ours = c["ours"]
    _palette = c
    matplotlib.style.use(Path(__file__).parent / "paper.mplstyle")
    contour_label_size = _number(t["contour-label"]["fontSize"])
    bar_label_size = _number(t["bar-label"]["fontSize"])
    label, tick_label, legend, value_label, title = (
        _number(t[name]["fontSize"]) for name in ("label", "tick-label", "legend", "value-label", "title"))
    tick_pad, tick_width = _number(s["tick-pad"]), _number(k["tick"]["width"])
    rcParams.update({
        "font.sans-serif": [t["label"]["fontFamily"]],
        "font.size": value_label, "axes.labelsize": label, "figure.labelsize": label, "legend.fontsize": legend,
        "xtick.labelsize": tick_label, "ytick.labelsize": tick_label,
        "axes.titlesize": title, "axes.titleweight": t["title"].get("fontWeight", 400),
        "axes.titlepad": _number(s["title-pad"]), "axes.labelpad": _number(s["label-pad"]),
        "axes.xmargin": _number(s["data-margin"]), "axes.ymargin": _number(s["data-margin"]),
        "xtick.major.pad": tick_pad, "xtick.minor.pad": tick_pad, "ytick.major.pad": tick_pad, "ytick.minor.pad": tick_pad,
        "xtick.major.width": tick_width, "xtick.minor.width": tick_width,
        "ytick.major.width": tick_width, "ytick.minor.width": tick_width,
        "xtick.major.size": _number(k["tick"]["size"]), "ytick.major.size": _number(k["tick"]["size"]),
        "xtick.minor.size": _number(k["tick"]["minor-size"]), "ytick.minor.size": _number(k["tick"]["minor-size"]),
        "text.color": c["ink"], "axes.labelcolor": c["ink"], "xtick.color": c["ink"], "ytick.color": c["ink"],
        "axes.edgecolor": k["axes"]["textColor"], "axes.linewidth": _number(k["axes"]["width"]),
        "grid.color": k["grid"]["color"], "grid.alpha": k["grid"]["opacity"], "grid.linewidth": _number(k["grid"]["width"]),
        "lines.linewidth": _number(k["line"]["width"]),
        "lines.markersize": _number(k["marker"]["size"]), "lines.markeredgewidth": _number(k["marker"]["edge-width"]),
        "patch.linewidth": _number(k["outline"]["width"]),
        "boxplot.boxprops.linewidth": _number(k["outline"]["width"]),
        "boxplot.whiskerprops.linewidth": _number(k["outline"]["width"]),
        "boxplot.capprops.linewidth": _number(k["outline"]["width"]),
        "boxplot.medianprops.linewidth": _number(k["median"]["width"]),
        "boxplot.flierprops.markersize": _number(k["marker"]["size"]), "boxplot.flierprops.markeredgewidth": _number(k["marker"]["edge-width"]),
        "contour.linewidth": _number(k["contour"]["width"]),
        "axes.prop_cycle": cycler(color=[v for name, v in c.items() if name.startswith("series-")] + [c["neutral"]]),
        "image.cmap": k["heatmap"]["colormap"],
        "figure.constrained_layout.w_pad": _number(s["layout-pad"]),
        "figure.constrained_layout.h_pad": _number(s["layout-pad"]),
    })
    dashed_width = _number(k["dashed-line"]["width"])
    highlight_size = _number(k["marker"]["highlight-size"])
    canvas_pad = _number(s["canvas-pad"])
    colorbar_width, colorbar_gap = _number(k["colorbar"]["width"]), _number(k["colorbar"]["gap"])
    filled_edge_width = _number(k["marker"]["filled-edge-width"])
    return c
