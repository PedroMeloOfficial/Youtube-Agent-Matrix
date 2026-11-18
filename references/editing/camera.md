# Camera Moves on the Presenter

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/etapa-camera.md`.
> Translated and adapted, not copied.

**Purpose.** The presenter's camera movement, designed **after** the animations are rendered, matched to
the speech and to each animation's entry and exit. It reaches Final Cut as scale and position keyframes on
the original clips — no video is rendered. Read by `camera-agent`. Curves are the same as
`motion-craft.md` §2–§4, so the camera and the animations move as one. How much movement and zoom is the
profile's; every value is a **craft default, overridden by the edit profile**.

**Contents:** 1 Automatic base · 2 Matching the animations · 3 Emphasis · 4 Care points · 5 The plan file ·
6 Review · 7 Sound events

---

## 1. Automatic base (`camera_curves.py` does it)

- **Plane alternation:** at each cut the plane switches between open (100%) and closed (e.g. 125%). This
  disguises the jump cut.
- **Slow push** underneath everything (e.g. 3–8% per segment), in its own layer, multiplied in.
- **The base obeys the designed moves:** each cut's plane is chosen from where the camera **actually
  ended** in the previous segment. A cut always changes plane; under 5% change it warns.
- The first segment and a new setting start open.

## 2. Matching the animations (what gives the most energy)

- **Before an animation that enters on a cut:** the camera accelerates into the face in the last
  0.2–0.25 s (`power4.in`, +7% to +18%) — move `push_in`.
- **After an animation that leaves with a speed ramp or a fast move:** the camera arrives moving in the
  same direction and speed and brakes (`expo.out`, 0.4–0.6 s, from ~1.3–1.5× the target) — move `arrive`.
  Exit up → arrive from below. Exit left → arrive from the right.
- **Side overlay:** the face goes to the opposite third (scale ~140%) only while the animation is on
  screen, and back to centre when it leaves (`power2.inOut`, ~0.7 s) — move `side_third`. A soft approach,
  starting a bit before; never jump-then-slide.
- **Cards entering at the bottom:** the face rises a little so it is not behind them.
- **Under full screen** the camera is not seen: spend no movement there.

## 3. Emphasis

- **Hard punch** on the climax word: enters ~5–7% above and settles in ~0.3 s (`power2.out`) — `punch`.
- **Zoom with speed ramp** (velocity peak on the word) when the trip to the close shot matters; a cut with
  speed ramp to return to open. Vary the forms; never the same twice in a row.
- **Face lock:** the camera follows the face so it stays still on screen while the background moves — for
  emphasis, at ~120% or more (it needs margin), ideally from cut to cut, short (~1 s) or long (5–7 s). It
  is an intent, not a professional track. Ending mid-shot, it lets go slowly (~0.4 s) — `lock`. Needs the
  face track (`face_track.py`).

## 4. Care points (each one looked like a bug when it happened)

- **No instant scale jump in the middle of a visible take.** Jumps only where hidden (out of full screen,
  on a cut) — the punch is the one deliberate exception.
- **Every move starts from where the camera is.** Starting elsewhere makes the camera "jump" before moving.
- **Never reverse direction across a cut:** accelerating in and then arriving closer and pulling back reads
  as senseless.
- **Eye line in close shots:** centring the frame on the middle of the face puts the eyes low and the head
  touching the top. Eyes at ~35% of the height with room above is right — the script does it when face
  data exists. Check every close shot.
- **One thing per layer:** two scale moves (or two position moves) at once fight. The slow push runs in
  parallel, in its own layer.
- **Never show the edge of the frame:** at scale ≥100%, position is limited by the margin (the script
  clamps it).

## 5. The plan file

`camera/plan.json` (owned by `camera-agent`), times in sequence seconds:

```json
{"base": {"closed_scale": 1.25, "creep": 0.05, "eye_line": 0.35},
 "segment_overrides": {"s014": {"plane": "open"}},
 "moves": [{"id": "cam01", "type": "punch", "time": 62.4, "amount": 0.10, "why": "climax word"},
           {"id": "cam02", "type": "push_in", "segment": "s021", "duration": 0.22, "amount": 0.12},
           {"id": "cam03", "type": "arrive", "segment": "s022", "from": "below", "duration": 0.5},
           {"id": "cam04", "type": "side_third", "start": 140.0, "end": 146.5, "side": "left"},
           {"id": "cam05", "type": "lock", "start": 201.2, "end": 203.0}]}
```

`camera_curves.py` computes base + moves into dense keyframes (`camera/camera.json`) and warns about
conflicts. Final Cut position units are a percentage of the frame height.

## 6. Review

- By number: "cam07 slower", "cam05 stronger", "cam12 out", "no punch in s014".
- A camera adjustment made by hand in Final Cut does not flow back into the plan: ask by number.
- If an animation changes later, the camera is recomputed.

## 7. Sound events

Every visible move (fast arrival, acceleration before a cut, punch, ramp) is a sound event with strength
and time (`camera.json` `events`), for the sound stage. Slow push and face lock are not.
