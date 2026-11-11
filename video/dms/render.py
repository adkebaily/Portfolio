"""Render dms.html to PNG frames: python render.py <lang> <out_dir> [t1 t2 ...] (no times = full 24 s at 30 fps)."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
lang, out = sys.argv[1], Path(sys.argv[2])
times = [float(x) for x in sys.argv[3:]] or [i / 30 for i in range(24 * 30)]
out.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1120, "height": 630})
    page.goto(f"file://{HERE / 'dms.html'}?lang={lang}")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(500)
    for i, t in enumerate(times):
        page.evaluate(f"seek({t})")
        page.screenshot(path=str(out / f"f{i:04d}.png"))
    b.close()
print(f"{len(times)} frames -> {out}")
