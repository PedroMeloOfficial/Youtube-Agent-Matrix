"""
Find the presenter's face over time, for camera framing (local, no network after setup).

Samples the kept parts of the camera files (the spine segments) every 0.2 s, downscales
each frame, and runs OpenCV's YuNet face detector. For each sample it records the face
centre and the eye line (normalized 0..1, origin top-left) of the largest face, then
smooths the track with a running median so detector jitter does not become camera shake.
Writes ``edit/camera/faces.json``; ``camera_curves.py`` reads it.

Needs ``opencv-python-headless`` in the editing virtualenv and the YuNet model file (a few
hundred KB, Apache-2.0, from the OpenCV model zoo) at
``~/.local/share/youtube-agent-matrix/models/face_detection_yunet_2023mar.onnx``.
Without them the camera still works, centred, and says so.

Usage:
    python execution/edit/face_track.py --edit-dir <video>/edit [--step 0.2]
"""

from __future__ import annotations

import argparse
import statistics
from pathlib import Path

from common import DependencyMissing, ExecutionError, die, emit, install_excepthook, read_json, require_module, write_json

MODEL = Path.home() / ".local" / "share" / "youtube-agent-matrix" / "models" / "face_detection_yunet_2023mar.onnx"
MODEL_URL = ("https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
             "face_detection_yunet_2023mar.onnx")
WIDTH = 640


def smooth(rows, k=5):
    out = []
    for i in range(len(rows)):
        win = rows[max(0, i - k // 2): i + k // 2 + 1]
        out.append([rows[i][0]] + [round(statistics.median(r[j] for r in win), 4) for j in (1, 2, 3)])
    return out


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Face centre and eye line over time, for camera framing.")
    ap.add_argument("--edit-dir", required=True)
    ap.add_argument("--step", type=float, default=0.2)
    a = ap.parse_args()
    try:
        cv2 = require_module("cv2")
        if not MODEL.exists():
            raise DependencyMissing(
                "The YuNet face model is not downloaded.",
                fix=[f"mkdir -p '{MODEL.parent}' && curl -L -o '{MODEL}' {MODEL_URL}",
                     "Without it the camera stays centred on the frame."])
        edit = Path(a.edit_dir).expanduser().resolve()
        footage = read_json(edit / "footage" / "footage.json")
        cuts = read_json(edit / "cuts" / "cuts.json")
        files = {f["id"]: f for f in footage["files"]}
        det = None
        result, misses = {}, 0
        for fid in sorted({s["file"] for s in cuts["segments"]}):
            cap = cv2.VideoCapture(files[fid]["path"])
            if not cap.isOpened():
                raise ExecutionError(f"OpenCV could not open {files[fid]['name']}.")
            rows = []
            for seg in (s for s in cuts["segments"] if s["file"] == fid):
                t = seg["in"]
                while t < seg["out"]:
                    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
                    ok, frame = cap.read()
                    t += a.step
                    if not ok:
                        continue
                    h, w = frame.shape[:2]
                    sc = WIDTH / w
                    small = cv2.resize(frame, (WIDTH, int(h * sc)))
                    if det is None:
                        det = cv2.FaceDetectorYN.create(str(MODEL), "", (small.shape[1], small.shape[0]), 0.7)
                    det.setInputSize((small.shape[1], small.shape[0]))
                    _, faces = det.detect(small)
                    if faces is None or len(faces) == 0:
                        misses += 1
                        continue
                    f = max(faces, key=lambda r: r[2] * r[3])
                    x, y, fw, fh = f[:4]
                    eye_y = (f[5] + f[7]) / 2  # right-eye y, left-eye y
                    rows.append([round(t - a.step, 3), float((x + fw / 2) / small.shape[1]),
                                 float(eye_y / small.shape[0]), float(fh / small.shape[0])])
            cap.release()
            result[fid] = smooth(rows)
        write_json(edit / "camera" / "faces.json", {"step": a.step, "columns": ["time", "cx", "eye_y", "height"],
                                                    "files": result})
        emit({"ok": True, "output": str(edit / "camera" / "faces.json"),
              "samples": sum(len(v) for v in result.values()), "no_face_samples": misses})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
