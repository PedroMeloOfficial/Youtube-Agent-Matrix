"""
Build the first-time test project: a short Final Cut delivery from synthetic media.

Before a delivery format is trusted with a real video (first run on a machine, or after a
Final Cut update), the creator imports this and checks it by eye -- see
references/editing/delivery-fcpxml.md §9. It exercises everything a real delivery uses:
three cuts on a camera clip with timecode 01:00:00:00, a screen-recording lane, a
full-screen animation, an alpha overlay, one camera move in scale and position, two sound
effects (one stacked on a second lane), ducked music, a to-do marker and a chapter marker.

Everything is created inside ``<edit-dir>/test-media/`` (its own footage/cuts/… folders),
never next to the creator's footage, and the delivery goes to ``<edit-dir>/deliveries/`` as
``format-test_vNN.fcpxml``.

Usage:
    python execution/edit/test_project.py --edit-dir <video>/edit [--rate 30000/1001] [--size 1920x1080]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from common import ExecutionError, die, emit, install_excepthook, write_json

HERE = Path(__file__).resolve().parent


def step(script, *args):
    proc = subprocess.run([sys.executable, str(HERE / script), *map(str, args)], capture_output=True, text=True)
    try:
        out = json.loads(proc.stdout)
    except ValueError as exc:
        raise ExecutionError(f"{script} printed no JSON.", details={"stderr": proc.stderr[-500:]}) from exc
    if not out.get("ok"):
        raise ExecutionError(f"{script} failed: {out.get('error', {}).get('message')}", details=out.get("error", {}))
    return out


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Synthetic test project to validate Final Cut delivery.")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--rate", default="30000/1001")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--version", help="FCPXML version (default: detected)")
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        t = edit / "test-media"
        media = step("make_test_media.py", "--out", t / "media", "--rate", a.rate, "--size", a.size)["files"]
        step("probe_footage.py", "--out", t / "footage" / "footage.json",
             "--role", f"camera={media['camera']}", "--role", f"screen={media['motion']}", media["camera"], media["motion"])
        write_json(t / "cuts" / "cuts.json", {
            "project_name": "Matrix format test", "event_name": "Matrix · format test",
            "segments": [{"id": "s001", "file": "cam01", "in": 0.5, "out": 3.2, "text": "frames 15-95"},
                         {"id": "s002", "file": "cam01", "in": 4.0, "out": 7.1, "text": "frames 120-212"},
                         {"id": "s003", "file": "cam01", "in": 8.0, "out": 11.5, "text": "frames 240-344"}],
            "markers": [{"id": "m001", "file": "cam01", "time": 5.0, "type": "test",
                         "text": "to-do marker: tick me off in the Timeline Index"}],
            "chapters": [{"file": "cam01", "time": 0.5, "title": "Chapter 1"},
                         {"file": "cam01", "time": 8.0, "title": "Chapter 2"}],
            "screen": [{"id": "scr1", "file": "scr02", "camera_file": "cam01", "camera_time": 4.4, "in": 0, "duration": 1.5}]})
        write_json(t / "motion" / "renders.json", {"items": [
            {"id": "mo01", "file": media["motion"], "format": "fullscreen", "rate": a.rate,
             "width": int(a.size.split("x")[0]), "height": int(a.size.split("x")[1]), "duration": 1.5,
             "seq_start": 0.6, "status": "rendered", "idea": "full-screen test"},
            {"id": "mo02", "file": media["overlay"], "format": "overlay", "rate": a.rate,
             "width": int(a.size.split("x")[0]), "height": int(a.size.split("x")[1]), "duration": 2.5,
             "seq_start": 6.2, "status": "rendered", "idea": "overlay test: amber bar, transparent around it"}]})
        write_json(t / "camera" / "plan.json", {"base": {"closed_scale": 1.25, "creep": 0.0},
                   "segment_overrides": {"s001": {"plane": "open"}, "s002": {"plane": "open"}, "s003": {"plane": "open"}},
                   "moves": [{"id": "cam01", "type": "arrive", "segment": "s002", "from": "right", "duration": 0.8, "amount": 0.3}]})
        (t / "transcript").mkdir(parents=True, exist_ok=True)
        words = [{"w": f"w{i}", "start": 0.5 + i * 0.5, "end": 0.9 + i * 0.5, "p": 1.0} for i in range(22)]
        write_json(t / "transcript" / "cam01.words.json", {"file": "cam01", "words": words})
        write_json(t / "sound" / "plan.json", {"voice_lufs": -16.0,
                   "items": [{"id": "sfx01", "time": 0.6, "file": media["sfx"], "layer": "main", "align": "start"},
                             {"id": "sfx02", "time": 0.75, "file": media["sfx"], "layer": "support", "align": "start"}],
                   "music": [{"id": "mus01", "file": media["music"], "start": 0.0, "end": 9.0, "duck": True}]})
        step("camera_curves.py", "--edit-dir", t)
        step("sound_place.py", "--edit-dir", t)
        step("timeline_compose.py", "--edit-dir", t, "--out", t / "timeline.json", "--stage", "final")
        args = [t / "timeline.json", "--out-dir", edit / "deliveries", "--stem", "format-test"]
        if a.version:
            args += ["--version", a.version]
        built = step("fcpxml_build.py", *args)
        emit({"ok": True, "delivery": built["output"], "fcpxml_version": built["fcpxml_version"],
              "validated": built["validated"], "reason": built.get("reason"),
              "check_in_final_cut": [
                  "It imports without errors (File → Import → XML…).",
                  "Three clips; each starts on the frame number written in its name.",
                  "Lane above: a blue 'MOTION' card at the start, an amber bar mid-way with the clip visible around it.",
                  "Clip 2 arrives zoomed and slides in from the right, settling at 100%.",
                  "Two short beeps at the start on two lanes below; a low tone (music) that dips while the words play.",
                  "A to-do marker in clip 2 and two chapter markers."]})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
