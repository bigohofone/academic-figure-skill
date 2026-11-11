"""Color-blind and grayscale safety: greys and part colors spread in lightness, and color helpers."""
import numpy as np
from matplotlib import colors

from . import design


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


def _grey_of_lightness(lightness):
    y = ((lightness + 16) / 116) ** 3
    c = 12.92 * y if y <= 0.0031308 else 1.055 * y ** (1 / 2.4) - 0.055
    return (c, c, c)


def baseline_greys(n):
    """n grey fills, evenly spaced in lightness from the design's neutral-light to neutral-dark, light to
    dark, skipping the band around ours' lightness; one series takes neutral."""
    neutral, light, dark = (design.colors[k] for k in ("neutral", "neutral-light", "neutral-dark"))
    if n == 1:
        return [tuple(colors.to_rgb(neutral))]
    top, bottom, ours = _lightness(light), _lightness(dark), _lightness(design.colors["ours"])
    segments = [(top, min(top, ours + GREY_GAP)), (max(bottom, ours - GREY_GAP), bottom)]
    segments = [(a, b) for a, b in segments if a > b]
    total = sum(a - b for a, b in segments)
    out = []
    for i in range(n):
        t = total * i / (n - 1)
        for a, b in segments:
            if t <= a - b + 1e-9:
                out.append(_grey_of_lightness(a - t))
                break
            t -= a - b
    return out


def part_colors(n):
    """n colors for the parts of one whole (bands, wedges, segments), in stacking order: the palette's
    hues, each moved to its own lightness, evenly spread from dark to light and alternating, so every
    two parts stay apart when printed in black and white."""
    hues = [colors.to_rgb(design.colors[k]) for k in ("series-1", "series-4", "series-6", "series-5", "series-3", "series-2")]
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


def text_color_on(fill):
    """Black or white, whichever reads on `fill`: for numbers written on bars, wedges, areas or heatmap cells."""
    return "white" if np.dot(colors.to_rgb(fill), [0.299, 0.587, 0.114]) < 0.5 else "black"


def lighten(color):
    """`color` mixed with white, 40% color: a box or violin fill, so the black median and points on it stay readable."""
    return [0.4 * c + 0.6 for c in colors.to_rgb(color)]
