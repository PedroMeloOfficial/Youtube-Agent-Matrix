"""
Turn the cut agent's decisions into frame-exact cuts, with every edge set on the audio.

The cut agent decides on **text**: which take, which sentence, where it starts and ends,
roughly. It writes ``edit/cuts/decisions.json``. This script does the arithmetic the
agent should not do by eye, and writes ``edit/cuts/cuts.json``:

1. **Snap to words.** Each edge goes to the nearest word boundary in the word-timed
   transcript.
2. **Refine on energy.** Whisper's word edges are off by ±0.1–0.2 s. The start moves to
   where the voice actually rises; the end to where it actually falls.
3. **Pad** by the profile's margin (craft default 0.10 s) so no syllable is clipped --
   but never into the neighbouring word that was cut away.
4. **Untranscribed filler at an edge** (voice glued to the edge word that the transcript
   did not write) is *kept* in the cut and gets a marker for the creator to check: from
   text alone it cannot be told whether cutting it would sound wrong.
5. **Frames.** Edges snap to whole frames of the main camera rate (``timebase.py``).

Segments flagged ``"locked": true`` (they came back from the creator's own Final Cut
edit) are passed through untouched: re-refining them would undo the creator's work.

decisions.json shape (written by cut-agent):
    {"segments": [{"id": "s001", "file": "cam01", "start": 12.4, "end": 19.8, "text": "first words…"}],
     "markers":  [{"file": "cam01", "time": 48.3, "type": "take_doubt", "text": "…"}],
     "chapters": [{"file": "cam01", "time": 12.4, "title": "…"}],
     "screen":   [{"id": "scr1", "file": "scr02", "camera_file": "cam01", "camera_time": 60.0, "in": 4.0, "duration": 12.0}],
     "padding": 0.10}

Usage:
    python execution/edit/cut_edges.py --edit-dir <video>/edit [--padding 0.1]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from audio_tools import envelope, speech_threshold
from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, read_pcm_mono, write_json
from timebase import frames_to_seconds, seconds_to_frames

HOP = 0.01
SEARCH = 0.25       # how far an edge may move to find where the voice really starts/ends
FILLER_MAX = 0.5    # longest untranscribed voice at an edge that is kept (and marked)
NEIGHBOUR_GAP = 0.03


def nearest_boundary(words, t: float, kind: str):
    key = "start" if kind == "start" else "end"
    return min(words, key=lambda w: abs(w[key] - t))


def refine(seg, words, env, thr, padding):
    start_w = nearest_boundary(words, seg["start"], "start")
    end_w = nearest_boundary(words, seg["end"], "end")
    if end_w["end"] <= start_w["start"]:
        raise InputInvalid(f"Segment {seg['id']} ends before it starts after snapping to words.")
    idx_s = words.index(start_w)
    idx_e = words.index(end_w)
    prev_end = words[idx_s - 1]["end"] if idx_s > 0 else 0.0
    next_start = words[idx_e + 1]["start"] if idx_e + 1 < len(words) else start_w["start"] + 1e9
    marker = []

    def voiced(t):
        i = int(t / HOP)
        return 0 <= i < len(env) and env[i] > thr

    # start: walk back from the word start while the voice is still there
    s = start_w["start"]
    t = s
    while t - HOP > max(prev_end + NEIGHBOUR_GAP, s - FILLER_MAX) and voiced(t - HOP):
        t -= HOP
    if s - t > SEARCH:  # more than word-edge error: something untranscribed was said
        marker.append({"time": t, "type": "filler_kept",
                       "text": "voice before the first word was kept (possible filler) — check"})
    s = max(prev_end + NEIGHBOUR_GAP, t - padding)

    # end: walk forward while the voice continues
    e = end_w["end"]
    t = e
    while t + HOP < min(next_start - NEIGHBOUR_GAP, e + FILLER_MAX) and voiced(t):
        t += HOP
    if t - e > SEARCH:
        marker.append({"time": e, "type": "filler_kept",
                       "text": "voice after the last word was kept (possible filler) — check"})
    e = min(next_start - NEIGHBOUR_GAP, t + padding)
    if e <= s:
        raise InputInvalid(f"Segment {seg['id']} collapsed while refining its edges.")
    return max(0.0, s), e, marker


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Frame-exact cuts from the cut agent's decisions, refined on the audio.")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--padding", type=float, help="seconds of air kept at each edge (default: decisions or 0.10)")
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        footage = read_json(edit / "footage" / "footage.json")
        dec = read_json(edit / "cuts" / "decisions.json")
        padding = a.padding if a.padding is not None else float(dec.get("padding", 0.10))
        files = {f["id"]: f for f in footage["files"]}
        rate = footage["main_rate"]
        cache = {}
        out_segs, markers = [], list(dec.get("markers", []))
        for seg in dec.get("segments", []):
            fid = seg["file"]
            if fid not in files:
                raise InputInvalid(f"Segment {seg['id']} refers to unknown file {fid}.")
            if seg.get("locked"):
                s, e = seg["start"], seg["end"]
            else:
                if fid not in cache:
                    words = read_json(edit / "transcript" / f"{fid}.words.json")["words"]
                    env = envelope(read_pcm_mono(Path(files[fid]["path"])))
                    cache[fid] = (words, env, speech_threshold(env))
                words, env, thr = cache[fid]
                if not words:
                    raise InputInvalid(f"No words transcribed for {fid}.")
                s, e, mk = refine(seg, words, env, thr, padding)
                markers += [{"file": fid, **m} for m in mk]
            fs, fe = seconds_to_frames(s, rate), seconds_to_frames(e, rate)
            if fe <= fs:
                raise InputInvalid(f"Segment {seg['id']} is shorter than one frame.")
            out_segs.append({"id": seg["id"], "file": fid,
                             "in": float(frames_to_seconds(fs, rate)), "out": float(frames_to_seconds(fe, rate)),
                             "text": seg.get("text", ""), "locked": bool(seg.get("locked"))})
        for i, m in enumerate(markers, 1):
            m.setdefault("id", f"m{i:03d}")
        raw = sum(f["duration"] for f in footage["files"] if f.get("role") == "camera")
        cut = sum(s["out"] - s["in"] for s in out_segs)
        result = {"rate": rate, "padding": padding, "segments": out_segs, "markers": markers,
                  "chapters": dec.get("chapters", []), "screen": dec.get("screen", []),
                  "project_name": dec.get("project_name"), "event_name": dec.get("event_name")}
        write_json(edit / "cuts" / "cuts.json", result)
        emit({"ok": True, "output": str(edit / "cuts" / "cuts.json"), "segments": len(out_segs),
              "raw_minutes": round(raw / 60, 2), "cut_minutes": round(cut / 60, 2),
              "markers": len(markers),
              "filler_markers": sum(1 for m in markers if m.get("type") == "filler_kept")})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
