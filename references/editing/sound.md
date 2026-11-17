# Sound Effects and Music

> Sound effects adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/etapa-sfx.md`.
> Translated and adapted, not copied. Music placement and ducking are this matrix's own.

**Purpose.** Sound goes in last, over the locked cut, animations and camera. It decides **where** sound
goes, **which**, and **how it stacks**, and delivers each sound on its role with the level set, for the
creator to refine. Read by `sound-agent`. Technical rules (sync, level, no repeats) are firm; density,
weight and favourite sounds are the profile's. Every number here is a **craft default, overridden by the
edit profile**.

**Contents:** 1 Events · 2 Principles · 3 The library · 4 Music · 5 The plan file · 6 Review

---

## 1. Events

Collected in sequence time: cuts (with and without plane change), camera moves (`camera.json` events),
animation entries/exits and trigger words, storyboard beats, and the events annotated while rendering
(`motion/events.json` — the most precise, with material and strength). The agent reads this list plus each
animation's idea and storyboard; it never opens frames or animation code.

## 2. Principles

1. **Sound follows what is seen.** A visible event asks for sound; what is not seen does not. A jump cut
   without a plane change is meant to be invisible: usually no sound. A cut, zoom or camera move under a
   full-screen animation is not seen: no sound. A visible camera move is like an animation: a whoosh with
   its peak where the camera brakes (arrival) or on the fastest frame (ramp); an impact on the climax punch.
   Slow push and face lock need no sound.
2. **One protagonist per moment.** Each event has a main layer; at most 3 layers per event, each in a
   different frequency band. Two sounds of the same kind on the same frame blur and lose their attack.
3. **Layers of a strong moment:** main (says what happened: impact, whoosh, pop, click) · low (a sub under
   the impact for weight — strong moments only) · support (prepares or accompanies: the whoosh leading in,
   a riser ending on the event) · sweet (a short, quiet high transient that defines the attack) · tail (rare:
   an ambience or reverb holding the moment).
4. **Anticipation and resolution.** Risers and reversed sounds build; the impact resolves. A riser ends on
   the event and cuts dead. Stronger with a breath: nothing else in the ~0.5 s before the impact. Sometimes
   the best sound is removing sound.
5. **Escalation.** The biggest impact goes on the climax of the opening (the key sentence). Smaller ones
   before. Nothing bigger in the body.
6. **Density by section** is the profile's. "A whoosh on every cut" is tiring after ten minutes: vary.
7. **Sync:** impact — the transient on the event frame · whoosh — the **peak** on the frame of the swap or
   arrival (where the element brakes), not on the first frame of the move · pop, click, ding — start on the
   event · camera whoosh — peak near the start of the move · a sound may lead by 1 frame to match
   perception; support layers staggered by 1–2 frames give depth.
8. **Sound matches movement and material.** Big and slow → low, long whoosh; small and fast → short and
   high. Paper asks for paper; tech and AI, glitch and interface; cursor, click; check, ding.
9. **Variation.** Never the same file within ~20 s; packs with variations exist for this.
10. **Level.** Well below the voice. Every sound is set from the **voice loudness** with a target per layer
    and capped so nothing is louder than the voice, except an intentional moment. The final mix is the
    creator's.

## 3. The library

- The creator's own folder (path in `edit-config.json`), one subfolder per category (whoosh, impact, low,
  riser, pop, click, glitch, interface, ding, paper…). **Read-only**: never moved, renamed or copied —
  Final Cut references the files where they are.
- `sound_index.py` measures every file: useful duration (without the silent head), **time to peak**,
  shape (sharp / medium / swell), brightness, loudness. Incremental.
- **Choosing:** the time to peak has to fit before the event; the useful duration has to fit before the next
  event; the shape matches the role; brightness separates layers (low under, bright on top).
- **Missing a sound?** Do not force a bad one: use the best available or leave it out, and add it to
  `edit/sound/missing.md`. New sounds enter through a folder the creator chooses; the agent proposes the
  category, the creator moves the file.
- No library yet: propose the categories that matter and a first free set with clear licences (check
  current sources and licences before recommending).

## 4. Music

- Optional per video (`edit-config.json`). The creator chooses the track from their folder or approves the
  agent's proposal by mood; choosing music is taste.
- Placed on its own role (`music`), fading in and out (~1 s and ~2 s).
- **Ducking:** keyframes lower it under speech and lift it in pauses longer than ~1.5 s, with ~0.3 s ramps.
  Targets relative to the voice: under speech −20 LU, alone −12 LU (craft defaults).
- Licence of the track is the creator's responsibility; note it for the video description.

## 5. The plan file

`sound/plan.json` (owned by `sound-agent`):

```json
{"items": [{"id": "sfx01", "event": "mo03 card locks", "time": 62.46, "layer": "main",
            "file": "/abs/SFX/impact/glass_lock_02.wav", "align": "peak", "gain_db": 0, "offset_frames": 0}],
 "music": [{"id": "mus01", "file": "/abs/Music/track.wav", "start": 0.0, "end": 48.0, "duck": true}]}
```

`sound_place.py` aligns, levels, fades and checks, into `sound/sound.json`. Warnings to fix before showing:
sound not found, repeated within 20 s, event without a main sound, two mains on top of each other.

## 6. Review

By number: "sfx12 lower" (−3 dB), "sfx05 out", "swap sfx07" (another sound of the same role),
"sfx03 one frame earlier". If the creator adjusts levels directly in Final Cut and approves that, the
difference is a learning for the profile's level targets.
