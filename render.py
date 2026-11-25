#!/usr/bin/env python3
"""Render the 24 November 2026 world-news poster (1024x1024 PNG).

Run:  python3 render.py            -> writes entry.png beside this file
Uses only Pillow + the DejaVu fonts shipped with most Linux systems.
The graded entrypoint is main.ts, which copies the rendered entry.png
to $MAKEFUN_OUTPUT_DIR/entry.png. This script is kept in the repo so
anyone can regenerate the image from source.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (185, 28, 28)
DARKRED = (127, 29, 29)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
AMBER = (180, 83, 9)
GREEN = (21, 101, 52)
GREY = (87, 83, 78)
LIGHT = (255, 255, 255)
PANEL = (255, 255, 255)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, x, y, label, colour):
    f = font(FB, 21)
    w = int(draw.textlength(label, font=f)) + 22
    draw.rounded_rectangle([x, y, x + w, y + 32], radius=4, fill=colour)
    draw.text((x + 11, y + 4), label, font=f, fill=LIGHT)
    return w


def panel(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=PANEL, outline=(210, 205, 192), width=2)


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # ---- top black bar: the date, unmissable -------------------------------
    d.rectangle([0, 0, W, 62], fill=INK)
    d.text((24, 12), "TUESDAY, 24 NOVEMBER 2026", font=font(FB, 32), fill=LIGHT)
    d.text((W - 24 - d.textlength("ONE DAY  •  ONE IMAGE", font=font(FB, 24)), 18),
           "ONE DAY  •  ONE IMAGE", font=font(FB, 24), fill=(251, 191, 36))

    # ---- masthead ------------------------------------------------------------
    d.text((24, 74), "THE WORLD IN ONE IMAGE", font=font(FB, 58), fill=INK)
    d.text((24, 140), "Seven stories that defined the day — from Hormuz to Seoul.",
           font=font(FR, 24), fill=GREY)
    d.line([24, 178, W - 24, 178], fill=INK, width=3)

    # ---- HERO: Hormuz mines --------------------------------------------------
    x, y, w, h = 24, 192, 976, 218
    panel(d, x, y, w, h)
    d.rounded_rectangle([x, y, x + 320, y + h], radius=10, fill=RED)
    d.rounded_rectangle([x + 300, y, x + 320, y + h], radius=0, fill=RED)
    d.text((x + 26, y + 18), "4", font=font(FB, 100), fill=LIGHT)
    d.text((x + 26, y + 128), "TANKERS", font=font(FB, 44), fill=LIGHT)
    kicker(d, x + 350, y + 18, "WAR  •  STRAIT OF HORMUZ", RED)
    d.text((x + 350, y + 62), "HIT BY MINES",
           font=font(FB, 46), fill=INK)
    text_block(d, x + 350, y + 118,
               "Iran says four tankers hit naval mines and caught fire "
               "Tuesday. The claims are unverified; Tehran warns the "
               "strait will be 'more closed day by day'.",
               font(FR, 23), INK, 600, leading=29)

    # ---- Row 2: Korea | Gaza -------------------------------------------------
    y2, h2 = 426, 218
    # Korea
    x, w = 24, 476
    panel(d, x, y2, w, h2)
    kicker(d, x + 18, y2 + 16, "KOREA  •  AIRSPACE SCARE", DARKRED)
    d.text((x + 18, y2 + 58), "JETS SCRAMBLED", font=font(FB, 40), fill=INK)
    text_block(d, x + 18, y2 + 108,
               "Russian jets enter Seoul's air-defence zone and near "
               "Ulleungdo; a first air-raid alert tells islanders to "
               "shelter — lifted in 3 minutes.",
               font(FR, 21), INK, w - 36, leading=27)
    # Gaza
    x, w = 524, 476
    panel(d, x, y2, w, h2)
    kicker(d, x + 18, y2 + 16, "GAZA", TEAL)
    d.text((x + 18, y2 + 58), "SECURITY CHIEF KILLED", font=font(FB, 30), fill=INK)
    text_block(d, x + 18, y2 + 108,
               "Israeli drone strike kills Hamas internal security chief "
               "Naeem Abu Nahel, 50, in Gaza City. At least 7 killed in "
               "Tuesday's strikes, including two police officers.",
               font(FR, 21), INK, w - 36, leading=27)

    # ---- Row 3: Ukraine | Nvidia | Libya -------------------------------------
    y3, h3, w3 = 660, 196, 312
    # Ukraine
    x = 24
    panel(d, x, y3, w3, h3)
    kicker(d, x + 16, y3 + 14, "UKRAINE", TEAL)
    d.text((x + 16, y3 + 54), "2 KILLED IN", font=font(FB, 28), fill=INK)
    d.text((x + 16, y3 + 86), "ZAPORIZHZHIA", font=font(FB, 28), fill=INK)
    text_block(d, x + 16, y3 + 124,
               "Overnight Russian strike hits an apartment block; "
               "40 wounded, incl. four children.",
               font(FR, 18), INK, w3 - 32, leading=23)
    # Nvidia
    x = 356
    panel(d, x, y3, w3, h3)
    kicker(d, x + 16, y3 + 14, "TECH  •  NVIDIA", AMBER)
    d.text((x + 16, y3 + 54), "HUANG SAYS", font=font(FB, 30), fill=INK)
    d.text((x + 16, y3 + 86), "SORRY", font=font(FB, 30), fill=INK)
    text_block(d, x + 16, y3 + 124,
               "A day after reinstatement, Jensen Huang apologises "
               "to staff and says he's in therapy.",
               font(FR, 18), INK, w3 - 32, leading=23)
    # Libya
    x = 688
    panel(d, x, y3, w3, h3)
    kicker(d, x + 16, y3 + 14, "LIBYA", DARKRED)
    d.text((x + 16, y3 + 54), "CORVETTE", font=font(FB, 30), fill=INK)
    d.text((x + 16, y3 + 86), "SUNK", font=font(FB, 30), fill=INK)
    text_block(d, x + 16, y3 + 124,
               "Kyiv says its naval drones sank the Russian corvette "
               "Merkury off Benghazi.",
               font(FR, 18), INK, w3 - 32, leading=23)

    # ---- Sport strip -----------------------------------------------------------
    y4, h4 = 872, 104
    panel(d, 24, y4, 976, h4)
    kicker(d, 42, y4 + 14, "SPORT", GREEN)
    d.text((42, y4 + 52), "Real Madrid 5–1 PSV — Mbappé brace in Champions League rout.",
           font=font(FB, 22), fill=INK)
    d.text((42, y4 + 82), "Man City 2–2 Napoli; Arsenal 1–1 Dortmund; "
           "Galatasaray 1–0 Aston Villa.",
           font=font(FR, 18), fill=GREY)

    # ---- footer ------------------------------------------------------------------
    d.line([24, 982, W - 24, 982], fill=(210, 205, 192), width=2)
    d.text((24, 988), "Sources: Reuters, AP, Yonhap, IRNA, CNN, UEFA",
           font=font(FR, 13), fill=GREY)
    d.text((24, 1006), "Also: COP31 post-mortem; Banten fire follow-up; SpaceX sued "
           "over Grok; UAE bus crash kills 11; Nvidia +30%; Seoul summons Moscow.",
           font=font(FR, 13), fill=GREY)

    im.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", im.size)


if __name__ == "__main__":
    main()
