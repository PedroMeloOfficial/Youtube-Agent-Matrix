# Motion Planning

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/etapa-motion-mapa.md`.
> Translated and adapted, not copied.

**Purpose.** The stage that most decides the video's quality: where animation goes, what it shows and
how, and the camera's intent around each one. **Nothing is animated here** — it is proposed in chat,
adjusted with the creator and saved. Changing here is cheap; after the render, a weak concept costs a
whole round. Read by `motion-plan-agent`, with `motion-craft.md` and the edit profile.

**Contents:** 1 Speech in sequence time · 2 Sections and density · 3 Storyboard · 4 Where (and where
not) · 5 Format · 6 Duration and sync · 7 Camera around it · 8 Assets · 9 Using the pre-production ·
10 The plan file and review

---

## Principle

- **Content decides the animation.** For each idea, the visual form that explains *that* idea best.
- **Style is constant:** craft, profile, identity.
- **The catalogue is repertoire, never an obligation.** At the start of the video especially, a concept
  of the video's own subject is worth more, so videos do not all look alike.

## 1. Speech in sequence time

`sequence_text.py` converts the transcript through the approved cut into `motion/sequence.txt`: one
sentence per line with its sequence timecode and segment, spoken notes inline, and at the end of every
segment the **exact cut time**. Exact word times for a stretch come on demand
(`sequence_text.py --words FROM TO`).

## 2. Sections and density

- Set the **end of the hook** (where the video's promise is delivered and the content starts), the
  **video type** and the **start of the close**. What the briefing does not say, confirm in one short
  message with a proposal ("Hook until 00:48, explainer, close from 11:20 — right?").
- **Density** per section is the profile's. The hook is usually denser and stronger.
- Plan **the hook first and in most detail**, almost sentence by sentence. It weighs most on retention.

## 3. Storyboard (required in the hook, optional in the body)

| Field | Describes |
|---|---|
| concept | the visual idea in one sentence, tied to what is being said |
| layers | background, middle, front: what is in each and how it moves |
| camera | what the virtual camera does inside the animation |
| beats | the strong moments (word, time, what happens) — they become sound events |
| hero | the climax, if any |
| life | the secondary motion after everything entered |
| exit | how it leaves or hands over to the next |

Before showing the hook, reread it: does the concept come from *this* speech, or would it fit any video?
Does the energy match that point? Is every animation using the same zoom-and-impact and the same entry?

## 4. Where (and where not)

- **Yes** where it explains better than the camera or gives real emphasis: a process, a step-by-step, a
  comparison, before/after, numbers, lists, abstract concepts, tools mentioned, the key sentence.
  Emphasis with judgement, so it keeps its force.
- **No** where a screen recording already shows the subject (except a punctual highlight), nor to
  decorate a sentence that stands on its own.
- **Spoken notes** about animation take priority: do what was asked, complete only what is missing.

## 5. Format

- **Full screen:** concepts, processes, big numbers. The voice keeps playing underneath.
- **Overlay:** short things over the presenter, transparent background.
- **Large side overlay:** the item says which side of the face; the camera moves the face to the
  opposite third while it is on screen.
- **Emphasis over footage:** darkening or a gradient at the bottom, in the render. Background blur goes
  as a post marker.
- **Entry and exit:** the animation starts already moving and ends with its own exit. In Final Cut it is
  a straight cut.

## 6. Duration and sync

- An animation lasts the stretch of speech it illustrates: minimum ~2 s, typical 3–8 s. Above ~12 s,
  split into scenes with transitions.
- **Reading time:** with text, it ends ~1–1.5 s after the last word, unless another animation or a cut
  forces otherwise.
- Every important entry has a **trigger word** with its exact time.
- **Edge on a cut:** when an animation starts or ends with a cut, use the **exact cut time**, not the
  word's. Because of edge padding the cut lands ~0.1–0.3 s before the first word; an animation timed to
  the word would leak frames into the neighbouring segment.

## 7. Camera around it (intent in words)

Written here, together with the animation; the camera stage decides curves and values after the render.
- Per item, when there is something to say: **before** ("accelerates into the face up to the cut"),
  **during** ("face in the left third"), **after** ("arrives from below, in the direction of the exit,
  and brakes").
- **Camera beats outside animations:** word, time and what happens ("hard punch on 'impossible'").
- An animation's exit asks for the camera to arrive in the same direction; an entry on a cut asks for
  the camera to accelerate before. Under full screen the camera is not seen: plan no movement there.

## 8. Assets

- Ask for what is missing instead of improvising something generic: a logo, a screenshot, a screen
  recording, a photo, a specific icon. **List the assets folder first** — a file may be there under
  another name.
- Each asset has a type and a search term: logo (brand name), icon (an English word), website capture
  (exact URL), stock photo or video, personal recording (only the creator can make it).
- Prefer SVG for logos and icons. Characters, shapes, built scenes and diagrams are **not assets**: the
  render draws them in code.
- This stage searches nothing; the asset stage does, after approval.

## 9. Using the pre-production

- `[B-ROLL: …]`, `[SCREEN: …]` and `[DATA: …]` lines of the approved script are starting points, not
  orders: keep what still fits the speech as recorded.
- Any number on screen comes from the research report or dossier, **with its source**; the source goes
  in the item (`source`) and, when the profile says so, small on screen.
- The channel's brand lines (`channel-profile.md` §6b) and reusable pieces (the intro sting) are placed
  where the script marked `[BRAND]`, from `workspace/edit-profile/pieces/`.

## 10. The plan file and review

`motion/plan.json` (owned by `motion-plan-agent`):

```json
{"hook_end": 48.2, "close_start": 680.0, "video_type": "explainer",
 "items": [{"id": "mo01", "status": "proposed", "seq_start": 3.2, "seq_end": 8.9, "format": "fullscreen",
            "idea": "…", "storyboard": {"concept": "…", "layers": "…", "camera": "…", "beats": [{"word": "…", "time": 5.1, "what": "…"}],
            "hero": "…", "life": "…", "exit": "up"},
            "text_on_screen": ["…"], "triggers": [{"word": "…", "time": 3.4}], "source": null,
            "camera_intent": {"before": "…", "during": "…", "after": "…"}, "assets": [{"id": "a01", "type": "logo", "query": "…"}]}],
 "camera_beats": [{"time": 120.4, "word": "…", "what": "hard punch"}]}
```

Shown in chat numbered (`mo01`, `mo02`…), one line each: time, format, idea, camera intent. In a long
video, approval can go by section, starting with the hook. The creator approves, adjusts or strikes by
number; approved items keep their status when the plan is saved again.
