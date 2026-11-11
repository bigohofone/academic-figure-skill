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


# the tokens the other modules and the scripts use, all set by apply_design()
colors = {}  # the colors tokens by name: colors["ours"], colors["neutral"], ...
dashed_width = None  # the dashed-line width; pass it to dashed and dotted lines
highlight_size = None  # the marker highlight-size, for a point of interest
filled_edge_width = None  # the marker filled-edge-width, for filled markers
canvas_pad = None  # inches of free space at each edge of the canvas
panel_gap = None  # inches of free space between a panel and the next one's y labels
contour_label_size = bar_label_size = legend_inside_size = None  # points
colorbar_width = colorbar_gap = None  # inches


def _resolve_token_refs(value, tokens):
    """Replace token references such as "{colors.series-2}" with the value they point to."""
    if isinstance(value, dict):
        return {k: _resolve_token_refs(v, tokens) for k, v in value.items()}
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        target = tokens
        for key in value[1:-1].split("."):
            target = target[key]
        return _resolve_token_refs(target, tokens)
    return value


def _points(value):
    """A token dimension ("3pt", "0.025in") in points, the unit matplotlib takes for sizes and pads."""
    number = float(str(value).rstrip("ptin"))
    return number * 72 if str(value).endswith("in") else number


def _inches(value):
    """A token dimension ("0.05in", "2pt") in inches, the unit of the canvas and the colorbar."""
    return _points(value) / 72


def apply_design(path="DESIGN.md"):
    """Set matplotlib's style from paper.mplstyle and the tokens in the front matter of `path`, a DESIGN.md.
    Returns the colors by name, e.g. colors["series-1"], colors["ours"]."""
    global colors, dashed_width, highlight_size, filled_edge_width, canvas_pad, panel_gap, colorbar_width, colorbar_gap, contour_label_size, bar_label_size, legend_inside_size
    # one renderer everywhere: screen backends measure text differently, so finalize_figure's layout and
    # checks would differ from what Agg saves; the scripts write files and never open a window
    matplotlib.use("agg", force=True)
    tokens = yaml.safe_load(Path(path).read_text().split("---")[1])
    tokens = _resolve_token_refs(tokens, tokens)
    c, t, s, k = tokens["colors"], tokens["typography"], tokens["spacing"], tokens["components"]
    colors = c
    matplotlib.style.use(Path(__file__).parent / "paper.mplstyle")
    contour_label_size = _points(t["contour-label"]["fontSize"])
    bar_label_size = _points(t["bar-label"]["fontSize"])
    legend_inside_size = _points(t["legend-inside"]["fontSize"])
    label, tick_label, legend, value_label, title = (
        _points(t[name]["fontSize"]) for name in ("label", "tick-label", "legend", "value-label", "title"))
    tick_pad, tick_width = _points(s["tick-pad"]), _points(k["tick"]["width"])
    rcParams.update({
        "font.sans-serif": [t["label"]["fontFamily"]],
        "font.size": value_label, "axes.labelsize": label, "figure.labelsize": label, "legend.fontsize": legend,
        "xtick.labelsize": tick_label, "ytick.labelsize": tick_label,
        "axes.titlesize": title, "axes.titleweight": t["title"].get("fontWeight", 400),
        "axes.titlepad": _points(s["title-pad"]), "axes.labelpad": _points(s["label-pad"]),
        "axes.xmargin": float(s["data-margin"].rstrip("%")) / 100, "axes.ymargin": float(s["data-margin"].rstrip("%")) / 100,
        "xtick.major.pad": tick_pad, "xtick.minor.pad": tick_pad, "ytick.major.pad": tick_pad, "ytick.minor.pad": tick_pad,
        "xtick.major.width": tick_width, "xtick.minor.width": tick_width,
        "ytick.major.width": tick_width, "ytick.minor.width": tick_width,
        "xtick.major.size": _points(k["tick"]["size"]), "ytick.major.size": _points(k["tick"]["size"]),
        "xtick.minor.size": _points(k["tick"]["minor-size"]), "ytick.minor.size": _points(k["tick"]["minor-size"]),
        "text.color": c["ink"], "axes.labelcolor": c["ink"], "xtick.color": k["axes"]["textColor"], "ytick.color": k["axes"]["textColor"],
        "xtick.labelcolor": c["ink"], "ytick.labelcolor": c["ink"],
        "axes.edgecolor": k["axes"]["textColor"], "axes.linewidth": _points(k["axes"]["width"]),
        "grid.color": k["grid"]["color"], "grid.alpha": k["grid"]["opacity"], "grid.linewidth": _points(k["grid"]["width"]),
        "lines.linewidth": _points(k["line"]["width"]),
        "lines.markersize": _points(k["marker"]["size"]), "lines.markeredgewidth": _points(k["marker"]["edge-width"]),
        "patch.linewidth": _points(k["outline"]["width"]),
        "boxplot.boxprops.linewidth": _points(k["outline"]["width"]),
        "boxplot.whiskerprops.linewidth": _points(k["outline"]["width"]),
        "boxplot.capprops.linewidth": _points(k["outline"]["width"]),
        "boxplot.medianprops.linewidth": _points(k["median"]["width"]),
        "boxplot.flierprops.markersize": _points(k["marker"]["size"]), "boxplot.flierprops.markeredgewidth": _points(k["marker"]["edge-width"]),
        "contour.linewidth": _points(k["contour"]["width"]),
        "axes.prop_cycle": cycler(color=[v for name, v in c.items() if name.startswith("series-")] + [c["neutral"]]),
        "image.cmap": k["heatmap"]["colormap"],
        "figure.constrained_layout.w_pad": _inches(s["layout-pad"]),
        "figure.constrained_layout.h_pad": _inches(s["layout-pad"]),
    })
    dashed_width = _points(k["dashed-line"]["width"])
    highlight_size = _points(k["marker"]["highlight-size"])
    canvas_pad = _inches(s["canvas-pad"])
    panel_gap = _inches(s["panel-gap"])
    colorbar_width, colorbar_gap = _inches(k["colorbar"]["width"]), _inches(k["colorbar"]["gap"])
    filled_edge_width = _points(k["marker"]["filled-edge-width"])
    return c
