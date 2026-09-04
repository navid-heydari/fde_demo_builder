# B-roll story scenes (v2)

Animated, word-synced HTML scenes — problem-statement openers, interstitials, finales —
rendered by headless Chrome and cut against re-voiced screen recordings. This is the "wow"
layer: the story an audience remembers before and after the product footage.

Everything here is driven by `scenes/broll_opener.example.html` (a working template) +
`render_scene.js` + `shot.js` + `gen_vo_multivoice.py`. This file is the method.

## The contract (non-negotiable)

- **Fixed 1280×720 `#stage`**, auto-scaled to the window. `render_scene.js` records it at
  1.5 DPR → real 1920×1080 output. Author all coordinates against 1280×720.
- **One pure `frame(t)`.** Every visual is a function of the clock — no accumulated state,
  no `setTimeout` choreography. This is what makes `window.__seek(t)` produce a truthful
  still for any instant, which is what makes QA cheap.
- **`?render` + `window.__start()`**: the renderer starts the animation clock *with* the
  recording. In preview (no `?render`) the scene loops for browser review.
- **`DELAY = 0.45` ↔ `adelay=450`**: the recorder spins up ~0.45 s before frames flow; the
  scene clock subtracts it and the muxer delays the audio by it. Change one, change both.
- **Timing comes from the measured VO**: the scene loads `scenes/timing_<name>.js`
  (`window.PHASES` + `window.WORDS`), never hardcoded phase times. Re-generate VO → phases
  move → the scene follows.

## Word-sync: key everything to `wt()`

`wt('storm','battery')` = the clock time the word "battery" is *spoken* in phase `storm`.
Every element lands via `on(el, t >= wt(phase, word) - 0.3)` — a small lead (0.2–0.5 s) so
the visual arrives with the word, not after it. Use the nth-occurrence argument for repeated
words (`wt('ladder','chain',2)`).

Pitfalls (all learned the hard way):

- **A missing word silently returns the phase start** → the element appears way too early.
  If an element shows up at a phase boundary, the lookup missed. Check spelling against
  `vo/<name>_words.json` — hyphenated phrases are ONE stripped token.
- **Key the title/headline to the phase start**, not to a word spoken late in the phase —
  otherwise the stage sits empty while the narrator builds to the reveal.
- **A layer's visibility window must end at the NEXT phase**, not at some later one, or it
  bleeds through the following act (classic: the "problem" layer still visible under the
  "solution" act).

## Structure of a scene

1. **Layers**: one absolutely-positioned `.layer` per act, toggled `.on` by phase windows.
   Elements animate with CSS transitions (translate/scale/opacity, `cubic-bezier` with a
   slight overshoot for "pop") — `frame(t)` only toggles classes; CSS does the easing.
2. **Canvas** (behind the DOM): particles and drawn charts. Both redraw fully every frame
   from `t` — again, no state.
3. **`#fadeb`**: a black overlay that fades in at the tail so segments concat cleanly.

## The particle field ("flakes") and friends

The ambient drifting-dot field gives every scene depth for ~15 lines of canvas code (see the
template's `drawBG`). Variants proven to work:

- **Flakes**: 40–60 soft dots, slow upward drift, per-dot sinusoidal twinkle, brand palette.
  On light backgrounds drop alpha to ~0.10 and use muted brand colors.
- **Confetti burst**: a denser, faster field faded in only for the title bookend.
- **Rain**: short angled strokes falling inside a band/clip-rect; ramp intensity with an
  envelope tied to the storm beat.
- **Data particles**: dots interpolated along hand-placed polylines (source → pipeline) —
  reads as "data flowing" with `u = (t*speed + seed) % 1` per particle.

Keep particle counts modest (≤ 250 drawn things/frame) — headless Chrome records at 30 fps
on one CPU; dropped frames show up as VO drift at the END of a scene.

## Cameras over a real diagram (Ken Burns + spotlight)

To animate over an existing architecture diagram (a frame extracted from the source video):

- Put the full-res image in a `#world` div; the camera is a `translate(...) scale(...)` on
  `#world` computed from keyframes `[phaseStart, cx, cy, zoom]`, eased over ~2 s, with a
  slow drift while parked (`z *= 1+0.03*park`, tiny sin/cos on cx/cy) so holds feel alive.
- Clamp the camera so the viewport never leaves the image:
  `hw = 640/scale; cx = clamp(cx, hw, IW-hw)` (same for cy).
- **Spotlight**: an absolutely-positioned div *inside* `#world` per region with
  `box-shadow: 0 0 0 6000px rgba(bg,.55)` + an accent border — one element dims everything
  else and rides the camera for free.
- A caption bar in **screen space** (outside `#world`) carries the label for each region.
- Canvas overlays (flowing sparks along the diagram's arrows) need image→screen mapping:
  `sx = 640 + (ix - cx) * scale`.

## QA with stills, then render once

Renders are realtime (a 100 s scene takes 100 s), stills are seconds:

```bash
node shot.js scenes/opener.html 12 qa/op_12.png     # one per beat
```

Read the stills like a reviewer: collisions, empty stretches (> 4 s with nothing new), an
element that appeared too early (= failed word lookup). Fix, re-shoot, only then render.

## Rendering gotchas (each cost a re-render)

- **Global `canvas{position:absolute;inset:0}`** also captures small in-card canvases
  (sparklines) — override `position:static` on those or they overlay their card's header.
- **`textContent` does not parse entities** — write `·` not `&middot;` in strings set from JS.
- **Canvas text near the bitmap edge clips** — keep `fillText` ≥ 20 px from the canvas edge;
  labels near a moving marker need a side-flip once the marker approaches another label.
- **Uppercase diacritics read wrong in some fonts** (Ā vs ā) — check glyphs in a QA still.
- Layer windows: see word-sync pitfalls above — it's the most common visual bug.
- Deterministic `rnd()` (seeded LCG, in the template) — Math.random() breaks `__seek`
  reproducibility between the still pass and the render.

## Palettes

The template ships **dark** (deep teal + coral accent) with a **light "paper"** variant in a
comment (warm paper + red accent + steel blue). Rules of thumb: one accent for emphasis, one
alternate hue for "data/calm", danger color reserved for the actual problem beat; on light
themes, shadows do the work borders do on dark ones. Keep one identity per demo — the b-roll
should look like the *deck* the team already presents, not like the other demos.
