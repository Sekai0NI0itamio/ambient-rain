"""Channel art for 'Ambientful Ambient Sounds' — matches the cloud-rain avatar.
- banner.png: 2560x1440 (TV), key content inside central 1546x423 safe area.
- watermark.png: 150x150 transparent, subtle cloud mark for video corner.
Usage: python3 make_channel_art.py
"""
from PIL import Image, ImageDraw

INK = (10, 14, 30)
NAVY = (18, 24, 46)
CREAM = (235, 230, 215)
RAIN = (125, 180, 220)


def banner():
    W, H = 2560, 1440
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    import random
    rng = random.Random(11)
    for _ in range(90):
        x = rng.randint(0, W)
        y = rng.randint(0, H)
        d.line([x, y, x - 14, y + 42], fill=RAIN, width=4)
    d.ellipse([1690, 330, 1970, 580], fill=CREAM)
    d.ellipse([1830, 270, 2110, 520], fill=CREAM)
    d.ellipse([1950, 340, 2160, 520], fill=CREAM)
    d.rectangle([1690, 450, 2160, 580], fill=CREAM)
    for i, x in enumerate([1780, 1870, 1960, 2050]):
        y0 = 640 + (i % 2) * 26
        d.line([x, y0, x - 26, y0 + 80], fill=RAIN, width=12)
    d.text((330, 560), "Ambientful Ambient Sounds", fill=CREAM,
           font_size=130, anchor="lm")
    d.text((335, 700), "sleep  •  study  •  work", fill=RAIN,
           font_size=64, anchor="lm")
    img.save("avatars/banner.png")


def watermark():
    S = 150
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([30, 42, 75, 82], outline=(235, 230, 215, 220), width=5)
    d.ellipse([58, 30, 103, 70], outline=(235, 230, 215, 220), width=5)
    d.ellipse([86, 45, 122, 78], outline=(235, 230, 215, 220), width=5)
    for x in [55, 75, 95]:
        d.line([x, 95, x - 6, 118], fill=(125, 180, 220, 220), width=5)
    img.save("avatars/watermark.png")


if __name__ == "__main__":
    banner()
    watermark()
    print("wrote avatars/banner.png avatars/watermark.png")
