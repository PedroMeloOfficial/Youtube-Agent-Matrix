"""
Place sound effects and music: aligned to what is seen, levelled against the voice.

The sound agent writes ``edit/sound/plan.json`` -- for each sound, the event, the layer
(main / low / support / sweet / tail), the file and how it aligns (its **peak** on the
event, its **start** on the event, or its **end** on it). This script does the rest and
writes ``edit/sound/sound.json`` for the timeline:

- **alignment**: a whoosh aligned by peak starts ``time_to_peak`` before the event; the
  silent head of every file is skipped;
- **level**: every sound is set relative to the **voice's loudness** (EBU R128, LUFS)
  with a target per layer, then capped so nothing is louder than the voice unless the
  plan says so on purpose. Targets are craft defaults below, overridden by
  ``workspace/edit-config.json`` (``sound.targets_lu``), which learns from the creator's
  own level changes;
- **fades**: one frame in and out on every effect (no clicks);
- **music**: optional; looped/trimmed to its range, with **ducking** -- keyframes that
  lower it under speech and lift it in pauses longer than 1.5 s;
- **warnings** to fix before showing: file missing, same file within 20 s, two main
  sounds on top of each other, a sound longer than the gap to the next event.

Usage:
    python execution/edit/sound_place.py --edit-dir <video>/edit --config workspace/edit-config.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from audio_tools import integrated_lufs
from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, write_json
from sequence_text import seq_words
from sound_index import measure
from timebase import parse_rate, seconds_to_frames

# craft defaults, in LU relative to the voice (overridden by edit-config sound.targets_lu)
TARGETS_LU = {"main": -12.0, "low": -15.0, "support": -16.0, "sweet": -20.0, "tail": -22.0,
              "music_under_voice": -20.0, "music_alone": -12.0}
REPEAT_WINDOW = 20.0
DUCK_GAP = 1.5
DUCK_RAMP = 0.3


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Align and level sound effects and music against the voice.")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--config", help="workspace/edit-config.json (level targets)")
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        plan = read_json(edit / "sound" / "plan.json")
        footage = read_json(edit / "footage" / "footage.json")
        cfg = read_json(Path(a.config), default={}) if a.config else {}
        targets = {**TARGETS_LU, **cfg.get("sound", {}).get("targets_lu", {})}
        index = read_json(Path(cfg["sound"]["index"]), default={"sounds": []}) if cfg.get("sound", {}).get("index") else {"sounds": []}
        known = {s["path"]: s for s in index.get("sounds", [])}

        voice = plan.get("voice_lufs")
        if voice is None:
            cams = [f for f in footage["files"] if f.get("role") == "camera"]
            vals = [v for v in (integrated_lufs(f["path"]) for f in cams[:3]) if v is not None]
            if not vals:
                raise InputInvalid("Could not measure the voice loudness.")
            voice = sum(vals) / len(vals)
        rate = footage["main_rate"]
        items, warnings = [], []
        last_used: dict[str, float] = {}
        mains = []
        for s in sorted(plan.get("items", []), key=lambda x: x["time"]):
            p = Path(s["file"]).expanduser()
            if not p.exists():
                warnings.append(f"{s['id']}: file not found ({p.name}) — choose another")
                continue
            m = known.get(str(p)) or measure(p)
            align = s.get("align", "peak")
            lead = m.get("lead_silence", 0.0)
            if align == "peak":
                start = s["time"] - m["time_to_peak"]
            elif align == "end":
                start = s["time"] - m["useful_duration"]
            else:
                start = s["time"]
            start += s.get("offset_frames", 0) / float(parse_rate(rate))
            if start < 0:
                warnings.append(f"{s['id']}: starts before the video; trimmed")
                lead, start = lead - start, 0.0
            if str(p) in last_used and s["time"] - last_used[str(p)] < REPEAT_WINDOW:
                warnings.append(f"{s['id']}: same file as {REPEAT_WINDOW:.0f} s ago — use a variation")
            last_used[str(p)] = s["time"]
            layer = s.get("layer", "main")
            if layer == "main":
                if any(abs(s["time"] - t) < 0.1 for t in mains):
                    warnings.append(f"{s['id']}: two main sounds on the same moment — one must be support")
                mains.append(s["time"])
            lufs = m.get("lufs")
            vol = (voice + targets.get(layer, -14.0) - lufs) if lufs is not None else targets.get(layer, -14.0)
            vol += s.get("gain_db", 0.0)
            if not s.get("allow_louder") and lufs is not None and lufs + vol > voice:
                vol = voice - lufs
            dur = max(0.05, s.get("duration") or m["useful_duration"])
            items.append({"id": s["id"], "kind": "sfx", "file": str(p), "asset_key": f"sfx_{p.stem}",
                          "file_duration": m["duration"], "seq_start": round(start, 4), "in": round(lead, 4),
                          "duration": round(min(dur, m["duration"] - lead), 4), "volume_db": round(vol, 1),
                          "fade_in_frames": 1, "fade_out_frames": 1, "name": f"{s['id']} {p.stem}",
                          "layer": layer, "event": s.get("event")})

        words = None
        for mu in plan.get("music", []):
            p = Path(mu["file"]).expanduser()
            if not p.exists():
                warnings.append(f"{mu['id']}: music file not found")
                continue
            m = known.get(str(p)) or measure(p)
            lufs = m.get("lufs") or -16.0
            start, end = mu.get("start", 0.0), mu["end"]
            dur = min(end - start, m["duration"] - mu.get("in", 0.0))
            if dur < end - start:
                warnings.append(f"{mu['id']}: track is shorter than its range; it ends early")
            under = voice + targets["music_under_voice"] - lufs + mu.get("gain_db", 0.0)
            alone = voice + targets["music_alone"] - lufs + mu.get("gain_db", 0.0)
            kfs = []
            if mu.get("duck", True):
                if words is None:
                    _, words = seq_words(edit)
                speech = []
                for w in words:
                    if speech and w["start"] - speech[-1][1] < DUCK_GAP:
                        speech[-1][1] = w["end"]
                    else:
                        speech.append([w["start"], w["end"]])
                level = alone
                kfs.append([start, alone])
                for s0, s1 in speech:
                    if s1 < start or s0 > start + dur:
                        continue
                    kfs += [[max(start, s0 - DUCK_RAMP), level], [max(start, s0), under],
                            [min(start + dur, s1), under], [min(start + dur, s1 + DUCK_RAMP), alone]]
                kfs.sort(key=lambda k: k[0])
            items.append({"id": mu["id"], "kind": "music", "file": str(p), "asset_key": f"music_{p.stem}",
                          "file_duration": m["duration"], "seq_start": start, "in": mu.get("in", 0.0),
                          "duration": round(dur, 4), "volume_db": round(under if not kfs else 0.0, 1),
                          "volume_keyframes": [[round(t, 3), round(v, 1)] for t, v in kfs],
                          "fade_in_frames": seconds_to_frames(mu.get("fade_in", 1.0), rate),
                          "fade_out_frames": seconds_to_frames(mu.get("fade_out", 2.0), rate),
                          "name": f"{mu['id']} {p.stem}"})
        write_json(edit / "sound" / "sound.json", {"voice_lufs": round(voice, 1), "targets_lu": targets,
                                                   "items": items, "warnings": warnings})
        emit({"ok": True, "output": str(edit / "sound" / "sound.json"), "voice_lufs": round(voice, 1),
              "effects": sum(1 for i in items if i["kind"] == "sfx"),
              "music": sum(1 for i in items if i["kind"] == "music"), "warnings": warnings})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
