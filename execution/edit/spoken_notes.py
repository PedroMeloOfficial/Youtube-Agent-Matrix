"""
Find spoken editing notes in the transcript.

Creators can leave instructions for the editor while recording -- "edit note, use this
take, end of note". This script finds each note in the word-timed transcript, tolerating
transcription variants, and writes ``edit/footage/notes.json``. The whole note, opening
and closing phrases included, is later removed from the cut; its content goes to the
stage it concerns.

- the opening and closing phrases come from ``workspace/edit-config.json``
  (``spoken_notes.open`` / ``spoken_notes.close``) or ``--open`` / ``--close``;
- matching ignores case, accents and punctuation, and accepts near misses (one word
  dropped or misheard), scored by similarity;
- an opening with no closing ends at the next pause of 1 s or more, marked ``low``
  confidence for the creator to check.

Usage:
    python execution/edit/spoken_notes.py --transcript-dir <video>/edit/transcript --out <video>/edit/footage/notes.json --open "edit note" --close "end of note"
"""

from __future__ import annotations

import argparse
import difflib
import re
import unicodedata
from pathlib import Path

from common import ExecutionError, InputInvalid, die, emit, install_excepthook, read_json, write_json

THRESHOLD = 0.78
LONG_PAUSE = 1.0


def norm(text: str) -> str:
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", "", t).strip()


def find_phrase(words, phrase: str, start_idx: int = 0):
    """Yield (i, j, score): words[i:j] best matching the phrase, scanning forward."""
    target = norm(phrase)
    n = len(target.split())
    if n == 0:
        return
    tokens = [norm(w["w"]) for w in words]

    def best_at(i):
        best = None
        for size in (n - 1, n, n + 1):
            if size < 1 or i + size > len(words):
                continue
            cand = " ".join(t for t in tokens[i:i + size] if t)
            score = difflib.SequenceMatcher(None, cand, target).ratio()
            if best is None or score > best[2]:
                best = (i, i + size, score)
        return best

    i = start_idx
    while i < len(words):
        best = best_at(i)
        if best and best[2] >= THRESHOLD:
            # a window starting one word later may fit better (e.g. "take, end of note")
            nxt = best_at(i + 1)
            if nxt and nxt[2] > best[2]:
                i += 1
                continue
            yield best
            i = best[1]
        else:
            i += 1


def find_notes(words, open_p: str, close_p: str, file_id: str):
    notes = []
    opens = list(find_phrase(words, open_p))
    for k, (i, j, s_open) in enumerate(opens):
        limit = opens[k + 1][0] if k + 1 < len(opens) else len(words)
        close = next(find_phrase(words[:limit], close_p, j), None)
        if close:
            ci, cj, s_close = close
            end_idx, conf = cj - 1, "high" if min(s_open, s_close) > 0.9 else "medium"
            body = words[j:ci]
        else:
            end_idx = j
            while end_idx + 1 < limit and words[end_idx + 1]["start"] - words[end_idx]["end"] < LONG_PAUSE:
                end_idx += 1
            body, conf = words[j:end_idx + 1], "low"
        notes.append({"file": file_id, "start": words[i]["start"], "end": words[end_idx]["end"],
                      "text": " ".join(w["w"] for w in body).strip(), "confidence": conf})
    return notes


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Find spoken editing notes in the word-timed transcript.")
    ap.add_argument("--transcript-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--open", required=True, help="opening phrase, as spoken")
    ap.add_argument("--close", required=True, help="closing phrase, as spoken")
    a = ap.parse_args()
    try:
        tdir = Path(a.transcript_dir).expanduser()
        files = sorted(tdir.glob("*.words.json"))
        if not files:
            raise InputInvalid("No *.words.json in the transcript folder.", fix="Run transcribe_footage.py first.")
        notes = []
        for f in files:
            data = read_json(f)
            notes += find_notes(data["words"], a.open, a.close, data["file"])
        for n, note in enumerate(notes, 1):
            note["id"] = f"n{n:02d}"
        write_json(Path(a.out), {"open": a.open, "close": a.close, "notes": notes})
        emit({"ok": True, "output": a.out, "notes": len(notes),
              "low_confidence": sum(1 for x in notes if x["confidence"] == "low")})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
