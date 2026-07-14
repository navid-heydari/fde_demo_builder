# Animated opener / outro (optional)

Polished bookends lift a demo, but they're **optional** — `build.py` works fine with `OPENER = None` /
`OUTRO = None`. When you want them, they're just short MP4s produced from an HTML/Canvas scene.

## How it works
1. Author a scene as a self-contained HTML file at 1920×1080 (`scenes/opener.html`). See
   `scenes/opener.example.html` for a clean, generic title card you can restyle.
2. The scene defines `window.__start()` to begin its animation. `render_bookend.js` calls it **after**
   recording starts, so the animation clock lines up with the video (otherwise it finishes before the
   recording is meaningful).
3. Render to MP4 (and mux narration if you have it):
   ```
   npm i puppeteer puppeteer-screen-recorder
   node render_bookend.js scenes/opener.html out/opener.mp4 12 vo/opener.mp3
   ```
4. Point `demo_config.py` at it: `OPENER = "out/opener.mp4"`.

## Design guidance
- Keep it short (10–20 s) and on-message: a kicker, a title, a one-line value tagline, maybe a simple
  pipeline/graphic. Restraint reads as "premium."
- **No customer names**, no internal URLs, no logos you don't have rights to. Use a neutral accent color.
- Match the outro to the opener (same type/color system) so the video feels bookended.

## Syncing beats to narration
If the bookend has VO, time its animation beats to the spoken words:
1. Transcribe the bookend narration for word timestamps (optional dependency):
   ```
   pip install faster-whisper
   ```
   Use the tiny/int8 model; it's fast and accurate enough for word anchors.
2. Set the scene's `setTimeout` delays so each element appears as its word is spoken.
3. Render for a duration ≥ the VO length; `render_bookend.js` pads audio so the tail isn't clipped.

## Rendering pitfalls
- One render at a time — parallel headless-Chrome instances can saturate the machine and time out.
- Force scale factor 1 and a 1920×1080 viewport (render_bookend.js does this) or you'll get wrong-res output.
- Toggle elements via opacity/transform, not `display:none`→`flex` (a later rule can override it; use
  `!important` if you must).
