# Footage: Inventory, Sync, Transcription, Spoken Notes

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/etapa-iniciar-preparar.md`
> and `guias/decisoes.md` §4–5. Translated and adapted, not copied.

**Purpose.** The footage stage turns raw files into something an agent can read: an inventory, sync,
a word-timed transcript and the spoken notes. Read by `footage-agent`. It decides nothing about the
edit — it prepares.

**Contents:** 1 Inventory · 2 Sync · 3 Transcription · 4 What the transcript swallowed ·
5 Silences · 6 Spoken notes · 7 What the agents read · 8 Using the pre-production

---

## 1. Inventory (`probe_footage.py`)

- Every file: duration, real frame rate (a fraction), resolution, codec, audio, timecode origin,
  recording date. Ordered by recording date (metadata; else file time — said so).
- **Main camera**: the first camera file. All project times are in the camera files' own time.
- **Alerts** to pass on, never hide: unreadable file · video without audio · frame rate differing from
  the main camera · **variable frame rate** (typical of screen recordings; it breaks sync and can drift
  in Final Cut — suggest re-exporting at a constant rate).
- Roles are guessed (camera / screen / external audio) and can be corrected with `--role`.
- Proxies: if the creator uses them, note it; deliveries still point at originals.

## 2. Sync (`sync_audio.py`)

- Screen recordings and external audio are synced to the camera by **cross-correlating the sound**,
  camera audio as reference. A screen recording is often partial: the offset says *where* it starts
  inside a camera file.
- Each sync = offset + confidence (`camera_time = file_time + offset`).
- Confidence below 0.3, or a file without audio: **do not guess**. Ask the creator to point at one
  distinctive moment, and confirm one memorable word in both files.
- Main audio: the camera's, unless there is an external microphone. If the external audio covers only
  part of the recording, ask which to use.

## 3. Transcription (`transcribe_footage.py`)

- From the main audio. Language from `workspace/config.json`.
- **No prompt, no carried-over context** (see `setup.md` §5). The approved script and the briefing are
  for checking spelling and recognizing takes **when reading** — never fed to the transcriber, and
  never used to replace what was said.
- Output per file: `<id>.words.json` (scripts only) and `transcript.txt` (agents read this).

## 4. What the transcript swallowed

Whisper sometimes drops a repeated take, a mumble or a filler, or invents text when it has context.
The script checks itself:

- speech regions (Silero VAD, or energy if missing) with no word over them are **re-transcribed
  alone, without context**; recovered words are flagged ⚑ in the transcript;
- what still has no words is listed as **◌ sound without words** in the transcript and in the file's
  `gaps` — the cut stage looks there before calling a sentence incomplete, and marks instead of cutting.

Tell the creator how many words were recovered and how many gaps remain.

## 5. Silences

Pauses between words of 0.3 s or more are mapped with how much voice energy they hold (a pause that
still has voice in it is likely an untranscribed filler). This stage only maps; the cut stage cuts.

## 6. Spoken notes (`spoken_notes.py`)

- Find every "<open phrase> … <close phrase>" from `edit-config.json`, tolerating transcription
  variants. Each note applies to what was **just said** unless it says otherwise.
- Record file, start and end (phrases included — the whole stretch leaves the cut), the text, a
  one-line interpretation and which stage it concerns (cuts, motion, camera, sound, other).
- An opening without a closing ends at the next pause of 1 s or more, with **low** confidence — listed
  for the creator.

## 7. What the agents read

`transcript.txt`: one sentence per line, `[file mm:ss.s–mm:ss.s] text ⟨pause⟩`, ⚑ recovered, ? low
confidence, ◌ sound without words. Word-level files are opened only by scripts, or for one specific
stretch.

## 8. Using the pre-production

When the video went through the matrix's pre-production, the editor passes its paths:
- **approved script** (`script-<x>-*.md`): recognize takes and correct spellings of names and terms
  when reading; `[BEAT]` lines are deliberate pauses; `[B-ROLL:]`, `[SCREEN:]`, `[DATA:]` feed the
  motion plan;
- **voice profile** (`workspace/voice/profile.md`): the creator's fillers and verbal habits — what is
  a habit to keep vs a stumble to cut;
- **research report** / dossier: the source of any number shown on screen.
Never treat the script as a transcript: what was said is what is in the footage.
