#!/usr/bin/env python3
"""
gen_vo.py — render one narration MP3 per beat using edge-tts (neural TTS).

Reads BEATS / VOICE / RATE from demo_config.py and writes vo/<beat id>.mp3.
Run this whenever you change any beat's `vo` text, then re-run build.py.

    pip install edge-tts
    python gen_vo.py

Tips for clean narration:
  - Spell numbers/units the way they should sound: "twenty-three point two newtons",
    "F T M one", "Q U V", "C O N twenty-twenty-six".
  - Keep each beat's line tight; build.py time-fits footage to the VO length, so shorter VO
    = less slow-motion / freeze needed.
"""
import asyncio
import os
import edge_tts
from demo_config import BEATS, VOICE, RATE

HERE = os.path.dirname(os.path.abspath(__file__))
VO_DIR = os.path.join(HERE, "vo")
os.makedirs(VO_DIR, exist_ok=True)


async def main():
    for b in BEATS:
        text = b.get("vo", "").strip()
        if not text:
            print(f"skip {b['id']} (no vo text)")
            continue
        path = os.path.join(VO_DIR, b["id"] + ".mp3")
        await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
        print("wrote", os.path.relpath(path, HERE))


if __name__ == "__main__":
    asyncio.run(main())
