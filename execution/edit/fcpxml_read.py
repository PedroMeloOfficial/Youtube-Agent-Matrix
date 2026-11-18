"""
Read back a project the creator adjusted in Final Cut Pro -- "the return trip".

After reviewing a delivery the creator may fix cuts by hand, add markers, nudge levels,
then **File > Export XML** into the video's ``edit/returns/`` folder. This script
reconstructs what they did, so the next steps start from *their* edit:

- the spine, as segments in source-file time (same schema as ``cuts/cuts.json``);
- their own markers (any marker whose text does not start with ``[C]``) as instructions,
  anchored to source time so they survive later versions;
- a diff against the previous cuts: segments added, removed, trimmed, moved;
- level changes on spine clips, as learnings for the edit profile.

**Their adjustments win.** This script never "corrects" them. What it cannot model it
reports instead of guessing: retimed clips, transitions, compound/multicam/sync clips,
J/L split edits, video effects, titles, and clips from files the matrix does not know.

Usage:
    python execution/edit/fcpxml_read.py <exported .fcpxml|.fcpxmld> --edit-dir <video>/edit --out <video>/edit/returns/return_v01.json
"""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, install_excepthook, path_from_url, read_json, write_json
from timebase import parse_fcp_time

UNSUPPORTED = {
    "transition": "transition",
    "ref-clip": "compound clip",
    "mc-clip": "multicam clip",
    "sync-clip": "synchronized clip",
    "title": "title",
    "audition": "audition",
}


def load(path: Path) -> ET.Element:
    p = Path(path).expanduser()
    if p.is_dir() and p.suffix == ".fcpxmld":
        p = p / "Info.fcpxml"
    if not p.exists():
        raise InputInvalid(f"{p} does not exist.", fix="Export from Final Cut with File > Export XML.")
    try:
        return ET.parse(p).getroot()
    except ET.ParseError as exc:
        raise InputInvalid(f"{p.name} is not readable XML: {exc}") from exc


def parse(root: ET.Element, footage: dict) -> dict:
    by_path = {str(Path(f["path"]).resolve()): f for f in footage["files"]}
    assets = {}
    for a in root.iter("asset"):
        rep = a.find("media-rep")
        src = rep.get("src") if rep is not None else None
        path = str(path_from_url(src).resolve()) if src else None
        assets[a.get("id")] = {"start": parse_fcp_time(a.get("start")), "path": path,
                               "file": by_path.get(path)}
    seqs = list(root.iter("sequence"))
    if not seqs:
        raise InputInvalid("No project/sequence found in this export.", fix="Export the project, not an event or a clip.")
    if len(seqs) > 1:
        warn_multi = f"{len(seqs)} projects in the export; only the first ({_proj_name(root)}) is read."
    else:
        warn_multi = None
    spine = seqs[0].find("spine")
    segments, markers, warnings, levels = [], [], [], []
    if warn_multi:
        warnings.append(warn_multi)
    seq_t = Fraction(0)
    n = 0
    for el in list(spine):
        tag = el.tag
        dur = parse_fcp_time(el.get("duration"))
        if tag in UNSUPPORTED:
            warnings.append(f"{UNSUPPORTED[tag]} at {float(seq_t):.2f}s in the spine — not modelled; kept as you left it, check by eye.")
            if tag != "transition":
                seq_t += dur
            continue
        if tag == "gap":
            warnings.append(f"gap of {float(dur):.2f}s at {float(seq_t):.2f}s — read as removed time.")
            seq_t += dur
            continue
        if tag not in ("asset-clip", "clip", "video"):
            warnings.append(f"<{tag}> at {float(seq_t):.2f}s not modelled.")
            seq_t += dur
            continue
        asset = assets.get(el.get("ref"))
        if asset is None or asset["file"] is None:
            warnings.append(f"clip '{el.get('name')}' at {float(seq_t):.2f}s comes from a file the matrix does not know.")
            seq_t += dur
            continue
        if el.find("timeMap") is not None or el.find("conform-rate") is not None:
            warnings.append(f"clip '{el.get('name')}' is retimed — speed changes are not modelled.")
        if el.get("audioStart") or el.get("audioDuration"):
            warnings.append(f"clip '{el.get('name')}' has a split edit (J/L cut) — kept as a plain cut in the model.")
        if el.find("filter-video") is not None:
            warnings.append(f"clip '{el.get('name')}' has a video effect — not modelled.")
        start = parse_fcp_time(el.get("start"))
        src_in = start - asset["start"]
        n += 1
        segments.append({"id": f"s{n:03d}", "file": asset["file"]["id"],
                         "in": round(float(src_in), 6), "out": round(float(src_in + dur), 6),
                         "seq_start": round(float(seq_t), 6)})
        vol = el.find("adjust-volume")
        if vol is not None and vol.get("amount") not in (None, "0dB"):
            levels.append({"segment": f"s{n:03d}", "amount": vol.get("amount")})
        for m in el:
            if m.tag in ("marker", "chapter-marker"):
                text = m.get("value", "")
                if text.startswith("[C]") or (m.tag == "chapter-marker" and m.get("note") == "matrix"):
                    continue  # the matrix's own markers
                local = parse_fcp_time(m.get("start"))
                markers.append({"file": asset["file"]["id"], "time": round(float(local - asset["start"]), 3),
                                "seq_time": round(float(seq_t + local - start), 3),
                                "kind": "chapter" if m.tag == "chapter-marker" else
                                ("todo" if m.get("completed") is not None else "standard"),
                                "done": m.get("completed") == "1", "text": text})
        seq_t += dur
    return {"project": _proj_name(root), "segments": segments, "creator_markers": markers,
            "level_changes": levels, "warnings": warnings,
            "duration_seconds": round(float(seq_t), 3)}


def _proj_name(root) -> str:
    p = root.find(".//project")
    return p.get("name") if p is not None else ""


def diff(old: list, new: list) -> dict:
    """Compare two segment lists by overlap in source time."""
    def ov(a, b):
        return a["file"] == b["file"] and min(a["out"], b["out"]) - max(a["in"], b["in"]) > 0.05
    added = [s["id"] for s in new if not any(ov(s, o) for o in old)]
    removed = [o["id"] for o in old if not any(ov(s, o) for s in new)]
    trimmed = []
    for s in new:
        match = next((o for o in old if ov(s, o)), None)
        if match and (abs(match["in"] - s["in"]) > 0.02 or abs(match["out"] - s["out"]) > 0.02):
            trimmed.append({"old": match["id"], "new": s["id"],
                            "in_delta": round(s["in"] - match["in"], 3),
                            "out_delta": round(s["out"] - match["out"], 3)})
    old_order = [o["id"] for o in old]
    order = [next((o["id"] for o in old if ov(s, o)), None) for s in new]
    order = [x for x in order if x]
    moved = order != sorted(order, key=old_order.index)
    return {"added": added, "removed": removed, "trimmed": trimmed, "reordered": moved}


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Reconstruct the creator's adjusted edit from a Final Cut export.")
    ap.add_argument("export", help="the .fcpxml or .fcpxmld the creator exported")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        footage = read_json(edit / "footage" / "footage.json")
        result = parse(load(Path(a.export)), footage)
        old = read_json(edit / "cuts" / "cuts.json", default={"segments": []}).get("segments", [])
        result["diff"] = diff(old, result["segments"])
        write_json(Path(a.out), result)
        emit({"ok": True, "output": a.out, "segments": len(result["segments"]),
              "creator_markers": len(result["creator_markers"]), "diff": result["diff"],
              "level_changes": result["level_changes"], "warnings": result["warnings"]})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
