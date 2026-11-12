"""Color-blind and grayscale safety: greys and part colors spread in lightness, and color helpers."""
import colorsys

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


def _at_lightness(rgb, target):
    """`rgb` mixed with white or black until its lightness is `target`."""
    toward = np.ones(3) if _lightness(rgb) < target else np.zeros(3)
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if (_lightness(tuple(np.array(rgb) * (1 - mid) + toward * mid)) < target) == (toward[0] == 1):
            lo = mid
        else:
            hi = mid
    return tuple(np.array(rgb) * (1 - lo) + toward * lo)


def ramp(color, n):
    """n shades of one hue for a sweep inside one group (depths, sizes, batch sizes), light to dark,
    evenly spread in lightness from L* 70 to 25, so neighbours stay apart in grayscale and the lightest still
    reads as a thin line on white. Each shade keeps the hue and its saturation (HLS lightness changes, not a
    mix with black), so the dark end stays a deep color rather than grey; a grey gives greys."""
    h, _, sat = colorsys.rgb_to_hls(*colors.to_rgb(color))
    if sat > 0.1:
        sat = max(sat, 0.65)  # a muted palette color still gives a vivid dark end
    else:
        sat = 0.0  # a grey has no hue to keep (colorsys reports hue 0, red)
    levels = np.linspace(70, 25, n) if n > 1 else [_lightness(color)]
    out = []
    for target in levels:
        lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if _lightness(colorsys.hls_to_rgb(h, mid, sat)) < target else (lo, mid)
        out.append(colorsys.hls_to_rgb(h, (lo + hi) / 2, sat))
    return out


def part_colors(n):
    """n colors for the parts of one whole (bands, wedges, segments), in stacking order: the palette's
    hues, each moved to its own lightness, evenly spread from dark to light and alternating, so every
    two parts stay apart when printed in black and white."""
    hues = [colors.to_rgb(design.colors[k]) for k in ("series-1", "series-4", "series-6", "series-5", "series-3", "series-2")]
    levels = list(np.linspace(34, 88, n)) if n > 1 else [50]
    order = [levels.pop(0) if i % 2 == 0 else levels.pop() for i in range(n)]  # dark, light, dark, light, ...
    return [_at_lightness(hue, target) for hue, target in zip(hues, order)]


def darken(color):
    """`color` darkened to 80%: for text or edges that belong to a series, so they read on white."""
    return [c * 0.8 for c in colors.to_rgb(color)]


def text_color_on(fill):
    """Black or white, whichever reads on `fill`: for numbers written on bars, wedges, areas or heatmap cells."""
    return "white" if np.dot(colors.to_rgb(fill), [0.299, 0.587, 0.114]) < 0.5 else "black"


def lighten(color):
    """`color` mixed with white, 40% color: a box or violin fill, so the black median and points on it stay readable."""
    return [0.4 * c + 0.6 for c in colors.to_rgb(color)]
