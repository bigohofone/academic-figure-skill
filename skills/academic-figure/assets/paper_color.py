"""Color-blind and grayscale safety: greys and part colors spread in lightness, color helpers, and the
check that series stay apart when printed in black and white."""
import warnings

import numpy as np
from matplotlib import colors
from matplotlib.collections import PolyCollection
from matplotlib.container import BarContainer
from matplotlib.patches import Rectangle

import paper


GREY_GAP = 12  # L* kept clear on each side of ours, so ours stays apart in grayscale


def _lightness(color):
    """CIE L* (0 black to 100 white): how light a color prints in grayscale."""
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in colors.to_rgb(color)]
    y = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    return 116 * y ** (1 / 3) - 16 if y > 0.008856 else 903.3 * y


def _over_white(rgba):
    """A translucent color as it looks over the white page."""
    r, g, b, alpha = colors.to_rgba(rgba)
    return tuple(alpha * c + (1 - alpha) for c in (r, g, b))


def _grey(lightness):
    y = ((lightness + 16) / 116) ** 3
    c = 12.92 * y if y <= 0.0031308 else 1.055 * y ** (1 / 2.4) - 0.055
    return (c, c, c)


def greys(n):
    """n grey fills, evenly spaced in lightness from the design's neutral-light to neutral-dark, light to
    dark, skipping the band around ours' lightness; one series takes neutral."""
    neutral, light, dark = paper._greys
    if n == 1:
        return [tuple(colors.to_rgb(neutral))]
    top, bottom, ours = _lightness(light), _lightness(dark), _lightness(paper._ours)
    segments = [(top, min(top, ours + GREY_GAP)), (max(bottom, ours - GREY_GAP), bottom)]
    segments = [(a, b) for a, b in segments if a > b]
    total = sum(a - b for a, b in segments)
    out = []
    for i in range(n):
        t = total * i / (n - 1)
        for a, b in segments:
            if t <= a - b + 1e-9:
                out.append(_grey(a - t))
                break
            t -= a - b
    return out


def parts(n):
    """n colors for the parts of one whole (bands, wedges, segments), in stacking order: the palette's
    hues, each moved to its own lightness, evenly spread from dark to light and alternating, so every
    two parts stay apart when printed in black and white."""
    hues = [colors.to_rgb(paper._palette[k]) for k in ("series-1", "series-4", "series-6", "series-5", "series-3", "series-2")]
    levels = list(np.linspace(34, 88, n)) if n > 1 else [50]
    order = [levels.pop(0) if i % 2 == 0 else levels.pop() for i in range(n)]  # dark, light, dark, light, ...
    out = []
    for hue, target in zip(hues, order):
        toward = np.ones(3) if _lightness(hue) < target else np.zeros(3)
        lo, hi = 0.0, 1.0
        for _ in range(30):  # mix with white or black until the lightness hits the target
            mid = (lo + hi) / 2
            if (_lightness(tuple(np.array(hue) * (1 - mid) + toward * mid)) < target) == (toward[0] == 1):
                lo = mid
            else:
                hi = mid
        out.append(tuple(np.array(hue) * (1 - lo) + toward * lo))
    return out


def darken(color):
    """`color` darkened to 80%: for text or edges that belong to a series, so they read on white."""
    return [c * 0.8 for c in colors.to_rgb(color)]


def text_color(fill):
    """Black or white, whichever reads on `fill`: for numbers written on bars, wedges, areas or heatmap cells."""
    return "white" if np.dot(colors.to_rgb(fill), [0.299, 0.587, 0.114]) < 0.5 else "black"


def lighten(color):
    """`color` mixed with white, 40% color: a box or violin fill, so the black median and points on it stay readable."""
    return [0.4 * c + 0.6 for c in colors.to_rgb(color)]


def _warn_grayscale(a):
    """Series told apart by color alone (lines of one style and marker, or bars) must differ in lightness,
    or they merge when printed in black and white."""
    groups = {}
    for line in a.get_lines():
        if not line.get_label().startswith("_"):
            key = ("line", str(line.get_linestyle()), str(line.get_marker()))
            groups.setdefault(key, []).append((line.get_label(), line.get_color()))
    for c in a.containers:
        if isinstance(c, BarContainer) and c.patches and not str(c.get_label()).startswith("_"):
            groups.setdefault(("bar",), []).append((c.get_label(), _over_white(c.patches[0].get_facecolor())))
    # histograms (step outlines or filled shapes) and labelled bands, translucent fills as seen over white
    for p in a.patches:
        label = p.get_label() or ""
        if not isinstance(p, Rectangle) and label and not label.startswith("_"):
            color = _over_white(p.get_facecolor()) if p.get_fill() else p.get_edgecolor()
            groups.setdefault(("fill",), []).append((label, color))
    for c in a.collections:
        label = c.get_label() or ""
        if isinstance(c, PolyCollection) and label and not label.startswith("_") and len(c.get_facecolor()):
            groups.setdefault(("fill",), []).append((label, _over_white(c.get_facecolor()[0])))
    for series in groups.values():
        for i in range(len(series)):
            for j in range(i + 1, len(series)):
                (n1, c1), (n2, c2) = series[i], series[j]
                if abs(_lightness(c1) - _lightness(c2)) < 10:
                    warnings.warn(f"series {n1!r} and {n2!r} look alike in grayscale in panel {a.get_title()!r} "
                                  f"(L* {_lightness(c1):.0f} vs {_lightness(c2):.0f}); use greys(n), or tell them "
                                  "apart by line style or marker (DESIGN.md Colors)")
