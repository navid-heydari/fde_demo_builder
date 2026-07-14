# Framing & zoom

## Default: original framing (1:1)
Keep each screen at its **native scale**. Don't crop-and-scale-to-fill — it changes the look reviewers
expect from the recording, and it can trim content off the sides. Instead, remove only the browser chrome
by **covering it with a color-matched bar** (see `privacy-scrubbing.md`), leaving the app exactly as
recorded inside a 1920×1080 frame.

Why not crop+scale to fill the frame? Because it (a) zooms ~10% and shifts the composition, (b) trims the
left nav or right margin, and (c) makes the body clips look different from the animated bookends. A viewer
comparing to the live product notices. Only crop when explicitly asked.

## Zoom for readability (not reframing)
When an answer is dense (small table text, many numbers), add a gentle **push-in** so viewers can read it —
without permanently reframing. In `demo_config.py`:
```python
dict(id="answer", zoom=(0.42, 0.44), ...)   # (fx, fy) focus fraction, 0..1
```
`build.py` implements it as a `zoompan` that holds 1.0 for ~1.5 s, then ramps to ~1.10 focused on
`(fx, fy)`, then holds. Effects:
- `fx` = horizontal focus (0 left, 1 right). Left-of-center answers ≈ 0.40–0.45; centered ≈ 0.5; Agent/chat
  panels that sit right-of-a-rail ≈ 0.55–0.6.
- `fy` = vertical focus. Answers near the top ≈ 0.40–0.45.

Keep the ramp subtle (≤1.10) so it reads as emphasis, not motion sickness. Combine with a `freeze` so the
zoom finishes on the held final answer.

## When to zoom vs. not
- **Zoom:** dense answers, tables, key numbers the VO calls out.
- **No zoom:** setup screens, scrolling views (a zoom fighting a scroll is busy), and anything already
  legible at native scale.

## Aspect / letterboxing
The chrome-cover-bar approach keeps the full 1920×1080 with no letterbox. If you must crop and end up with
a non-16:9 region, scale to fit and pad to 1920×1080 with a color close to the app background rather than
pure black, so it doesn't look like a broken export.
