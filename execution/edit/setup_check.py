"""
Report what the editing layer can use on this machine -- without installing anything.

The editor runs this on ``/yt edit setup`` and whenever a step fails for a missing tool.
It lists each requirement, whether it is present, and the exact command to install what
is missing, so the creator decides before anything is installed.

Checks: ffmpeg/ffprobe, xmllint, the editing virtualenv and its packages (numpy,
mlx-whisper, faster-whisper, OpenCV), Node.js/npx (HyperFrames), the YuNet face model,
the installed Final Cut Pro version, the FCPXML version it uses and its DTD.

Usage:
    python execution/edit/setup_check.py
"""

from __future__ import annotations

import argparse
import importlib.util
import platform
import shutil
import subprocess
import sys

from common import EDIT_VENV, INSTALL, emit, install_excepthook
from face_track import MODEL, MODEL_URL
from fcpxml_build import detect_version, find_dtd


def version_of(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def main() -> None:
    install_excepthook()
    argparse.ArgumentParser(description="What the editing layer can use on this machine.").parse_args()
    checks = []

    def add(name, ok, detail, fix=None, needed_for=""):
        checks.append({"name": name, "ok": bool(ok), "detail": detail, "needed_for": needed_for,
                       **({} if ok else {"install": fix})})

    for tool, need in (("ffmpeg", "everything"), ("ffprobe", "everything"), ("xmllint", "validating deliveries")):
        p = shutil.which(tool)
        add(tool, p, version_of([tool, "-version"]) if p and tool != "xmllint" else p, INSTALL[tool], need)
    in_venv = sys.prefix == str(EDIT_VENV) or str(EDIT_VENV) in sys.executable
    add("editing virtualenv", EDIT_VENV.exists(), str(EDIT_VENV),
        f"python3 -m venv {EDIT_VENV}", "Python packages below")
    for mod, need in (("numpy", "audio analysis"), ("mlx_whisper", "transcription on Apple Silicon (GPU)"),
                      ("faster_whisper", "speech detection (VAD); CPU transcription fallback"),
                      ("cv2", "face tracking for the camera (optional)")):
        add(mod, importlib.util.find_spec(mod) is not None, "installed" if importlib.util.find_spec(mod) else "missing",
            INSTALL[mod], need)
    add("node / npx", shutil.which("npx"), version_of(["node", "--version"]), "brew install node",
        "animations (HyperFrames)")
    add("YuNet face model", MODEL.exists(), str(MODEL),
        f"mkdir -p '{MODEL.parent}' && curl -L -o '{MODEL}' {MODEL_URL}", "face tracking (optional)")
    fcp = detect_version()
    add("Final Cut Pro", fcp["app"], f"{fcp['fcp_version']} → FCPXML {fcp['fcpxml_version']}" if fcp["app"] else "not found in /Applications",
        "Install Final Cut Pro, or set fcpxml_version in workspace/edit-config.json", "the delivery version")
    dtd = find_dtd(fcp["fcpxml_version"] or "1.14")
    add("FCPXML DTD", dtd, str(dtd) if dtd else "not found",
        "Set FCPXML_DTD to the .dtd inside Final Cut Pro.app (find /Applications/Final\\ Cut*.app -name '*.dtd')",
        "validating deliveries")
    emit({"ok": True, "platform": f"{platform.system()} {platform.machine()}", "python": sys.version.split()[0],
          "running_in_edit_venv": in_venv, "checks": checks,
          "missing": [c["name"] for c in checks if not c["ok"]]})


if __name__ == "__main__":
    main()
