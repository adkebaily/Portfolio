"""Génère les images d'aperçu (LinkedIn, WhatsApp…) : public/assets/og-fr.jpg et og-en.jpg (1200×630).
Usage : python3 src/tools/make_og_image.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PHOTO = ROOT / "public" / "assets" / "photo.jpg"
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
W, H = 1200, 630

TEXTS = {
    "fr": ("Ingénierie IA · Agents IA · IA générative", "Master 1 Traitement du signal et des images — ULCO"),
    "en": ("AI Engineering · AI Agents · Generative AI", "Master's in Signal and Image Processing — ULCO"),
}


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def background():
    # dégradé indigo → violet → cyan, comme le site
    img = Image.new("RGB", (W, H))
    stops = [(0.0, (49, 46, 129)), (0.55, (79, 70, 229)), (1.0, (8, 145, 178))]
    px = img.load()
    for x in range(W):
        for y in range(H):
            t = min(1, max(0, (x / W) * 0.75 + (y / H) * 0.25))
            for (a, ca), (b, cb) in zip(stops, stops[1:]):
                if a <= t <= b:
                    k = (t - a) / (b - a)
                    px[x, y] = tuple(round(ca[i] + (cb[i] - ca[i]) * k) for i in range(3))
                    break
    # grille légère
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 14))
    for y in range(0, H, 48):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 14))
    return img


def round_photo(size):
    src = Image.open(PHOTO).convert("RGB")
    w, h = src.size
    side = min(w, h)
    top = int((h - side) * 0.25)          # garder le visage
    src = src.crop(((w - side) // 2, top, (w - side) // 2 + side, top + side)).resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4, size * 4), fill=255)
    out = Image.new("RGBA", (size, size))
    out.paste(src, (0, 0), mask.resize((size, size), Image.LANCZOS))
    return out


def make(lang):
    img = background().convert("RGBA")
    size = 300
    ring = Image.new("RGBA", (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, size + 23, size + 23), fill=(255, 255, 255, 235))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((828, 178, 828 + size + 24, 178 + size + 24), fill=(10, 10, 40, 110))
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(22)))
    img.alpha_composite(ring, (820, 160))
    img.alpha_composite(round_photo(size), (832, 172))

    d = ImageDraw.Draw(img)
    x = 80
    d.rounded_rectangle((x, 92, x + 70, 162), radius=20, fill=(255, 255, 255))
    d.text((x + 35, 127), "CK", font=font("Inter-ExtraBold.otf", 30), fill=(79, 70, 229), anchor="mm")
    d.text((x, 205), "Chems Eddine Adel", font=font("Inter-ExtraBold.otf", 62), fill="white")
    d.text((x, 280), "Kebaily", font=font("Inter-ExtraBold.otf", 62), fill=(165, 243, 252))
    line1, line2 = TEXTS[lang]
    d.text((x, 385), line1, font=font("Inter-SemiBold.otf", 30), fill="white")
    d.text((x, 432), line2, font=font("Inter-Medium.otf", 24), fill=(224, 231, 255))
    d.text((x, 530), "chemseddine-kebaily.netlify.app", font=font("Inter-SemiBold.otf", 24), fill=(253, 230, 138))
    out = ROOT / "public" / "assets" / f"og-{lang}.jpg"
    img.convert("RGB").save(out, quality=88, optimize=True, progressive=True)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    for lang in TEXTS:
        make(lang)
