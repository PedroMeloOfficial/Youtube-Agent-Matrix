# Building and Rendering Animations with HyperFrames

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/hyperframes.md` and
> `guias/etapa-motion-render.md`. Translated and adapted, not copied. HyperFrames is by HeyGen
> (Apache-2.0): https://github.com/heygen-com/hyperframes

**Purpose.** How `motion-render-agent` turns each approved plan item into a rendered file Final Cut can
use. HyperFrames renders HTML/CSS/GSAP to video from the command line (`npx hyperframes …`). Commands and
options change between versions: **check `npx hyperframes@<version> --help` and the version's own docs**
before relying on a flag. HyperFrames ships its own agent skills (`npx skills add heygen-com/hyperframes`);
when installed, read them for composition rules.

**Contents:** 1 Version and projects · 2 Composition · 3 The build cycle · 4 Output formats for Final Cut ·
5 Check and register · 6 Sound events · 7 Traps · 8 Chunks, revisions, learning

---

## 1. Version and projects

- **Version:** the newest when a video starts, **pinned for the whole video** (`edit-state.json`
  `tools.hyperframes`); every command carries it: `npx --yes hyperframes@<version> …`. Changing mid-video
  can change the look of what was already approved. Node.js ≥ 22.
- **One project per animation** (or per chained sequence, like a hook with several scene changes) in
  `edit/motion/projects/<id>/`.
- **Compose at 1080p, render at the video's resolution** (`--resolution landscape-4k` from a 1080p
  composition is an exact multiple). Faster to work and to snapshot.
- **Frame rate = the sequence's exact rate:** `--fps 30000/1001` for 29.97. Never round it.
- **Exact duration:** root duration `(N − 0.5) / fps`, where N is the number of frames the item occupies
  in the sequence; the renderer rounds `duration × fps` up, and the direct sum gives some items one extra
  frame.
- **Motion blur** on at the root (`data-motion-blur="on"`) in `data-motion-blur-tier="filter"` mode.
- **CSS inline** in `index.html`, never via `<link>` (a link changed the letterforms in the render).
- **Reusable pieces:** the first time an element turns out well (card, label, background, emphasis),
  make it a piece in `workspace/edit-profile/pieces/` (look in CSS, movement in JS). Later videos start from
  them. The channel's **intro sting** is built once as a piece and reused.

## 2. Composition

- Content from the plan item: concept, storyboard, on-screen text (in the creator's language),
  format, trigger words, camera intent, exit direction.
- **Time 0 of the animation = its start in the sequence;** each trigger enters at
  `word_time − item_start`.
- **Full screen:** complete scene with background and the virtual camera the profile asks for (push and
  drift in parallel layers), arriving in motion and leaving on its own.
- **Overlay:** transparent background, elements only (`html`, `body` and any full-frame background must
  stay transparent). On a side overlay, elements sit opposite the face.
- **Exit marked with a direction** ("up", "left") so the camera can arrive in the same direction.
- **Text:** at least 28 px at 1080p (56 px at 4K), inside the safe area (80% of the frame).
- **Missing asset:** build with a visible placeholder of the same size and time ("MISSING ASSET: logo X");
  swap and re-render only that item when the file arrives.

## 3. The build cycle (every animation)

1. `npx hyperframes@<v> lint` and `check` — fix every error (an "empty first frame" warning is expected
   for an animation that starts arriving).
2. `snapshot --at <entry>,<climax>,<exit>` and **look**: text legible, nothing hidden, transparency
   right, inside the safe area.
3. Render (in the background, queued while the next one is built).
4. Inspect one or two frames of the final file.

## 4. Output formats for Final Cut

| Format | Command | Why |
|---|---|---|
| Full screen | `render --format mp4 --fps <rate> --quality high --output <id>_v01.mp4` | opaque, small |
| Overlay | `render --format mov --fps <rate> --output <id>_v01.mov` | **ProRes 4444 with alpha** — what Final Cut reads with transparency |

Never `--prores-profile hq/422/lt/proxy` for an overlay: those have no alpha and transparent areas render
black. Never WebM for Final Cut: only browsers decode its alpha. Names are versioned; a delivered render
is never overwritten.

## 5. Check and register

`render_check.py --id <id> --file … --format fullscreen|overlay --seq-start … --frames N` refuses a render
whose resolution, exact frame rate or frame count differ from the item, or an overlay without alpha in
ProRes 4444. Only a passing render enters `motion/renders.json`, which the timeline reads.

## 6. Sound events

While building, write into `motion/events.json` everything a sound editor would want to know: what
**arrives, leaves, hits, swaps, clicks, types, counts, reveals**. Each event: the sequence time, a free
type that says what happens (`glass_cracks`, `needle_locks`, not just "impact"), strength (light /
medium / strong), duration if it lasts, and a line for whoever picks the sound ("big glass card drops
fast and locks with a jolt"). "Life" motion (drift, particles, reflections) is not an event.

## 7. Traps (each one cost a round)

- **Snapshot and render only agree if:** every chained move has an explicit start (`fromTo`; with `to`
  the start is read from the screen); every new tween has `lazy: false`; tweens on the same property do
  not overlap (cut the previous where the next begins).
- **`fromTo` starting visible** (opacity > 0 in "from"): always `immediateRender: false`.
- **Transform origin** with `immediateRender: false`: when a frame is computed by jumping straight to it
  (snapshot, parallel render) the origin is lost and the zoom shifts. Fix it with
  `tl.set(target, {transformOrigin: …}, <tween start>)`.
- **Measuring layout** (a word's width): build the timeline inside `document.fonts.ready.then(…)`.
- **Gradient text clips its last letter** (`background-clip: text` + negative letter spacing): give it room
  — `display:inline-block; padding:0.1em 0.14em; margin:-0.1em -0.14em;`. Check the last letter of every
  gradient word in a frame of the final render.
- **Motion blur:** in the default "capture" tier animated elements are drawn on top of everything — use
  `filter`. No `backdrop-filter` on cards with animated text (fill solid; the glass look comes from border,
  gradient and light). No `filter: drop-shadow` on gradient text (a box shows while animating; put the glow
  in its own layer behind). Blur only applies to the **outermost** animated element and ignores
  full-frame transparent layers, 3D (`perspective`, `rotateX`) and elements larger than half the frame —
  animate the smallest element possible (each digit, not the whole counter), or draw a directional blur
  (SVG `feGaussianBlur` from the velocity).
- **Full-frame vignette:** `box-shadow: inset`, not `background` (the check flags hidden text).
- **Light inside a card:** `z-index` below the text. **Glow inside a window with `overflow:hidden`:** clip
  only on the axis of movement, with room for the glow.
- **Generated effects** (noise, an image forming): canvas drawn in an `onUpdate`, with a **fixed seed**.
- **Checking an overlay over the camera:** extract the MOV frame to PNG first, then composite over the
  camera frame (compositing straight from the MOV with `-ss` came out empty).
- **The render is not 100% deterministic:** two renders differ by up to ~1/255 in a few pixels near motion
  blur. That is the noise margin when comparing before and after.
- **HyperFrames' own guidance** calls a slow continuous push and a title that keeps moving signs of
  generated video. If the profile asks for a living camera, the profile wins.

## 8. Chunks, revisions, learning

- The creator can ask for a chunk ("renders up to 3:00", "mo08 to mo15", "the hook"): build only items
  that **start** in it. The delivery includes everything rendered so far.
- Revisions by number ("mo04 slower", "mo07 out"): change only those, render a new version, rebuild the
  delivery. General quality feedback ("basic", "amateur", "lifeless") means **rebuild**: reread the
  references, state the new direction in one sentence per item, build again.
- If a revision changes a duration, change it in the plan and the composition, and register again.
- If the creator edited an animation project directly, keep their changes.
- On approval: a pattern that repeated becomes a catalogue item; an element that worked becomes a piece.
