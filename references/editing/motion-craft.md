# Motion Craft

> Adapted from **fluxo-de-edicao** by Lucas Leite (MIT, © 2026), `guias/oficio-motion.md`.
> Translated and adapted, not copied.

**Purpose.** How animations move well in any style: curves, speeds, scene changes, reading time and
layout — measured on professional references and tested on real videos. Read by `motion-plan-agent`
and `motion-render-agent`, together with `hyperframes.md`. Values in frames at 30 fps; scale
proportionally for other rates.

Every value here is a **craft default, overridden by the edit profile**. The look (colours, fonts,
material) and the taste (how much overshoot, how much secondary motion) always come from the profile.

**Contents:** 0 Principle · 1 Speed hierarchy · 2 Curve by role · 3 Virtual camera · 4 Scene changes ·
5 Entries and exits · 6 Living text · 7 Layers and depth · 8 Secondary motion · 9 Over the presenter ·
10 In the render or in post · 11 Avoid · 12 How to know it is fluid

---

## 0. Principle

- **What appears on screen is born from what is being explained.** Never fit content to a template:
  find the visual metaphor that explains *that* idea best and build it with these rules and the profile.
- **One protagonist at a time:** at any moment, one element draws attention.
- **Show the real thing when it fits:** if the speech mentions something that can be shown happening,
  that explains better than a generic card with its name. Used where it fits, without excess.
- **Layout and alignment:** every element aligned to what it accompanies (the label to its icon, the
  lines of a block to each other). Misalignment is what reads as amateur fastest.

## 1. Speed hierarchy

| Layer | Speed | Example |
|---|---|---|
| Elements entering | ~15 f (0.5 s); opacity and focus in 6–10 f | card, icon, label |
| Elements leaving | ~8 f (0.25 s), faster than the entry | card, label, caption |
| Text | 6–12 f per word | emphasis sentence |
| Camera | slow: 1.5–3.5 s | push, pull, drift |
| Secondary | continuous | orbit, particles, light |

Contrast of speeds is what reads as fluid: a quick entry over a slow camera.

## 2. Curve by role (GSAP)

| Role | Curve | Duration |
|---|---|---|
| Element entry | position/scale ease-out (overshoot is the profile's); opacity/focus `expo.out`, shorter | ~15 f |
| Element exit | `power3.in`, one movement (falls or shrinks + blur + fade) | ~8 f |
| Group rearranging | words `power3.out`; cards `power2.out` | 15 f; 21 f |
| Camera push/pull at opening | `power2.out` (soft) to `circ.out` (brakes earlier) | 1.5–3.5 s |
| Camera drift after it settles | `none` (linear) or `sine.out` | to the end of the scene |
| Punch to a detail | asymmetric in-out, peak at ~30% (`expo.in` short + `expo.out` long) | ~1–1.7 s |
| Carousel step, item swap | `power4.inOut` or `expo.inOut` | 13 f + ~7 f still |
| Dim or blur the background | `power1.inOut` | ~14 f |
| Light up a solemn title | opacity + blur, `power2.out` | ~20 f |
| Progress, rotation, following a bar | `none` | — |
| Speed ramp (scene change) | `power4.in` → cut → `expo.out` | ~1 s + ~1.5 s |

**Nothing moves linearly** except camera drift and what follows a progress.

## 3. Virtual camera (inside an animation)

- **Push and drift run together, in separate layers:** two nested containers — the outer does the
  push with an ease-out, the inner a linear drift for the whole scene. Chaining an ease-out that ends
  still with a linear move makes velocity drop to zero and restart: the zoom "stutters".
- **Follow** what progresses (a bar, a timeline) at constant speed.
- **Punch** (~25%) with an asymmetric in-out to highlight a detail, then return.
- **Changing zoom** (wide → close on the area of interest → back), three forms for different moments:
  1. **Hard cut:** the close shot enters ~5–10% larger and settles (~0.3 s), with a flash on the cut.
  2. **Continuous zoom with speed ramp, no cut:** accelerate (`power4.in`) and brake (`expo.out`) with
     matched speeds, peak at ~30%, flash at the peak.
  3. **Cut with light speed ramp:** the outgoing shot accelerates toward the zoom in its last frames
     (~0.2 s, +5%, `power4.in`), cut on the fastest frame, the incoming shot arrives already moving in the
     same direction and decelerates (~0.42 s, starting ~6% before target, `expo.out`). Subtle; smooths.
  - Zooming into an element (icon, card) usually reads better continuous; a hard cut there can look
    like a scene change.
- **Fluid camera:** what looks most amateur is a "truncated" camera — several moves that start and end
  still, in sequence. One move flows into the next without velocity reaching zero. If it stops, it stops
  very softly. Smoother is not slower. A pull that reveals keeps pulling slowly the same way.
- **The main content enters centred from the start**, even with the larger zoom; the pull reveals the
  rest and recentres.

## 4. Scene changes

- **Speed ramp:** the scene accelerates in one direction (`power4.in`, ~1 s), directional motion blur at
  the peak, cut on the fastest frame, the new scene arrives in the same direction and speed and brakes
  (`expo.out`, ~1.5 s). The exit is shorter than the arrival.
  - **Travel:** content must still be in frame at the cut. At 1080p, ~700 px leaving and ~560 px
    arriving. With ~1,300 px the content leaves early and empty frames remain.
  - **Match speed at the cut:** end speed of `power4.in` = 4·D/T; start speed of `expo.out` ≈ 6.93·D/T.
    E.g. 700 px in 1 s → 2,800 px/s; 560 px in 1.5 s → ~2,590 px/s.
  - The new scene arrives with its main content in frame; details cascade in ~0.2 s later.
- **Fast move in the same world:** what leaves accelerates, what enters brakes, same direction. A bit
  longer than ~20 f; shorter reads "stiff".
- **A speed-ramp arrival never stops dead:** long soft braking, then keeps moving.
- **Cut with settle:** the new scene enters ~5% larger and settles in ~6 f.
- Vary the transition type through the video; never the same one twice in a row.

## 5. Entries and exits

- **Entry:** ~0.5 s, opacity and focus first. From zero (or from ~60% + opacity 0) to final size.
- **Cascade and overlap:** 2–4 f between siblings; the next move starts before the previous settles.
- **Cursor and click:** the cursor travels in an arc, like a hand; each click sinks and springs back.
- **Groups that arrive in sequence stay centred as one group:** the first is born centred; when the next
  arrives, the whole group slides to be centred again.
- **Lines in step with speech:** words enter one by one when spoken, and the line slides to stay centred
  (~0.5 s, `power3.out`). Alternative: the whole line appears dimmed and each word lights up when spoken.
  Revealing word by word **without** recentring leaves the start lopsided: never. Short titles enter whole;
  the key word gets the punch when spoken.
- **Sync with speech:** the element representing a word enters **on the word** (transcript time), not on
  a fixed interval.
- **Exits:** faster than entries (~0.25 s, `power3.in`), one movement, or carried by the camera or the
  scene change.
- **Reading time:** a caption does not leave glued to the last word; with nothing right after, it holds
  ~1–1.5 s after the final word.
- **The final hero has time to be seen** (the logo, the reveal).

## 6. Living text

Typed text: ~23 characters per second, each letter entering with a soft edge (opacity and blur);
several lines in parallel offset by 3–4 f.

## 7. Layers and depth

- Depth of field for focus: blur what is not the subject of the moment.
- Background and foreground move subtly, at the periphery: slow drift at corners and edges. Never
  crossing toward the area of interest, never mixing with the main animation.

## 8. Secondary motion

What keeps moving after everything entered has a purpose (shows flow, data, energy), not floating for
its own sake. How much is the profile's. Light running along a rail passes **behind** the nodes.

## 9. Over the presenter

- Short, punctual elements (labels, icons, numbers, emphasis at the bottom) with transparent background.
- **A flash in an overlay stays on the element.** A full-frame flash over the presenter looks like a bug.
- A large side element: the camera moves the face to the opposite third while it is on screen and back
  to centre afterwards (`camera.md`).

## 10. In the render or in post

- **In the render:** camera and zoom inside the animation, depth of field, motion blur, glow, light,
  particles.
- **In post (in Final Cut, as a `[C]` marker):** the whole-video "look" (lens effects, grain, glitch,
  textures, background blur under an emphasis). So it never doubles up and stays adjustable.

## 11. Avoid

Everything entering with the same fade and slide; several protagonists at once; lens effects in the
render; a camera that stops and restarts in sequence.

## 12. How to know it is fluid

Render and measure: the curve measured in the video (same method as `style-profile.md` §3) must match the
intended curve and these durations. Adjust until it does. General quality feedback ("basic", "lifeless")
means **rebuild** the animation, not retouch it.
