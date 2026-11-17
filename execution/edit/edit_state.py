"""
Read and update a video's editing state without opening whole files.

Each editing stage owns its own decision file (``cuts/cuts.json``, ``motion/plan.json``,
…). ``edit-state.json`` holds only what the **editor skill** tracks across sessions: the
status of each stage, pending requests, deliveries. This script is the one way the
editor reads all of it -- a long video's files run to tens of thousands of tokens, and
reading them whole on every turn is pure waste.

Commands:
    status                    stages, pending requests, alerts, deliveries, learnings count
    show <block>              a compact summary of one block: footage | cuts | notes | motion |
                              renders | camera | sound | deliveries   (--json for the full block)
    item <id>                 one item by id: s012, m004, mo03, cam07, sfx12, n02, p01
    --init <slug>             create edit-state.json for a new video
    --stage <stage>=<status>  set a stage's status
    --pending <stage> <text>  record a request not yet applied
    --resolve <id>            mark a pending request done
    --delivery <path>         record a delivered file
    --set <key> <value>       set a top-level field (profile, tools.hyperframes, …)

Statuses: pending · in_progress · awaiting_review · done · not_needed.

**Alerts** are computed, not stored: a stage that was approved before the stage it depends
on changed (e.g. the cut changed after the motion plan) is flagged as stale.

Usage:
    python execution/edit/edit_state.py <video>/edit status
    python execution/edit/edit_state.py <video>/edit show cuts
    python execution/edit/edit_state.py <video>/edit --stage cuts=awaiting_review
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, write_json

STAGES = ["briefing", "footage", "cuts", "motion_plan", "assets", "motion_render", "camera", "sound"]
STATUSES = {"pending", "in_progress", "awaiting_review", "done", "not_needed"}

# stage -> (decision file it owns, stages whose files it was built from)
DEPENDS = {
    "cuts": ("cuts/cuts.json", ["footage"]),
    "motion_plan": ("motion/plan.json", ["cuts"]),
    "motion_render": ("motion/renders.json", ["motion_plan"]),
    "camera": ("camera/camera.json", ["cuts", "motion_render"]),
    "sound": ("sound/sound.json", ["cuts", "motion_render", "camera"]),
}
FILES = {"footage": "footage/footage.json", "cuts": "cuts/cuts.json", "notes": "footage/notes.json",
         "motion": "motion/plan.json", "renders": "motion/renders.json",
         "camera": "camera/camera.json", "sound": "sound/sound.json"}


def state_path(edit: Path) -> Path:
    return edit / "edit-state.json"


def load(edit: Path) -> dict:
    p = state_path(edit)
    if not p.exists():
        raise InputInvalid("This video has no editing state yet.", fix="Start it with `/yt edit` (the editor runs --init).")
    return read_json(p)


def alerts(edit: Path, st: dict):
    out = []
    for stage, (own, deps) in DEPENDS.items():
        own_p = edit / own
        if st["stages"].get(stage) not in ("done", "awaiting_review") or not own_p.exists():
            continue
        for d in deps:
            dep_file = edit / (DEPENDS[d][0] if d in DEPENDS else FILES.get(d, ""))
            if dep_file.exists() and dep_file.stat().st_mtime > own_p.stat().st_mtime + 1:
                out.append(f"{stage} was built before {d} last changed — recheck or rebuild {stage}")
    return out


def learnings_open(edit: Path) -> int:
    p = edit / "learnings.md"
    if not p.exists():
        return 0
    return sum(1 for ln in p.read_text(encoding="utf-8").splitlines() if ln.startswith("- [ ]"))


def summarize(edit: Path, block: str):
    if block == "deliveries":
        return load(edit).get("deliveries", [])
    data = read_json(edit / FILES[block], default={})
    if block == "footage":
        return [{k: f.get(k) for k in ("id", "role", "name", "rate", "width", "height", "duration", "alerts")}
                for f in data.get("files", [])]
    if block == "cuts":
        segs = data.get("segments", [])
        return {"segments": len(segs), "minutes": round(sum(s["out"] - s["in"] for s in segs) / 60, 2),
                "markers": len(data.get("markers", [])), "chapters": [c["title"] for c in data.get("chapters", [])],
                "first": [f"{s['id']} {s['file']} {s['in']:.2f}-{s['out']:.2f} {s.get('text', '')[:50]}" for s in segs[:8]]}
    if block == "notes":
        return [f"{n['id']} {n['file']} {n['start']:.1f}s [{n['confidence']}] {n['text'][:80]}" for n in data.get("notes", [])]
    if block in ("motion", "renders", "camera", "sound"):
        items = data.get("items", data.get("moves", []))
        return [f"{i.get('id')} {i.get('status', '')} {i.get('seq_start', i.get('time', ''))} "
                f"{(i.get('idea') or i.get('what') or i.get('name') or '')[:60]}" for i in items]
    return data


def find_item(edit: Path, item_id: str):
    prefix = re.match(r"[a-z]+", item_id).group(0)
    where = {"s": ("cuts", "segments"), "m": ("cuts", "markers"), "n": ("notes", "notes"),
             "mo": ("motion", "items"), "cam": ("camera", "moves"), "sfx": ("sound", "items"),
             "mus": ("sound", "items"), "p": (None, "pending")}.get(prefix)
    if not where:
        raise InputInvalid(f"Unknown id prefix in {item_id!r}.")
    block, key = where
    data = load(edit) if block is None else read_json(edit / FILES[block], default={})
    for it in data.get(key, []):
        if it.get("id") == item_id:
            return it
    raise InputInvalid(f"{item_id} not found.")


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Editing state: status, summaries and small updates.")
    ap.add_argument("edit_dir")
    ap.add_argument("command", nargs="?", choices=("status", "show", "item"))
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--init", metavar="SLUG")
    ap.add_argument("--stage", metavar="STAGE=STATUS")
    ap.add_argument("--pending", nargs=2, metavar=("STAGE", "TEXT"))
    ap.add_argument("--resolve", metavar="ID")
    ap.add_argument("--delivery", metavar="PATH")
    ap.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"))
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        if a.init:
            if state_path(edit).exists():
                raise InputInvalid("This video already has an editing state; nothing was overwritten.",
                                   fix=f"Run `{Path(sys.argv[0]).name} {a.edit_dir} status`.")
            st = {"video": a.init, "created": date.today().isoformat(), "profile": "default", "tools": {},
                  "stages": {s: "pending" for s in STAGES}, "pending": [], "deliveries": []}
            write_json(state_path(edit), st)
            emit({"ok": True, "initialized": str(state_path(edit))})
        st = load(edit)
        changed = False
        if a.stage:
            stage, _, status = a.stage.partition("=")
            if stage not in STAGES or status not in STATUSES:
                raise InputInvalid(f"Bad --stage {a.stage!r}.", fix=f"stages: {STAGES}; statuses: {sorted(STATUSES)}")
            st["stages"][stage] = status
            changed = True
        if a.pending:
            n = 1 + max([int(p["id"][1:]) for p in st["pending"]] or [0])
            st["pending"].append({"id": f"p{n:02d}", "stage": a.pending[0], "text": a.pending[1],
                                  "date": date.today().isoformat(), "done": False})
            changed = True
        if a.resolve:
            for p in st["pending"]:
                if p["id"] == a.resolve:
                    p["done"] = True
                    changed = True
        if a.delivery:
            st["deliveries"].append({"path": a.delivery, "date": date.today().isoformat()})
            changed = True
        if a.set:
            key, value = a.set
            node = st
            parts = key.split(".")
            for k in parts[:-1]:
                node = node.setdefault(k, {})
            node[parts[-1]] = value
            changed = True
        if changed:
            write_json(state_path(edit), st)
        if a.command == "show":
            if a.arg not in list(FILES) + ["deliveries"]:
                raise InputInvalid(f"Unknown block {a.arg!r}.", fix=f"One of: {', '.join(list(FILES) + ['deliveries'])}")
            emit({"ok": True, "block": a.arg,
                  "data": read_json(edit / FILES[a.arg], default={}) if a.json and a.arg in FILES else summarize(edit, a.arg)})
        if a.command == "item":
            emit({"ok": True, "item": find_item(edit, a.arg)})
        emit({"ok": True, "video": st["video"], "profile": st.get("profile"), "stages": st["stages"],
              "next": next((s for s in STAGES if st["stages"][s] in ("pending", "in_progress", "awaiting_review")), None),
              "pending": [p for p in st["pending"] if not p["done"]], "alerts": alerts(edit, st),
              "deliveries": st["deliveries"][-3:], "learnings_open": learnings_open(edit), "tools": st.get("tools", {})})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
