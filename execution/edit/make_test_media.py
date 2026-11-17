"""
Generate short synthetic media for testing a delivery format, with ffmpeg.

The first time a delivery format is used (or after it changes), the creator imports a
**short test project** built from synthetic media and confirms it opens correctly in
Final Cut Pro, before the format is trusted with a real video. This script makes that
media: a "camera" clip with a moving test pattern, a burned-in frame counter and a tone
(so a cut point can be checked by eye and ear), a 1 s timecode track starting at
01:00:00:00, a full-screen "motion" MP4, an "overlay" MOV ProRes 4444 with alpha, a
short "sfx" WAV and a "music" WAV.

Everything is written into the folder you pass -- normally the video's
``edit/test-media/`` -- never next to the creator's footage.

Usage:
    python execution/edit/make_test_media.py --out <folder> [--rate 30000/1001] [--size 1920x1080] [--seconds 12]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import ExecutionError, die, emit, install_excepthook, require_tool, run
from timebase import parse_rate


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Synthetic media for a short delivery test.")
    ap.add_argument("--out", required=True)
    ap.add_argument("--rate", default="30000/1001")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--seconds", type=float, default=12.0)
    a = ap.parse_args()
    try:
        require_tool("ffmpeg")
        out = Path(a.out).expanduser().resolve()
        out.mkdir(parents=True, exist_ok=True)
        r = parse_rate(a.rate)
        rate = f"{r.numerator}/{r.denominator}"
        w, h = a.size.split("x")
        sec = a.seconds
        files = {}

        cam = out / "test_camera.mov"
        run(["ffmpeg", "-y", "-v", "error",
             "-f", "lavfi", "-i", f"testsrc2=size={a.size}:rate={rate}:duration={sec}",
             "-f", "lavfi", "-i", f"sine=frequency=440:sample_rate=48000:duration={sec}",
             "-vf", "drawtext=text='%{frame_num}':x=40:y=40:fontsize=72:fontcolor=white:box=1:boxcolor=black",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ac", "2",
             "-timecode", "01:00:00:00", "-shortest", str(cam)], timeout=300)
        files["camera"] = str(cam)

        mo = out / "test_motion_fullscreen.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", f"color=c=0x1d4ed8:size={a.size}:rate={rate}:duration=3",
             "-vf", "drawtext=text='MOTION':x=(w-tw)/2:y=(h-th)/2:fontsize=160:fontcolor=white",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(mo)], timeout=300)
        files["motion"] = str(mo)

        ov = out / "test_overlay_alpha.mov"
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", f"color=c=black@0.0:size={a.size}:rate={rate}:duration=3,format=rgba",
             "-vf", f"drawbox=x={int(w) // 2 - 300}:y={int(h) - 260}:w=600:h=160:color=0xf59e0b@1:t=fill",
             "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(ov)], timeout=300)
        files["overlay"] = str(ov)

        sfx = out / "test_sfx.wav"
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", "sine=frequency=1200:sample_rate=48000:duration=0.4",
             "-af", "afade=t=out:st=0.05:d=0.35", "-ac", "2", str(sfx)], timeout=120)
        files["sfx"] = str(sfx)

        music = out / "test_music.wav"
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
             "-i", f"sine=frequency=220:sample_rate=48000:duration={sec}",
             "-ac", "2", str(music)], timeout=120)
        files["music"] = str(music)

        emit({"ok": True, "folder": str(out), "files": files})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
