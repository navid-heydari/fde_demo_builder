# Voiceover & sync

## Writing the narration
- One tight line per beat, in `demo_config.py`'s `vo` field. Lead with the point; don't narrate the mouse.
- **Explain, don't just read.** For a technical demo, say what the screen *means* (what the metric is, why
  the result matters), grounded in the numbers actually on screen.
- **Spell for TTS.** Numbers and acronyms read better spelled: "twenty-three point two", "F T M one",
  "Q U V", "C O N twenty-twenty-six", "S Q L". Test-listen and adjust.
- **Never state a number that isn't visible** at that moment. If the VO says it, the frame must show it.
- Keep it short — shorter VO means the footage time-fit stays near 1.0× (no slow-motion).

Regenerate after edits:
```
python gen_vo.py
```

## How sync works
`build.py` sets each beat's on-screen duration to `vo_duration + 0.4s` and time-fits the footage to it:
```
factor = (vo_dur + 0.4) / footage_dur
setpts = factor * (PTS - STARTPTS)
```
- `factor ≈ 1.0` is ideal (natural speed). 0.85–1.15 is fine.
- The narration is delayed 150 ms (`adelay=150`) so it doesn't start on the very first frame, and padded so
  the beat ends ~0.25 s after the voice.

## When footage is shorter than the VO
Don't stretch heavily (looks like a stall). **Freeze-hold** the last frame instead:
```python
dict(id="answer", spans=[(609, 620)], freeze=8.0, ...)
```
This plays the real footage, then holds the fully-rendered answer while the voice finishes — which reads as
"let the result land." A push-in `zoom` during the freeze adds life. Prefer freeze whenever `factor` would
exceed ~1.3 (build.py warns you).

## Keep the answer on screen during its numbers
Structure beats so the answer renders early and stays visible (or is frozen) through the number-heavy part
of the narration. If the VO cites three figures over 8 seconds, all three must be readable for those 8
seconds — scroll the footage so it settles on them, or freeze on the frame that shows them.

## Opener/outro sync
For animated bookends, time the animation beats to VO word anchors. Transcribe the bookend VO with
faster-whisper to get word timestamps, then set the scene's `setTimeout`s to match. See `opener-outro.md`.
