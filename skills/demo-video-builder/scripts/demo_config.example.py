"""
demo_config.py — the single source of truth for your demo video.

Both gen_vo.py (narration) and build.py (assembly) import THIS file. Copy it to `demo_config.py`,
then edit the BEATS list. Everything below uses generic placeholder content — replace it with your own.

A screen recording at 1920x1080 is assumed. If yours differs, adjust W/H and the mask coordinates.
"""

# ---- source & bookends -------------------------------------------------------
SRC    = "recording.mp4"     # your raw screen recording
OPENER = None                # e.g. "out/opener.mp4"  (rendered via render_bookend.js) or None to skip
OUTRO  = None                # e.g. "out/outro.mp4"   or None to skip

# ---- output format -----------------------------------------------------------
W, H, FPS = 1920, 1080, 30

# ---- voiceover ---------------------------------------------------------------
VOICE = "en-US-AndrewNeural" # any edge-tts voice; list with:  edge-tts --list-voices
RATE  = "+2%"                # speaking rate

# ---- mask helpers (privacy) --------------------------------------------------
# Coordinates are in NATIVE recording pixels (top-left origin). color: "white", "black",
# "0xRRGGBB", or "0xRRGGBB@alpha". Use enable="between(t,START,END)" to mask ONLY during a
# time window (concat-relative seconds, before time-fit) — essential when the page scrolls
# mid-beat and a fixed box would otherwise cover the wrong content later.
def box(x, y, w, h, color="white", enable=None):
    s = f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}:t=fill"
    if enable:
        s += f":enable='{enable}'"
    return s

# Chrome-cover bar colors: pick one that matches the app so the bar blends in.
CHROME_DARK  = "0x111318"    # for apps with a dark top header
CHROME_LIGHT = "0xFFFFFF"    # for light UIs

# ---- beats -------------------------------------------------------------------
# Each beat:
#   id     : short slug (also the vo/<id>.mp3 filename)
#   vo     : narration text (numbers spelled out read best, e.g. "twenty-three point two")
#   spans  : [(start,end), ...] seconds in SRC. Multiple spans CONCATENATE — the gaps between
#            them (thinking/loading lags) are dropped. This is how you cut dead air.
#   chrome : color to cover the top browser-chrome bar (CHROME_DARK/LIGHT), or None
#   masks  : list of box(...) privacy masks (native coords), or []
#   zoom   : (fx, fy) focus fraction (0..1) for a gentle push-in, or None. e.g. (0.5,0.44)
#   freeze : seconds to hold the last frame (use when footage is shorter than the VO)
BEATS = [
    dict(
        id="setup",
        vo="Here's the workflow. We connect the agent to the data and give it governed "
           "instructions, so every answer is grounded and traceable.",
        spans=[(4, 12), (20, 30)],       # keep 4-12 and 20-30; drop the 12-20 loading lag
        chrome=CHROME_DARK,
        masks=[box(216, 214, 756, 36)],  # example: cover a subtitle line that shows an internal name
        zoom=None,
        freeze=0,
    ),
    dict(
        id="question-1",
        vo="First question, asked in plain English. The agent returns the result in seconds — "
           "the key metric moves from one hundred at baseline to eighty-three after the change, "
           "with the top segment holding up best.",
        spans=[(48, 52), (70, 92)],      # question bubble, then the answer (thinking lag cut)
        chrome=CHROME_DARK,
        masks=[box(216, 214, 756, 36)],
        zoom=(0.42, 0.44),               # push in on the answer for readability
        freeze=0,
    ),
    dict(
        id="question-2",
        vo="Second question. Same experience — a grounded, cited answer with the supporting "
           "table, and an honest flag where the data needs review.",
        spans=[(120, 124), (140, 150)],
        chrome=CHROME_LIGHT,             # this screen has a light UI
        masks=[box(1550, 898, 72, 50),   # cover an extension badge in the composer
               box(0, 992, 152, 56, color="0xF7F7F7")],  # cover a username bottom-left
        zoom=(0.55, 0.44),
        freeze=6.0,                      # footage is short; hold the final answer while VO finishes
    ),
]
