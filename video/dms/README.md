Source of `public/assets/demo-dms*.{mp4,webm,jpg}`. Edit `dms.html` (texts in `T`, timing in `seek`), then:

    python3 render.py en frames_en && python3 render.py fr frames_fr
    ffmpeg -framerate 30 -i frames_en/f%04d.png -c:v libopenh264 -b:v 180k -pix_fmt yuv420p -movflags +faststart ../../public/assets/demo-dms-en.mp4
    ffmpeg -framerate 30 -i frames_en/f%04d.png -c:v libvpx-vp9 -b:v 0 -crf 46 ../../public/assets/demo-dms-en.webm
    ffmpeg -i frames_en/f0420.png -q:v 4 ../../public/assets/demo-dms-en.jpg

Same for `fr` without the `-en` suffix. Needs Python Playwright with Chromium.
