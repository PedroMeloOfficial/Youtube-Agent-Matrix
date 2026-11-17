"""
Compute the presenter's camera moves as dense Final Cut keyframes.

The camera agent writes **intent** in ``edit/camera/plan.json`` -- a base (how closed
the close shot is, how much slow push) and numbered moves (``cam01`` …). This script
does the maths and writes ``edit/camera/camera.json``: per spine segment, keyframes of
scale and position for the clip's Transform, sampled every frame during a move and
thinned where the curve is straight, so the curve that plays in Final Cut is the curve
that was designed (Final Cut itself only interpolates between keyframes).

**Base, automatic.** Each cut alternates the plane -- open (100 %) and closed
(``closed_scale``) -- which disguises jump cuts. The plane of a segment is chosen from
where the camera *actually ended* in the previous one, so a cut always changes plane;
a cut with less than 5 % change is warned about. The first segment starts open. A slow
push (``creep``) runs underneath, multiplied in, never fighting another move.

**Moves** (all times are sequence seconds):
    punch       {"time", "amount"=0.10, "overshoot"=0.06, "settle"=0.3}  sharp punch-in on a word; holds to the cut
    push_in     {"segment", "duration"=0.22, "amount"=0.12, "ease"="power4.in"}  accelerates into the face before the cut
    arrive      {"segment", "duration"=0.5, "amount"=0.08, "from"="below|above|left|right", "ease"="expo.out"}
                arrives already moving after a cut, in the direction an animation left, and brakes
    side_third  {"start", "end", "side"="left|right", "scale"=1.4, "transition"=0.7}  face to a third while an overlay is up
    lock        {"start", "end"}  face stays still on screen while the frame follows it (needs face data)

**Framing.** With face data (``face_track.py``) closed shots put the eyes at the profile's
eye line (craft default 35 % from the top) and keep the face centred; without it the
frame stays centred. The image edge is never shown: position is clamped by the margin the
scale allows.

**Units.** Final Cut's Transform position is written as a percentage of the frame height
(x right, y up). This is checked by the first test import (``references/editing/delivery-fcpxml.md``).

Usage:
    python execution/edit/camera_curves.py --edit-dir <video>/edit
"""

from __future__ import annotations

import argparse
import bisect
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, write_json
from easing import ease
from timebase import parse_rate

TOL_SCALE = 0.0015
TOL_POS = 0.04          # in Final Cut position units
SPARSE = 1.0            # seconds between keyframes where nothing but the creep happens


def load_faces(edit: Path):
    data = read_json(edit / "camera" / "faces.json", default={"files": {}})
    out = {}
    for fid, rows in data.get("files", {}).items():
        rows = sorted(rows)
        out[fid] = ([r[0] for r in rows], rows)
    return out


def face_at(faces, fid, t):
    if fid not in faces:
        return None
    times, rows = faces[fid]
    if not times:
        return None
    i = bisect.bisect_left(times, t)
    cand = [rows[j] for j in (i - 1, i) if 0 <= j < len(rows)]
    r = min(cand, key=lambda r: abs(r[0] - t))
    return r if abs(r[0] - t) < 1.0 else None


class Camera:
    def __init__(self, plan, cuts, footage, faces):
        self.base = {"closed_scale": 1.25, "creep": 0.05, "creep_ease": "sine.out", "eye_line": 0.35,
                     **plan.get("base", {})}
        self.moves = plan.get("moves", [])
        self.overrides = plan.get("segment_overrides", {})
        self.segs = cuts["segments"]
        self.faces = faces
        self.rate = parse_rate(footage["main_rate"])
        main = next(f for f in footage["files"] if f.get("role") == "camera")
        self.W, self.H = main["width"], main["height"]
        self.warnings = []
        self.events = []
        t = 0.0
        for s in self.segs:
            s["_seq_in"], t = t, t + (s["out"] - s["in"])
            s["_seq_out"] = t

    # ---- helpers
    def source_time(self, seg, t):
        return seg["in"] + (t - seg["_seq_in"])

    def framing(self, seg, t, scale, target_x=0.5, eye_line=None):
        """Normalized translation (fraction of width/height) to put the face where wanted."""
        f = face_at(self.faces, seg["file"], self.source_time(seg, t))
        if f is None or scale <= 1.0001:
            return 0.0, 0.0
        _, fx, fy_eye, _size = f
        ey = eye_line if eye_line is not None else self.base["eye_line"]
        px = target_x - 0.5 - (fx - 0.5) * scale
        py = ey - 0.5 - (fy_eye - 0.5) * scale
        lim = (scale - 1) / 2
        return max(-lim, min(lim, px)), max(-lim, min(lim, py))

    def to_fcp(self, px, py):
        return px * self.W / self.H * 100.0, -py * 100.0

    # ---- evaluation
    def evaluate(self):
        out, last_scale = {}, 1.0
        for i, seg in enumerate(self.segs):
            ov = self.overrides.get(seg["id"], {}).get("plane")
            closed = self.base["closed_scale"]
            if ov == "open":
                plane = 1.0
            elif ov == "closed":
                plane = closed
            elif i == 0:
                plane = 1.0
            else:
                plane = 1.0 if last_scale > (1.0 + closed) / 2 else closed
                if abs(plane - last_scale) / last_scale < 0.05:
                    self.warnings.append(f"{seg['id']}: cut with under 5% change of framing — jump cut may show")
            moves = [m for m in self.moves if self._in_seg(m, seg)]
            samples = self._sample(seg, plane, moves)
            last_scale = samples[-1][1]
            out[seg["id"]] = [{"seq_time": round(t, 4), "scale": [round(s, 4), round(s, 4)],
                               "position": [round(x, 3), round(y, 3)]} for t, s, x, y in self._thin(samples)]
        return out

    def _in_seg(self, m, seg):
        if "segment" in m:
            return m["segment"] == seg["id"]
        t0 = m.get("time", m.get("start"))
        if t0 is None:
            raise InputInvalid(f"Camera move {m.get('id')} has no time, start or segment.")
        return seg["_seq_in"] <= t0 < seg["_seq_out"]

    def _sample(self, seg, plane, moves):
        a, b = seg["_seq_in"], seg["_seq_out"]
        fd = float(1 / self.rate)
        times = set()
        t = a
        while t < b:
            times.add(round(t, 6))
            t += SPARSE
        times.add(round(b - fd, 6))
        for m in moves:
            lo, hi = self._window(m, seg)
            t = lo
            while t <= hi:
                times.add(round(t, 6))
                t += fd
            times.add(round(max(a, lo - fd), 6))
        res = []
        for t in sorted(x for x in times if a <= x < b):
            s, x, y = self._at(seg, plane, moves, t)
            res.append((t, s, x, y))
        return res

    def _window(self, m, seg):
        typ = m["type"]
        if typ == "punch":
            return m["time"], m["time"] + m.get("settle", 0.3)
        if typ == "push_in":
            return seg["_seq_out"] - m.get("duration", 0.22), seg["_seq_out"]
        if typ == "arrive":
            return seg["_seq_in"], seg["_seq_in"] + m.get("duration", 0.5)
        if typ in ("side_third", "lock"):
            tr = m.get("transition", 0.7) if typ == "side_third" else 0.4
            return max(seg["_seq_in"], m["start"] - tr), min(seg["_seq_out"], m["end"] + tr)
        raise InputInvalid(f"Unknown camera move type {typ!r} ({m.get('id')}).")

    def _at(self, seg, plane, moves, t):
        a, b = seg["_seq_in"], seg["_seq_out"]
        prog = (t - a) / max(1e-6, b - a)
        mult = 1.0 + self.base["creep"] * ease(self.base["creep_ease"], prog)
        dx = dy = 0.0
        target_x, eye = 0.5, None
        lock = None
        for m in moves:
            typ = m["type"]
            if typ == "punch" and t >= m["time"]:
                amt, over, settle = m.get("amount", 0.10), m.get("overshoot", 0.06), m.get("settle", 0.3)
                k = ease("power2.out", (t - m["time"]) / settle)
                mult *= (1 + amt) * (1 + over * (1 - k))
            elif typ == "push_in":
                lo = b - m.get("duration", 0.22)
                if t >= lo:
                    mult *= 1 + m.get("amount", 0.12) * ease(m.get("ease", "power4.in"), (t - lo) / (b - lo))
            elif typ == "arrive":
                d = m.get("duration", 0.5)
                if t < a + d:
                    k = 1 - ease(m.get("ease", "expo.out"), (t - a) / d)
                    amt = m.get("amount", 0.08) * m.get("overshoot", 1.4)
                    mult *= 1 + amt * k
                    sx, sy = {"below": (0, 1), "above": (0, -1), "left": (-1, 0), "right": (1, 0)}[m.get("from", "below")]
                    dx += sx * amt / 2 * k
                    dy += sy * amt / 2 * k
            elif typ == "side_third":
                tr = m.get("transition", 0.7)
                if t < m["start"]:
                    k = ease("power2.inOut", 1 - (m["start"] - t) / tr)
                elif t > m["end"]:
                    k = ease("power2.inOut", 1 - (t - m["end"]) / tr)
                else:
                    k = 1.0
                k = max(0.0, min(1.0, k))
                side_scale = m.get("scale", 1.4)
                mult = mult * (1 + (side_scale / plane - 1) * k)
                target_x = 0.5 + ((1 / 3 if m.get("side", "left") == "left" else 2 / 3) - 0.5) * k
            elif typ == "lock" and m["start"] <= t <= m["end"]:
                lock = m
        scale = plane * mult
        px, py = self.framing(seg, t, scale, target_x, eye)
        if lock is not None:
            fx = face_at(self.faces, seg["file"], self.source_time(seg, lock["start"]))
            if fx is None:
                self.warnings.append(f"{lock.get('id')}: face lock without face data — ignored")
            else:
                cur = face_at(self.faces, seg["file"], self.source_time(seg, t)) or fx
                px += -(cur[1] - fx[1]) * scale
                py += -(cur[2] - fx[2]) * scale
        lim = (scale - 1) / 2
        px = max(-lim, min(lim, px + dx * (scale - 1)))
        py = max(-lim, min(lim, py + dy * (scale - 1)))
        x, y = self.to_fcp(px, py)
        return scale, x, y

    @staticmethod
    def _thin(samples):
        """Keep a sample only where straight-line interpolation would miss the curve."""
        if len(samples) <= 2:
            return samples
        kept = [samples[0]]
        for i in range(1, len(samples) - 1):
            p0, p1, p2 = kept[-1], samples[i], samples[i + 1]
            span = p2[0] - p0[0]
            r = (p1[0] - p0[0]) / span if span else 0
            pred = [p0[j] + (p2[j] - p0[j]) * r for j in (1, 2, 3)]
            if (abs(pred[0] - p1[1]) > TOL_SCALE or abs(pred[1] - p1[2]) > TOL_POS
                    or abs(pred[2] - p1[3]) > TOL_POS):
                kept.append(p1)
        kept.append(samples[-1])
        return kept

    def sound_events(self):
        ev = []
        for m in self.moves:
            typ = m["type"]
            if typ == "punch":
                ev.append({"time": m["time"], "kind": "camera_punch", "strength": "strong" if m.get("amount", 0.1) >= 0.1 else "medium", "move": m.get("id")})
            elif typ in ("push_in", "arrive"):
                seg = next(s for s in self.segs if s["id"] == m["segment"])
                t = seg["_seq_out"] if typ == "push_in" else seg["_seq_in"] + m.get("duration", 0.5) * 0.3
                ev.append({"time": round(t, 3), "kind": f"camera_{typ}", "strength": "medium", "move": m.get("id")})
        return ev


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Dense camera keyframes from the camera agent's plan.")
    ap.add_argument("--edit-dir", required=True)
    a = ap.parse_args()
    try:
        edit = Path(a.edit_dir).expanduser().resolve()
        plan = read_json(edit / "camera" / "plan.json")
        cuts = read_json(edit / "cuts" / "cuts.json")
        footage = read_json(edit / "footage" / "footage.json")
        cam = Camera(plan, cuts, footage, load_faces(edit))
        kfs = cam.evaluate()
        out = {"keyframes": kfs, "moves": cam.moves, "events": cam.sound_events(),
               "warnings": sorted(set(cam.warnings)), "units": "position: % of frame height (x right, y up)"}
        write_json(edit / "camera" / "camera.json", out)
        emit({"ok": True, "output": str(edit / "camera" / "camera.json"), "segments": len(kfs),
              "keyframes": sum(len(v) for v in kfs.values()), "moves": len(cam.moves),
              "warnings": out["warnings"]})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
