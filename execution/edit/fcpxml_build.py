"""
Build a Final Cut Pro project (FCPXML) from a timeline description.

The editing agents never write XML. They write *decisions* -- which source ranges, which
renders where, which sounds at what level -- and the stage scripts turn those into a
**timeline JSON**. This script turns a timeline JSON into an FCPXML that Final Cut Pro
imports as a project, then validates it.

Final Cut has no tracks. The layout is fixed so the creator always finds things in the
same place (see references/editing/delivery-fcpxml.md):

    spine           camera takes (video + their own audio)          roles: video / dialogue
    lane +1         screen recordings                               video.screen
    lane +2         full-screen motion graphics (MP4)               video.motion
    lane +3         overlays with alpha (MOV ProRes 4444)           video.overlay
    lane -1         external microphone, synced                     dialogue
    lanes -2..-4    sound effects, stacked only when they overlap   effects.sfx
    lane -5         music                                           music

Rules this script enforces, because each one has broken a real import somewhere:
- every time is exact rational seconds via ``timebase.py``; spine offsets and durations are
  whole frames of the *sequence* rate, clip starts whole frames of the *asset* rate;
- a clip ``start`` is measured from the file's timecode origin, so a camera file whose
  timecode begins at 01:00:00:00 is addressed from 3600 s, not 0;
- a connected item belongs to the spine clip it sits on, and its ``offset`` is in that
  clip's local time -- computed here, never by an agent;
- every clip points at the whole original file; never a proxy, never a copy;
- markers by the matrix are to-do markers whose text starts with ``[C]``;
- outputs are versioned (``_v01``, ``_v02``...) and never overwrite a delivery;
- nothing is ever written inside a ``.fcpbundle``.

Validation: ``xmllint --dtdvalid`` against the DTD of the same version. The DTD is looked
up in ``$FCPXML_DTD``, then inside the installed Final Cut Pro app. If it cannot be found
the result says ``"validated": false`` with the reason -- a weaker check is never
substituted silently, and ``--require-dtd`` turns that into a failure.

Usage:
    python execution/edit/fcpxml_build.py timeline.json --out-dir <video>/edit/deliveries --stem <slug>_cuts
    python execution/edit/fcpxml_build.py timeline.json --out-dir ... --stem ... --bundle   # .fcpxmld
    python execution/edit/fcpxml_build.py --detect-version

Exit 0 with ``{"ok": true, "output": ..., "validated": ...}``; exit 1 with an error object.
"""

from __future__ import annotations

import argparse
import glob
import os
import plistlib
import re
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from xml.sax.saxutils import quoteattr

from common import (
    ExecutionError,
    InputInvalid,
    die,
    emit,
    file_url,
    guard_not_in_library,
    install_excepthook,
    next_version,
    read_json,
    write_text,
)
from timebase import fcp_time, parse_rate, seconds_to_frames

DEFAULT_VERSION = "1.14"

LANES = {
    "screen": 1, "motion": 2, "overlay": 3,
    "external_audio": -1, "sfx": -2, "music": -5,
}
SFX_LANES = [-2, -3, -4]

ROLES = {
    "camera": ("video", "dialogue"),
    "screen": ("video.screen", None),
    "motion": ("video.motion", None),
    "overlay": ("video.overlay", None),
    "external_audio": (None, "dialogue"),
    "sfx": (None, "effects.sfx"),
    "music": (None, "music"),
}

# Known FFVideoFormat names. Anything else gets an unnamed custom format (still valid).
_FORMAT_NAMES = {
    (1920, 1080, "24000/1001"): "FFVideoFormat1080p2398",
    (1920, 1080, "24/1"): "FFVideoFormat1080p24",
    (1920, 1080, "25/1"): "FFVideoFormat1080p25",
    (1920, 1080, "30000/1001"): "FFVideoFormat1080p2997",
    (1920, 1080, "30/1"): "FFVideoFormat1080p30",
    (1920, 1080, "60000/1001"): "FFVideoFormat1080p5994",
    (1920, 1080, "60/1"): "FFVideoFormat1080p60",
    (3840, 2160, "24000/1001"): "FFVideoFormat3840x2160p2398",
    (3840, 2160, "24/1"): "FFVideoFormat3840x2160p24",
    (3840, 2160, "25/1"): "FFVideoFormat3840x2160p25",
    (3840, 2160, "30000/1001"): "FFVideoFormat3840x2160p2997",
    (3840, 2160, "30/1"): "FFVideoFormat3840x2160p30",
    (3840, 2160, "60000/1001"): "FFVideoFormat3840x2160p5994",
    (3840, 2160, "60/1"): "FFVideoFormat3840x2160p60",
}

# FCP marketing version -> FCPXML version it exports (and therefore imports at most).
_FCP_TO_FCPXML = [
    ((12, 0), "1.14"), ((11, 1), "1.13"), ((11, 0), "1.12"),
    ((10, 7), "1.11"), ((10, 6), "1.10"),
]


# ------------------------------------------------------------------ discovery


def find_fcp_apps() -> list[Path]:
    return [Path(p) for p in sorted(glob.glob("/Applications/Final Cut Pro*.app"))]


def detect_version() -> dict:
    for app in find_fcp_apps():
        plist = app / "Contents" / "Info.plist"
        try:
            with plist.open("rb") as fh:
                short = plistlib.load(fh).get("CFBundleShortVersionString", "")
        except (OSError, ValueError):
            continue
        nums = tuple(int(x) for x in re.findall(r"\d+", short)[:2]) or (0, 0)
        for floor, fx in _FCP_TO_FCPXML:
            if nums >= floor:
                return {"app": str(app), "fcp_version": short, "fcpxml_version": fx}
    return {"app": None, "fcp_version": None, "fcpxml_version": None}


def find_dtd(version: str) -> Path | None:
    env = os.environ.get("FCPXML_DTD")
    if env and Path(env).exists():
        return Path(env)
    tag_u, tag_d = version.replace(".", "_"), version
    for app in find_fcp_apps():
        for dtd in app.rglob("*.dtd"):
            name = dtd.name
            if tag_u in name or f"version_{tag_d}" in name or f"v{tag_d}" in name:
                return dtd
    return None


def validate(path: Path, version: str) -> dict:
    dtd = find_dtd(version)
    if dtd is None:
        return {"validated": False,
                "reason": f"No DTD for FCPXML {version} found (set FCPXML_DTD or install Final Cut Pro)."}
    if not shutil.which("xmllint"):
        return {"validated": False, "reason": "xmllint is not installed."}
    # xmllint reads --dtdvalid as a URL and cannot open a path with spaces -- and the real DTD
    # lives inside "/Applications/Final Cut Pro.app". Validate against a copy in a plain path.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        plain = Path(tmp) / "fcpxml.dtd"
        shutil.copyfile(dtd, plain)
        proc = subprocess.run(["xmllint", "--noout", "--dtdvalid", str(plain), str(path)],
                              capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise ExecutionError(
            "The generated FCPXML does not validate against the Final Cut DTD.",
            fix="This is a bug in the generator, not in your project. Report the errors below.",
            details={"dtd": str(dtd), "errors": proc.stderr.strip().splitlines()[:20]},
        )
    return {"validated": True, "dtd": str(dtd)}


# ------------------------------------------------------------------ model


class Asset:
    def __init__(self, key: str, spec: dict, seq_rate: Fraction):
        self.key = key
        self.path = Path(spec["path"]).expanduser()
        if not self.path.is_absolute():
            raise InputInvalid(f"Asset {key} path must be absolute: {self.path}")
        self.has_video = bool(spec.get("has_video", True))
        self.has_audio = bool(spec.get("has_audio", True))
        self.rate = parse_rate(spec["rate"]) if self.has_video else seq_rate
        self.width = spec.get("width")
        self.height = spec.get("height")
        self.audio_rate = int(spec.get("audio_rate", 48000))
        self.audio_channels = int(spec.get("audio_channels", 2))
        tc_frames = int(spec.get("tc_start_frames", 0) or 0)
        self.start = Fraction(tc_frames) / self.rate
        self.tc_drop = bool(spec.get("tc_drop", False))
        dur = Fraction(str(spec["duration"]))
        if self.has_video:
            self.duration = Fraction(int(dur * self.rate)) / self.rate  # floor to a frame
        else:
            self.duration = Fraction(int(dur * self.audio_rate), self.audio_rate)
        self.id = ""
        self.format_id = ""

    def source(self, seconds) -> Fraction:
        """File-relative seconds -> asset-local time, snapped to a frame of this asset."""
        frames = seconds_to_frames(seconds, self.rate)
        return self.start + Fraction(frames) / self.rate


def _fmt_key(rate: Fraction, w, h):
    return (int(w), int(h), f"{rate.numerator}/{rate.denominator}")


def _db(value) -> str:
    v = float(value)
    return f"{v:g}dB"


# ------------------------------------------------------------------ builder


class Builder:
    def __init__(self, tl: dict, version: str):
        self.tl = tl
        self.version = version
        seq = tl["sequence"]
        self.seq_rate = parse_rate(seq["rate"])
        self.seq_w, self.seq_h = int(seq["width"]), int(seq["height"])
        self.warnings: list[str] = []
        self.assets = {k: Asset(k, v, self.seq_rate) for k, v in tl["assets"].items()}
        self.formats: dict = {}
        self._ids = 0
        self.seq_format = self._format(self.seq_rate, self.seq_w, self.seq_h)
        by_path: dict = {}
        for a in self.assets.values():
            twin = by_path.get(str(a.path))
            if twin is not None:  # the same file under two keys is one asset in Final Cut
                a.id, a.format_id, a.duplicate = twin.id, twin.format_id, True
                continue
            by_path[str(a.path)] = a
            a.id = self._next_id()
            if a.has_video:
                a.format_id = self._format(a.rate, a.width or self.seq_w, a.height or self.seq_h)
        self.spine = self._layout_spine(tl.get("spine", []))

    def _next_id(self) -> str:
        self._ids += 1
        return f"r{self._ids}"

    def _format(self, rate, w, h) -> str:
        key = _fmt_key(rate, w, h)
        if key not in self.formats:
            self.formats[key] = self._next_id()
        return self.formats[key]

    def sf(self, seconds) -> Fraction:
        """Sequence seconds snapped to a sequence frame."""
        return Fraction(seconds_to_frames(seconds, self.seq_rate)) / self.seq_rate

    # -- spine ---------------------------------------------------------------

    def _layout_spine(self, items):
        if not items:
            raise InputInvalid("The timeline has no spine clips.", fix="Run the cuts step first.")
        laid, t = [], Fraction(0)
        for it in items:
            a = self._asset(it["asset"], it.get("id"))
            start = a.source(it["in"])
            frames = seconds_to_frames(Fraction(str(it["out"])) - Fraction(str(it["in"])), self.seq_rate)
            if frames <= 0:
                raise InputInvalid(f"Spine clip {it.get('id')} has no duration.")
            dur = Fraction(frames) / self.seq_rate
            if start < a.start or start + dur > a.start + a.duration + Fraction(1, 1000):
                raise InputInvalid(f"Spine clip {it.get('id')} reaches outside its source file.")
            laid.append({"spec": it, "asset": a, "offset": t, "start": start, "duration": dur,
                         "children": [], "markers": []})
            t += dur
        return laid

    def _asset(self, key, owner=None) -> Asset:
        if key not in self.assets:
            raise InputInvalid(f"{owner or 'An item'} refers to unknown asset '{key}'.")
        return self.assets[key]

    def parent_at(self, seq_t: Fraction):
        for clip in self.spine:
            if clip["offset"] <= seq_t < clip["offset"] + clip["duration"]:
                return clip
        if seq_t >= self.spine[-1]["offset"]:
            return self.spine[-1]
        return self.spine[0]

    @staticmethod
    def local(clip, seq_t: Fraction) -> Fraction:
        """Sequence time -> the parent clip's local (asset) time."""
        return clip["start"] + (seq_t - clip["offset"])

    # -- connected items, markers -------------------------------------------

    def attach(self):
        sfx_busy: dict[int, list] = {ln: [] for ln in SFX_LANES}
        for it in sorted(self.tl.get("connected", []), key=lambda x: float(x["seq_start"])):
            kind = it["kind"]
            if kind not in LANES:
                raise InputInvalid(f"Connected item {it.get('id')} has unknown kind '{kind}'.")
            a = self._asset(it["asset"], it.get("id"))
            seq_t = self.sf(it["seq_start"])
            src_in = a.source(it.get("in", 0))
            dur = self.sf(it["duration"])
            if dur <= 0:
                raise InputInvalid(f"Connected item {it.get('id')} has no duration.")
            lane = it.get("lane", LANES[kind])
            if kind == "sfx" and "lane" not in it:
                lane = None
                for ln in SFX_LANES:
                    if all(seq_t >= e or seq_t + dur <= s for s, e in sfx_busy[ln]):
                        lane = ln
                        break
                if lane is None:
                    lane = SFX_LANES[-1]
                    self.warnings.append(f"{it.get('id')}: more than {len(SFX_LANES)} overlapping sounds; stacked in lane {lane}.")
                sfx_busy[lane].append((seq_t, seq_t + dur))
            parent = self.parent_at(seq_t)
            parent["children"].append({"spec": it, "asset": a, "kind": kind, "lane": lane,
                                       "offset": self.local(parent, seq_t), "start": src_in,
                                       "duration": dur, "seq_t": seq_t})
        for m in self.tl.get("markers", []):
            seq_t = self.sf(m["seq_time"])
            parent = self.parent_at(seq_t)
            parent["markers"].append({**m, "local": self.local(parent, seq_t)})
        for clip in self.spine:
            for m in clip["spec"].get("markers", []):
                local = clip["asset"].source(m["source_time"])
                if not (clip["start"] <= local < clip["start"] + clip["duration"]):
                    self.warnings.append(f"Marker '{m.get('text', '')[:30]}' is outside clip {clip['spec'].get('id')}; dropped.")
                    continue
                clip["markers"].append({**m, "local": local})

    # -- xml -----------------------------------------------------------------

    def _transform_xml(self, clip, ind: str) -> list[str]:
        tr = clip["spec"].get("transform")
        if not tr:
            return []
        kf = tr.get("keyframes", [])
        if not kf:
            return []
        out = [f"{ind}<adjust-transform>"]
        for pname, key in (("position", "position"), ("scale", "scale")):
            pts = [k for k in kf if key in k]
            if not pts:
                continue
            out.append(f'{ind}  <param name="{pname}">')
            out.append(f"{ind}    <keyframeAnimation>")
            last = None
            for k in pts:
                t = self.local(clip, self.sf(k["seq_time"]))
                if last is not None and t <= last:
                    continue  # one keyframe per frame
                last = t
                x, y = k[key]
                out.append(f'{ind}      <keyframe time="{fcp_time(t)}" value="{x:.4f} {y:.4f}" interp="linear" curve="linear"/>')
            out.append(f"{ind}    </keyframeAnimation>")
            out.append(f"{ind}  </param>")
        out.append(f"{ind}</adjust-transform>")
        return out

    def _volume_xml(self, spec, clip_like, ind: str) -> list[str]:
        db = spec.get("volume_db")
        fin = spec.get("fade_in_frames")
        fout = spec.get("fade_out_frames")
        kfs = spec.get("volume_keyframes", [])
        if db is None and not fin and not fout and not kfs:
            return []
        amount = f' amount="{_db(db)}"' if db is not None else ""
        if not fin and not fout and not kfs:
            return [f"{ind}<adjust-volume{amount}/>"]
        out = [f"{ind}<adjust-volume{amount}>", f'{ind}  <param name="amount">']
        if fin:
            out.append(f'{ind}    <fadeIn type="easeIn" duration="{fcp_time(Fraction(int(fin)) / self.seq_rate)}"/>')
        if fout:
            out.append(f'{ind}    <fadeOut type="easeOut" duration="{fcp_time(Fraction(int(fout)) / self.seq_rate)}"/>')
        if kfs:
            out.append(f"{ind}    <keyframeAnimation>")
            last = None
            for seq_t, val in kfs:
                t = clip_like["start"] + (self.sf(seq_t) - clip_like["seq_t"])
                if last is not None and t <= last:
                    continue
                last = t
                out.append(f'{ind}      <keyframe time="{fcp_time(t)}" value="{_db(val)}"/>')
            out.append(f"{ind}    </keyframeAnimation>")
        out.append(f"{ind}  </param>")
        out.append(f"{ind}</adjust-volume>")
        return out

    def _marker_xml(self, m, ind: str) -> str:
        kind = m.get("kind", "todo")
        text = m.get("text", "")
        start = fcp_time(m["local"])
        one = fcp_time(1 / self.seq_rate)
        if kind == "chapter":
            return f"{ind}<chapter-marker start={quoteattr(start)} duration={quoteattr(one)} value={quoteattr(text)} note=\"matrix\" posterOffset=\"0s\"/>"
        if not text.startswith("[C]"):
            text = f"[C] {text}"
        done = ' completed="0"' if kind == "todo" else ""
        return f"{ind}<marker start={quoteattr(start)} duration={quoteattr(one)} value={quoteattr(text)}{done}/>"

    def _child_xml(self, ch, ind: str) -> list[str]:
        a, spec, kind = ch["asset"], ch["spec"], ch["kind"]
        vrole, arole = ROLES[kind]
        attrs = [
            f"ref={quoteattr(a.id)}", f"lane={quoteattr(str(ch['lane']))}",
            f"offset={quoteattr(fcp_time(ch['offset']))}", f"name={quoteattr(spec.get('name', spec.get('id', a.key)))}",
            f"start={quoteattr(fcp_time(ch['start']))}", f"duration={quoteattr(fcp_time(ch['duration']))}",
        ]
        if a.has_video and vrole:
            attrs.append(f"format={quoteattr(a.format_id)}")
        if vrole and a.has_video:
            attrs.append(f"videoRole={quoteattr(vrole)}")
        if arole and a.has_audio:
            attrs.append(f"audioRole={quoteattr(arole)}")
        if kind in ("sfx", "music", "external_audio"):
            attrs.append('srcEnable="audio"')
        elif not (a.has_audio and spec.get("keep_audio")):
            attrs.append('srcEnable="video"')
        body = []
        if a.has_audio and kind in ("sfx", "music", "external_audio"):
            body = self._volume_xml(spec, ch, ind + "  ")
        if not body:
            return [f"{ind}<asset-clip {' '.join(attrs)}/>"]
        return [f"{ind}<asset-clip {' '.join(attrs)}>", *body, f"{ind}</asset-clip>"]

    def xml(self) -> str:
        self.attach()
        L = ['<?xml version="1.0" encoding="UTF-8"?>', "<!DOCTYPE fcpxml>", "",
             f'<fcpxml version="{self.version}">', "  <resources>"]
        for (w, h, rate), fid in sorted(self.formats.items(), key=lambda kv: int(kv[1][1:])):
            r = parse_rate(rate)
            name = _FORMAT_NAMES.get((w, h, rate))
            nm = f" name={quoteattr(name)}" if name else ""
            L.append(f'    <format id="{fid}"{nm} frameDuration="{fcp_time(1 / r)}" width="{w}" height="{h}"/>')
        for a in self.assets.values():
            if getattr(a, "duplicate", False):
                continue
            attrs = [f'id="{a.id}"', f"name={quoteattr(a.path.stem)}", f'start="{fcp_time(a.start)}"',
                     f'duration="{fcp_time(a.duration)}"', f'hasVideo="{int(a.has_video)}"',
                     f'hasAudio="{int(a.has_audio)}"']
            if a.has_video:
                attrs.append(f'format="{a.format_id}"')
                attrs.append('videoSources="1"')
            if a.has_audio:
                attrs += ['audioSources="1"', f'audioChannels="{a.audio_channels}"', f'audioRate="{a.audio_rate}"']
            L.append(f"    <asset {' '.join(attrs)}>")
            L.append(f'      <media-rep kind="original-media" src={quoteattr(file_url(a.path))}/>')
            L.append("    </asset>")
        L.append("  </resources>")
        total = sum((c["duration"] for c in self.spine), Fraction(0))
        ev = self.tl.get("event", "Matrix")
        pj = self.tl.get("project", "Matrix edit")
        L += [f"  <event name={quoteattr(ev)}>", f"    <project name={quoteattr(pj)}>",
              f'      <sequence format="{self.seq_format}" duration="{fcp_time(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">',
              "        <spine>"]
        ind = " " * 10
        for clip in self.spine:
            a, spec = clip["asset"], clip["spec"]
            attrs = [f'ref="{a.id}"', f'offset="{fcp_time(clip["offset"])}"',
                     f"name={quoteattr(spec.get('name', spec.get('id', a.key)))}",
                     f'start="{fcp_time(clip["start"])}"', f'duration="{fcp_time(clip["duration"])}"',
                     f'format="{a.format_id}"', f'tcFormat="{"DF" if a.tc_drop else "NDF"}"']
            if a.has_audio:
                attrs.append('audioRole="dialogue"')
            inner = self._transform_xml(clip, ind + "  ")
            if a.has_audio:
                clip_like = {"start": clip["start"], "seq_t": clip["offset"]}
                inner += self._volume_xml(spec, clip_like, ind + "  ")
            for ch in sorted(clip["children"], key=lambda c: c["offset"]):
                inner += self._child_xml(ch, ind + "  ")
            for m in sorted(clip["markers"], key=lambda m: m["local"]):
                inner.append(self._marker_xml(m, ind + "  "))
            if inner:
                L.append(f"{ind}<asset-clip {' '.join(attrs)}>")
                L += inner
                L.append(f"{ind}</asset-clip>")
            else:
                L.append(f"{ind}<asset-clip {' '.join(attrs)}/>")
        L += ["        </spine>", "      </sequence>", "    </project>", "  </event>", "</fcpxml>", ""]
        return "\n".join(L)


def build(timeline: dict, out_dir: Path, stem: str, version: str, bundle: bool, require_dtd: bool) -> dict:
    out_dir = Path(out_dir).expanduser().resolve()
    guard_not_in_library(out_dir)
    b = Builder(timeline, version)
    text = b.xml()
    suffix = ".fcpxmld" if bundle else ".fcpxml"
    target = next_version(out_dir, stem, suffix)
    xml_path = target / "Info.fcpxml" if bundle else target
    write_text(xml_path, text)
    result = validate(xml_path, version)
    if require_dtd and not result["validated"]:
        raise ExecutionError(result["reason"], fix="Point FCPXML_DTD at the DTD inside Final Cut Pro.app.")
    total = sum((c["duration"] for c in b.spine), Fraction(0))
    return {"output": str(target), "fcpxml_version": version, "duration_seconds": round(float(total), 3),
            "spine_clips": len(b.spine),
            "connected": sum(len(c["children"]) for c in b.spine),
            "markers": sum(len(c["markers"]) for c in b.spine),
            "warnings": b.warnings, **result}


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Build a Final Cut Pro FCPXML from a timeline JSON.")
    ap.add_argument("timeline", nargs="?", help="timeline JSON written by an editing stage")
    ap.add_argument("--out-dir", help="deliveries folder (versioned names, never overwritten)")
    ap.add_argument("--stem", help="file stem, e.g. <slug>_cuts")
    ap.add_argument("--version", help="FCPXML version (default: detected from Final Cut, else 1.14)")
    ap.add_argument("--bundle", action="store_true", help="write a .fcpxmld bundle instead of .fcpxml")
    ap.add_argument("--require-dtd", action="store_true", help="fail if DTD validation cannot run")
    ap.add_argument("--detect-version", action="store_true", help="report Final Cut and FCPXML versions")
    a = ap.parse_args()
    try:
        if a.detect_version:
            emit({"ok": True, **detect_version()})
        if not (a.timeline and a.out_dir and a.stem):
            raise InputInvalid("timeline, --out-dir and --stem are required.")
        tl = read_json(Path(a.timeline))
        version = a.version or tl.get("fcpxml_version") or detect_version()["fcpxml_version"] or DEFAULT_VERSION
        emit({"ok": True, **build(tl, Path(a.out_dir), a.stem, version, a.bundle, a.require_dtd)})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
