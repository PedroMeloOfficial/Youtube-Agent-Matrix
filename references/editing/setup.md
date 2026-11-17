# Editing Setup

> Partly adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/decisoes.md` and
> `SKILL.md` (environment and interview). Translated and adapted, not copied.

**Purpose.** What `/yt edit setup` asks, checks and installs, and where the answers live. Read by
the editor skill. Runs once per creator; re-run any time to change an answer.

**Contents:** 1 Environment · 2 Installation · 3 The setup questions · 4 `edit-config.json` ·
5 Transcription choice · 6 First-time delivery test

---

## 1. Environment

Run `execution/edit/setup_check.py` first. It installs nothing; it reports what is present and the
exact command for what is missing:

| Need | Used for | Without it |
|---|---|---|
| ffmpeg / ffprobe | everything | editing cannot start |
| xmllint | validating deliveries | deliveries are marked unvalidated |
| editing virtualenv + numpy | audio analysis | editing cannot start |
| mlx-whisper | transcription on the Apple Silicon GPU | use `--engine faster` (CPU, slower) |
| faster-whisper | speech detection (Silero VAD, no PyTorch); CPU transcription | energy-based detection, said so |
| Node.js ≥ 22 / npx | HyperFrames animations | no motion stage |
| OpenCV + YuNet model | face-aware camera framing | camera stays centred |
| Final Cut Pro (and its DTD) | delivery version and validation | set the version by hand |

Nothing runs on a GPU other than Apple's; no NVIDIA card is assumed.

## 2. Installation (only after the creator says yes)

```bash
brew install ffmpeg node                                     # if missing
python3 -m venv ~/.local/share/youtube-agent-matrix/edit-venv
~/.local/share/youtube-agent-matrix/edit-venv/bin/pip install -r "${CLAUDE_PLUGIN_ROOT}/execution/edit/requirements.txt"
```

The virtualenv lives **outside the plugin** (the plugin is replaced on every update) and outside
the system Python. Every editing script is run with that virtualenv's `python`. Model weights
download once on first use (transcription: about 1.5 GB for `large-v3-turbo`). Explain each step in
one line before running it, and stop at the first refusal.

## 3. The setup questions

One question (or one small linked block) at a time, each with a recommendation and a one-line why.
Recommendations below are **craft defaults** — the creator's answer wins.

1. **Where they review.** In Final Cut Pro (the supported path). Detect the version; confirm it.
2. **Format.** Horizontal 16:9 is the default; vertical 9:16 for Shorts. Frame rate and size are
   **always read from the files**, never asked.
3. **Raw footage folder pattern.** Where they keep raw files (e.g. one folder per video). The matrix
   only reads it. Multiple files per video are normal; they are ordered by recording date.
4. **Camera and microphone.** One camera? External microphone? (Decides whether sync is needed.)
5. **Spoken editing notes.** Suggest the habit: say an opening phrase, the instruction, a closing
   phrase while recording ("edit note … end of note", in their language). Agree both phrases.
6. **Pace.** Air left between sentences: tight (~0.15 s), natural (~0.25 s), relaxed (~0.4 s).
7. **Hesitations.** Default: cut only isolated, long ones; keep the rest and mark them.
8. **Animation.** Yes/no; density by section (hook denser, body only where it explains, close
   light); full-screen and/or overlays. Brand colours and fonts (hex + font names) — or let the
   style agent propose from references.
9. **Camera.** Close-shot scale (125% default), punch strength, slow push, face lock for emphasis.
10. **Sound.** Effects density (low / medium / high). Path to their sound-effect library — or build
    a first free library with clear licences. Music: never / optional per video (default) / always,
    and the path to their music folder.
11. **Review points.** Default: review in Final Cut after cuts, after motion, and the final; the
    motion plan by chat.
12. **References.** 5–10 short clips (5–30 s) of videos whose editing they like, each with one line on
    why. Without them motion tends to the average. Not blocking: the profile can start simple.

Record each answer as it is given, not at the end.

## 4. `workspace/edit-config.json`

Owned by the editor skill. Shape:

```json
{
  "review_in": "final-cut",
  "fcpxml_version": "1.14", "bundle": false,
  "validated": null,
  "raw_pattern": "/abs/path/to/raw/<video>/",
  "spoken_notes": {"open": "<phrase>", "close": "<phrase>"},
  "cuts": {"air": 0.25, "padding": 0.10, "hesitations": "isolated-long-only"},
  "motion": {"enabled": true, "density": {"hook": "high", "body": "medium", "close": "low"},
             "hyperframes_version": null},
  "camera": {"closed_scale": 1.25, "punch": 0.10, "creep": 0.05, "face_lock": "emphasis-only"},
  "sound": {"density": "medium", "library": "/abs/path/SFX", "index": "workspace/edit-profile/sound-index.json",
            "music": "optional", "music_library": "/abs/path/Music", "targets_lu": {}},
  "review_points": ["cuts", "motion", "final"],
  "transcription": {"engine": "mlx", "model": null, "language": "<from workspace/config.json>"}
}
```

Craft defaults the profile overrides are listed in the stage references, each marked as such.

## 5. Transcription choice

| Engine | Runs on | Word times | Notes |
|---|---|---|---|
| **mlx-whisper** `large-v3-turbo` (default) | Apple Silicon GPU | yes (alignment inside Whisper) | fast, light install, strong in Portuguese, Spanish and English |
| faster-whisper `large-v3-turbo` | CPU | yes | fallback; same model family; slower |

Both run **without a prompt and without carrying context between windows** — the two settings that
make Whisper invent sentences or swallow repeated takes — and both are followed by the
sound-without-words check (`footage.md` §4). Word edges from Whisper are within ±0.1–0.2 s; cuts are
refined on the audio, so that never reaches the edit. Other engines (forced alignment, Parakeet) can
be added behind the same interface if a real video shows a need.

## 6. First-time delivery test

Last step of setup: `execution/edit/test_project.py`, then `delivery-fcpxml.md` §9. Setup is complete
only when the creator confirms the test project in Final Cut.
