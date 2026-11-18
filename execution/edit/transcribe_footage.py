"""
Transcribe raw footage with a time for every word, for editing.

This is **not** ``execution/transcribe_audio.py``. That one serves voice samples and is
primed with filler words on purpose; priming and carried-over context are exactly what
make Whisper invent sentences or swallow repeated takes, which would be fatal here.
So this script runs with **no initial prompt** and **without conditioning on previous
text**, and then checks its own work:

1. **Speech regions** from Silero VAD (the ONNX model bundled with faster-whisper; no
   PyTorch) or, if that is missing, from audio energy -- the method used is reported.
2. **Transcription** with word timestamps:
   - ``mlx`` (default on Apple Silicon): ``mlx-whisper`` on the GPU, model
     ``mlx-community/whisper-large-v3-turbo``;
   - ``faster``: ``faster-whisper`` on the CPU, the fallback when MLX is unavailable.
3. **Sound without words**: every speech region with no transcribed word over it (a
   swallowed take, a mumble, a filler) is re-transcribed **on its own, without context**.
   What comes back is merged and flagged ``recovered``; what still has no words is listed
   in ``gaps`` so the cut step marks it instead of deleting it.
4. **Silences**: pauses between words (≥ 0.3 s) with their energy, for the cut step.

Outputs, per source file, into ``edit/transcript/``:
- ``<id>.words.json`` -- every word: text, start, end, probability (for scripts only);
- ``<id>.json`` -- regions, gaps, silences, engine, model;
- ``transcript.txt`` -- one sentence per line with timecode and marked pauses, across all
  camera files in recording order. **This is what the agents read.**

Times are seconds from the start of each file. Accuracy of word edges from Whisper is
roughly ±0.1–0.2 s; ``cut_edges.py`` refines every cut on the audio itself.

Runs locally. No credentials, no network after the first model download.

Usage:
    python execution/edit/transcribe_footage.py --footage <video>/edit/footage/footage.json --out-dir <video>/edit/transcript --lang pt
    python execution/edit/transcribe_footage.py ... --engine faster --model large-v3-turbo
    python execution/edit/transcribe_footage.py ... --only cam01
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from audio_tools import RATE, envelope, speech_regions, speech_threshold
from common import (
    DependencyMissing,
    ExecutionError,
    InputInvalid,
    die,
    emit,
    install_excepthook,
    read_json,
    read_pcm_mono,
    write_json,
    write_text,
)
from timebase import clock

MLX_MODEL = "mlx-community/whisper-large-v3-turbo"
FASTER_MODEL = "large-v3-turbo"
PAUSE_MARK = 0.6     # pause long enough to show in the transcript the agents read
SILENCE_MIN = 0.3    # pause long enough to map for the cut step
GAP_MIN = 0.35       # speech region without words worth re-checking


# --------------------------------------------------------------------- engines


def _words_from_segments(segments, offset: float = 0.0):
    out = []
    for seg in segments:
        words = seg.get("words") if isinstance(seg, dict) else getattr(seg, "words", None)
        for w in words or []:
            get = (lambda k: w.get(k)) if isinstance(w, dict) else (lambda k: getattr(w, k, None))
            text = (get("word") or "").strip()
            if not text:
                continue
            out.append({"w": text, "start": round(float(get("start")) + offset, 3),
                        "end": round(float(get("end")) + offset, 3),
                        "p": round(float(get("probability") or 0.0), 3)})
    return out


class Engine:
    def __init__(self, name: str, model: str | None, lang: str | None):
        self.name, self.lang = name, lang
        if name == "mlx":
            try:
                import mlx_whisper  # noqa: F401
            except ImportError as exc:
                raise DependencyMissing(
                    "mlx-whisper is not installed (needs a Mac with Apple Silicon).",
                    fix=["~/.local/share/youtube-agent-matrix/edit-venv/bin/pip install mlx-whisper",
                         "or run with --engine faster (CPU, slower)."]) from exc
            self.model = model or MLX_MODEL
        elif name == "faster":
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise DependencyMissing("faster-whisper is not installed.",
                                        fix="~/.local/share/youtube-agent-matrix/edit-venv/bin/pip install faster-whisper") from exc
            self.model = model or FASTER_MODEL
            self._fw = WhisperModel(self.model, device="cpu", compute_type="int8")
        else:
            raise InputInvalid(f"Unknown engine {name!r}.", fix="Use --engine mlx or --engine faster.")

    def words(self, pcm, offset: float = 0.0):
        if self.name == "mlx":
            import mlx_whisper

            kw = _supported(mlx_whisper.transcribe, path_or_hf_repo=self.model, language=self.lang,
                            word_timestamps=True, condition_on_previous_text=False,
                            initial_prompt=None, verbose=None, hallucination_silence_threshold=2.0)
            res = mlx_whisper.transcribe(pcm, **kw)
            return _words_from_segments(res.get("segments", []), offset)
        kw = _supported(self._fw.transcribe, language=self.lang, word_timestamps=True,
                        condition_on_previous_text=False, initial_prompt=None, vad_filter=False,
                        hallucination_silence_threshold=2.0)
        segs, _ = self._fw.transcribe(pcm, **kw)
        return _words_from_segments(list(segs), offset)


def _supported(fn, **kwargs):
    """Pass only the options this installed version accepts (they differ between releases).
    The ones that guard against invented text -- no prompt, no carried-over context, word
    timestamps -- exist in every version that can be used here."""
    import inspect

    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return kwargs
    # explicit parameters only; `language` is a decoding option and always accepted
    return {k: v for k, v in kwargs.items() if k in params or k == "language"}


# --------------------------------------------------------------------- analysis


def regions_without_words(regions, words, min_len=GAP_MIN):
    gaps = []
    for s, e in regions:
        if e - s < min_len:
            continue
        covered = [w for w in words if w["end"] > s and w["start"] < e]
        if not covered:
            gaps.append((s, e))
            continue
        # uncovered stretches inside a region (a swallowed repeat is often here)
        cursor = s
        for w in sorted(covered, key=lambda w: w["start"]):
            if w["start"] - cursor >= min_len * 2:
                gaps.append((cursor, w["start"]))
            cursor = max(cursor, w["end"])
        if e - cursor >= min_len * 2:
            gaps.append((cursor, e))
    return gaps


def silences(words, env, threshold, hop=0.01):
    out = []
    for a, b in zip(words, words[1:]):
        gap = b["start"] - a["end"]
        if gap >= SILENCE_MIN:
            lo, hi = int(a["end"] / hop), int(b["start"] / hop)
            seg = env[lo:hi] if hi > lo else env[lo:lo + 1]
            voiced = float((seg > threshold).mean()) if len(seg) else 0.0
            out.append({"start": a["end"], "end": b["start"], "length": round(gap, 3),
                        "voiced_fraction": round(voiced, 2)})
    return out


_END = re.compile(r"[.!?…]+[\"')\]]*$")


def sentences(words, file_id):
    lines, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        pause = (nxt["start"] - w["end"]) if nxt else 0.0
        if nxt is None or _END.search(w["w"]) or pause >= PAUSE_MARK or len(cur) >= 40:
            text = " ".join(x["w"] for x in cur)
            flag = " ⚑" if any(x.get("recovered") for x in cur) else ""
            low = " ?" if sum(x["p"] for x in cur) / len(cur) < 0.5 else ""
            lines.append({"file": file_id, "start": cur[0]["start"], "end": cur[-1]["end"],
                          "text": text + flag + low, "pause_after": round(pause, 2)})
            cur = []
    return lines


def render_txt(all_lines, gaps_by_file) -> str:
    out = ["# Transcript — one sentence per line",
           "# [file start–end] text   ⟨pause⟩ after it. ⚑ = recovered by re-transcription,",
           "# ? = low confidence. ◌ = sound without words (not transcribed). Times are file time.", ""]
    for fid, lines in all_lines:
        out.append(f"## {fid}")
        gaps = list(gaps_by_file.get(fid, []))
        for ln in lines:
            while gaps and gaps[0]["start"] < ln["start"]:
                g = gaps.pop(0)
                out.append(f"[{fid} {clock(g['start'])}–{clock(g['end'])}] ◌ sound without words")
            pause = f"   ⟨{ln['pause_after']:.1f}s⟩" if ln["pause_after"] >= PAUSE_MARK else ""
            out.append(f"[{fid} {clock(ln['start'])}–{clock(ln['end'])}] {ln['text']}{pause}")
        for g in gaps:
            out.append(f"[{fid} {clock(g['start'])}–{clock(g['end'])}] ◌ sound without words")
        out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------- main


def transcribe_file(engine: Engine, f: dict, out_dir: Path) -> dict:
    pcm = read_pcm_mono(Path(f["path"]), RATE)
    if len(pcm) < RATE // 2:
        raise InputInvalid(f"{f['name']} has less than half a second of audio.")
    regions, vad = speech_regions(pcm, RATE)
    words = engine.words(pcm)
    recovered = 0
    gaps_left = []
    for s, e in regions_without_words(regions, words):
        lo, hi = max(0, int((s - 0.1) * RATE)), min(len(pcm), int((e + 0.1) * RATE))
        extra = engine.words(pcm[lo:hi], offset=lo / RATE) if hi - lo > RATE // 4 else []
        extra = [w for w in extra if w["end"] > s and w["start"] < e]
        if extra:
            for w in extra:
                w["recovered"] = True
            words.extend(extra)
            recovered += len(extra)
        else:
            gaps_left.append({"start": round(s, 3), "end": round(e, 3)})
    words.sort(key=lambda w: w["start"])
    env = envelope(pcm)
    thr = speech_threshold(env)
    sil = silences(words, env, thr)
    write_json(out_dir / f"{f['id']}.words.json", {"file": f["id"], "words": words})
    meta = {"file": f["id"], "path": f["path"], "engine": engine.name, "model": engine.model,
            "vad": vad, "regions": [[round(a, 3), round(b, 3)] for a, b in regions],
            "gaps": gaps_left, "silences": sil, "recovered_words": recovered,
            "speech_threshold_db": round(thr, 1)}
    write_json(out_dir / f"{f['id']}.json", meta)
    return {"words": words, "gaps": gaps_left, "meta": meta}


def main() -> None:
    install_excepthook()
    ap = argparse.ArgumentParser(description="Word-timed transcription of raw footage, for editing.")
    ap.add_argument("--footage", required=True, help="edit/footage/footage.json")
    ap.add_argument("--out-dir", required=True, help="edit/transcript/")
    ap.add_argument("--lang", help="language code, e.g. pt, en (default: detect)")
    ap.add_argument("--engine", choices=("mlx", "faster"), default="mlx")
    ap.add_argument("--model", help="override the model name")
    ap.add_argument("--only", action="append", help="transcribe only these file ids")
    a = ap.parse_args()
    try:
        footage = read_json(Path(a.footage))
        out_dir = Path(a.out_dir).expanduser().resolve()
        files = [f for f in footage["files"] if f.get("role") in ("camera", "external_audio")
                 and f.get("readable", True) and f.get("has_audio")]
        if a.only:
            files = [f for f in files if f["id"] in a.only]
        if not files:
            raise InputInvalid("No camera or external-audio file with audio to transcribe.")
        lang = (a.lang or "").split("-")[0] or None
        engine = Engine(a.engine, a.model, lang)
        all_lines, gaps_by_file, summary = [], {}, []
        for f in files:
            res = transcribe_file(engine, f, out_dir)
            lines = sentences(res["words"], f["id"])
            all_lines.append((f["id"], lines))
            gaps_by_file[f["id"]] = res["gaps"]
            summary.append({"file": f["id"], "words": len(res["words"]), "sentences": len(lines),
                            "recovered_words": res["meta"]["recovered_words"],
                            "sound_without_words": len(res["gaps"]), "vad": res["meta"]["vad"]})
        write_text(out_dir / "transcript.txt", render_txt(all_lines, gaps_by_file))
        emit({"ok": True, "engine": engine.name, "model": engine.model, "output": str(out_dir / "transcript.txt"),
              "files": summary})
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
