# vo_script.example.py — the spec gen_vo_multivoice.py reads. Copy to vo_script.py and edit.
#
# Everything below is FICTIONAL (an invented "Acme Utilities") with synthetic numbers —
# replace with your demo's story. Never put customer names or internal identifiers here.
#
# VOICES: cast 2–3 edge-tts voices with per-voice base rates.
#   Browse voices:  edge-tts --list-voices
#   Christopher reads ~10% slower than Andrew/Ava — give his beats bigger budgets.
VOICES = {
    "narrator":  ("en-US-AndrewNeural",      "+3%"),   # the story, the turns, the close
    "guide":     ("en-US-AvaNeural",         "+4%"),   # the product walkthrough
    "character": ("en-US-ChristopherNeural", "+2%"),   # an operator / exec voice moment
}

# SCENES: sequential phases for animated b-roll (openers / interstitials / finales).
# gen_vo_multivoice.py emits scenes/timing_<name>.js so the scene HTML can key every
# animation to a spoken word (see scenes/broll_opener.example.html and
# references/broll-scenes.md).
SCENES = {
    "opener": {
        "gap": 0.4,                       # breath between phases, seconds
        "phases": [
            {"name": "cold", "voice": "narrator", "text":
             "Acme Utilities runs four hundred substations. And every night, "
             "one number decides whether the morning is boring, or expensive."},
            {"name": "ops", "voice": "character", "radio": True, "text":
             "Control room. I've got twelve alerts and one crew. Which one is real?"},
            {"name": "promise", "voice": "narrator", "text":
             "This is a fictional utility, on synthetic data. The platform underneath "
             "is real. Here is how it answers that question, in time."},
            {"name": "handoff", "voice": "guide", "text":
             "It starts with one sensor. Watch."},
        ],
    },
    # Add "finale": {...} the same way.
}

# PLACED: re-voice a screen recording so each line lands on its on-screen action.
#   1. Cut the recording segment (note the cut start second in the source).
#   2. For each original narration beat, offset `at` = original start − cut start.
#   3. `budget` = seconds until the next beat starts (minus ~0.3s of air).
# The generator auto-bumps the speaking rate (twice, +7% each) if a beat overruns,
# then WARNs. Verify placement afterwards with:
#   ffmpeg -i vo_walkthrough.mp3 -af silencedetect=noise=-38dB:d=1.2 -f null -
PLACED = {
    "walkthrough": {
        "length": 62.0,                   # duration of the cut recording segment
        "beats": [
            {"name": "b1", "voice": "guide", "at": 0.5, "budget": 14.0, "text":
             "This is the live scoreboard. Four hundred substations, one governed "
             "table, refreshed every minute."},
            {"name": "b2", "voice": "guide", "at": 15.0, "budget": 18.0, "text":
             "One click opens the anomaly. The platform correlates three alerts "
             "into a single event, and ranks it."},
            {"name": "b3", "voice": "narrator", "at": 33.5, "budget": 16.0, "text":
             "And here is the part a dashboard cannot do. It explains why, and "
             "shows the query behind every number."},
            {"name": "b4", "voice": "guide", "at": 50.0, "budget": 11.5, "text":
             "The crew gets one work order. Everything else stays quiet."},
        ],
    },
}
