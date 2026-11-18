"""
Shared plumbing for the editing scripts in ``execution/edit/``.

Every script here follows rule 6 of ``CLAUDE.md`` as amended for editing: JSON on stdout,
no stack traces, ``--help`` via argparse. This module holds what they all need: the JSON
error helpers (re-exported from ``utils/youtube_auth.py``), ffmpeg/ffprobe runners that
fail with an install command instead of a traceback, JSON file I/O that never leaves a
half-written file, versioned output names that never overwrite a delivery, and the
``file://`` URL form Final Cut Pro expects.

Nothing in here touches the creator's media: every function either reads it or writes
into the video's ``edit/`` working folder.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from utils.youtube_auth import (  # noqa: E402,F401  (re-exported)
    DependencyMissing,
    ExecutionError,
    InputInvalid,
    die,
    emit,
    install_excepthook,
)

#: Where the editing virtualenv lives -- outside the plugin, which is read-only and is
#: replaced on every update. Documented in references/editing/setup.md.
EDIT_VENV = Path.home() / ".local" / "share" / "youtube-agent-matrix" / "edit-venv"

INSTALL = {
    "ffmpeg": "brew install ffmpeg",
    "ffprobe": "brew install ffmpeg",
    "xmllint": "xmllint ships with macOS; on Linux: apt install libxml2-utils",
    "numpy": f"{EDIT_VENV}/bin/pip install numpy",
    "mlx_whisper": f"{EDIT_VENV}/bin/pip install mlx-whisper",
    "faster_whisper": f"{EDIT_VENV}/bin/pip install faster-whisper",
    "cv2": f"{EDIT_VENV}/bin/pip install opencv-python-headless",
}


# --------------------------------------------------------------------------- tools


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise DependencyMissing(
            f"`{name}` is not installed, and this editing step needs it.",
            fix=INSTALL.get(name, f"Install {name} and try again."),
        )
    return path


def require_module(name: str):
    try:
        return __import__(name)
    except ImportError as exc:
        raise DependencyMissing(
            f"The Python package `{name}` is not installed in this environment.",
            fix=[
                INSTALL.get(name, f"pip install {name}"),
                f"Run editing scripts with {EDIT_VENV}/bin/python so they find it.",
            ],
        ) from exc


def run(cmd: list[str], timeout: int = 600, binary: bool = False):
    """Run a command; on failure raise ExecutionError with the tail of stderr."""
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ExecutionError(f"{Path(cmd[0]).name} timed out after {timeout}s.") from exc
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-6:]
        raise ExecutionError(
            f"{Path(cmd[0]).name} failed (exit {proc.returncode}).",
            details={"stderr": "\n".join(err)},
        )
    return proc.stdout if binary else proc.stdout.decode("utf-8", "replace")


def ffprobe_json(path: Path) -> dict:
    require_tool("ffprobe")
    out = run(
        [
            "ffprobe", "-v", "error", "-print_format", "json",
            "-show_format", "-show_streams", str(path),
        ],
        timeout=120,
    )
    return json.loads(out)


def read_pcm_mono(path: Path, rate: int = 16000, start: float | None = None,
                  duration: float | None = None):
    """Decode a file's first audio stream to mono float32 PCM with ffmpeg."""
    np = require_module("numpy")
    require_tool("ffmpeg")
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if start is not None:
        cmd += ["-ss", f"{max(0.0, start):.6f}"]
    cmd += ["-i", str(path)]
    if duration is not None:
        cmd += ["-t", f"{max(0.0, duration):.6f}"]
    cmd += ["-map", "0:a:0", "-ac", "1", "-ar", str(rate), "-f", "f32le", "-"]
    raw = run(cmd, timeout=3600, binary=True)
    return np.frombuffer(raw, dtype=np.float32)


# --------------------------------------------------------------------------- files


def read_json(path: Path, default=None):
    path = Path(path)
    if not path.exists():
        if default is not None:
            return default
        raise InputInvalid(f"{path} does not exist.", fix="Check the path, or run the step that writes it.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise InputInvalid(f"{path} is not valid JSON: {exc}") from exc


def write_json(path: Path, data) -> Path:
    """Atomic write: a crash never leaves a half-written state file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)
    return path


def write_text(path: Path, text: str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)
    return path


def next_version(folder: Path, stem: str, suffix: str) -> Path:
    """`<stem>_v01<suffix>`, `_v02`… -- the first name not taken. Never overwrites."""
    folder = Path(folder)
    taken = set()
    pattern = re.compile(re.escape(stem) + r"_v(\d{2,})" + re.escape(suffix) + r"$")
    if folder.exists():
        for p in folder.iterdir():
            m = pattern.match(p.name)
            if m:
                taken.add(int(m.group(1)))
    n = (max(taken) + 1) if taken else 1
    return folder / f"{stem}_v{n:02d}{suffix}"


def file_url(path: Path | str) -> str:
    """Absolute ``file://`` URL with percent-encoding, as Final Cut writes it."""
    p = Path(path).expanduser().resolve()
    return "file://" + quote(str(p), safe="/")


def path_from_url(url: str) -> Path:
    from urllib.parse import unquote, urlparse

    return Path(unquote(urlparse(url).path))


def guard_not_in_library(path: Path) -> None:
    """Refuse to write anywhere inside a Final Cut library bundle."""
    for part in Path(path).resolve().parts:
        if part.endswith(".fcpbundle"):
            raise InputInvalid(
                f"Refusing to write inside a Final Cut library: {path}",
                fix="Write deliveries to the video's edit/deliveries/ folder and import them.",
            )
