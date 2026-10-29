# Gala Kaplun site clone

Static rebuild of https://www.galakaplun.com/ (originally a Wix site) as plain HTML/CSS.

Live: https://galakaplun-eng.github.io/galakaplun-site/ (GitHub Pages, served from `docs/` on `main`).

- `build.py` — all page content (project list, video sources, gallery layout) and CSS; generates `docs/`.
- `docs/` — the built site. `docs/assets/img` holds the original Wix media (67 images), `docs/assets/video` the four Wix-hosted MP4s.

## Run locally

```
python3 build.py            # regenerate after editing build.py
cd docs && python3 -m http.server 8000
```

Open http://localhost:8000/

Project-page players for YouTube, Vimeo and Facebook are embedded from their platforms. The hero showreel, the four Wix-hosted videos (Bezalel, Taboola, SolarEdge, On Parole) and all hover previews (`docs/assets/preview/`) are local files.

To refresh the hero showreel from a new export: `ffmpeg -i SRC -an -vf scale=1280:-2 -c:v libx264 -preset slow -crf 28 -movflags +faststart -pix_fmt yuv420p docs/assets/video/showreel.mp4`
