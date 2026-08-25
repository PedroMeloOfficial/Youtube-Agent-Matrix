# Shorts Playbook

Method for making vertical short-form that survives the swipe — ranking model, hook craft, loop design, vertical composition, audio economics, serialisation, cross-format strategy and testing without native A/B — for any creator in any language.

> **Every specification, threshold and benchmark lives in `benchmarks.md`.** This file teaches the craft and names the section where each number lives.

**Contents:** [1 Explore/Exploit](#1-exploreexploit-ranking) · [2 Signal Hierarchy](#2-the-signal-hierarchy-and-how-to-design-for-it) · [3 Vertical Frame](#3-vertical-frame-craft) · [4 Text & Captions](#4-on-screen-text-and-captions) · [5 Cover & First Frame](#5-cover-frame-and-first-frame) · [6 Hook Craft](#6-hook-craft-in-a-13-second-window) · [7 Loops](#7-loop-design) · [8 Audio vs Revenue](#8-audio-trending-sound-vs-revenue) · [9 Series](#9-series-and-serialisation) · [10 Cadence & Freshness](#10-cadence-and-the-freshness-window) · [11 Subscriber Conversion](#11-shorts-to-subscriber-conversion) · [12 Both Directions](#12-shorts-and-long-form-both-directions) · [13 Testing Without A/B](#13-testing-shorts-without-native-ab) · [14 Comments](#14-comments-and-pinning) · [15 Cross-Platform Specs](#15-cross-platform-spec-comparison) · [16 Decision Rules](#16-decision-rules)

## 1. Explore/Exploit Ranking

Shorts run on a ranking system separate from Browse and Search (`benchmarks.md` §5). The mechanism is a bandit: a small seed cohort **explores**, and if retained attention clears the bar, distribution **exploits** — widening in steps, each step re-testing.

| Property | Consequence for the creator |
|---|---|
| The feed auto-plays; nothing is clicked | **CTR is irrelevant.** There is no click decision to optimise, and the cover image does not sell the video |
| The competing action is the swipe | The entire first second buys the *absence* of a swipe |
| Each widening re-tests | A Short that plateaus failed a later cohort, not the first |
| Ignition is often delayed | A Short can enter exploit days after upload — do not delete an underperformer early |
| Freshness gates re-testing | Past the freshness window (`benchmarks.md` §8) the system largely stops re-testing |
| Ranking is per-Short | Subscriber count buys a slightly warmer seed cohort and nothing else |

Practical reading: nothing about packaging matters here, and everything about the **first second and the last second** does.

## 2. The Signal Hierarchy and How to Design for It

Ranked signals and their numeric thresholds: `benchmarks.md` §8.

> **Read the threshold reconciliation in `benchmarks.md` §8 before using any of these numbers.** Completion rate, Viewed-vs-Swiped-Away and the emergency rewrite threshold measure three different things and are never comparable. Completion is *did they reach the end*; Viewed-vs-Swiped-Away is *did the opening hold them past the swipe decision*; the emergency threshold is a diagnostic floor on the second of those, not a lower target for the first.

| Signal | What it actually measures | How to design for it |
|---|---|---|
| Completion | Reached the end | Cut to the shortest version that still lands; delete every beat that is neither setup nor payoff |
| Loop / replay | Watched past the end into a second pass | Design the ending to hand back to the beginning (§7) |
| Comments and shares | Worth acting on | Build in one specific disagreement, one gap, or one "send this to X" moment |
| Viewed vs Swiped Away | The hook held past the decision point | Rewrite the first 1–3 seconds (§6); nothing else moves this number |
| Satisfaction | Long-press, surveys, "more like this" | Deliver exactly what the opening promised; never bait |

**Length is the completion lever.** The bimodal length pattern and the dead zone in `benchmarks.md` §8 exist because a Short is either a single beat or a complete miniature story — the middle is a beat stretched too far. Decide which of the two the idea is, then cut to that band. **Density is the second lever:** something must change visually at the Shorts interrupt cadence in `benchmarks.md` §2 — cut, zoom, angle change, text change, graphic entry. Stillness is a swipe cue.

## 3. Vertical Frame Craft

The frame is 1080×1920 (`benchmarks.md` §8), but a substantial part is covered by interface. Composing for the full frame puts content under UI.

| Region of the 1920px frame | Occupied by | Rule |
|---|---|---|
| Top ~10% | Status bar, search and menu affordances | No text, no critical detail |
| Bottom ~20–25% | Title, channel name, description preview, sound attribution, progress bar | **The most damaging zone** — no subtitles, faces or key action |
| Right ~15% of width, lower two-thirds | Like / comment / share / remix column, channel avatar | No text, no key subject; a face here is partly covered |
| Outer margins | Cropping on some devices and previews | Keep a ~5% inset all round |
| **Safe centre band** | Middle ~60% of height, left ~80% of width | Subject, action and all text go here |

| Composition rule | Reason |
|---|---|
| Subject in the upper-middle third | Lower placement risks the UI band; dead centre reads static |
| Frame vertically at capture | Cropping horizontal footage either loses the subject or forces a soft blow-up |
| Never letterbox horizontal footage with blank bars | Reads as repurposed and wastes the safe band; use blurred-fill or split-screen instead, subject scaled into the band |
| Close crops, high contrast | The frame is narrow, and Shorts are watched one-handed, in poor light, at low brightness |

## 4. On-Screen Text and Captions

Sound-off viewing is common and captions raise watch time (`benchmarks.md` §6), so burned-in text is not optional here.

| Property | Rule |
|---|---|
| Minimum size | Cap height **≥4% of frame height** (≈75px at 1080×1920); the hook line ≥6% |
| Weight and legibility | Bold or heavier, with a stroke or semi-opaque plate; never plain white over unknown footage |
| Position | Inside the safe centre band only (§3) — never the lower quarter |
| Line length | 3–5 words per line, two lines maximum on screen at once |
| Caption style | Word-by-word or phrase-by-phrase reveal synced to speech; static block captions underperform |
| Burn-in vs uploaded track | **Burn in** styled captions for the feed **and** upload a caption track for accessibility and indexing |
| Colour | One accent colour for emphasis words, consistent across the channel |

**Language adaptation:** the size floor is a legibility floor, so scripts with fine strokes or complex glyphs (Chinese, Japanese, Thai, Devanagari, Arabic) need a *larger* floor and fewer glyphs per line, not the minimum. RTL text needs an RTL-capable renderer — many caption tools silently reverse or disconnect Arabic and Hebrew letterforms, so always verify rendered output. Where auto-caption accuracy in the language is weak, type the captions rather than correcting a bad transcript.

## 5. Cover Frame and First Frame

In the feed the cover image does nothing — the Short auto-plays. It acts as a thumbnail only on the channel's Shorts tab, in search results and on shelves, so pick a legible, high-contrast frame and add a two-to-three-word label where the tool allows. Choose cover frames that make the Shorts-tab grid read as a coherent set: that grid is what a viewer sees after tapping through from a Short they liked, and it is where subscriptions actually happen (§11).

**The first frame of video is the hook.** It is displayed and playing before any decision is made, so it must be high-contrast, one clear subject, mid-action rather than mid-setup, and already carrying the hook text if the hook is verbal. A first frame that is a black fade, a logo sting or an establishing shot is a swipe. Never open a Short with a channel intro.

## 6. Hook Craft in a 1–3 Second Window

The window is 1–3 seconds (`benchmarks.md` §8). In it the viewer must learn what the payoff is and that it is close.

| Hook type | Shape | Best for |
|---|---|---|
| Result-first | Show the finished outcome, then rewind | Builds, transformations, cooking |
| Contradiction | "Everyone does X. X is wrong." | Education, commentary |
| Direct address of a state | "If your X keeps doing Y, this is why." | Problem-solving |
| Visual anomaly | An image that should not be possible | Anything visual; no words needed |
| Countdown / stakes | "Three things, and the third is the one." | Lists |
| Mid-sentence entry | Start inside the action, no preamble | Story, reaction |
| Question with a delayed answer | Ask, then withhold for a beat | Explainers |

**Rules.** No preamble — delete greetings, channel names, "in this video", context-setting; context arrives *after* the hook. State and show simultaneously: verbal hook, matching visual, and the hook as on-screen text — three channels, one message. Name the payoff, not the topic. Promise something small and near, because a big promise raises the completion bar the Short then fails. First cut inside the first second. And the hook must survive muting: if it only works with audio, most of the seed cohort never receives it.

**Diagnosis:** if Viewed-vs-Swiped-Away is below the emergency threshold (`benchmarks.md` §8), the opening is the only thing to change — do not lengthen, add music, or re-edit the middle. A published Short's opening cannot be repaired in place; re-cut the first three seconds and publish as a new Short.

## 7. Loop Design

A loop converts one viewer into multiple counted views (`benchmarks.md` §8 view counting) and pushes average-percent-viewed past the loopable threshold in `benchmarks.md` §8 — a strong promotion signal.

| Technique | How | Fits |
|---|---|---|
| Frame match | Last frame compositionally identical to the first | Any format — the most reliable |
| Sentence wrap | Final words complete the first sentence's clause | Talking-head, narration |
| Cyclical action | The action ends where it began | Crafts, motion, demos |
| Payoff stated too fast to catch | A second pass is needed to get it | Fast facts, numbers |
| Question-answer flip | Ends on the question the opening answered | Explainers |
| Hard cut, no outro | No fade, no end card, no subscribe tail | Universal — outros are the biggest loop killer |

**Build:** choose or shoot a last frame matching the first in framing, lighting and subject position; trim so the cut lands *on* the action rather than after it; remove every trailing frame of silence. Test by watching twice in a row — a felt seam is a swipe point. Do **not** fake a loop by cutting mid-sentence with no payoff; that reads as a broken video and depresses satisfaction signals.

## 8. Audio: Trending Sound vs Revenue

Every licensed track splits the revenue pool (`benchmarks.md` §8). Trending audio raises early distribution; licensed audio lowers the creator's share. The tradeoff resolves by asking what the Short is *for*.

| Purpose of the Short | Audio choice | Reasoning |
|---|---|---|
| Reach, discovery, growth phase | A trending licensed track is acceptable | The revenue share on a low-RPM format is small; distribution is the asset |
| Monetisation in a high-RPM niche | **No licensed music** | The pool split costs more than the trend gains (`benchmarks.md` §9 vs the §8 split rule) |
| Conversion to long-form or a product | No licensed music | Value is downstream, and the track competes with the voice |
| Longer Shorts near the maximum length | **No Content ID music** | It blocks longer Shorts in some territories (`benchmarks.md` §8) |
| Dialogue-led or explainer | Voice only, or a royalty-free bed low in the mix | Music competes with comprehension |
| Trend participation is the concept | The required track | The format does not exist without it |

**Default:** the creator's own voice and sound design; add a licensed trending track only when the purpose is reach *and* the track is genuinely part of the concept. Never add a second licensed track — the split worsens sharply (`benchmarks.md` §8). Sound design substitutes well: transitions, whooshes, impacts and clean room tone hold attention at no revenue cost. Loudness matters more than the track — normalise dialogue, cut silence to near zero, make the first word audible immediately.

## 9. Series and Serialisation

Serialised Shorts convert far better than isolated ones, because they give a reason to subscribe rather than merely to watch.

| Element | Rule |
|---|---|
| Format lock | Same opening structure, text style, length band and accent colour every episode |
| Numbering | Visible in the on-screen text and the title ("Part 7") — implies a back catalogue |
| Recognisable first frame | The series should be identifiable before any audio plays |
| Playlist | Every episode into one playlist, linked in the description |
| Cadence promise | Stated once per episode ("one of these every day") |
| Inter-episode loop | End on what the next episode covers — but only after the current payoff lands |
| Arc length | Plan a finite arc; open-ended series lose urgency |

A series also solves ideation: one validated format yields dozens of episodes, and each episode is comparable to the last — which is exactly what makes the testing method in §13 work.

## 10. Cadence and the Freshness Window

Upload frequency effects: `benchmarks.md` §4. Freshness window: `benchmarks.md` §8.

| Implication | Action |
|---|---|
| Re-testing largely stops after the freshness window | Treat a Short's life as short; **volume, not longevity**, is the growth mechanism |
| Evergreen Shorts still decay | An evergreen *idea* can be re-made later; the old file will not revive |
| Re-uploading the same file | Poor practice — exposure to the inauthentic-content policy (`benchmarks.md` §5) with no history benefit |
| Re-making an evergreen idea | Legitimate — new hook, new footage, new framing, months apart |
| Notification limits | Bunching uploads in one day wastes notifications (`benchmarks.md` §4) |
| Batch production | Shoot a series in one session, publish on a spaced schedule |

Consistency beats bursts: a steady near-daily cadence keeps the channel continuously inside the exploration system, while a burst followed by silence spends the freshness window all at once.

## 11. Shorts to Subscriber Conversion

Be honest about the ceiling: Shorts and long-form audiences overlap only slightly, and in-video links convert poorly (`benchmarks.md` §8). Shorts build reach; conversion must be engineered.

| Tactic | Mechanism | Realistic effect |
|---|---|---|
| Numbered series | Gives a reason to return, which is what a subscription is | Highest leverage |
| Consistent on-screen identity | The channel is recognised across separate Shorts before it is ever visited | High |
| A coherent Shorts-tab grid | The tap-through destination looks like a body of work | High |
| Verbal ask tied to the value just delivered | "There are nine more of these" beats "subscribe" | Medium |
| Pinned comment linking the series playlist | Catches the viewer already in the comments | Medium |
| End-card subscribe screen | Kills the loop (§7) and costs completion | **Net negative — avoid** |
| Linking long-form inside the Short | Conversion is very low (`benchmarks.md` §8) | Low; put it in the description instead |

The realistic model: Shorts produce a large, shallow audience; a fraction subscribes and a smaller fraction of those watch long-form. Channels running both formats grow faster than either alone (`benchmarks.md` §4, §8) — through breadth of reach, not direct funnelling.

## 12. Shorts and Long-Form, Both Directions

**Long-form → Shorts.** Select only self-contained moments with a setup and a payoff inside the clip; a clip needing the video's context is not a Short. Never publish a raw excerpt — re-cut it as hook → value → resolution with a new opening line, recompose to vertical with the subject in the safe band (§3, never letterboxed), re-caption in the Shorts template rather than the long-form style, and add a loop point the original did not have (§7). Publish across days, not all at once, and reference the full video in the description and pinned comment rather than by breaking the ending.

| Shorts → long-form | Method |
|---|---|
| Hook testing | Publish several openings as separate Shorts; the best Viewed-vs-Swiped-Away becomes the long-form opening |
| Topic validation | An overperforming Short identifies demand worth a full video |
| Format validation | A working Short series becomes a long-form segment structure |
| Audience research | Comments surface the questions a long-form video should answer |

Shorts are the cheapest experiment surface a channel has: low production cost, distribution not gated by subscriber count, and feedback within days.

## 13. Testing Shorts Without Native A/B

Native thumbnail and title A/B testing does not cover Shorts (`benchmarks.md` §7). The substitute is **sequential comparison against the channel's own baseline**.

1. **Establish a baseline.** Log the last 10–20 Shorts with length band, hook type, format, audio choice, Viewed-vs-Swiped-Away, average percent viewed, completion and shares. The median of each is the baseline — not a published benchmark.
2. **Change one variable** and hold it across a block.
3. **Run 3–5 Shorts per variant.** Single-Short results are dominated by cohort noise.
4. **Compare medians, not means** — one viral outlier destroys a mean.
5. **Match the metric to the variable**, and compare Shorts of similar age; one past the freshness window is not comparable to a fresh one.

| Variable changed | Metric that answers it |
|---|---|
| Hook (first 1–3s) | Viewed vs Swiped Away |
| Length or structure | Completion rate |
| Ending or loop point | Average percent viewed |
| Topic or claim | Shares and comments |
| Caption style, legibility | Viewed vs Swiped Away *and* completion |
| Audio choice | Completion, with revenue share as a cost |

**The A/B-adjacent trick:** publish two genuinely different hooks on the *same* core content, days apart, and compare. Not a controlled experiment — audience state and timing differ — but across a series it identifies which hook family this audience responds to. Keep a running log; the value is the pattern across dozens of Shorts, never one result.

## 14. Comments and Pinning

Comments and shares outrank likes in the Shorts signal hierarchy (`benchmarks.md` §8), and early replying correlates with reach (`benchmarks.md` §5). Engineer **one specific question** answerable in three words — open-ended questions get no replies. Leave a deliberate gap people will fill in the comments, but never omit the payoff. Pin a comment immediately, before hostile or off-topic threads set the tone; if something is wrong, pin the correction plainly rather than an excuse. Reply fast and early — the first hours matter far more than the total — and reply with a follow-up hook ("the full version is in the pinned playlist"), which converts better than a link inside the Short. Do not argue: sorting a comment section into a fight raises comment count and lowers satisfaction.

Write pins in the spoken language. When a Short breaks out into a foreign-language audience — visible in the geography report — add a short translated line to the pin.

## 15. Cross-Platform Spec Comparison

For the repurposing workflow. Verify current values before a large campaign; short-form specs change frequently.

| Property | YouTube Shorts | TikTok | Instagram Reels |
|---|---|---|---|
| Max length | See `benchmarks.md` §8 | Up to 10 min (longer tiers by account) | Up to 3 min (longer for some accounts) |
| Practical sweet spot | See `benchmarks.md` §8 | 15–34s for completion, longer for depth | 15–30s |
| Aspect / resolution | 9:16, see `benchmarks.md` §8 | 9:16, 1080×1920 | 9:16, 1080×1920 |
| Caption / description limit | Long description; only the first characters preview (`benchmarks.md` §8) | ~2,200 characters | ~2,200 characters |
| Hashtags | See `benchmarks.md` §6 | Heavily used; several per post is normal | Moderate; keyword-style captions matter more |
| Foreign watermarks | **Suppressed** — remove before upload | Suppressed | Suppressed |
| Audio licensing | Licensed tracks split the revenue pool (`benchmarks.md` §8) | Commercial accounts restricted to the commercial library | Commercial accounts restricted to the commercial library |
| Monetisation model | Revenue-pool share (`benchmarks.md` §9) | Rewards-programme model, eligibility-gated, favours longer posts | Bonus programmes intermittent; brand deals dominate |
| Ranking emphasis | Completion, loops, shares | Completion, rewatch, shares, comment depth | Sends and shares weighted heavily, then watch time |
| Freshness behaviour | Deprioritised after the window (`benchmarks.md` §8) | Long tail; old posts can resurface | Short tail, but sends can revive a post |
| Search relevance | Strong — platform and web search | Growing; captions indexed | Growing; captions and on-screen text indexed |
| Safe-zone caution | Bottom band and right rail (§3) | Bottom band, right rail, top-centre search chip | Bottom band, right rail; extra care if cross-posted to Stories |

**Repurposing rules:** export one master with no platform-specific UI and no watermark; keep all text and subjects inside the strictest common safe band; burn in captions, since caption systems differ; rewrite the description per platform instead of pasting one everywhere; never re-upload a file carrying another platform's watermark.

## 16. Decision Rules

- A Short is being optimised for clicks → **stop**; there is no click, optimise the first second.
- First frame is a fade, a logo or an establishing shot → **replace it** with mid-action.
- The hook does not work muted → **rewrite it**; most of the seed cohort receives it silently.
- Viewed-vs-Swiped-Away below the emergency threshold (`benchmarks.md` §8) → **change only the opening** and republish as a new Short.
- Completion low but the hook holds → **cut length**, do not add production value.
- Length falls in the dead zone (`benchmarks.md` §8) → **cut down, or extend into a full miniature story**.
- Nothing changes visually at the Shorts interrupt cadence (`benchmarks.md` §2) → **add cuts**.
- Text or a face in the lower quarter or the right rail → **move it into the safe centre band**.
- Captions below the size floor → **enlarge and cut words**; complex scripts need a larger floor.
- The Short ends with an outro or subscribe card → **delete it**; it kills the loop.
- The ending does not hand back to the beginning → **redesign the last beat** before publishing.
- High-RPM niche and the Short is monetisation-oriented → **use no licensed music**; a second licensed track → **never**.
- The Short is near maximum length → **avoid Content ID music entirely**.
- A Short underperforms in its first days → **wait**; ignition is often delayed.
- A Short is past the freshness window → **do not re-upload it**; re-make the idea instead.
- Testing a variable → **run 3–5 Shorts and compare medians to the channel's own baseline**, never one Short against a published benchmark.
- A long-form clip needs the full video's context → **it is not a Short**; rebuild it with its own setup and payoff.
- A long-form excerpt is going out unedited → **re-cut it** with a new hook, vertical reframe and loop point.
- Subscriber conversion is the goal → **build a numbered series**, not a stronger call to action.
- A file carries another platform's watermark → **do not upload it**.
