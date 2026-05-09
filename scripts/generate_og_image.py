#!/usr/bin/env python3
"""Generate the Open Graph share image for seniorhomecarefinder.com.

Output: static/images/og-image.png (1200x630, PNG)

The image is checked into the repo and served from /static/images/og-image.png.
Rerun this script if the brand text or palette changes. Pure PIL — no external assets.

Palette is the SHCF healthcare-native theme:
  primary  #1E4D8C (deep trustworthy blue)
  text     #1A2332 (deep navy-black)
  accent   #D97706 (gold-leaf amber)
  bg       #FAF9F6 (warm off-white)
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630
OUTPUT = Path(__file__).resolve().parent.parent / "static" / "images" / "og-image.png"

PRIMARY = (30, 77, 140)        # #1E4D8C
PRIMARY_DARK = (20, 54, 100)   # darker shade for gradient bottom
TEXT_DARK = (26, 35, 50)       # #1A2332
ACCENT = (217, 119, 6)         # #D97706 — used sparingly
WARM_BG = (250, 249, 246)      # #FAF9F6
WHITE = (255, 255, 255)
INK_85 = (221, 228, 238)       # 85% white on primary blue (matches site's --color-primary-ink-85)

WORDMARK = "Senior Home Care Finder"
TAGLINE = "Find Trusted Home Care Agencies"
DOMAIN = "seniorhomecarefinder.com"


def gradient_background():
    img = Image.new("RGB", (WIDTH, HEIGHT), PRIMARY)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(PRIMARY[0] + (PRIMARY_DARK[0] - PRIMARY[0]) * t)
        g = int(PRIMARY[1] + (PRIMARY_DARK[1] - PRIMARY[1]) * t)
        b = int(PRIMARY[2] + (PRIMARY_DARK[2] - PRIMARY[2]) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_house_mark(draw, cx, cy, size):
    """Render the SHCF house mark (matches the inline SVG in base.html).

    Path data from base.html:
        M9 22 V14 l7-5 7 5 v8 h-4 v-6 h-6 v6 H9 z
    Drawn into a `size`-wide square centered at (cx, cy).
    """
    # Background rounded square
    radius = size // 6
    sq = [cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2]
    # PIL's rounded_rectangle requires Pillow 8.2+ — fall back to ellipse-bordered rectangle.
    try:
        draw.rounded_rectangle(sq, radius=radius, fill=WHITE)
    except AttributeError:
        draw.rectangle(sq, fill=WHITE)

    # Map the SVG viewBox 32x32 path to our square. Original path covers x:5-23, y:9-22.
    # Scale and center.
    s = size / 32  # 1 SVG unit = s pixels
    x0 = cx - size // 2
    y0 = cy - size // 2

    # Roof (triangle from peak (16,9) over to (9,14) and (23,14))
    peak = (x0 + 16 * s, y0 + 9 * s)
    left_eave = (x0 + 9 * s, y0 + 14 * s)
    right_eave = (x0 + 23 * s, y0 + 14 * s)
    # House body silhouette: 9,14 → 9,22 → 13,22 → 13,16 → 19,16 → 19,22 → 23,22 → 23,14
    body = [
        left_eave,
        (x0 + 9 * s, y0 + 22 * s),
        (x0 + 13 * s, y0 + 22 * s),
        (x0 + 13 * s, y0 + 16 * s),
        (x0 + 19 * s, y0 + 16 * s),
        (x0 + 19 * s, y0 + 22 * s),
        (x0 + 23 * s, y0 + 22 * s),
        right_eave,
    ]
    # Combine roof peak with body to get the closed silhouette
    silhouette = [peak] + body
    draw.polygon(silhouette, fill=PRIMARY)


def main():
    img = gradient_background()
    draw = ImageDraw.Draw(img)

    title_font = load_font(72, bold=True)
    tagline_font = load_font(38)
    domain_font = load_font(28)

    # House mark — left-aligned, vertically centered with the wordmark block
    mark_size = 120
    mark_cx, mark_cy = 110, 260
    draw_house_mark(draw, mark_cx, mark_cy, mark_size)

    # Wordmark — to the right of the mark
    wm_x = mark_cx + mark_size // 2 + 32
    wm_y = mark_cy - 52
    draw.text((wm_x, wm_y), WORDMARK, fill=WHITE, font=title_font)

    # Tagline — under wordmark
    tag_y = wm_y + 100
    draw.text((wm_x, tag_y), TAGLINE, fill=INK_85, font=tagline_font)

    # Amber accent rule — short bar under the tagline, brand-aligned
    rule_y = tag_y + 68
    draw.rectangle([wm_x, rule_y, wm_x + 80, rule_y + 6], fill=ACCENT)

    # Domain — bottom right
    dom_w = draw.textlength(DOMAIN, font=domain_font)
    draw.text((WIDTH - dom_w - 56, HEIGHT - 64), DOMAIN, fill=INK_85, font=domain_font)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Wrote {OUTPUT}  ({OUTPUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
