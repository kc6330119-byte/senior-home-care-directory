#!/usr/bin/env python3
"""Generate favicon.ico for seniorhomecarefinder.com.

Output: static/favicon.ico (multi-size: 16, 32, 48, 64)

Brand mark — the same simple house silhouette that appears in base.html's
inline SVG favicon, rendered as a transparent-background ICO so the legacy
/favicon.ico path also returns a real icon (fixes the 404).
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUTPUT = Path(__file__).resolve().parent.parent / "static" / "favicon.ico"

PRIMARY = (30, 77, 140, 255)     # #1E4D8C
WHITE = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)


def make_mark(size):
    """Render the SHCF house mark on a rounded primary-blue square."""
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    radius = size // 6
    try:
        draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=PRIMARY)
    except AttributeError:
        draw.rectangle([0, 0, size - 1, size - 1], fill=PRIMARY)

    # House silhouette — same path data as the inline SVG (viewBox 32x32).
    s = size / 32
    peak = (16 * s, 9 * s)
    left_eave = (9 * s, 14 * s)
    right_eave = (23 * s, 14 * s)
    body = [
        left_eave,
        (9 * s, 22 * s),
        (13 * s, 22 * s),
        (13 * s, 16 * s),
        (19 * s, 16 * s),
        (19 * s, 22 * s),
        (23 * s, 22 * s),
        right_eave,
    ]
    silhouette = [peak] + body
    draw.polygon(silhouette, fill=WHITE)
    return img


def main():
    sizes = [16, 32, 48, 64]
    img = make_mark(max(sizes))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, format="ICO", sizes=[(s, s) for s in sizes])
    print(f"Wrote {OUTPUT}  ({OUTPUT.stat().st_size} bytes, sizes={sizes})")


if __name__ == "__main__":
    main()
