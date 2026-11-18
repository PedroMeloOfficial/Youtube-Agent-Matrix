"""
Sync a screen recording or an external microphone to the main camera, by its sound.

Cross-correlates the audio of each non-camera file against every camera file and writes
``edit/footage/sync.json`` with, per file: the camera file it belongs to, the offset
(``camera_time = file_time + offset``) and a confidence (0..1, the correlation over the
overlap). A screen recording is usually partial: the offset says *where* inside the camera
file it starts.

Below the confidence floor (0.3) the result is **not used**: the file is listed as
unsynced with the reason, and the editor asks the creator for help instead of guessing.
A file without audio cannot be synced this way at all.

Correlation runs at 4 kHz to keep long files cheap; the result is precise to well under a
frame.

Usage:
    python execution/edit/sync_audio.py --footage <video>/edit/footage/footage.json --out <video>/edit/footage/sync.json
"""

from __future__ import annotations

import argparse
from pathlib import Path

from audio_tools import cross_correlate
from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, read_pcm_mono, write_json

RATE = 4000
FLOOR = 0.3


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Sync screen recordings and external audio to the camera by waveform.")
    ap.add_argument("--footage", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        footage = read_json(Path(a.footage))
        cams = [f for f in footage["files"] if f.get("role") == "camera" and f.get("has_audio")]
        others = [f for f in footage["files"] if f.get("role") in ("screen", "external_audio")]
        if not cams:
            raise InputInvalid("No camera file with audio to sync against.")
        cam_pcm = {c["id"]: read_pcm_mono(Path(c["path"]), RATE) for c in cams}
        results = []
        for f in others:
            if not f.get("has_audio"):
                results.append({"file": f["id"], "synced": False, "reason": "no audio track — place it by hand or tell me where it starts"})
                continue
            pcm = read_pcm_mono(Path(f["path"]), RATE)
            best = None
            for cid, ref in cam_pcm.items():
                lag, conf = cross_correlate(ref, pcm, RATE)
                if best is None or conf > best[2]:
                    best = (cid, lag, conf)
            cid, lag, conf = best
            ok = conf >= FLOOR
            results.append({"file": f["id"], "camera_file": cid, "offset": round(lag, 4),
                            "confidence": round(conf, 3), "synced": ok,
                            **({} if ok else {"reason": "weak match — confirm one distinctive word in both files"})})
        write_json(Path(a.out), {"rule": "camera_time = file_time + offset", "files": results})
        emit({"ok": True, "output": a.out, "synced": sum(r["synced"] for r in results),
              "unsynced": [r["file"] for r in results if not r["synced"]]})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
