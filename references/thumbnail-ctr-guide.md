# Thumbnail & CTR Guide

Method for designing a thumbnail that earns a click in under a second — composition, text, faces, faceless formats, image-model prompting, packaging iteration and testing — for any channel in any language.

> **Every specification, limit and benchmark lives in `benchmarks.md`.** This file teaches the craft and names the section where each number lives.

**Contents:** [1 The Job](#1-the-job-of-a-thumbnail) · [2 Information Split](#2-the-information-split-rule-in-practice) · [3 Composition](#3-composition-frameworks) · [4 Colour](#4-colour-discipline) · [5 Text & Safe Zones](#5-text-treatment-and-safe-zones) · [6 Faces](#6-face-thumbnails) · [7 Faceless](#7-faceless-channels) · [8 Small-Surface Design](#8-designing-for-the-smallest-surface) · [9 Packaging Loop](#9-the-packaging-loop) · [10 Prompting](#10-prompt-engineering-for-image-models) · [11 Worked Prompt](#11-worked-prompt-example) · [12 Before/After](#12-beforeafter-critique) · [13 A/B Testing](#13-native-ab-testing) · [14 Re-Thumbnailing](#14-re-thumbnailing-an-existing-video) · [15 Policy](#15-policy-exposure) · [16 Decision Rules](#16-decision-rules)

## 1. The Job of a Thumbnail

A thumbnail does not describe the video. It opens a gap the title closes, or states a payoff the title makes specific. The click happens when the viewer holds two pieces of information that only resolve by watching.

| Job | The thumbnail supplies | The title supplies |
|---|---|---|
| Curiosity gap (browse) | An image that raises a question | The subject that makes the question matter |
| Confirmation (search) | Proof this is the right video | The exact phrase searched |
| Stakes | Scale, consequence, contrast | The outcome |
| Identity | Recognisable style, so regulars click faster | Continuity of the series |

Decision time is under a second (`benchmarks.md` §7), so a thumbnail is not read — it is *recognised*. Anything needing interpretation has already lost. **Failure archetypes:** the illustration (shows the topic, raises nothing) · the poster (a paragraph of text) · the screenshot (no focal point) · the duplicate (says exactly what the title says).

## 2. The Information Split Rule in Practice

Definition and rationale: `benchmarks.md` §7.

| Title | Weak thumbnail (duplicate) | Strong thumbnail (split) |
|---|---|---|
| "I Cooked For 100 People With $20" | Text "100 people, $20" | Overwhelmed cook behind an enormous tray, one small banknote in frame |
| "Why Is My Laptop Slow?" | Text "SLOW LAPTOP" | Hand on a hot chassis, a visibly dust-choked fan |
| "The Cheapest Camera That Still Looks Good" | Photo of the camera + price text | Two frames side by side, one price tag visible, one hidden |
| "5 Mistakes Beginners Make" | Text "5 MISTAKES" | One mistake shown mid-failure, "#3?" the only text |

**Test:** cover the title — does the thumbnail still create a question? Cover the thumbnail — does the title still promise something? If either answer is no, one of two persuasion surfaces is wasted.

## 3. Composition Frameworks

**Rule of thirds.** Place the focal point on a grid intersection, not dead centre — centred subjects read as static and collide with play-button and duration overlays on some surfaces. Keep the eyeline on the upper third line.

**Z-pattern reading.** Left-to-right readers scan a small image top-left → top-right → bottom-left → bottom-right. Put the entry idea top-left, the payoff along the descending diagonal. **For right-to-left audiences (Arabic, Hebrew, Persian, Urdu), mirror the layout** — the scan starts top-right. Mirroring is free at design time.

**Figure/ground separation.** The subject must separate from the background by at least one of: luminance contrast, hue contrast, focus (sharp subject / blurred background), or an explicit edge (rim light, stroke, cut-out with a subtle outer glow). Two of the four is safer. A subject sharing its background's brightness disappears at small size regardless of colour.

**The silhouette test.** Fill the subject solid black, the background solid white. If the shape is still identifiable as what it is, the composition works; if it becomes a blob, the pose, crop or separation is wrong. Fastest structural check available.

| Further checks | Pass condition |
|---|---|
| Focal count · negative space | Exactly one focal point; negative space within the band in `benchmarks.md` §7 |
| Depth | Foreground subject, mid-ground context, simplified background |
| Diagonals | At least one strong diagonal; pure horizontals and verticals read as flat |
| Direction | Gaze or gesture points at the text or the object of interest, never off-frame |
| Crop | Chest-up or tighter for faces; wide shots lose everything at feed size |

## 4. Colour Discipline

| Principle | Rule |
|---|---|
| Palette size | Keep to the small primary-colour count in `benchmarks.md` §7 — more colours means no colour |
| Contrast | Complementary or near-complementary pairing between subject and background |
| Saturation | Saturate the subject, desaturate the background; a uniformly saturated frame reads as noise |
| Feed context | Avoid a background matching the platform UI in either theme, or the thumbnail loses its edge |
| Brand consistency | One fixed accent colour on every thumbnail, so regulars recognise the channel pre-cognitively |
| Accessibility | Never encode meaning in red-versus-green alone |

Broad associations (warm = urgency, cool = calm and trust, black = premium, high-key = approachable) are useful defaults, **but colour meaning is culturally variable** — white, red and green in particular differ across markets. When targeting a specific culture, copy what top channels in that language actually use rather than importing a Western colour-psychology table.

## 5. Text Treatment and Safe Zones

Word-count limits: `benchmarks.md` §7.

| Property | Rule |
|---|---|
| Purpose | Text adds what the image cannot show — a number, a name, a stake. Never a caption of the image |
| Weight and size | Heavy or extra-bold only; cap height **≥10% of frame height** for the primary word, ≥7% for a secondary line |
| Line count | One line ideally, two maximum |
| Legibility | Solid fill plus a hard stroke, drop shadow, or a solid block behind. Never gradient on gradient |
| Placement | Into the negative space the composition already reserves — never across a face |

| Safe zone (16:9) | Risk | Rule |
|---|---|---|
| Bottom-right corner | Duration stamp overlays it on nearly every surface | Keep permanently clear |
| Bottom edge strip | Progress bar on watched videos; gradient on some surfaces | Lower ~10% free of text |
| Top-right corner · centre | Menu and queue affordances; play/hover overlays | No critical detail, no small text |
| Outer margin | Rounded corners crop the extremes | All text inside a ~5% inset |

Build these zones once as a template layer so every thumbnail inherits them. **Language adaptation:** the word limit is a *reading-time* limit. In Japanese, Chinese, Korean and Thai a few glyphs carry what several English words carry — use fewer glyphs, larger. In German, Finnish and other compounding languages a single word may not fit at the size floor; substitute a shorter synonym or drop the text entirely. RTL text needs a proper RTL-capable renderer — image models and naive editors reverse or disconnect Arabic letterforms.

## 6. Face Thumbnails

Faces lift CTR (`benchmarks.md` §7), but only under conditions.

| Expression | Reads as | Works when |
|---|---|---|
| Concerned / worried | "Something is wrong and I should know what" | **Most reliable default** — implies stakes without over-claiming |
| Curious / puzzled | "I don't understand this either" | Explainers, mysteries, reviews |
| Determined / focused | "This is hard and I'm doing it" | Challenges, builds, endurance |
| Delighted, genuinely | "Something good happened" | Positive reveals, reactions |
| Shocked (mouth and eyes wide) | "Extreme event" | Only when the video genuinely delivers one |
| Neutral | Nothing | Almost never — underperforms no face at all |

**Why concerned often beats shocked:** shock is a claim of magnitude. If the video does not deliver a shocking event, the packaging over-promises, which shows up as high CTR with low retention and exposes the video to metadata-mismatch suppression (`benchmarks.md` §5, §10). Concern implies stakes without specifying their size, so the video can meet it — and shock is the most imitated expression on the platform, while concern still reads as specific.

**Craft:** eyes sharp and lit; close crop; face about a third of frame width; gaze either at the camera (direct address) or at the object of interest (directs attention). Never combine a large face with a busy background. **Use no face when** the object is the story, the reveal is the subject, the channel is faceless (§7), or the creator's face carries no recognition yet and the object is more interesting than a stranger.

## 7. Faceless Channels

A large share of channels never show a face. These substitutes carry the focal point instead.

| Substitute | Method | Fits |
|---|---|---|
| Object hero | One object, dramatic light, shallow depth, clean background | Reviews, tech, crafts, cooking |
| Hands | Hands mid-action on the object — presence without identity | Tutorials, making, repair |
| Before/after split | Hard vertical divider, two states of one thing | Transformations, comparisons |
| Data shape | One oversized number, chart line or arrow as the subject | Finance, analytics, research |
| Character or mascot | A consistent illustrated or 3D avatar with variable expressions | Animation, education, gaming |
| Small figure in a large scene | A tiny silhouette against a vast environment — scale and stakes | Documentary, history, exploration |
| Text-as-image | One word treated as the visual object, typographically | Essays, commentary, lists |
| Annotated screenshot | Screenshot plus one circle or arrow marking the anomaly | Software, gaming, analysis |

**Faceless rules:** consistency substitutes for facial recognition, so lock a template — same accent colour, same type, same layout family — and let only the object change. Emotion is carried by lighting, framing and gesture instead of expression, and contrast must be manufactured deliberately, because objects on plain backgrounds default to low separation. Run the silhouette test hard: object thumbnails fail it most often.

## 8. Designing for the Smallest Surface

Most views are mobile (`benchmarks.md` §7); a feed thumbnail is roughly **168×94 px**.

| Check | How |
|---|---|
| Shrink test | View at feed size, at arm's length. Whatever is unreadable is deleted, not shrunk further |
| Squint test | Blur heavily; the focal point and text block must still be locatable |
| Grid test | Paste beside eight competing thumbnails from the niche; it must be identifiable within a second |
| Theme test | Check on light and dark backgrounds — a dark thumbnail can vanish into a dark UI |
| TV test | Also check at full resolution; large screens expose soft upscaling and compression |

Work at the recommended resolution (`benchmarks.md` §7) but *evaluate* at 168×94. Designing at small size produces crude work; evaluating at small size produces legible work.

## 9. The Packaging Loop

Thumbnail and title are one artefact, iterated together, before production where possible. **The 10/10 drill:**

1. Write **10 titles** without editing — quantity first. Force variety: search-shaped, curiosity-shaped, contrarian, numbered, personal, outcome-led.
2. Sketch **10 thumbnail concepts** as crude boxes and labels, thirty seconds each. Not finished art.
3. Build the pairing grid — which concepts split information with which titles (§2)?
4. Cut to the **3 strongest pairs**; each must pass the cover-one-surface test.
5. Show the 3 pairs to someone who has not seen the video, at feed size, for one second each. Ask which they would click **and what they think the video is about** — wrong guesses are more informative than preferences.
6. Produce the winner; keep the runner-up as an A/B variant (§13).

Do this **before filming** when packaging is the concept. If no title and thumbnail can be made compelling for a planned video, the video is the problem — kill it at the sketch stage, which costs an hour instead of a week.

## 10. Prompt Engineering for Image Models

**Prompt structure, in order:** (1) shot type — close-up/medium/wide, lens feel, angle; (2) subject with specific attributes; (3) action or expression; (4) environment, simplified and named; (5) lighting — key direction, rim light, contrast level; (6) colour — two or three named colours plus a dominant; (7) composition — thirds, subject placement, reserved negative space for text; (8) style — photographic / 3D / illustration and its grammar; (9) technical — 16:9, high detail, sharp focus on subject; (10) negatives — **"no text, no words, no letters, no watermark"**.

**Write prompts in English regardless of the channel's language.** Image models are trained overwhelmingly on English caption data; non-English prompts degrade composition control and attribute binding, and often silently drop modifiers. Compose in English, then set on-screen text in the video's own language in an editor. **Always append "no text"** — models render letters unreliably and mangle non-Latin scripts almost always. Generate clean; add text where font, size floor, safe zones and language shaping are all under control (§5).

**Consistency for a recurring face or character:** feed one fixed, clean reference image (image-to-image); reuse a verbatim character-description block in every prompt; keep the last three prompt slots (style, technical, negatives) locked; reuse the seed where supported. For a real person, **composite a photographed cut-out onto a generated background** — generated likenesses drift between uploads, destroying the recognition value the face was there to provide.

| Symptom | Cause | Prompt fix |
|---|---|---|
| Garbled text in image | Model rendering letters | Text negatives; add text in the editor |
| Subject lost in background | No separation specified | "Rim light on subject, dark simplified background, shallow depth of field" |
| Cluttered frame | Too many nouns | Delete nouns until one subject remains; add "minimal background" |
| Flat, dull look | No lighting specified | Name key direction and contrast ("hard side light, high contrast") |
| Warped hands | Known weak region | Crop them out or specify "hands out of frame" |
| Wrong aspect | Format unstated | State 16:9 explicitly; never crop a square down |
| No room for text | Composition unconstrained | "Subject on the right third, large empty space on the left" |
| Every upload looks different | Style drifting | Lock and reuse the style tail verbatim |

## 11. Worked Prompt Example

Video: a no-bake cheesecake built from three ingredients. Faceless home-cooking channel publishing in **Japanese**, search-targeted, food-hero template.

**Two languages here, deliberately.** The prompt below is in English; the overlay text is in Japanese. That split is the rule from §10, not an oversight. Image models are trained overwhelmingly on English caption data, so an English prompt buys far tighter control over composition, lighting and attribute binding — and no viewer ever sees a prompt. What the viewer sees is the overlay, and that must be in the channel's own language, set in an editor where font, size floor and safe zones are all under control. Asking the model to render the Japanese itself would fail twice: it would surrender the compositional control, and diffusion models mangle non-Latin scripts almost without exception. **Prompt in English, publish in the audience's language** — that holds for every language the channel might be in.

```
Close-up food photograph, slight high angle, 50mm look.
Subject: a single slice of no-bake cheesecake lifted on a cake server, its cut
face smooth and pale, one soft crumb breaking from the lower edge.
Environment: pale wooden table, heavily simplified, thrown far out of focus.
Lighting: soft window key from the left grazing the cut face so its texture reads,
faint cool rim along the top edge for separation, medium-high contrast.
Colour: dominant deep berry-red background, warm cream cheesecake, one muted green herb accent. Three colours only.
Composition: slice on the right two-thirds, on the right-third line; large clean
empty space upper left reserved for a text overlay; one focal point at the cut face.
Style: realistic editorial food photography, crisp, appetising, filmic.
Technical: 16:9, 1920x1080, sharp focus on the cut face, shallow depth of field.
Negative: no text, no words, no letters, no Japanese characters, no logos, no watermark, no hands, no clutter.
```

**Editor pass:** set 「材料3つ」 — *three ingredients* — in the reserved upper-left space. Four marks, extra-bold gothic, cap height ~14% of frame height, cream fill with a hard dark stroke, inset from every edge, bottom-right corner left clear for the duration stamp. Note the count: CJK carries in four marks what would take five English words, so the text is set *larger*, not longer (`localization-guide.md` §6). The title carries the searched phrase — the dish and the no-oven method; the thumbnail names what the title does not, that it needs only three ingredients. The information split holds in Japanese, produced from an English prompt.

## 12. Before/After Critique

**Before.** Wide shot of a whole cheesecake on a kitchen counter, mixing bowls and a stand mixer competing behind it, room evenly lit. Across the bottom in a medium-weight gothic, the full recipe name in Japanese, wrapping onto two lines. Six colours. The duration stamp lands on the final characters.

| Fault | Consequence |
|---|---|
| No single focal point — cake, bowls, mixer compete | Nothing is recognised in under a second |
| Subject too small, crop too wide | At 168×94 the cake is a pale smudge |
| Flat even lighting, no separation | Silhouette test fails |
| Six colours | Visual noise; no channel identity |
| Text duplicates the title | One of two persuasion surfaces wasted |
| Full recipe name set small, wrapping to two lines | Unreadable on mobile; the CJK advantage thrown away by writing a sentence instead of a phrase |
| Text in the bottom strip, no question raised | Overlapped by the duration stamp; nothing to resolve and nothing to want |

**After.** Tight crop on the lifted slice and its cut face; soft window key from the left, cool rim along the top edge; background collapsed to defocused berry-red; three colours; upper-left negative space holding 「材料3つ」 in extra-bold cream with a hard stroke, inset from the edges; bottom-right clear. Result: one focal point recognisable at a glance, a composition that survives feed size, a passing silhouette test, a fixed accent colour building channel recognition, four marks legible at thumbnail size where a wrapped sentence was not, and an intact information split against a title that already said *no-bake cheesecake*.

## 13. Native A/B Testing

Variant count, optimisation metric, duration, verdict types, setup surface and exclusions: `benchmarks.md` §7.

**Method.** Test **structurally different** concepts, not colour tweaks — two variants sharing a layout teach nothing. Change **one variable across the set** (all three same layout with different expressions, *or* three different layouts with the same text); mixed changes give an uninterpretable winner. Start **at publish**, so every variant sees the same traffic mix. Let it run the full window — ending early on an appealing lead promotes noise. Log the winner *and why you think it won*; the pattern across ten tests is worth more than any single result.

| Verdict | Meaning | Action |
|---|---|---|
| **Winner** | One variant produced a meaningfully higher share of watch time | Adopt it; log the structural reason |
| **Same** | Variants performed equivalently | Keep the one that fits channel identity; **stop testing that dimension** — it does not move this audience |
| **Inconclusive** | Not enough traffic to separate them | Not a failure — do not run tests on low-impression videos |

It optimises for **watch-time share, not CTR**: a lower-CTR variant can win by attracting viewers who stay, and a verdict must never be overridden by a raw CTR comparison. **It cannot test** titles and thumbnails simultaneously (separate tests, and the pairing effect is invisible to both), Shorts or made-for-kids content (`benchmarks.md` §7), a video already past its distribution push, or anything on a channel too small to reach significance. **When native testing is unavailable**, the substitute is comparative rather than experimental: publish variants of the same packaging *pattern* across successive videos, holding topic type constant, and compare launch-window CTR against the channel's own baseline — weak per video, useful only across many.

## 14. Re-Thumbnailing an Existing Video

| Situation | Re-thumbnail? |
|---|---|
| High impressions, CTR in the "packaging is the bottleneck" tier (`benchmarks.md` §1) | Yes — packaging is the constraint |
| High CTR, low retention (`benchmarks.md` §10) | Yes — it over-promised; make the packaging *less* aggressive |
| Low impressions, high CTR | No — packaging is fine; the topic or the demand is the problem |
| Currently being pushed and performing at or above baseline | **No** — changing it resets the audience's learned signal mid-distribution |
| Evergreen video whose steady traffic flattened months ago | Yes — low risk, real upside |
| The channel's calling card, recognised by regulars | Only with a variant preserving the recognisable elements |

**Risks:** a returning viewer no longer recognises a video they meant to finish; a change during an active push can flatten it; and the new file replaces the old one, so archive the original first. Change the thumbnail **or** the title in one move, never both — otherwise the result is uninterpretable.

## 15. Policy Exposure

Strike mechanics and the immediate-termination case: `benchmarks.md` §7. Categories: sexual content (including implied or suggestive framing) · graphic violence · misleading packaging (depicting an event the video does not contain, fabricated headlines, fake UI or fake alerts) · impersonation (another person's face or a brand's marks implying involvement) · hate and harassment · child safety · vulgar on-image text · synthetic likeness of a real person in a scene they were never in.

The risk that catches ordinary creators is not an obvious category — it is **metadata mismatch**, evaluated automatically against the video's actual content (`benchmarks.md` §5). The guard is simple: every element depicted in the thumbnail must appear in the video, in the form depicted. For generated imagery, additionally: no real identifiable person; no synthetic depiction of a sensitive real-world event presented as documentary; and the video's own synthetic-content disclosure obligations apply independently of the thumbnail.

## 16. Decision Rules

- Thumbnail and title carry the same information → **rewrite one**; a duplicate wastes half the packaging.
- Silhouette test fails → **fix separation first** (lighting, focus, or an explicit edge).
- More than one focal point → **delete elements until there is one**.
- Primary text's cap height under 10% of frame height → **cut words until it fits**.
- Text or critical detail in the bottom-right corner or bottom strip → **move it**; UI overlays it.
- Design evaluated only at full size → **re-evaluate at 168×94** before approving.
- Expression is neutral → **use no face at all**.
- The video will not deliver a shocking event → **use concerned, not shocked**.
- Channel is faceless → **lock a template** and let only the object change.
- Audience reads right-to-left → **mirror the Z-pattern layout**.
- No title pairs with any of the ten thumbnail sketches → **kill the video idea**, not the thumbnail.
- Prompt written in the channel's non-English language → **rewrite it in English**; add text in the editor.
- Prompt lacks "no text" → **add it**; never let the model set type.
- A recurring real face is needed → **composite a photograph**, do not generate the likeness.
- Two A/B variants share a layout → **replace one**; a colour tweak teaches nothing.
- Verdict is Same → **stop testing that dimension** on this channel. Verdict is Inconclusive → **conclude nothing**; the video lacked impressions.
- CTR high, retention low → **make the packaging less aggressive**, not more.
- Video is in an active distribution push → **do not change its thumbnail**.
- Changing packaging → **change the thumbnail or the title, never both at once**.
- Any element in the thumbnail does not appear in the video → **remove it**; that is the mismatch penalty, not creative licence.
