"""Generate netlify/functions/card-page.mjs from card/template.html.

The card page is served by the Netlify function `card.mjs` (never from public/),
so the phone number and the secret link stay out of this public repository.

Usage: python3 card/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html = (ROOT / "card" / "template.html").read_text(encoding="utf-8")
out = ROOT / "netlify" / "functions" / "card-page.mjs"
out.write_text(
    "// Généré par card/build.py à partir de card/template.html : ne pas modifier à la main.\n"
    f"export const PAGE = {json.dumps(html, ensure_ascii=False)};\n",
    encoding="utf-8",
)
print(f"built {out.relative_to(ROOT)}")
