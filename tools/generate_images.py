#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates elegant branded placeholder "photography" plates for TravelDore.
No external network calls — fully self-contained so the site works offline
and never shows broken images. Swap these files for real photography later;
filenames are stable (images/<seed>.jpg) so a straight file-replace works.
"""
import os, hashlib, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images")
os.makedirs(OUT, exist_ok=True)

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"

# Brand palette (hex)
DEEP_PLUM   = (49, 20, 50)
DARK_PURPLE = (74, 35, 90)
LAVENDER    = (180, 151, 214)
SOFT_LILAC  = (220, 206, 248)
GOLD        = (212, 175, 55)
GOLD_SOFT   = (232, 206, 121)
IVORY       = (250, 248, 252)

# A handful of tasteful diagonal gradient pairings built from the brand palette
VARIANTS = [
    (DEEP_PLUM, DARK_PURPLE),
    (DARK_PURPLE, LAVENDER),
    (DEEP_PLUM, LAVENDER),
    ((38, 15, 40), DARK_PURPLE),
    (DARK_PURPLE, (98, 60, 120)),
    ((30, 12, 34), (90, 48, 100)),
]

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def variant_for(seed):
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return VARIANTS[h % len(VARIANTS)], h

def gradient(w, h, c1, c2, angle=135):
    """Diagonal linear gradient."""
    base = Image.new("RGB", (w, h), c1)
    top = Image.new("RGB", (w, h), c2)
    mask = Image.new("L", (w, h))
    md = ImageDraw.Draw(mask)
    rad = math.radians(angle)
    dx, dy = math.cos(rad), math.sin(rad)
    length = abs(w*dx) + abs(h*dy)
    for y in range(h):
        # sample a row of gradient values (approx, fast enough for placeholder sizes)
        pass
    # Faster vectorized-ish approach using per-pixel via numpy-free loop on small grid then resize
    steps = 64
    grad_strip = Image.new("L", (steps, 1))
    for i in range(steps):
        grad_strip.putpixel((i, 0), int(255 * i/(steps-1)))
    grad_strip = grad_strip.resize((w, h), Image.BILINEAR)
    # rotate the strip to angle by resizing a rotated canvas
    diag = int(math.hypot(w, h))
    big = Image.new("L", (diag, diag))
    strip = Image.new("L", (diag, 1))
    for i in range(diag):
        strip.putpixel((i, 0), int(255 * i/(diag-1)))
    strip = strip.resize((diag, diag), Image.BILINEAR)
    rotated = strip.rotate(angle, resample=Image.BICUBIC)
    left = (diag - w)//2
    top_ = (diag - h)//2
    mask = rotated.crop((left, top_, left+w, top_+h))
    return Image.composite(top, base, mask)

def vignette(img, strength=0.55):
    w, h = img.size
    vg = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(vg)
    maxr = math.hypot(w/2, h/2)
    d.ellipse([-w*0.25, -h*0.25, w*1.25, h*1.25], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(min(w, h)//6))
    dark = Image.new("RGB", (w, h), (10, 4, 12))
    return Image.composite(img, dark, vg.point(lambda p: int(p*(1-strength) + 255*strength) if False else int(255-(255-p))))

def add_vignette(img, strength=110):
    w, h = img.size
    overlay = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(overlay)
    d.ellipse([w*-0.35, h*-0.35, w*1.35, h*1.35], fill=strength)
    overlay = overlay.filter(ImageFilter.GaussianBlur(min(w, h)//5))
    dark = Image.new("RGB", (w, h), (12, 5, 14))
    mask = overlay.point(lambda p: 255-p)
    return Image.composite(img, dark, mask)

def speckle(img, seed, density=140, color=(255, 255, 255)):
    w, h = img.size
    rnd = random.Random(seed)
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    for _ in range(density):
        x, y = rnd.randint(0, w), rnd.randint(0, h)
        r = rnd.choice([1,1,1,2])
        a = rnd.randint(6, 22)
        d.ellipse([x-r, y-r, x+r, y+r], fill=color+(a,))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def frame(img, gold=GOLD, inset=None):
    w, h = img.size
    inset = inset or max(8, min(w, h)//60)
    d = ImageDraw.Draw(img)
    d.rectangle([inset, inset, w-inset-1, h-inset-1], outline=gold, width=2)
    return img

def label_plate(img, text, small=""):
    w, h = img.size
    d = ImageDraw.Draw(img, "RGBA")
    size = max(20, min(w, h)//16)
    try:
        font = ImageFont.truetype(FONT_SERIF, size)
        small_font = ImageFont.truetype(FONT_SERIF_IT, max(12, size//2))
    except Exception:
        font = ImageFont.load_default()
        small_font = font
    txt = text.upper()
    bbox = d.textbbox((0,0), txt, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    cx, cy = w/2, h/2
    line_w = min(w*0.28, 140)
    d.line([(cx-line_w/2-tw/2-18, cy), (cx-tw/2-18, cy)], fill=GOLD_SOFT+(200,), width=1)
    d.line([(cx+tw/2+18, cy), (cx+tw/2+18+line_w/2, cy)], fill=GOLD_SOFT+(200,), width=1)
    d.text((cx-tw/2, cy-th/1.6), txt, font=font, fill=(255,255,255,235))
    if small:
        sb = d.textbbox((0,0), small, font=small_font)
        stw = sb[2]-sb[0]
        d.text((cx-stw/2, cy+th*0.9), small, font=small_font, fill=GOLD_SOFT+(210,))
    return img

def make_plate(seed, w, h, label="TravelDore", small=""):
    fname = f"{seed}-{w}x{h}.jpg"
    fpath = os.path.join(OUT, fname)
    if os.path.exists(fpath):
        return fname
    (c1, c2), hval = variant_for(seed)
    angle = 115 + (hval % 40)
    img = gradient(w, h, c1, c2, angle=angle)
    img = add_vignette(img, strength=95)
    img = speckle(img, seed, density=int((w*h)/9000))
    img = frame(img)
    img = label_plate(img, label, small)
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    img.save(fpath, "JPEG", quality=82)
    return fname

if __name__ == "__main__":
    print("This module is imported by build.py — run build.py to generate the full site.")
