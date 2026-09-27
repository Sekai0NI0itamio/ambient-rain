"""Branded 5s intro card for Ambientful Ambient Sounds.

Renders 150 frames with PIL (icon fade-in, name, tagline, subscribe pill
slide-up, like/share, global fade-out), then encodes with ffmpeg. No ffmpeg
text filters needed, so it behaves identically on laptop and runner.
Usage:
  python3 scripts/make_intro.py --out intro.mp4 --icon avatars/v1_moon_rain.png
Drop your own avatar at avatars/icon.png and pass --icon avatars/icon.png.
"""
import argparse
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

INK = (10, 14, 30)
CREAM = (235, 230, 215)
MOON = (240, 234, 210)
RAIN = (125, 180, 220)
RED = (200, 30, 30)

FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # runner (apt fonts-dejavu-core)
    "/System/Library/Fonts/Helvetica.ttc",                   # macOS
    "/Library/Fonts/Arial Bold.ttf",
]


def pick_font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def fade(t, t0, t1):
    if t <= t0:
        return 0.0
    if t >= t1:
        return 1.0
    return (t - t0) / (t1 - t0)


def text_layer(w, h, s, pos, anchor="mm", color=CREAM, alpha=255):
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text(pos, s, font=pick_font(int(h * 0.075) if anchor == "big" else 36),
           fill=color + (int(alpha * 255),), anchor="mm")
    return layer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="intro.mp4")
    ap.add_argument("--icon", default="avatars/v1_moon_rain.png")
    ap.add_argument("--name", default="Ambientful Ambient Sounds")
    ap.add_argument("--tagline", default="sleep  •  study  •  work")
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--duration", type=float, default=5.0)
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()

    w = 1280 if a.height == 720 else 1920
    h = a.height
    frames = int(a.duration * a.fps)
    tmp = tempfile.mkdtemp()

    icon = Image.open(a.icon).convert("RGBA").resize((220, 220))
    name_f = pick_font(int(h * 0.075))
    tag_f = pick_font(int(h * 0.042))
    sub_f = pick_font(int(h * 0.05))
    small_f = pick_font(int(h * 0.032))

    for i in range(frames):
        t = i / a.fps
        img = Image.new("RGBA", (w, h), INK + (255,))
        d = ImageDraw.Draw(img)
        for x in range(0, w, 46):
            d.line([x, 0, x - 18, h], fill=RAIN + (28,))
        a_icon = fade(t, 0.0, 0.8)
        if a_icon > 0:
            ic = icon.copy()
            px = ic.load()
            # cheap global alpha: composite via alpha scaling
            alpha = ic.split()[3].point(lambda v: int(v * a_icon))
            ic.putalpha(alpha)
            img.alpha_composite(ic, (w // 2 - 110, int(h * 0.13)))

        def stamped(s, font, y, color, a_in, a_full):
            al = fade(t, a_in, a_full)
            if al <= 0:
                return
            tw = d.textlength(s, font=font)
            layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ImageDraw.Draw(layer).text((w / 2, y), s, font=font,
                                       fill=color + (int(al * 255),), anchor="mm")
            img.alpha_composite(layer)

        stamped(a.name, name_f, int(h * 0.55), CREAM, 0.3, 1.1)
        stamped(a.tagline, tag_f, int(h * 0.65), RAIN, 1.0, 1.8)

        slide = fade(t, 1.6, 2.2)
        if slide > 0:
            pw, ph = 380, int(h * 0.11)
            py = int(h * 0.76 + (1 - slide) * 120)
            pill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            pd = ImageDraw.Draw(pill)
            pd.rounded_rectangle([w / 2 - pw / 2, py, w / 2 + pw / 2, py + ph],
                                radius=ph // 3, fill=RED + (int(slide * 255),))
            pd.text((w / 2, py + ph / 2), "SUBSCRIBE", font=sub_f,
                    fill=(255, 255, 255, int(slide * 255)), anchor="mm")
            img.alpha_composite(pill)

        stamped("LIKE  &  SHARE", small_f, int(h * 0.90), CREAM, 2.2, 2.8)

        out_f = fade(t, a.duration - 0.8, a.duration)
        if out_f < 1:
            img = Image.blend(Image.new("RGBA", (w, h), (0, 0, 0, 255)), img, out_f)
        img.convert("RGB").save(f"{tmp}/f{i:04d}.png")

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(a.fps), "-i", f"{tmp}/f%04d.png",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-pix_fmt", "yuv420p", "-an", a.out,
    ], check=True)
    print(f"[intro] wrote {a.out} ({a.duration}s, {w}x{h})")


if __name__ == "__main__":
    main()
