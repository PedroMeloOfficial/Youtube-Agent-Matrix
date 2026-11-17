"""
Index the creator's sound-effect library so sounds can be chosen by measurement.

Walks the library folder named in ``workspace/edit-config.json`` (read-only -- files are
never moved, renamed or copied) and measures every audio file: duration, **useful
duration** (without leading/trailing silence), **time to peak** (a whoosh peaking at
0.4 s must start 0.4 s before the event), attack shape (sharp / swell), brightness
(spectral centroid, to separate layers: low under, bright on top) and integrated
loudness. Categories come from the first folder level (``whoosh/``, ``impact/`` …).

The index is incremental: unchanged files (same size and mtime) are not re-measured.
Writes ``workspace/edit-profile/sound-index.json``.

Usage:
    python execution/edit/sound_index.py --library "/abs/path/SFX" --out workspace/edit-profile/sound-index.json
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from audio_tools import envelope, integrated_lufs
from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, read_pcm_mono, require_module, write_json

AUDIO = {".wav", ".aif", ".aiff", ".mp3", ".m4a", ".flac", ".caf", ".ogg"}
RATE = 22050


def measure(path: Path) -> dict:
    np = require_module("numpy")
    pcm = read_pcm_mono(path, RATE)
    if len(pcm) == 0:
        return {"error": "no audio"}
    env = envelope(pcm, RATE)
    peak_db = float(env.max())
    on = np.where(env > peak_db - 40)[0]
    first, last = (int(on[0]), int(on[-1])) if len(on) else (0, len(env) - 1)
    peak_i = int(np.argmax(env))
    rise = (peak_i - first) * 0.01
    spec = np.abs(np.fft.rfft(pcm[: RATE * 2] * np.hanning(min(len(pcm), RATE * 2))))
    freqs = np.fft.rfftfreq(min(len(pcm), RATE * 2), 1 / RATE)
    centroid = float((spec * freqs).sum() / (spec.sum() + 1e-9))
    return {"duration": round(len(pcm) / RATE, 3), "lead_silence": round(first * 0.01, 3),
            "useful_duration": round((last - first) * 0.01, 3), "time_to_peak": round(rise, 3),
            "shape": "sharp" if rise < 0.03 else ("swell" if rise > 0.25 else "medium"),
            "brightness_hz": int(centroid), "lufs": integrated_lufs(path)}


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Measure and index a sound-effect library (read-only).")
    ap.add_argument("--library", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        lib = Path(a.library).expanduser().resolve()
        if not lib.is_dir():
            raise InputInvalid(f"{lib} is not a folder.", fix="Set sound.library in workspace/edit-config.json.")
        old = {e["path"]: e for e in read_json(Path(a.out), default={"sounds": []})["sounds"]}
        sounds, measured = [], 0
        for root, _, names in os.walk(lib):
            for n in sorted(names):
                p = Path(root) / n
                if p.suffix.lower() not in AUDIO or n.startswith("."):
                    continue
                st = p.stat()
                prev = old.get(str(p))
                if prev and prev.get("size") == st.st_size and prev.get("mtime") == int(st.st_mtime):
                    sounds.append(prev)
                    continue
                rel = p.relative_to(lib)
                entry = {"path": str(p), "name": p.stem, "category": rel.parts[0] if len(rel.parts) > 1 else "uncategorized",
                         "size": st.st_size, "mtime": int(st.st_mtime), **measure(p)}
                entry["favorite"] = prev.get("favorite", False) if prev else False
                sounds.append(entry)
                measured += 1
        cats = {}
        for s in sounds:
            cats[s["category"]] = cats.get(s["category"], 0) + 1
        write_json(Path(a.out), {"library": str(lib), "sounds": sounds})
        emit({"ok": True, "output": a.out, "sounds": len(sounds), "newly_measured": measured, "categories": cats})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
