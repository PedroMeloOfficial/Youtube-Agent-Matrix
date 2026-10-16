"""
Transcribe a voice recording of the creator, keeping the way they actually talk.

The voice agent learns how a creator speaks from samples of them speaking. The best
sample is the creator talking freely, as if recording a video -- and the natural way
to give that is a voice memo, not typed text. This turns the memo into text.

**Verbatim, not cleaned.** Speech-to-text models tidy speech by default: they drop
fillers, smooth false starts, normalise slang. For any other use that is a feature;
here it destroys the signal. The model is primed with a prompt full of the language's
discourse markers, which makes it far more likely to keep them, and no post-processing
is applied. Even so, a transcript under-represents fillers -- the voice agent is told so.

Runs locally. Nothing is uploaded anywhere, no credentials, no quota.

Requires ``faster-whisper`` (preferred; decodes audio itself) or ``openai-whisper``
(which also needs ``ffmpeg``). If neither model package is installed the script fails with the
install command and the manual fallback -- dictate into any app, or record on the
phone and use its built-in transcription, then paste the text. A missing transcriber
slows the voice workflow down; it never blocks it.

The first run downloads the model weights once (hundreds of MB for ``small``).

Usage:
    python execution/transcribe_audio.py memo.m4a --lang pt
    python execution/transcribe_audio.py memo.m4a --lang pt --output workspace/voice/samples/2026-10-14_free-talk.md
    python execution/transcribe_audio.py memo.wav --model medium

Exit 0 with ``{"ok": true, ...}``; exit 1 with ``{"ok": false, "error": {...}}``.
"""

from __future__ import annotations

import argparse
import shutil
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

AUDIO_SUFFIXES = {".m4a", ".mp3", ".wav", ".ogg", ".opus", ".flac", ".aac", ".webm", ".mp4", ".mov"}

# Priming prompts: plain speech dense with the language's fillers and colloquial
# forms. Whisper conditions on the prompt's style, so it keeps what it would
# otherwise clean away. Languages without an entry get no prompt.
PRIMING = {
    "pt": "Então, tipo, né, a gente tá aqui, sabe? Cara, tipo assim, pô, é, tá ligado? "
    "Aí, beleza, então, mano, olha só, sacou?",
    "en": "So, like, um, you know, I mean, uh, basically, right? Okay so, yeah, kind of, "
    "sort of, like.",
    "es": "Entonces, o sea, este, bueno, ¿sabes?, tipo, pues, vale, eh, ¿no?",
}


def pick_backend():
    try:
        import faster_whisper  # noqa: F401

        return "faster-whisper"
    except ImportError:
        pass
    try:
        import whisper  # noqa: F401

        return "openai-whisper"
    except ImportError:
        pass
    raise DependencyMissing(
        "No local speech-to-text model is installed, so the recording cannot be transcribed.",
        fix=[
            "Install one: `pip install faster-whisper` (preferred, faster on CPU) "
            "or `pip install openai-whisper`. openai-whisper also needs ffmpeg (`brew install ffmpeg`).",
            "Or skip this step: dictate the sample into any app, or use your phone's "
            "built-in transcription, and paste the text in. Keep the fillers and slang.",
        ],
    )


def transcribe(path: Path, lang: str | None, model_size: str, backend: str):
    prompt = PRIMING.get((lang or "").split("-")[0].lower())

    if backend == "faster-whisper":
        from faster_whisper import WhisperModel

        model = WhisperModel(model_size, device="auto", compute_type="int8")
        segments, info = model.transcribe(
            str(path),
            language=lang,
            initial_prompt=prompt,
            vad_filter=True,
            condition_on_previous_text=True,
        )
        parts = [s.text.strip() for s in segments]
        return parts, info.language, float(info.duration or 0)

    import whisper

    model = whisper.load_model(model_size)
    result = model.transcribe(str(path), language=lang, initial_prompt=prompt, fp16=False)
    parts = [s["text"].strip() for s in result.get("segments", [])]
    duration = result["segments"][-1]["end"] if result.get("segments") else 0.0
    return parts, result.get("language", lang), float(duration)


def main() -> None:
    install_excepthook()

    ap = argparse.ArgumentParser(
        description="Transcribe a creator's voice recording verbatim, fillers and slang kept."
    )
    ap.add_argument("audio", help="the recording (m4a, mp3, wav, ogg, ...)")
    ap.add_argument("--lang", help="language code, e.g. pt or en (default: auto-detect)")
    ap.add_argument(
        "--model",
        default="small",
        help="model size: tiny, base, small (default), medium, large-v3",
    )
    ap.add_argument("--output", help="write the transcript to this Markdown file")
    args = ap.parse_args()

    audio = Path(args.audio).expanduser()
    if not audio.exists():
        die(InputInvalid(f"{audio} does not exist.", fix="Check the path and try again."))
    if audio.suffix.lower() not in AUDIO_SUFFIXES:
        die(
            InputInvalid(
                f"{audio.name} does not look like an audio file.",
                fix=f"Pass one of: {', '.join(sorted(AUDIO_SUFFIXES))}.",
            )
        )

    try:
        backend = pick_backend()
        # faster-whisper decodes audio itself; openai-whisper shells out to ffmpeg.
        if backend == "openai-whisper" and not shutil.which("ffmpeg"):
            raise DependencyMissing(
                "ffmpeg is needed to read this audio format and is not installed.",
                fix="Install it (`brew install ffmpeg`), or convert the file to .wav first.",
            )

        try:
            parts, detected, duration = transcribe(audio, args.lang, args.model, backend)
        except ExecutionError:
            raise
        except Exception as exc:  # model download, decoding, corrupt file
            name = type(exc).__name__
            network = any(k in f"{name} {exc}".lower() for k in ("proxy", "connection", "http", "ssl", "timeout"))
            raise ExecutionError(
                "The model could not be downloaded." if network else "Transcription failed.",
                fix=(
                    "The first run downloads the model weights once and needs internet access. "
                    "Check the connection and try again."
                    if network
                    else "Check the file plays normally; if it does, try a .wav copy of it."
                ),
                details={"reason": f"{name}: {exc}"[:300]},
            ) from exc
        text = "\n\n".join(p for p in parts if p)
        if not text.strip():
            raise ExecutionError(
                "The recording produced no text.",
                fix="Check the file has speech in it and is not silent or corrupted.",
            )

        written = None
        if args.output:
            out = Path(args.output).expanduser()
            out.parent.mkdir(parents=True, exist_ok=True)
            header = (
                f"# Voice sample — {audio.name}\n\n"
                f"Source: audio recording · transcribed locally with {backend} ({args.model}) · "
                f"language: {detected} · duration: {duration:.0f}s\n\n"
                "Verbatim machine transcript. Fillers are likely under-represented.\n\n---\n\n"
            )
            out.write_text(header + text + "\n", encoding="utf-8")
            written = str(out)

        emit(
            {
                "ok": True,
                "backend": backend,
                "model": args.model,
                "language": detected,
                "duration_seconds": round(duration),
                "words": len(text.split()),
                "output": written,
                "text": text if not written else None,
                "note": "Machine transcripts drop some fillers even when primed; treat filler "
                "frequency as a lower bound.",
            }
        )
    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
