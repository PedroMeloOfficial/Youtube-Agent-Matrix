# Style References and the Edit Profile

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/referencias.md` and
> `modelos/perfil.md`. Translated and adapted, not copied.

**Purpose.** How the creator's taste is measured from references and written into
`workspace/edit-profile/`. Read by `edit-style-agent`; every other editing agent reads the profile it
produces. Without references the matrix animates "at the average"; with them it measures what the
creator likes and turns it into rules.

**Contents:** 1 Gathering references · 2 Looking · 3 Measuring · 4 Writing the profile ·
5 Checking with the creator · 6 Growing the profile

---

## 1. Gathering references

- 5–10 short clips (5–30 s) of videos whose animation, camera or editing the creator would like to have.
  Different channels are fine.
- One clip per file in `workspace/edit-profile/references/`, each with one line from the creator: what
  caught their eye ("the way the cards come in", "the camera never stops").
- References measure **how things move**. They are never a design to copy.

## 2. Looking (what is seen)

- **Dense contact sheets:** frames every few frames, side by side, with the time on each — they show
  how an element enters, settles and leaves.
- **Scene cuts:** a scene detector (PySceneDetect, or ffmpeg's scene score) separates shots; one sheet
  per shot with start, middle and end.
- **A summary strip per reference:** 6–8 frames in one image — what is re-read later instead of opening
  everything again.

## 3. Measuring (what is felt)

- **Camera:** zoom, shift and rotation frame by frame, from optical flow and a global affine transform
  (tracked points + RANSAC). Shows whether the camera stops or keeps drifting, and with what curve.
- **Elements:** optical flow minus what the camera explains — what moves on its own.
- **Fades and brightness:** frame differences (a fade produces no optical flow).
- **Curves:** for each marked movement, from the last still frame before to the first still frame after,
  compare the measured curve with GSAP curves (`power2.out`, `expo.out`, `power4.in`…); record the closest
  and the duration in frames.
- Tracking fails in dark and very blurred frames (near fast cuts): measure up to 1–2 frames before.

The measuring scripts (OpenCV, NumPy, ffmpeg) are written on the first analysis, into the video's or the
profile's working folder, and reused.

## 4. Writing the profile

One sheet per reference (what was measured, with numbers) and a synthesis. From the synthesis:

| File | Decides | Read by |
|---|---|---|
| `identity.md` | colours (codes), fonts, background, material (glass, paper, flat, 3D), logo, what never to use — **from the creator and the channel profile, not from references** | motion plan, motion render |
| `motion-style.md` | speeds and curves, overshoot (if any, how much), secondary motion (how much), scene transitions, animation density per section, sentence emphasis | motion plan, motion render |
| `camera-style.md` | close-shot scale, punch strength, slow push, how much movement in hook and body, face lock | motion plan, camera |
| `cut-style.md` | air between sentences, edge padding, hesitations, how the creator records | cuts |
| `sound-style.md` | density by section, weight, favourite sounds, level targets by category | sound |
| `catalog.md` | animation patterns that worked (repertoire, never an obligation) | motion plan |
| `pieces/` | reusable elements (CSS look + JS movement) and channel pieces such as the intro sting | motion render |

`motion-style.md` uses the same section numbers as `motion-craft.md` (§1 speed, §2 curves, §3 camera…),
so it is obvious where the profile overrides craft — and when it does, the profile wins.

**Every rule carries its number and its origin** ("entries ~15 frames, `expo.out`, refs 02 and 05";
"asked on 2026-03-12"). A rule without an origin is a guess.

## 5. Checking with the creator

Show the synthesis in plain words: 3–5 sentences like "your favourite videos do X". The creator
confirms, corrects or adds. The profile is theirs; references only help put into words what they
already feel.

## 6. Growing the profile

- Start simple; the profile grows with the learnings notebook.
- On approval of motion, a pattern that repeated becomes a catalogue item; an element that turned out
  well becomes a reusable piece.
- Level changes the creator made by hand in Final Cut on an approved delivery update the sound targets.
