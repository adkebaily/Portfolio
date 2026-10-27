"""Génère les images d'aperçu (LinkedIn, WhatsApp…) : public/assets/og-fr.jpg et og-en.jpg (1200×630).
Même identité que le site : vitre de scanner, feuille, palette viridis.
Usage : python3 src/tools/make_og_image.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PHOTO = ROOT / "public" / "assets" / "photo.jpg"
FONT_DIR = Path(__file__).resolve().parent / "fonts"   # polices OFL (Google Fonts)
W, H = 1200, 630
GLASS, PAPER, LINE = (238, 242, 241), (251, 252, 251), (204, 214, 211)
INK, SOFT, FAM = (29, 43, 54), (75, 90, 100), (68, 1, 84)
VIRIDIS = [(68, 1, 84), (59, 82, 139), (33, 145, 140), (94, 201, 98), (253, 231, 37)]

TEXTS = {
    "fr": ("Ingénierie IA, agents IA, IA générative", "Stage dès le 1er avril 2027, 5 mois max."),
    "en": ("AI engineering, AI agents, generative AI", "Internship from 1 April 2027, up to 5 months"),
}


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def viridis(t):
    t = min(max(t, 0), 1) * (len(VIRIDIS) - 1)
    i = min(int(t), len(VIRIDIS) - 2)
    k = t - i
    return tuple(round(VIRIDIS[i][c] + (VIRIDIS[i + 1][c] - VIRIDIS[i][c]) * k) for c in range(3))


def id_photo(w, h):
    src = Image.open(PHOTO).convert("RGB")
    sw, sh = src.size
    cw = min(sw, round(sh * w / h))
    ch = round(cw * h / w)
    top = int((sh - ch) * 0.25)
    return src.crop(((sw - cw) // 2, top, (sw - cw) // 2 + cw, top + ch)).resize((w, h), Image.LANCZOS)


def make(lang):
    img = Image.new("RGB", (W, H), GLASS)
    d = ImageDraw.Draw(img)
    # feuille posée sur la vitre, avec repères de cadrage
    sx, sy, ex, ey = 60, 120, 800, 470
    d.rectangle((sx, sy, ex, ey), fill=PAPER, outline=LINE)
    for (x, y, dx, dy) in [(sx - 10, sy - 10, 1, 1), (ex + 10, ey + 10, -1, -1)]:
        d.line([(x, y), (x + 22 * dx, y)], fill=VIRIDIS[2], width=3)
        d.line([(x, y), (x, y + 22 * dy)], fill=VIRIDIS[2], width=3)
    big = font("BricolageGrotesque-ExtraBold.ttf", 74)
    d.text((sx + 44, sy + 40), "Chems Eddine Adel", font=big, fill=INK)
    d.text((sx + 44, sy + 122), "Kebaily", font=big, fill=FAM)
    d.text((sx + 46, sy + 250), TEXTS[lang][0], font=font("IBMPlexSans-SemiBold.ttf", 28), fill=SOFT)
    # photo d'identité avec décalage viridis
    pw, ph = 250, 312
    px, py = 880, 120
    d.rectangle((px + 10, py + 10, px + pw + 10, py + ph + 10), fill=VIRIDIS[2])
    d.rectangle((px - 4, py - 4, px + pw + 4, py + ph + 4), fill=PAPER, outline=LINE)
    img.paste(id_photo(pw, ph), (px, py))
    # disponibilité et adresse du site
    tag = font("IBMPlexSans-SemiBold.ttf", 24)
    text = TEXTS[lang][1]
    tw = d.textlength(text, font=tag)
    d.rectangle((sx, 515, sx + tw + 28, 557), fill=VIRIDIS[4])
    d.text((sx + 14, 536), text, font=tag, fill=INK, anchor="lm")
    d.text((1140, 536), "chemseddine-kebaily.netlify.app", font=font("IBMPlexSans-Medium.ttf", 22), fill=SOFT, anchor="rm")
    for x in range(W):
        d.line([(x, H - 14), (x, H)], fill=viridis(x / (W - 1)))
    out = ROOT / "public" / "assets" / f"og-{lang}.jpg"
    img.save(out, quality=90, optimize=True, progressive=True)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    for lang in TEXTS:
        make(lang)
