"""Color-blind and grayscale safety: greys and part colors spread in lightness, and color helpers."""
import colorsys

import numpy as np
from matplotlib import colors

from . import design


STOP = 12  # L* one stop moves: two series this far apart stay apart printed in black and white
LIGHTEST, DARKEST = 80, 25  # L* range of make_shades: the lightest still reads as a thin line on white


def _lightness(color):
    """CIE L* (0 black to 100 white): how light a color prints in grayscale."""
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in colors.to_rgb(color)]
    y = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    return 116 * y ** (1 / 3) - 16 if y > 0.008856 else 903.3 * y


def _over_white(rgba):
    """A translucent color as it looks over the white page."""
    r, g, b, alpha = colors.to_rgba(rgba)
    return tuple(alpha * c + (1 - alpha) for c in (r, g, b))


def _hue_and_saturation(color):
    h, _, sat = colorsys.rgb_to_hls(*colors.to_rgb(color))
    return h, (sat if sat > 0.1 else 0.0)  # a grey has no hue to keep (colorsys reports hue 0, red)


def _at_hls_lightness(h, sat, target):
    """The color of hue `h` and saturation `sat` whose grayscale lightness is `target` L*."""
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _lightness(colorsys.hls_to_rgb(h, mid, sat)) < target else (lo, mid)
    return colorsys.hls_to_rgb(h, (lo + hi) / 2, sat)


def shift_lightness(color, stops):
    """`color` lighter (stops > 0) or darker (stops < 0), like an exposure dial: each stop moves its
    grayscale lightness by STOP L*, keeping hue and saturation. -1: series text and edges on white;
    +2: box and violin fills, light enough for the black median on them."""
    h, sat = _hue_and_saturation(color)
    return _at_hls_lightness(h, sat, min(100, max(0, _lightness(color) + STOP * stops)))


def make_shades(color, n):
    """n shades of `color`, light to dark, evenly spread in grayscale lightness from LIGHTEST to DARKEST:
    a sweep inside one group (depths, sizes), or greys for n compared series. Greys skip the band around
    ours' lightness, so ours stays apart in grayscale. One shade: `color` itself."""
    if n == 1:
        return [tuple(colors.to_rgb(color))]
    h, sat = _hue_and_saturation(color)
    if sat:
        sat = max(sat, 0.65)  # a muted palette color still gives a vivid dark end
    segments = [(LIGHTEST, DARKEST)]
    if not sat:
        ours = _lightness(design.colors["ours"])
        segments = [(a, b) for a, b in [(LIGHTEST, min(LIGHTEST, ours + STOP)), (max(DARKEST, ours - STOP), DARKEST)] if a > b]
    total = sum(a - b for a, b in segments)
    out = []
    for i in range(n):
        t = total * i / (n - 1)
        for a, b in segments:
            if t <= a - b + 1e-9:
                out.append(_at_hls_lightness(h, sat, a - t))
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


def make_part_colors(n):
    """n colors for the parts of one whole (bands, wedges, segments), in stacking order: the palette's
    hues, each moved to its own lightness, evenly spread from dark to light and alternating, so every
    two parts stay apart when printed in black and white."""
    hues = [colors.to_rgb(design.colors[k]) for k in ("series-1", "series-4", "series-6", "series-5", "series-3", "series-2")]
    levels = list(np.linspace(34, 88, n)) if n > 1 else [50]
    order = [levels.pop(0) if i % 2 == 0 else levels.pop() for i in range(n)]  # dark, light, dark, light, ...
    return [_at_lightness(hue, target) for hue, target in zip(hues, order)]
