# FDE Demo Builder

A Claude Code plugin that turns a **raw screen recording** of a product/customer demo into a
**polished, voice‑narrated, privacy‑scrubbed demo video** — with an optional animated opener/outro —
**entirely from scripts**. No video editor, no manual timeline. Edit a config, run one command, get a
shareable `.mp4`.

## What it does

Given one screen recording, the pipeline:

1. **Maps** the recording into named "beats" (setup, question 1, answer 1, …).
2. **Cuts the dead air** — the "thinking…", spinner, and loading lags between actions.
3. **Scrubs privacy leaks** — browser chrome (URL/token/bookmarks), usernames, extension badges, internal
   names — by covering/masking them (including *time‑gated* masks for content that scrolls mid‑beat).
4. **Generates the voiceover** with neural TTS (`edge-tts`, Andrew voice by default).
5. **Syncs VO to the screen** — each beat's footage is time‑fit to its narration so words land on the
   on‑screen action; short answers can freeze‑hold; a gentle push‑in zoom improves readability.
6. **Bookends** with an animated opener/outro (headless‑Chrome render of an HTML/Canvas scene) — optional.
7. **Self‑QAs** — decode integrity, silence gaps, and a frame contact sheet; plus an adversarial QA agent.

Everything is driven by a single `demo_config.py` (one source of truth for beats + narration) and two
scripts (`gen_vo.py`, `build.py`). It's fully reproducible: change the config, re‑run.

## Prerequisites

| Tool | Why | Check |
|---|---|---|
| **ffmpeg / ffprobe** (≥ 6) | all video assembly | `ffmpeg -version` |
| **Python** (≥ 3.10) + **edge-tts** | narration | `pip install edge-tts` |
| **Node.js** (≥ 18) + **puppeteer** + **puppeteer-screen-recorder** | animated opener/outro (optional) | `npm i puppeteer puppeteer-screen-recorder` |
| *(optional)* **faster-whisper** | word‑timestamps to sync opener beats to VO | `pip install faster-whisper` |

A **1920×1080** source recording is assumed throughout (adjust coords if yours differs).

## Install (as a Claude Code plugin)

Clone this repo, then add it as a local plugin (or via your team marketplace):

```bash
git clone https://github.com/ahmedawan-oracle/fde_demo_builder.git
# In Claude Code:  /plugin  → add local plugin → point at the cloned folder
```

Once installed you get:

- **Skill** `demo-video-builder` — the full methodology; Claude follows it when you ask to build a demo video.
- **Command** `/fde-demo-builder:new-demo <name>` — scaffolds a new demo project (scripts + starter config).
- **Agent** `demo-qa-reviewer` — adversarially QAs a finished video (privacy, VO‑sync, readability, playback).

## Quickstart

```
/fde-demo-builder:new-demo acme-widgets
```

Then, in the new `acme-widgets/` folder:

1. Drop your recording in as `recording.mp4`.
2. Edit `demo_config.py` — list your beats: `spans` (start/end seconds), `vo` (narration), and any
   `masks`/`zoom`/`freeze`.
3. `python gen_vo.py`   → narration MP3s in `vo/`
4. `python build.py`    → `out/demo.mp4`
5. Ask Claude to run the `demo-qa-reviewer` agent on `out/demo.mp4`; fix anything it flags; rebuild.

See [skills/demo-video-builder/SKILL.md](skills/demo-video-builder/SKILL.md) and the
[references/](skills/demo-video-builder/references/) for the detailed method and hard‑won ffmpeg lessons.

## Scope

This plugin builds the **demo video** from a recording. The *live* demo backend it records
(data, agents, connectors) is out of scope and set up separately.

## License

Released under the MIT License. See [LICENSE](LICENSE).
