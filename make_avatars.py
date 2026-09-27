"""Avatar options for 'Ambient Sounds' YouTube channel. 800x800 PNG, circle-safe
(keep art inside central 700px). Flat 2-3 color icons, readable at 98px.
Usage: python3 make_avatars.py && ls -lh avatars/
"""
from PIL import Image, ImageDraw

S = 800
NAVY = (18, 24, 46)
INK = (10, 14, 30)
CREAM = (235, 230, 215)
MOON = (240, 234, 210)
RAIN = (125, 180, 220)
TEAL = (32, 70, 90)
SAGE = (52, 84, 78)

BG = {"v1_moon_rain": NAVY, "v2_monogram": TEAL, "v3_cloud": INK}


def base(name):
    img = Image.new("RGB", (S, S), BG[name])
    return img, ImageDraw.Draw(img)


def v1_moon_rain():
    img, d = base("v1_moon_rain")
    cx, cy, r = 400, 330, 150
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MOON)
    d.ellipse([cx - r + 55, cy - r - 25, cx + r + 55, cy + r - 25], fill=NAVY)
    for sx, sy in [(180, 150), (640, 200), (590, 600), (200, 620)]:
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=CREAM)
    for i, x in enumerate([300, 360, 420, 480]):
        y0 = 520 + (i % 2) * 22
        d.line([x, y0, x - 22, y0 + 60], fill=RAIN, width=14)
    img.save("avatars/v1_moon_rain.png")


def v2_monogram():
    img, d = base("v2_monogram")
    d.ellipse([70, 70, 730, 730], outline=CREAM, width=10)
    d.text((400, 400), "AS", fill=CREAM, font_size=330, anchor="mm")
    d.line([250, 620, 220, 672], fill=RAIN, width=12)
    d.line([400, 620, 370, 672], fill=RAIN, width=12)
    d.line([550, 620, 520, 672], fill=RAIN, width=12)
    img.save("avatars/v2_monogram.png")


def v3_cloud():
    img, d = base("v3_cloud")
    d.ellipse([230, 300, 430, 470], fill=CREAM)
    d.ellipse([340, 260, 540, 430], fill=CREAM)
    d.ellipse([450, 310, 610, 460], fill=CREAM)
    d.rectangle([230, 380, 610, 470], fill=CREAM)
    for i, x in enumerate([320, 390, 460, 530]):
        y0 = 520 + (i % 2) * 20
        d.line([x, y0, x - 20, y0 + 55], fill=RAIN, width=13)
    d.text((400, 640), "z   z", fill=MOON, font_size=72, anchor="mm")
    img.save("avatars/v3_cloud.png")


if __name__ == "__main__":
    v1_moon_rain()
    v2_monogram()
    v3_cloud()
    print("wrote avatars/v1_moon_rain.png v2_monogram.png v3_cloud.png")
