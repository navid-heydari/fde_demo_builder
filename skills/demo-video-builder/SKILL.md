---
name: demo-video-builder
description: Use when building a polished, voice-narrated demo video from a screen recording — turning a raw capture of a product demo into a shareable MP4 with cut lag, scrubbed privacy leaks, synced VO, optional animated opener/outro. v2 adds cinematic "story rebuilds" — animated b-roll acts (problem-statement openers, interstitials, finales) word-synced to a multi-voice cast, and re-voicing existing recordings with placed narration beats. Triggers on "build a demo video", "narrate this recording", "make a demo from this screen capture", "cut the thinking lags and add voiceover", "add a wow animated opener", "multi voice demo", "b-roll story animation", "turn this demo into an animated story".
---

# Demo Video Builder

Turn one screen recording into a polished, narrated, privacy-clean demo video — **fully scripted**, no
video editor.

## Operating principles (read first)

- **Use the real screen, never mock-ups.** Every frame comes from the actual recording. Do not fabricate
  UI, type-ins, or numbers. If a number is spoken in VO, it must be visible on screen at that moment.
- **Privacy is non-negotiable and easy to miss.** Real recordings bake in leaks: address-bar URLs with
  tokens/tenancy IDs, personal bookmarks, browser-extension badges (e.g. Grammarly), usernames, avatars,
  and internal engineer/customer names typed into fields. **Every** shipped frame must be scrubbed. See
  `references/privacy-scrubbing.md`.
- **Original framing by default.** Keep each screen at its native scale; only cover the browser chrome.
  Reframe/crop only when asked. Use a gentle push-in *zoom* for readability, not a permanent crop.
- **Sync VO to the action.** Fit each beat's footage to its narration so words land on what's on screen.
- **Cut the dead air.** Remove "thinking…" / spinner / loading lags — they're the difference between a
  3:30 slog and a tight 3:00.
- **One source of truth.** `demo_config.py` holds the beats *and* their narration. `gen_vo.py` and
  `build.py` both read it. Change the config, re-run — never hand-edit intermediate files.
- **QA until clean.** A demo isn't done until an adversarial pass finds no privacy leak, no VO-sync drift,
  and clean playback. Use the `demo-qa-reviewer` agent.

## The pipeline (7 phases)

1. **Map** the recording into beats. Watch/scrub it; note the start/end seconds of each meaningful action
   (setup, question typed, answer rendered) and every lag to cut. → `references/map-and-cut.md`
2. **Cut lags** — a beat's `spans` list concatenates only the kept ranges; the gaps (thinking/loading) are
   dropped automatically. → `references/map-and-cut.md`
3. **Scrub privacy** — cover the browser chrome with a color-matched bar; `drawbox`-mask any residual leak
   (subtitle names, extension badges, usernames). Use *time-gated* masks when content scrolls mid-beat.
   → `references/privacy-scrubbing.md`
4. **Frame & zoom** — keep native scale (cover chrome, don't crop); add a slow push-in `zoompan` on dense
   answers for readability. → `references/framing-and-zoom.md`
5. **Voiceover** — write tight, domain-accurate narration per beat in `demo_config.py`; `gen_vo.py`
   renders one MP3 per beat with `edge-tts`. → `references/voiceover-and-sync.md`
6. **Assemble & sync** — `build.py` time-fits each beat's footage to its VO (freeze-hold if footage is
   short), overlays the VO, and concatenates with the opener/outro. → `references/voiceover-and-sync.md`
7. **QA** — decode integrity, silence gaps, contact sheet, then the `demo-qa-reviewer` agent. Fix, rebuild.
   → `references/qa-checklist.md`

## Files (in a scaffolded demo project)

```
my-demo/
├── recording.mp4          # your source capture (1920x1080 recommended)
├── demo_config.py         # THE spec: beats (spans, vo text, masks, zoom, freeze) + settings
├── gen_vo.py              # reads demo_config → vo/<beat>.mp3     (edit rarely)
├── build.py               # reads demo_config → out/demo.mp4      (edit rarely)
├── render_bookend.js      # optional: HTML/Canvas scene → mp4 (opener/outro)
├── scenes/opener.html     # optional: your animated title card
├── vo/                    # generated narration
└── out/                   # clips/ + demo.mp4 + qa/
```

Scaffold one with `/fde-demo-builder:new-demo <name>`, or copy `scripts/` from this skill.

## Typical loop

```bash
python gen_vo.py        # regenerate narration after editing demo_config.py
python build.py         # rebuild the video
# then: run the demo-qa-reviewer agent on out/demo.mp4, fix flags, repeat
```

## Key techniques (the "cool" parts)

- **Lag cutting** — `spans=[(a,b),(c,d)]` keeps only b−a and d−c; the (b→c) thinking gap vanishes.
- **Chrome-cover bar** — a `drawbox` over the top ~96px hides the address bar/bookmarks/extensions while
  keeping the app at 1:1 (dark bar for dark app headers, white for light UIs, so it blends).
- **Time-gated masks** — `enable='between(t,5.5,12)'` covers a leak (e.g. a typed internal name) only for
  the span where it's visible, so it doesn't blank content after the page scrolls.
- **VO time-fit** — `setpts=factor*PTS` with `factor = (vo_dur+0.4)/footage_dur`; keep factor ≈ 1.0.
- **Freeze-hold** — `tpad=stop_duration=N:stop_mode=clone` holds the last answer frame when the VO outlasts
  the footage (better than heavy slow-mo).
- **Push-in zoom** — `zoompan` ramp 1.0→1.10 focused on the answer, for readability without reframing.
- **Animated bookends** — an HTML/Canvas scene recorded via headless Chrome; beats timed to VO word
  anchors (whisper). → `references/opener-outro.md`

Detailed, copy-pasteable ffmpeg and the pitfalls that will bite you are in `references/ffmpeg-gotchas.md`.
Read it before debugging — most "it silently produced a stale/black/soundless file" issues are listed there.

## v2 — Story rebuilds: b-roll acts + a multi-voice cast

The v1 pipeline polishes **one recording**. The v2 workflow rebuilds a demo as a **film**:
animated story acts around (and over) the real product footage, narrated by a cast of voices.
Use it when someone says "make this a wow demo", "add an animated problem-statement story",
or "multi-voice this".

The five moves:

1. **Review the source** — extract frames (`ffmpeg -vf fps=1/12`) and transcribe the audio
   (faster-whisper) to map its structure: which stretches are slides (replace with b-roll),
   which are real product recordings (keep, re-voice), and the exact cut boundaries.
2. **Write the script** — `vo_script.py`: cast 2–3 voices (narrator / guide / character),
   sequential `SCENES` for the animated acts, `PLACED` beats pinned to the recording's
   original narration offsets. → `references/multi-voice.md`
3. **Generate VO** — `python gen_vo_multivoice.py` renders every phrase with word-level
   timestamps and emits `scenes/timing_<name>.js` for the scenes.
4. **Build the b-roll scenes** — clock-driven HTML (`scenes/broll_opener.example.html` is a
   working template): one pure `frame(t)`, every element keyed to spoken words via `wt()`,
   canvas particle fields ("flakes"), optional Ken Burns camera + spotlight over a diagram
   frame. QA with `node shot.js <scene> <t> <png>` stills, then render with
   `node render_scene.js <scene> <vo.mp3> <out.mp4>`. → `references/broll-scenes.md`
5. **Assemble** — mux placed VO over the video-only recording cuts, concat all segments,
   one `loudnorm` on the final mix. → `assemble.example.sh`

Hard rules carried over from v1: real screens only in recording segments (b-roll is clearly
stylized, fictional-branded, and labeled synthetic); privacy-scrub every recorded frame; and
**no customer names or internal identifiers anywhere** — in scenes, VO text, file names, or
example data.
