# Gala Kaplun site clone

Static rebuild of https://www.galakaplun.com/ (originally a Wix site) as plain HTML/CSS.

- `build.py` — all page content (project list, video sources, gallery layout) and CSS; generates `site/`.
- `site/` — the built site. `site/assets/img` holds the original Wix media (67 images), `site/assets/video` the four Wix-hosted MP4s.

## Run locally

```
python3 build.py            # regenerate after editing build.py
cd site && python3 -m http.server 8000
```

Open http://localhost:8000/

YouTube, Vimeo and Facebook videos are embedded from their platforms, so they need internet. The four Wix-hosted videos (Bezalel, Taboola, SolarEdge, On Parole) play from local files.
