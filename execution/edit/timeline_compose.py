"""
Assemble the timeline JSON that ``fcpxml_build.py`` turns into a Final Cut project.

Each editing stage owns one decision file; this script is the only place they meet:

    footage/footage.json   footage-agent   the media: rates, sizes, timecode origins
    cuts/cuts.json         cut-agent       spine segments (source time), markers, chapters,
                                           screen-recording placements
    motion/renders.json    motion-render   rendered animations, placed in sequence time
    camera/camera.json     camera-agent    keyframes per spine segment (camera_curves.py)
    sound/sound.json       sound-agent     sound effects and music (sound_place.py)

Whatever exists is included, so the same script builds the cuts-only delivery and the
final one. Times anchored to the source footage (markers, chapters, screen recordings)
are mapped to sequence time through the spine segments; an item whose source time falls
in a part that was cut out is reported, not silently moved.

Usage:
    python execution/edit/timeline_compose.py --edit-dir <video>/edit --out <video>/edit/timeline.json [--stage cuts|motion|final]
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, write_json

SPINE_FADE_FRAMES = 1  # craft default: 1 frame each side of every join removes clicks


def source_to_seq(segments, file_id: str, t: float):
    """Map a time in a source file to sequence time, or None if that moment was cut."""
    seq = 0.0
    for s in segments:
        if s["file"] == file_id and s["in"] <= t < s["out"]:
            return seq + (t - s["in"])
        seq += s["out"] - s["in"]
    return None


def compose(edit_dir: Path, stage: str) -> tuple[dict, list[str]]:
    footage = read_json(edit_dir / "footage" / "footage.json")
    cuts = read_json(edit_dir / "cuts" / "cuts.json")
    files = {f["id"]: f for f in footage["files"]}
    warnings: list[str] = []
    segs = cuts.get("segments", [])
    if not segs:
        raise InputInvalid("cuts.json has no segments.", fix="Run the cuts step first.")

    main = next(f for f in footage["files"] if f.get("role") == "camera")
    tl = {
        "project": cuts.get("project_name", f"{edit_dir.parent.name} {stage}"),
        "event": cuts.get("event_name", f"Matrix · {edit_dir.parent.name}"),
        "sequence": {"rate": footage["main_rate"], "width": main["width"], "height": main["height"]},
        "assets": {}, "spine": [], "connected": [], "markers": [],
    }

    def use(fid_or_path: str, key: str | None = None, **spec):
        if fid_or_path in files:
            f = files[fid_or_path]
            k = key or fid_or_path
            tl["assets"].setdefault(k, {
                "path": f["path"], "rate": f.get("rate") or footage["main_rate"],
                "width": f.get("width"), "height": f.get("height"), "duration": f["duration"],
                "has_video": f.get("has_video", True), "has_audio": f.get("has_audio", True),
                "audio_channels": f.get("audio_channels", 2), "audio_rate": f.get("audio_rate", 48000),
                "tc_start_frames": f.get("tc_start_frames", 0), "tc_drop": f.get("tc_drop", False),
            })
            return k
        k = key or Path(fid_or_path).stem
        tl["assets"].setdefault(k, {"path": fid_or_path, **spec})
        return k

    camera = read_json(edit_dir / "camera" / "camera.json", default={}) if stage == "final" else {}
    kf_by_seg = camera.get("keyframes", {})

    for s in segs:
        if s["file"] not in files:
            raise InputInvalid(f"Segment {s['id']} refers to unknown file {s['file']}.")
        item = {"id": s["id"], "asset": use(s["file"]), "in": s["in"], "out": s["out"],
                "name": f"{s['id']} {s.get('text', '')[:40]}".strip(),
                "fade_in_frames": SPINE_FADE_FRAMES, "fade_out_frames": SPINE_FADE_FRAMES,
                "markers": []}
        if s.get("volume_db") is not None:
            item["volume_db"] = s["volume_db"]
        if s["id"] in kf_by_seg:
            item["transform"] = {"keyframes": kf_by_seg[s["id"]]}
        tl["spine"].append(item)

    for m in cuts.get("markers", []):
        t = source_to_seq(segs, m["file"], m["time"])
        if t is None:
            # the moment was cut: pin the marker to the nearest remaining cut instead
            t = _nearest_cut(segs, m["file"], m["time"])
            warnings.append(f"Marker {m.get('id')} sits in a removed part; placed at the nearest cut.")
        tl["markers"].append({"seq_time": t, "text": m["text"], "kind": "todo", "type": m.get("type", "note")})
    for c in cuts.get("chapters", []):
        t = source_to_seq(segs, c["file"], c["time"])
        if t is None:
            warnings.append(f"Chapter '{c['title']}' starts in a removed part; skipped.")
            continue
        tl["markers"].append({"seq_time": t, "text": c["title"], "kind": "chapter"})

    for sc in cuts.get("screen", []):
        t = source_to_seq(segs, sc["camera_file"], sc["camera_time"])
        if t is None:
            warnings.append(f"Screen recording {sc.get('id')} starts in a removed part; skipped.")
            continue
        tl["connected"].append({"id": sc.get("id", "scr"), "kind": "screen", "asset": use(sc["file"]),
                                "seq_start": t, "in": sc["in"], "duration": sc["duration"]})

    if stage in ("motion", "final"):
        renders = read_json(edit_dir / "motion" / "renders.json", default={"items": []})
        for r in renders.get("items", []):
            if r.get("status") not in (None, "rendered", "approved"):
                continue
            key = use(r["file"], key=r["id"], rate=r["rate"], width=r["width"], height=r["height"],
                      duration=r["duration"], has_video=True, has_audio=False)
            tl["connected"].append({"id": r["id"], "kind": "motion" if r["format"] == "fullscreen" else "overlay",
                                    "asset": key, "seq_start": r["seq_start"], "in": 0, "duration": r["duration"],
                                    "name": f"{r['id']} {r.get('idea', '')[:30]}".strip()})
            if r.get("missing_assets"):
                tl["markers"].append({"seq_time": r["seq_start"], "kind": "todo",
                                      "text": f"asset missing in {r['id']}: {', '.join(r['missing_assets'])}"})
            for note in r.get("post_notes", []):
                tl["markers"].append({"seq_time": r["seq_start"], "kind": "todo", "text": f"{r['id']} post: {note}"})

    if stage == "final":
        sound = read_json(edit_dir / "sound" / "sound.json", default={"items": []})
        for snd in sound.get("items", []):
            key = use(snd["file"], key=snd["asset_key"], duration=snd["file_duration"], has_video=False,
                      has_audio=True, rate=footage["main_rate"], audio_channels=snd.get("channels", 2),
                      audio_rate=snd.get("audio_rate", 48000))
            item = {k: snd[k] for k in ("id", "kind", "seq_start", "in", "duration", "volume_db",
                                        "fade_in_frames", "fade_out_frames", "volume_keyframes", "name") if k in snd}
            item["asset"] = key
            tl["connected"].append(item)

    return tl, warnings


def _nearest_cut(segs, file_id: str, t: float) -> float:
    seq, best, best_d = 0.0, 0.0, None
    for s in segs:
        for edge_src, edge_seq in ((s["in"], seq), (s["out"], seq + s["out"] - s["in"])):
            if s["file"] == file_id:
                d = abs(edge_src - t)
                if best_d is None or d < best_d:
                    best, best_d = edge_seq, d
        seq += s["out"] - s["in"]
    return max(0.0, best - 0.001)


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Assemble the timeline JSON from the stage decision files.")
    ap.add_argument("--edit-dir", required=True, help="<video>/edit")
    ap.add_argument("--out", required=True, help="timeline JSON to write")
    ap.add_argument("--stage", choices=("cuts", "motion", "final"), default="cuts")
    a = ap.parse_args()
    try:
        tl, warnings = compose(Path(a.edit_dir).expanduser().resolve(), a.stage)
        write_json(Path(a.out), tl)
        dur = sum(Fraction(str(s["out"])) - Fraction(str(s["in"])) for s in tl["spine"])
        emit({"ok": True, "output": a.out, "stage": a.stage, "spine": len(tl["spine"]),
              "connected": len(tl["connected"]), "markers": len(tl["markers"]),
              "duration_seconds": round(float(dur), 2), "warnings": warnings})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
