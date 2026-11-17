"""
Inventory the raw footage of one video: what each file is, in recording order.

Reads every media file with ffprobe -- the creator's files are only ever read -- and
writes ``footage.json`` in the video's ``edit/footage/`` folder. Each entry carries what
the later steps and the FCPXML generator need, exactly:

- the real frame rate as a fraction (``30000/1001``), never a rounded decimal;
- resolution, duration, codec, audio channels and sample rate;
- the timecode origin (``tc_start_frames``) -- a clip ``start`` is measured from it;
- the recording date (metadata, else file modification time) used to order the files;
- **alerts**: unreadable file, video without audio, frame rate differing from the main
  camera, and variable frame rate (common in screen recordings, bad for sync).

The first camera file (by recording order) is the **main camera**: every time in the
project is expressed in its files' own time. Roles can be overridden with ``--role``.

No credentials, no network, no quota.

Usage:
    python execution/edit/probe_footage.py /abs/path/raw1.mov /abs/path/raw2.mov --out <video>/edit/footage/footage.json
    python execution/edit/probe_footage.py --dir "/abs/path/Raw" --out ...
    python execution/edit/probe_footage.py --dir ... --role screen=/abs/path/screen.mov --out ...
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, ffprobe_json, install_excepthook, write_json
from timebase import parse_rate, timecode_to_frames

MEDIA = {".mov", ".mp4", ".m4v", ".mxf", ".mkv", ".avi", ".mts", ".m2ts",
         ".wav", ".aif", ".aiff", ".mp3", ".m4a", ".flac", ".caf"}


def _rate(stream) -> Fraction | None:
    for key in ("r_frame_rate", "avg_frame_rate"):
        v = stream.get(key)
        if v and v not in ("0/0", "0/1"):
            try:
                return parse_rate(v)
            except (ValueError, ZeroDivisionError):
                continue
    return None


def probe(path: Path) -> dict:
    entry = {"path": str(path), "name": path.name, "alerts": []}
    try:
        info = ffprobe_json(path)
    except ExecutionError as exc:
        entry.update(readable=False)
        entry["alerts"].append(f"unreadable: {exc.message}")
        return entry
    entry["readable"] = True
    fmt = info.get("format", {})
    streams = info.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"
              and not s.get("disposition", {}).get("attached_pic")), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    entry["duration"] = float(fmt.get("duration") or (v or a or {}).get("duration") or 0)
    entry["has_video"] = v is not None
    entry["has_audio"] = a is not None
    if v:
        r = _rate(v)
        avg = v.get("avg_frame_rate")
        entry.update(
            rate=f"{r.numerator}/{r.denominator}" if r else None,
            width=v.get("width"), height=v.get("height"), codec=v.get("codec_name"),
            pix_fmt=v.get("pix_fmt"),
            alpha=v.get("pix_fmt", "").startswith(("yuva", "rgba", "argb", "bgra", "abgr", "gbrap", "ya")),
        )
        try:
            if r and avg and avg not in ("0/0",) and abs(float(parse_rate(avg)) - float(r)) > 0.01:
                entry["vfr"] = True
                entry["alerts"].append(f"variable frame rate (nominal {float(r):.3f}, average {float(parse_rate(avg)):.3f}) — sync and import can drift")
        except (ValueError, ZeroDivisionError):
            pass
    if a:
        entry.update(audio_channels=int(a.get("channels", 2)), audio_rate=int(a.get("sample_rate", 48000)))
    elif v:
        entry["alerts"].append("video without audio — it cannot be synced by waveform")
    tags = {**fmt.get("tags", {}), **((v or {}).get("tags", {}))}
    for s in streams:
        if s.get("codec_type") == "data" and "timecode" in s.get("tags", {}):
            tags.setdefault("timecode", s["tags"]["timecode"])
    tc = tags.get("timecode")
    entry["tc_start_frames"], entry["tc_drop"] = 0, False
    if tc and entry.get("rate"):
        try:
            entry["tc_start_frames"], entry["tc_drop"] = timecode_to_frames(tc, entry["rate"])
            entry["timecode"] = tc
        except ValueError:
            entry["alerts"].append(f"unreadable timecode '{tc}' — treated as 00:00:00:00")
    created = tags.get("creation_time") or tags.get("com.apple.quicktime.creationdate")
    if created:
        entry["recorded_at"] = created
        entry["recorded_at_source"] = "metadata"
    else:
        entry["recorded_at"] = datetime.fromtimestamp(os.path.getmtime(path), timezone.utc).isoformat()
        entry["recorded_at_source"] = "file modification time"
    return entry


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Inventory raw footage (read-only) into footage.json.")
    ap.add_argument("files", nargs="*", help="absolute paths of media files")
    ap.add_argument("--dir", help="folder of raw footage (read-only; not recursive)")
    ap.add_argument("--role", action="append", default=[],
                    help="override a role: screen=/abs/file, external_audio=/abs/file, camera=/abs/file")
    ap.add_argument("--out", required=True, help="footage.json to write")
    a = ap.parse_args()
    try:
        paths = [Path(p).expanduser() for p in a.files]
        if a.dir:
            d = Path(a.dir).expanduser()
            if not d.is_dir():
                raise InputInvalid(f"{d} is not a folder.")
            paths += [p for p in sorted(d.iterdir()) if p.suffix.lower() in MEDIA and not p.name.startswith(".")]
        if not paths:
            raise InputInvalid("No media files given.", fix="Pass file paths or --dir with the raw footage folder.")
        for p in paths:
            if not p.is_absolute():
                raise InputInvalid(f"Use absolute paths: {p}")
            if not p.exists():
                raise InputInvalid(f"{p} does not exist.")
        overrides = {}
        for r in a.role:
            if "=" not in r:
                raise InputInvalid(f"--role expects role=/abs/path, got {r!r}")
            role, p = r.split("=", 1)
            overrides[str(Path(p).expanduser())] = role
        files = [probe(p) for p in paths]
        files.sort(key=lambda f: (f.get("recorded_at", ""), f["name"]))
        for f in files:
            if f["path"] in overrides:
                f["role"] = overrides[f["path"]]
            elif not f.get("has_video"):
                f["role"] = "external_audio"
            elif f.get("vfr") or (f.get("has_video") and not f.get("has_audio")):
                f["role"] = "screen"
            else:
                f["role"] = "camera"
        cams = [f for f in files if f.get("role") == "camera" and f.get("readable")]
        if not cams:
            raise InputInvalid("No camera file found (video with audio).", fix="Mark one with --role camera=/abs/path.")
        main_rate = cams[0]["rate"]
        for i, f in enumerate(files, 1):
            f["id"] = {"camera": "cam", "screen": "scr", "external_audio": "ext"}.get(f["role"], "src") + f"{i:02d}"
            if f.get("rate") and f.get("role") == "camera" and f["rate"] != main_rate:
                f["alerts"].append(f"frame rate {f['rate']} differs from the main camera ({main_rate})")
        out = {"main_rate": main_rate, "main_resolution": [cams[0]["width"], cams[0]["height"]],
               "files": files}
        write_json(Path(a.out), out)
        emit({"ok": True, "output": a.out, "files": len(files), "main_rate": main_rate,
              "total_minutes": round(sum(f.get("duration", 0) for f in files if f.get("role") == "camera") / 60, 1),
              "alerts": [f"{f['name']}: {al}" for f in files for al in f["alerts"]]})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
