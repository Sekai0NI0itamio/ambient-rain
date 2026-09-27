"""Transparent subscribe-overlay TEMPLATE as PNG sequence (RGBA + alpha).

A lower-third card that slides in over ANY footage: channel icon + name +
red SUBSCRIBE pill, holds, slides out. PNG sequences carry real transparency
everywhere (our pipeline, CapCut, Premiere, DaVinci) — no alpha-codec needed.
Usage:
  python3 scripts/make_overlay.py --outdir overlay_frames --icon avatars/v1_moon_rain.png
  python3 scripts/apply_overlay.py --video preview_woods.mp4 --frames overlay_frames --out preview_ov.mp4
"""
import argparse
import json
import os

from PIL import Image, ImageDraw

from make_intro import pick_font, fade, INK, CREAM, RAIN, RED  # noqa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="overlay_frames")
    ap.add_argument("--icon", default="avatars/v1_moon_rain.png")
    ap.add_argument("--name", default="Ambientful Ambient Sounds")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--duration", type=float, default=6.0)
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()

    w, h = a.width, a.height
    frames = int(a.duration * a.fps)
    os.makedirs(a.outdir, exist_ok=True)
    icon = Image.open(a.icon).convert("RGBA").resize((120, 120))
    name_f = pick_font(44)
    sub_f = pick_font(34)

    cw, chh = 640, 170
    for i in range(frames):
        t = i / a.fps
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        slide = fade(t, 0.5, 1.2) - fade(t, a.duration - 0.8, a.duration - 0.1)
        if slide > 0:
            x1 = int(w - cw - 60 - (1 - slide) * (cw + 120))
            y1 = h - chh - 90
            card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            d = ImageDraw.Draw(card)
            al = int(210 * slide)
            d.rounded_rectangle([x1, y1, x1 + cw, y1 + chh], radius=28,
                                fill=(10, 14, 30, al))
            card.alpha_composite(icon, (x1 + 22, y1 + 25))
            d.text((x1 + 158, y1 + 52), a.name, font=name_f,
                   fill=CREAM + (int(255 * slide),))
            d.rounded_rectangle([x1 + 158, y1 + 100, x1 + 380, y1 + 145], radius=14,
                                fill=RED + (int(255 * slide),))
            d.text((x1 + 269, y1 + 122), "SUBSCRIBE", font=sub_f,
                   fill=(255, 255, 255, int(255 * slide),), anchor="mm")
            img.alpha_composite(card)
        img.save(f"{a.outdir}/f{i:04d}.png")

    with open(f"{a.outdir}/manifest.json", "w") as fh:
        json.dump({"fps": a.fps, "frames": frames, "width": w, "height": h,
                   "duration": a.duration}, fh)
    print(f"[overlay] wrote {frames} frames to {a.outdir}/ (+ manifest.json)")


if __name__ == "__main__":
    main()
