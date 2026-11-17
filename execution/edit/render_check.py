"""
Check a rendered animation and register it for the timeline -- or refuse it.

Every render is checked before it can reach a delivery:
- the file opens and has video;
- resolution equals the sequence's (or ``--width/--height``);
- frame rate is **exactly** the sequence rate (``30000/1001`` is not ``30``);
- frame count equals the frames the item occupies in the sequence (± 0: a render one
  frame long leaks into the next shot);
- overlays carry an alpha channel in a format Final Cut reads (ProRes 4444 in a MOV);
  full-screen renders are opaque MP4/MOV.

Only a render that passes is written into ``edit/motion/renders.json`` (owned by the
motion-render agent), with its sequence start, format and version. The output names are
versioned by the caller (``mo03_v02.mov``); this script never overwrites a render.

Usage:
    python execution/edit/render_check.py --edit-dir <video>/edit --id mo03 --file /abs/mo03_v01.mov \
        --format overlay --seq-start 62.462 --frames 150 [--idea "…"] [--missing-asset "logo X"] [--post-note "…"]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, ffprobe_json, install_excepthook, read_json, write_json
from timebase import frames_to_seconds, parse_rate

ALPHA_FMTS = ("yuva", "rgba", "argb", "bgra", "abgr", "gbrap")


def check(path: Path, fmt: str, rate, width: int, height: int, frames: int):
    info = ffprobe_json(path)
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    problems = []
    if v is None:
        raise InputInvalid(f"{path.name} has no video stream.")
    if (v.get("width"), v.get("height")) != (width, height):
        problems.append(f"resolution {v.get('width')}x{v.get('height')}, expected {width}x{height}")
    r = parse_rate(v.get("r_frame_rate", "0/1")) if v.get("r_frame_rate") not in (None, "0/0") else None
    if r != parse_rate(rate):
        problems.append(f"frame rate {v.get('r_frame_rate')}, expected {rate}")
    n = v.get("nb_frames")
    if n is None or n == "N/A":
        dur = float(v.get("duration") or info["format"].get("duration") or 0)
        n = round(dur * float(parse_rate(rate)))
    n = int(n)
    if n != frames:
        problems.append(f"{n} frames, expected {frames}")
    pix = v.get("pix_fmt", "")
    if fmt == "overlay":
        if not pix.startswith(ALPHA_FMTS):
            problems.append(f"overlay without alpha (pix_fmt {pix})")
        if v.get("codec_name") != "prores" or path.suffix.lower() != ".mov":
            problems.append("overlay must be ProRes 4444 in a .mov for Final Cut")
    return problems, {"codec": v.get("codec_name"), "pix_fmt": pix, "frames": n}


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Verify a rendered animation and register it for the timeline.")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--format", choices=("fullscreen", "overlay"), required=True)
    ap.add_argument("--seq-start", type=float, required=True)
    ap.add_argument("--frames", type=int, required=True)
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--idea", default="")
    ap.add_argument("--exit-direction", default="")
    ap.add_argument("--missing-asset", action="append", default=[])
    ap.add_argument("--post-note", action="append", default=[])
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        footage = read_json(edit / "footage" / "footage.json")
        main_file = next(f for f in footage["files"] if f.get("role") == "camera")
        rate = footage["main_rate"]
        w, h = a.width or main_file["width"], a.height or main_file["height"]
        path = Path(a.file).expanduser().resolve()
        if not path.exists():
            raise InputInvalid(f"{path} does not exist.")
        problems, info = check(path, a.format, rate, w, h, a.frames)
        if problems:
            emit({"ok": False, "error": {"code": "render_rejected", "message": f"{a.id} rejected",
                                         "fix": problems}}, 1)
        reg_path = edit / "motion" / "renders.json"
        reg = read_json(reg_path, default={"items": []})
        version = 1 + max([i.get("version", 0) for i in reg["items"] if i["id"] == a.id] or [0])
        reg["items"] = [i for i in reg["items"] if i["id"] != a.id]
        reg["items"].append({"id": a.id, "file": str(path), "format": a.format, "rate": rate,
                             "width": w, "height": h, "duration": float(frames_to_seconds(a.frames, rate)),
                             "frames": a.frames, "seq_start": a.seq_start, "version": version,
                             "status": "rendered", "idea": a.idea, "exit_direction": a.exit_direction,
                             "missing_assets": a.missing_asset, "post_notes": a.post_note, **info})
        reg["items"].sort(key=lambda i: i["seq_start"])
        write_json(reg_path, reg)
        emit({"ok": True, "registered": a.id, "version": version, **info})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
