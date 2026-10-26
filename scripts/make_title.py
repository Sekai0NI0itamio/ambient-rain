#!/usr/bin/env python3
"""Render the title card at 4K.

Rendered at 3840x2160 and downscaled to 1080p at composite time: the text is
supersampled, so edges stay clean instead of the stair-stepping you get when a
1080p raster is laid over 1080p video.

Usage: python3 scripts/make_title.py [--title "..."] [--sub "..."] [--out path]
"""
import argparse

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 3840, 2160
S = W / 1920.0  # every 1080p measurement below is multiplied by this

DIDOT = "/System/Library/Fonts/Didot.ttc"
AVENIR = "/System/Library/Fonts/Avenir Next.ttc"


def tracked(draw, xy, text, font, tracking=0, fill=(255, 255, 255, 255)):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def tracked_w(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", default="Rain in the Forest")
    ap.add_argument("--sub", default="by Ambient Rain")
    ap.add_argument("--out", default="assets/title.png")
    a = ap.parse_args()

    didot = ImageFont.truetype(DIDOT, int(76 * S), index=0)
    avenir = ImageFont.truetype(AVENIR, int(26 * S), index=0)
    t_track, s_track = 2 * S, 7 * S

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    measure = ImageDraw.Draw(img)
    tw = tracked_w(measure, a.title, didot, t_track)
    sw = tracked_w(measure, a.sub, avenir, s_track)
    tx, ty = (W - tw) / 2, 452 * S
    sx, sy = (W - sw) / 2, 566 * S

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    tracked(ds, (tx, ty), a.title, didot, t_track, (0, 0, 0, 110))
    tracked(ds, (sx, sy), a.sub, avenir, s_track, (0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6 * S))
    img = Image.alpha_composite(img, shadow)

    d = ImageDraw.Draw(img)
    tracked(d, (tx, ty), a.title, didot, t_track, (255, 255, 255, 255))
    tracked(d, (sx, sy), a.sub, avenir, s_track, (255, 255, 255, 215))

    img.save(a.out)
    print(f"{a.out}: {img.size[0]}x{img.size[1]}  title {int(tw)}px wide, centred at x={int(tx + tw / 2)}")


if __name__ == "__main__":
    main()
