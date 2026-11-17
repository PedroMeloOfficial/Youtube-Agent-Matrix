"""
The one place time is converted. Every editing script imports this module.

Final Cut Pro stores time as a rational number of seconds ("1001/30000s"). Every
``offset``, ``start`` and ``duration`` in a delivery must be an exact multiple of the
frame duration of the material's **real** rate -- 29.97 is ``30000/1001``, not 30, and
an error there shows up as drift that grows toward the end of a long video. So:

- rates are ``Fraction`` objects, parsed from ffprobe's ``r_frame_rate`` ("30000/1001");
- seconds become frames by rounding to the nearest frame, here and nowhere else;
- frames become FCPXML strings by exact multiplication, never through a float.

Also converts SMPTE timecode (drop-frame and non-drop-frame) to frame counts, because a
camera file whose timecode starts at 01:00:00:00 has a media start of 3600 s, and a clip's
``start`` attribute is measured from there.

Usage (for a quick check from the shell):
    python execution/edit/timebase.py --rate 30000/1001 --seconds 12.345
    python execution/edit/timebase.py --rate 30000/1001 --timecode "01:00:00;00"
"""

from __future__ import annotations

import argparse
import re
from fractions import Fraction

COMMON_RATES = {
    "23.976": Fraction(24000, 1001), "23.98": Fraction(24000, 1001),
    "24": Fraction(24), "25": Fraction(25),
    "29.97": Fraction(30000, 1001), "30": Fraction(30),
    "50": Fraction(50), "59.94": Fraction(60000, 1001), "60": Fraction(60),
}


def parse_rate(value) -> Fraction:
    """'30000/1001', '29.97', 30, Fraction -> exact Fraction frames per second."""
    if isinstance(value, Fraction):
        rate = value
    elif isinstance(value, int):
        rate = Fraction(value)
    else:
        text = str(value).strip()
        if text in COMMON_RATES:
            rate = COMMON_RATES[text]
        elif "/" in text:
            num, den = text.split("/", 1)
            rate = Fraction(int(num), int(den))
        else:
            # A decimal that is not a known broadcast rate: snap NTSC-looking values.
            f = float(text)
            for known in COMMON_RATES.values():
                if abs(float(known) - f) < 0.005:
                    return known
            rate = Fraction(text).limit_denominator(1001)
    if rate <= 0:
        raise ValueError(f"Frame rate must be positive, got {value!r}")
    return rate


def frame_duration(rate) -> Fraction:
    return 1 / parse_rate(rate)


def seconds_to_frames(seconds, rate) -> int:
    """Nearest frame. The only rounding of time in the whole editing layer."""
    exact = Fraction(str(seconds)) * parse_rate(rate)
    # round-half-up, not banker's rounding: deterministic and unsurprising
    return int((exact + Fraction(1, 2)) // 1)


def frames_to_seconds(frames: int, rate) -> Fraction:
    return Fraction(int(frames)) / parse_rate(rate)


def fcp_time(seconds: Fraction) -> str:
    """Exact Fraction of seconds -> FCPXML time string ('1001/30000s', '5s', '0s')."""
    seconds = Fraction(seconds)
    if seconds.denominator == 1:
        return f"{seconds.numerator}s"
    return f"{seconds.numerator}/{seconds.denominator}s"


def frames_to_fcp(frames: int, rate) -> str:
    return fcp_time(frames_to_seconds(frames, rate))


def parse_fcp_time(text: str | None) -> Fraction:
    """'1001/30000s' | '5s' | '0s' | None -> Fraction seconds."""
    if text is None or text == "":
        return Fraction(0)
    t = text.strip()
    if not t.endswith("s"):
        raise ValueError(f"Not an FCPXML time: {text!r}")
    t = t[:-1]
    if "/" in t:
        num, den = t.split("/", 1)
        return Fraction(int(num), int(den))
    return Fraction(t)


def is_frame_aligned(seconds: Fraction, rate) -> bool:
    return (Fraction(seconds) * parse_rate(rate)).denominator == 1


# ------------------------------------------------------------------- timecode

_TC = re.compile(r"^(\d{1,2})[:;.](\d{2})[:;.](\d{2})([:;.])(\d{2,3})$")


def nominal_fps(rate) -> int:
    return round(float(parse_rate(rate)))


def timecode_to_frames(tc: str, rate) -> tuple[int, bool]:
    """SMPTE timecode -> (frame count, drop_frame). ';' before frames means drop-frame."""
    m = _TC.match(tc.strip())
    if not m:
        raise ValueError(f"Not a timecode: {tc!r}")
    hh, mm, ss, sep, ff = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5))
    fps = nominal_fps(rate)
    drop = sep in ";." and parse_rate(rate).denominator == 1001
    frames = ((hh * 60 + mm) * 60 + ss) * fps + ff
    if drop:
        drop_per_min = 2 if fps == 30 else 4  # 29.97 drops 2, 59.94 drops 4
        total_minutes = hh * 60 + mm
        frames -= drop_per_min * (total_minutes - total_minutes // 10)
    return frames, drop


def timecode(frames: int, rate, drop: bool = False) -> str:
    """Frame count -> display timecode (for chat and markers only, never for FCPXML math)."""
    fps = nominal_fps(rate)
    frames = int(frames)
    if drop:
        drop_per_min = 2 if fps == 30 else 4
        per_10 = fps * 600 - drop_per_min * 9
        per_min = fps * 60 - drop_per_min
        d, m = divmod(frames, per_10)
        if m > drop_per_min:
            frames += drop_per_min * 9 * d + drop_per_min * ((m - drop_per_min) // per_min)
        else:
            frames += drop_per_min * 9 * d
    ff = frames % fps
    s = frames // fps
    sep = ";" if drop else ":"
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}{sep}{ff:02d}"


def clock(seconds) -> str:
    """Seconds -> 'mm:ss.t' (or 'h:mm:ss.t'), for transcripts the agents read."""
    s = float(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h >= 1:
        return f"{int(h)}:{int(m):02d}:{sec:04.1f}"
    return f"{int(m):02d}:{sec:04.1f}"


if __name__ == "__main__":
    import json

    ap = argparse.ArgumentParser(description="Exact frame/time conversion used by every editing script.")
    ap.add_argument("--rate", required=True, help="frame rate, e.g. 30000/1001 or 29.97")
    ap.add_argument("--seconds", help="seconds to snap to a frame")
    ap.add_argument("--timecode", help="timecode to convert to frames")
    a = ap.parse_args()
    r = parse_rate(a.rate)
    out = {"ok": True, "rate": f"{r.numerator}/{r.denominator}", "frame_duration": fcp_time(1 / r)}
    if a.seconds:
        f = seconds_to_frames(a.seconds, r)
        out.update(frames=f, fcpxml=frames_to_fcp(f, r))
    if a.timecode:
        f, drop = timecode_to_frames(a.timecode, r)
        out.update(frames=f, drop_frame=drop, fcpxml=frames_to_fcp(f, r))
    print(json.dumps(out, indent=2))
