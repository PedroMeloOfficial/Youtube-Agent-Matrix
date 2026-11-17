"""
The approved cut, as text in **sequence time** -- what the motion, camera and sound
agents read.

After the cut is approved, everything downstream is planned against the edited video,
not the raw files. This script maps the word-timed transcript through the spine segments
and writes ``edit/motion/sequence.txt``:

- one sentence per line, with its sequence timecode and segment id;
- spoken notes that concern later stages, inline;
- at the end of each segment, the **exact cut time** -- an animation that starts or ends
  on a cut must use this time, not the word's, or it leaks frames into the neighbouring
  segment (the cut sits 0.1–0.3 s before the first word because of the edge padding).

``--words FROM TO`` prints the words of one sequence range with exact times, for placing
a trigger word precisely, without reading the whole transcript.

Usage:
    python execution/edit/sequence_text.py --edit-dir <video>/edit
    python execution/edit/sequence_text.py --edit-dir <video>/edit --words 62.0 75.5
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import ExecutionError, die, emit, install_excepthook, read_json, write_text
from timebase import clock


def seq_words(edit: Path):
    cuts = read_json(edit / "cuts" / "cuts.json")
    cache, out, seq = {}, [], 0.0
    for s in cuts["segments"]:
        if s["file"] not in cache:
            cache[s["file"]] = read_json(edit / "transcript" / f"{s['file']}.words.json")["words"]
        for w in cache[s["file"]]:
            mid = (w["start"] + w["end"]) / 2
            if s["in"] <= mid < s["out"]:
                out.append({"w": w["w"], "seg": s["id"],
                            "start": round(seq + max(0.0, w["start"] - s["in"]), 3),
                            "end": round(seq + min(s["out"], w["end"]) - s["in"], 3)})
        seq += s["out"] - s["in"]
    return cuts, out


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Transcript in sequence time, for planning after the cut.")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--words", nargs=2, type=float, metavar=("FROM", "TO"),
                    help="print exact word times for one sequence range instead")
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        cuts, words = seq_words(edit)
        if a.words:
            lo, hi = a.words
            emit({"ok": True, "words": [w for w in words if w["end"] > lo and w["start"] < hi]})
        notes = read_json(edit / "footage" / "notes.json", default={"notes": []})["notes"]
        lines = ["# Sequence transcript — times are SEQUENCE time (the edited video).",
                 "# ✂ marks each cut with its exact time: use it for anything that starts or ends on a cut.", ""]
        seq = 0.0
        for s in cuts["segments"]:
            seg_words = [w for w in words if w["seg"] == s["id"]]
            line, start = [], None
            for w in seg_words:
                start = w["start"] if start is None else start
                line.append(w["w"])
                if w["w"].endswith((".", "?", "!", "…")):
                    lines.append(f"[{clock(start)}] {s['id']}  {' '.join(line)}")
                    line, start = [], None
            if line:
                lines.append(f"[{clock(start)}] {s['id']}  {' '.join(line)}")
            for n in notes:
                if n["file"] == s["file"] and s["in"] - 30 <= n["start"] <= s["out"] + 30:
                    lines.append(f"    ✎ spoken note {n['id']}: {n['text']}")
            seq += s["out"] - s["in"]
            lines.append(f"    ✂ cut at {seq:.3f}s ({clock(seq)})")
        write_text(edit / "motion" / "sequence.txt", "\n".join(lines) + "\n")
        emit({"ok": True, "output": str(edit / "motion" / "sequence.txt"),
              "duration_seconds": round(seq, 2), "segments": len(cuts["segments"])})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
