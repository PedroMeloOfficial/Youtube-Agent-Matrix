# Delivery to Final Cut Pro (FCPXML)

> Partly adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/entrega-no-editor.md`
> (the Premiere/XML rules that carry over). The Final Cut specifics are this matrix's own, built
> from Apple's FCPXML reference and DTD. See `THIRD_PARTY_NOTICES.md`.

**Purpose.** How every editing stage reaches the creator: a Final Cut Pro project they import,
review, finish by hand — and can export back. Read by the editor skill and by any agent whose stage
ends in a delivery. Agents never write XML: `execution/edit/timeline_compose.py` assembles the
decisions and `execution/edit/fcpxml_build.py` writes and validates the file.

**Contents:** 1 What a delivery is · 2 Layout: spine, lanes, roles · 3 Time · 4 Clips point at
originals · 5 Markers · 6 Camera, levels, fades · 7 Versions and names · 8 Validation ·
9 The first-time test project · 10 The return trip · 11 What is not modelled

---

## 1. What a delivery is

An `.fcpxml` (or `.fcpxmld` bundle, if `edit-config.json` says so) containing one **event** and one
**project**. The creator imports it with **File → Import → XML…** into the library of their choice;
Final Cut asks which library. Nothing is written into a library by the matrix.

Deliveries, in order: `<slug>_cuts_vNN` (after the cut), `<slug>_motion_vNN` (cut + animations),
`<slug>_final_vNN` (cut + animations + camera + sound and music). Each contains everything approved
so far.

## 2. Layout: spine, lanes, roles

Final Cut has no tracks. The layout is fixed, so the creator always finds things in the same place:

| What | Where | Role |
|---|---|---|
| Camera takes (video + their own audio) | **spine** | `video` · `dialogue` |
| Screen recordings | lane **+1** | `video.screen` |
| Full-screen animations (MP4) | lane **+2** | `video.motion` |
| Overlays with alpha (MOV ProRes 4444) | lane **+3** | `video.overlay` |
| External microphone, synced | lane **−1** | `dialogue` |
| Sound effects | lanes **−2, −3, −4** — a new lane only when sounds overlap | `effects.sfx` |
| Music | lane **−5** | `music` |

Roles use Final Cut's built-in roles with subroles, so the Timeline Index can show, hide and solo
each family. A connected clip belongs to the spine clip it sits on; its offset is in that clip's
local time. The generator computes this — when a cut moves, everything connected moves with it,
which is what the creator expects in Final Cut.

## 3. Time

- Final Cut stores time as **rational seconds** (`1001/30000s`). Every offset, start and duration is
  an exact multiple of a frame: spine offsets and durations of the **sequence** rate, clip starts of
  the **source file's** rate.
- Rates are read from the file (`ffprobe` → `30000/1001`), never assumed. 29.97 is not 30: the error
  shows as drift that grows toward the end of a long video.
- One conversion function (`execution/edit/timebase.py`), used by every script, no floats.
- A clip's `start` is measured from the file's **timecode origin** — a camera file whose timecode
  begins at `01:00:00:00` is addressed from 3600 s. `probe_footage.py` reads it; drop-frame
  timecode is handled.
- The sequence takes the main camera's rate and size; the timeline starts at `00:00:00:00`.

## 4. Clips point at the originals

- Every clip references the **whole original file** by absolute `file://` URL and only defines the
  range used. Never a proxy, never a copy — the creator links proxies in Final Cut if they use them.
- The same file used twice is one asset.
- If a file moves after delivery, Final Cut shows it offline; relinking is the creator's call.

## 5. Markers

- The matrix's markers are **to-do markers** whose text starts with `[C]` ("Claude"): take doubts,
  hesitations kept, low-confidence spoken notes, missing assets, effects for post ("blur the
  background here"). The creator ticks them off in the Timeline Index.
- **Chapter markers** at the start of each section (the matrix's carry the note `matrix`). The
  metadata agent can reuse them as YouTube chapters.
- The creator's own markers — any colour, any text without `[C]` — come back as instructions on the
  return trip (§10).
- Markers are anchored to source time in the stage files, so they survive new versions of the cut.
- Text in the creator's output language, short and direct.

## 6. Camera, levels, fades

- **Camera** = keyframes of `scale` and `position` on each spine clip's Transform, one per frame
  during a move and thinned where the curve is straight, so the curve designed is the curve played.
  Position is written as a **percentage of the frame height** (x right, y up); confirmed by the
  first-time test (§9).
- **Levels**: `adjust-volume` per clip in dB. Sound effects are set against the voice's loudness
  (see `sound.md`).
- **Fades**: one frame in and out on every camera clip and every effect, to remove clicks at joins.
  Music fades in and out over about a second and ducks under speech with volume keyframes.
- **No native titles.** Any text on screen is rendered inside the animations — native titles depend
  on effect IDs that differ between machines.

## 7. Versions and names

- Never overwrite: `next_version()` picks the first free `_vNN`. Each stage continues its own
  numbering.
- Deliveries go to the video's `edit/deliveries/` folder. Writing inside a `.fcpbundle` is refused.
- The project inside is named `<slug> <stage>`; the event `Matrix · <slug>`.

## 8. Validation

- Every file is validated with `xmllint --dtdvalid` against the DTD of **the same FCPXML version**.
- The version is the one the installed Final Cut exports (`fcpxml_build.py --detect-version`:
  Final Cut 12 → 1.14, 11.1 → 1.13, 11.0 → 1.12, 10.7 → 1.11, 10.6 → 1.10), or the one set in
  `edit-config.json`.
- The DTD is found through `$FCPXML_DTD` or inside the installed Final Cut app. **If it cannot be
  found, the delivery says `validated: false` and the editor tells the creator** — never a silent
  substitute. Apple publishes only older DTDs online; the one inside the app is the authority.
- Validation failing is a generator bug, not the creator's problem: stop and report it.

## 9. The first-time test project

Before the first real delivery on a machine (or after a Final Cut update):

1. `make_test_media.py` creates synthetic media in `edit/test-media/`: a camera clip with a frame
   counter and timecode starting at 01:00:00:00, a full-screen render, an alpha overlay, a sound
   effect and a music bed.
2. The editor builds a test delivery from them with cuts, a screen/overlay/motion lane each, one
   camera move (scale and position), effects, ducked music, a to-do marker and a chapter marker.
3. The creator imports it and checks, in plain words: it opens without errors · the cuts land on the
   frame numbers shown · the overlay is transparent · the zoom moves the way described (and in the
   right direction) · effects and music sit on their roles at the expected levels · both markers
   show.
4. Confirmed → `edit-config.json` gets `"validated": {"fcpxml": "<version>", "date": "…"}`.
   Anything wrong → it is reported and fixed in the generator before any real video.

## 10. The return trip

- The creator may fix things in Final Cut and then **File → Export XML…** into `edit/returns/`.
- `fcpxml_read.py` reconstructs the spine as segments in source time, reads the creator's markers,
  the level changes, and a diff against the previous cut (added, removed, trimmed, reordered).
- **Their adjustments win.** Segments that came back are `locked`: no script re-refines their edges.
- Their level changes on approved deliveries are learnings for the profile.
- Manual changes to animations, camera or sound in Final Cut do not flow back into those stages —
  ask by number instead ("cam07 slower"), or keep the hand finishing for after the last stage.

## 11. What is not modelled (reported, never guessed)

Retimed clips, transitions, compound / multicam / synchronized clips, J/L split edits, video
effects, titles, clips from files the matrix does not know. The return trip lists each one with its
position; the creator's version stays as they left it in Final Cut.
