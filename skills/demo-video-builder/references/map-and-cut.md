# Map the recording & cut the dead air

## Map into beats
Watch the recording and write down, in seconds, the meaningful **actions** and every **lag**:

- Actions to keep: a form being filled, a question typed, an answer rendering, a table/chart appearing,
  a screen transition that tells the story.
- Lags to cut: "Thinking…", spinners, "Agent is still working…", tool-call lists building up, blank/loading
  screens, false-start submits, duplicate takes.

A good beat is one narratable idea: *setup*, *connect data*, *question 1*, *answer 1*, *summary*, etc.
Aim for 5–8 beats for a ~3-minute demo.

To find exact timestamps, extract candidate frames and look:
```
for t in 30 60 90 120; do ffmpeg -v error -ss $t -i recording.mp4 -frames:v 1 -q:v 3 out/qa/f_$t.jpg; done
```
Read the frames, note where each action starts/ends and where each lag sits.

## Cut the lags via spans
A beat's `spans` list keeps only the ranges you want; the gaps between spans are dropped. Example — keep
the question bubble (48–52s) and the answer (70–92s), dropping the 52–70s "thinking" spinner:
```python
dict(id="question-1", spans=[(48, 52), (70, 92)], ...)
```
`build.py` trims each span and concatenates them, so the 18 seconds of dead air simply never appear.

## Duplicates & false starts
Recordings often contain retries (the same question asked twice, a submit that spun and was re-sent). Keep
the single cleanest take; drop the rest by simply not including their ranges in `spans`.

## Rule of thumb
If a stretch has no new information appearing on screen, cut it. The goal is a tight demo where something
is always happening and the narration never waits on a spinner.
