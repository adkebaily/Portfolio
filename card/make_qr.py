"""Generate print-ready QR codes for the digital business card.

Usage:
    pip install segno
    python make_qr.py https://your-card.netlify.app
"""
import sys
from pathlib import Path

import segno

url = sys.argv[1] if len(sys.argv) > 1 else "https://YOUR-CARD.netlify.app"
out = Path(__file__).parent / "qr"
out.mkdir(exist_ok=True)

# Error level "H" (30% redundancy) keeps it scannable even if printed small or slightly damaged
qr = segno.make(url, error="h")

# SVG: vector, ideal for a printed business card / CV / slide
qr.save(out / "qr.svg", scale=10, border=2, dark="#0b0d12", light=None)
# PNG: for sharing on screens, LinkedIn banner, etc.
qr.save(out / "qr.png", scale=20, border=2, dark="#0b0d12", light="#ffffff")

print(f"QR for {url} saved in {out}/ (qr.svg, qr.png)")
