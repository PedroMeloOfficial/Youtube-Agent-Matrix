"""
Render a creator-facing Markdown file as a Word document.

Two deliverables in this system are written for a human rather than for an agent:
the recording script and the channel summary. Markdown is the wrong container for
both. A creator reading a script with a camera running does not want to parse
asterisks and backticks, and a summary they want to highlight and annotate belongs
in something that has real bold, real bullets and real headings.

So the agent writes Markdown -- which is what an agent is good at -- and this script
renders it to ``.docx``. The Markdown is an intermediate; the agent deletes it once
the document exists. Nothing downstream ever reads either file: derived creator-facing
views are never inputs to another agent.

**Never clobbers a document the creator has annotated.** Every render records the
output's SHA-256 in ``.reader-docs.json`` beside it. On the next render, a file whose
hash still matches is untouched and is overwritten in place; a file whose hash has
changed was edited by hand, so the new version is written as ``<name>-v2.docx``
(``-v3`` and so on) and the response says which file it wrote and why.

Rendering conventions -- the Markdown this reads is written for this converter:

  ``# Heading``      document title
  ``## Heading``     section heading
  ``### Heading``    sub-heading
  ``> line``         stage direction: rendered small, grey and italic, so it is
                     visually impossible to confuse with a line to say out loud
  plain paragraph    spoken text or prose, rendered at reading size
  ``- item``         real bulleted list
  ``| a | b |``      real table with a header row
  ``---``            ignored; spacing is handled by the styles
  ``**bold**`` / ``*italic*`` / ``` `code` ``` render as real formatting

Requires ``python-docx``. If it is missing, ``pandoc`` is used instead when present,
which produces a plainer but perfectly usable document. If neither exists the script
fails with the exact install command, and the caller keeps the Markdown -- a missing
converter degrades the deliverable's format, never the pipeline.

Usage:
    python execution/build_reader_doc.py INPUT.md
    python execution/build_reader_doc.py INPUT.md --output path/to/Name.docx
    python execution/build_reader_doc.py INPUT.md --title "Recording Script"
    python execution/build_reader_doc.py INPUT.md --overwrite     # ignore hand edits

Exit 0 with ``{"ok": true, ...}``; exit 1 with ``{"ok": false, "error": {...}}``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.youtube_auth import (  # noqa: E402
    DependencyMissing,
    ExecutionError,
    InputInvalid,
    die,
    emit,
    install_excepthook,
)

MANIFEST_NAME = ".reader-docs.json"

# Point sizes chosen for reading off a screen at arm's length while recording.
BODY_PT = 13
DIRECTION_PT = 10.5


# --------------------------------------------------------------------------- utils


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(folder: Path) -> dict:
    path = folder / MANIFEST_NAME
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def save_manifest(folder: Path, data: dict) -> None:
    try:
        (folder / MANIFEST_NAME).write_text(
            json.dumps(data, indent=2, sort_keys=True), encoding="utf-8"
        )
    except OSError:
        pass  # the manifest is an optimisation, never load-bearing


def resolve_target(output: Path, overwrite: bool) -> tuple[Path, str]:
    """Return the path to write and why. Never silently replaces a hand-edited file."""
    if not output.exists():
        return output, "created"
    if overwrite:
        return output, "overwritten (--overwrite)"

    recorded = load_manifest(output.parent).get(output.name)
    if recorded and recorded == sha256_of(output):
        return output, "overwritten (unchanged since last render)"

    stem, suffix = output.stem, output.suffix
    base = re.sub(r"-v\d+$", "", stem)
    for n in range(2, 100):
        candidate = output.with_name(f"{base}-v{n}{suffix}")
        if not candidate.exists():
            return candidate, f"written as a new version — {output.name} has been edited by hand"
    raise InputInvalid(
        f"{output.name} already has 98 versions beside it.",
        fix="Archive the old ones, or pass --overwrite to replace the file in place.",
    )


# ------------------------------------------------------------------- markdown model


def parse_blocks(text: str):
    """Markdown subset -> ('kind', payload) blocks. Deliberately small and predictable."""
    lines = text.replace("\r\n", "\n").split("\n")
    blocks, i = [], 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            blocks.append(("heading", (len(m.group(1)), m.group(2).strip())))
            i += 1
            continue

        if stripped.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]).strip())
                i += 1
            blocks.append(("direction", " ".join(x for x in buf if x)))
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                blocks.append(("table", rows))
            continue

        m = re.match(r"^[-*+]\s+(.*)$|^\d+[.)]\s+(.*)$", stripped)
        if m:
            items, ordered = [], bool(re.match(r"^\d+[.)]\s", stripped))
            while i < len(lines):
                cur = lines[i].strip()
                mm = re.match(r"^[-*+]\s+(.*)$|^\d+[.)]\s+(.*)$", cur)
                if not mm:
                    break
                items.append((mm.group(1) or mm.group(2) or "").strip())
                i += 1
            blocks.append(("list", (ordered, items)))
            continue

        buf = []
        while i < len(lines):
            cur = lines[i].strip()
            if (
                not cur
                or cur.startswith(("#", ">", "|", "- ", "* ", "+ "))
                or re.match(r"^\d+[.)]\s", cur)
                or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", cur)
            ):
                break
            buf.append(cur)
            i += 1
        if buf:
            blocks.append(("paragraph", " ".join(buf)))

    return blocks


INLINE = re.compile(r"(\*\*.+?\*\*|(?<!\*)\*[^*]+?\*(?!\*)|`[^`]+?`)", re.S)


def add_runs(paragraph, text: str, size_pt: float, italic=False, grey=False):
    from docx.shared import Pt, RGBColor

    for part in INLINE.split(text):
        if not part:
            continue
        bold = it = mono = False
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            part, bold = part[2:-2], True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            part, it = part[1:-1], True
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            part, mono = part[1:-1], True

        run = paragraph.add_run(part)
        run.bold = bold
        run.italic = it or italic
        run.font.size = Pt(size_pt)
        if mono:
            run.font.name = "Menlo"
        if grey:
            run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)


# ------------------------------------------------------------------ docx rendering


def render_with_python_docx(blocks, target: Path, title: str | None) -> None:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor

    doc = Document()

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(BODY_PT)
    normal.paragraph_format.space_after = Pt(10)
    normal.paragraph_format.line_spacing = 1.25

    if title:
        h = doc.add_heading(title, level=0)
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT

    seen_h1 = False
    for kind, payload in blocks:
        if kind == "heading":
            level, text = payload
            if level == 1 and not title and not seen_h1:
                doc.add_heading(text, level=0)
                seen_h1 = True
            else:
                doc.add_heading(text, level=min(max(level, 1), 4))

        elif kind == "direction":
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(14)
            p.paragraph_format.space_after = Pt(8)
            add_runs(p, payload, DIRECTION_PT, italic=True, grey=True)

        elif kind == "paragraph":
            p = doc.add_paragraph()
            add_runs(p, payload, BODY_PT)

        elif kind == "list":
            ordered, items = payload
            style = "List Number" if ordered else "List Bullet"
            for item in items:
                p = doc.add_paragraph(style=style)
                add_runs(p, item, BODY_PT)

        elif kind == "table":
            rows = payload
            cols = max(len(r) for r in rows)
            table = doc.add_table(rows=0, cols=cols)
            table.style = "Light Grid Accent 1"
            for r_i, row in enumerate(rows):
                cells = table.add_row().cells
                for c_i in range(cols):
                    text = row[c_i] if c_i < len(row) else ""
                    para = cells[c_i].paragraphs[0]
                    add_runs(para, text, BODY_PT - 1.5)
                    if r_i == 0:
                        for run in para.runs:
                            run.bold = True

    doc.save(str(target))


def render_with_pandoc(source: Path, target: Path) -> None:
    try:
        subprocess.run(
            ["pandoc", str(source), "-o", str(target)],
            check=True,
            capture_output=True,
            timeout=120,
        )
    except subprocess.CalledProcessError as exc:
        raise ExecutionError(
            "pandoc could not convert the file.",
            fix="Check that the Markdown is well formed, or install python-docx "
            "(pip install python-docx) for the richer renderer.",
            details=(exc.stderr or b"").decode("utf-8", "replace")[:500],
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise ExecutionError("pandoc timed out after 120s.") from exc


def pick_renderer():
    try:
        import docx  # noqa: F401

        return "python-docx"
    except ImportError:
        pass
    if shutil.which("pandoc"):
        return "pandoc"
    raise DependencyMissing(
        "Neither python-docx nor pandoc is available, so the Word file cannot be built.",
        fix="Install one of them: `pip install python-docx` (preferred, richer output) "
        "or `brew install pandoc`. Until then the Markdown version is the deliverable.",
    )


# ------------------------------------------------------------------------- entry


def main() -> None:
    install_excepthook()

    ap = argparse.ArgumentParser(
        description="Render a creator-facing Markdown file as a Word document."
    )
    ap.add_argument("input", help="the Markdown file to render")
    ap.add_argument("--output", help="target .docx (default: same name, .docx extension)")
    ap.add_argument("--title", help="document title; defaults to the file's first H1")
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="replace the target even if it was edited by hand",
    )
    ap.add_argument(
        "--keep-source",
        action="store_true",
        help="keep the Markdown file (default: the caller deletes it)",
    )
    args = ap.parse_args()

    source = Path(args.input).expanduser()
    if not source.exists():
        die(InputInvalid(f"{source} does not exist.", fix="Check the path and try again."))
    if source.suffix.lower() not in (".md", ".markdown", ".txt"):
        die(
            InputInvalid(
                f"{source.name} is not a Markdown file.",
                fix="Pass the .md file the agent wrote.",
            )
        )

    output = Path(args.output).expanduser() if args.output else source.with_suffix(".docx")
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        renderer = pick_renderer()
        target, disposition = resolve_target(output, args.overwrite)

        if renderer == "python-docx":
            text = source.read_text(encoding="utf-8")
            blocks = parse_blocks(text)
            if not blocks:
                die(
                    InputInvalid(
                        f"{source.name} has no renderable content.",
                        fix="The agent should write the document body before converting it.",
                    )
                )
            render_with_python_docx(blocks, target, args.title)
        else:
            render_with_pandoc(source, target)

        manifest = load_manifest(target.parent)
        manifest[target.name] = sha256_of(target)
        save_manifest(target.parent, manifest)

        if not args.keep_source:
            try:
                source.unlink()
                source_state = "deleted"
            except OSError:
                source_state = "kept (could not be deleted)"
        else:
            source_state = "kept"

        emit(
            {
                "ok": True,
                "output": str(target),
                "renderer": renderer,
                "disposition": disposition,
                "markdown_source": source_state,
                "hand_edited_preserved": "-v" in target.stem and target != output,
            }
        )
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
