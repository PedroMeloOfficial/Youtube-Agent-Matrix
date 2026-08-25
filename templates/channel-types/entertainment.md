---
archetype: entertainment
display_name: Entertainment
axes:
  traffic: [browse, suggested]
  intent: be-entertained
  format: [narrative, performance]
  monetization: sponsorship-primary
  production: [solo, small-team, studio]
benchmarks:
  ctr_target: "3.5% browse baseline · 6.0% Entertainment niche average"
  retention_target: "40%+ AVD (ahead of ~83% of channels)"
  length_min: 8
  length_max: 12
  cadence_solo: "1/week"
  cadence_team: "2/week"
  shorts_per_week: "5-7"
  rpm_range_usd: "2-5 (Entertainment / Commentary)"
  evergreen_share: "50-60%"
traffic_mix:
  browse: 45
  suggested: 25
  shorts: 20
  search: 5
  external: 5
---

# Entertainment Channel

> Browse-dominant. Nobody searched for this. The thumbnail has under one second to make the
> case.

---

## 1. Channel DNA

Entertainment is the **highest-variance archetype on the platform**, and variance is not a
footnote here — it is the defining structural fact. One breakout video compresses every timeline
at once, taking a channel through two tiers in a month, which means growth arrives in
discontinuous jumps rather than the steady accumulation an education or tutorial channel can
forecast. The consequence is that planning is unreliable and **packaging becomes the dominant
skill**: this archetype lives on browse, where CTR runs 3.5% because the video is served cold
against everything else on the platform and the viewer decides in under one second
(`benchmarks.md` §1, §7). No keyword rescues a weak thumbnail here — there is no search intent to
fall back on. The economics invert the usual stack: Entertainment sits in RPM tier 3 at $2–5
(`benchmarks.md` §9), the lowest band outside music, so **brand deals outrank AdSense** and a
channel with 50K–250K views per video earns $1,250–6,250 from one sponsor slot against a few
hundred dollars of ad revenue for the same video. Retention behaves differently too: the viewer
is not trying to finish, they are deciding every thirty seconds whether to keep being
entertained, which makes pattern interrupts and open loops structural rather than decorative —
the suspension-bridge curve correlates with 68% higher completion (`benchmarks.md` §2). The
characteristic trap is **thumbnail fatigue**: the visual formula that produced the breakout gets
repeated until the audience stops registering it, CTR erodes a fraction of a point at a time —
and 0.5 points is significant at scale (`benchmarks.md` §1) — and the creator diagnoses a content
problem while looking at a packaging problem.

---

## 2. Content Mix

| Type | Share | Purpose |
|---|---|---|
| **Hub** (the repeatable format the channel is known for) | 55–60% | The reliable base. A format viewers recognize converts on browse without explanation. |
| **Hero** (high-concept, high-budget swings) | 25–30% | Where breakouts come from. Deliberately over-invested and deliberately infrequent. |
| **Help** (behind-the-scenes, how-it-was-made, bloopers) | 15% | Cheap to produce, converts the casual viewer into a subscriber, fills the calendar between heroes. |

**Evergreen vs trending:** 50–60% evergreen. Entertainment ages better than commentary and worse
than education — a good format video is watchable a year later, but suggested traffic favors
recency, so the catalog supports rather than carries.

**Budget asymmetry is the strategy.** Spend disproportionately on a small number of heroes rather
than evenly across the calendar. Variance means the expected value of ten average videos is lower
than that of eight average videos plus two genuinely ambitious ones.

---

## 3. Cadence & Length

| Setup | Long-form | Shorts | Notes |
|---|---|---|---|
| Solo | 1/week | 5–7/week | Production value per video matters more than frequency; Shorts carry the volume requirement |
| Small team (2–3) | 2/week | 7+/week | Long-form plus Shorts together grows 40–60% faster than either alone (`benchmarks.md` §4) |

**Optimal length:** 8–12 minutes (`benchmarks.md` §3). This band clears the mid-roll threshold
while staying inside the attention the format can hold. The 5–10 minute band posts the highest
average retention on the platform at 31.5%, so the bottom of the range is not a compromise.

**Mid-roll:** 8:00 unlocks mid-rolls for roughly a 50% revenue increase (`benchmarks.md` §3) —
which is significant precisely because base RPM is $2–5. Place breaks immediately after a
resolution, never inside a build-up.

**Shorts:** the primary discovery instrument for this archetype, not a side channel. Shorts are
75% of platform views (`benchmarks.md` §3) and rank on completion (`benchmarks.md` §8). Note the
~10% audience overlap with long-form (`benchmarks.md` §8) — Shorts build reach, and reach is what
a browse-dependent channel needs.

---

## 4. Title Patterns

1. `I [EXTREME ACTION] for [DURATION]`
2. `[N] People vs [OPPONENT OR OBSTACLE]`
3. `We Tried [ABSURD PREMISE] and [UNEXPECTED OUTCOME]`
4. `Last to [ACTION] Wins $[AMOUNT]`
5. `[EXTREME ADJECTIVE] [NOUN] vs [EXTREME ADJECTIVE] [NOUN]`
6. `I Spent $[AMOUNT] on [THING]`
7. `[ACTION] — But Every Time [CONSTRAINT], [CONSEQUENCE]`
8. `Surviving [DIFFICULT SITUATION] With Only [LIMITATION]`
9. `I Let [PERSON OR GROUP] Control My [THING] for [DURATION]`
10. `[SUPERLATIVE] [THING] in [PLACE OR CATEGORY]`

**Length rule:** browse-dominant archetype, so keep titles under 50 characters — short titles read
faster in a scrolling feed and this is the surface the archetype competes on (`benchmarks.md`
§6). Shorter is better than shorter-but-vague: the concept must be legible in one glance. Numbers
lift CTR 20–30% (`benchmarks.md` §6) and concrete stakes read faster than adjectives. For a non-English channel the formulas are shapes, not sentences to translate: rebuild them from the wording that reads fast to that audience in a feed, taken from top local channels rather than from the English above (`references/localization-guide.md` §5).

---

## 5. Thumbnail Formula

- **Face:** near-mandatory here, at genuine emotional peak, filling a large share of the frame.
  Faces lift CTR 20–30% (`benchmarks.md` §7) and the expression is what sells the premise.
- **Text:** ≤5 words, 3 ideal (`benchmarks.md` §7). Text carries the stake or the number; the image
  carries the emotion. They must never say the same thing — the Information Split Rule
  (`benchmarks.md` §7).
- **Colors:** 2–3 highly saturated primaries. A consistent, recognizable palette is worth more
  here than in any archetype except education, because a browse viewer recognizes the channel
  before reading the title.
- **Composition:** exactly one focal point, 30–40% negative space. The strongest structure is a
  visible contrast — a before/after, a scale mismatch, a person against an obviously difficult
  situation. The premise must be readable at mobile size with 70%+ of views on mobile.
- **Avoid:** running the same layout more than roughly six videos in a row (thumbnail fatigue),
  wide shots where the face is small, more than one idea, and text the viewer must read to
  understand the image.
- **Target CTR:** 6.0% is the Entertainment niche average and 3.5% is the browse baseline
  (`benchmarks.md` §1). Diagnose against the traffic-source table — a browse-dominant video at
  4% is healthy even though the niche average reads 6%.
- **Test everything.** Native A/B testing runs up to 3 variants over up to 2 weeks and optimizes
  for watch-time share, with documented CTR gains of 37–110% (`benchmarks.md` §7). In the
  archetype where packaging is the dominant skill, not running the test is leaving the largest
  available lever untouched.

---

## 6. Hook Style

**Primary — Stakes Framing.** State what is at risk and what happens if it goes wrong, in the
first sentence. The viewer stays to find out the outcome, and the outcome is the only thing
holding them.
> "If we don't finish this before the tide comes in, everything in the truck is gone."

**Secondary — Curiosity Gap.** Cold-open on the most visually arresting moment in the video, cut
away before it resolves, then start.
> "That's forty minutes from now. It goes badly. Here's how we got there."

**Timing:** the first 5 seconds decide the video — 20% of viewers leave in the first 10 seconds
and 55% in the first 60 (`benchmarks.md` §2). Place a pattern interrupt inside the first 5
seconds (+23% retention) and roughly every 30 seconds thereafter, both `benchmarks.md` §2. Open
loops are the archetype's core retention device: the suspension-bridge curve correlates with 68%
higher completion, and rhythmic sawtooth re-engagement with 43% (`benchmarks.md` §2).

Full taxonomy in `references/hook-library.md`.

---

## 7. Monetization Stack

> All figures are **US baseline**. Apply `references/localization-guide.md` before quoting
> revenue for a non-US channel.

| Rank | Stream | Why This Position |
|---|---|---|
| 1 | Brand deals | Outranks AdSense outright: 50K–250K views pays $1,250–6,250 per video against tier-3 $2–5 RPM on the same views (`benchmarks.md` §9) |
| 2 | AdSense | Reliable and uncapped by negotiation, but the lowest RPM band outside music — volume is the only way it scales |
| 3 | Shorts ad share | Ranked unusually high here because Shorts volume is highest in this archetype; still only $0.01–0.05 per 1K in comedy/lifestyle (`benchmarks.md` §9) |
| 4 | Shopping affiliate | Merchandise and channel-branded products convert on identity rather than utility; 5–20% commission on affiliate items (`benchmarks.md` §9) |
| 5 | Memberships | Works once the audience is attached to the people rather than the format; behind-the-scenes tiers convert best |
| 6 | External funnels | Real but slow — a second channel, a podcast, or live events rather than a course |
| 7 | Super Chat / Thanks | Only where the channel streams; the edited format offers no live moment to tip |

**Q4 matters disproportionately.** CPMs run 30–60% higher than average in Q4
(`benchmarks.md` §9) and sponsors spend against the same calendar. Schedule the most expensive
heroes into it and the experiments into January, the cheapest month.

---

## 8. Growth Trajectory

| Tier | What Changes | Key Lever | Revenue Character |
|---|---|---|---|
| 0–500 | Under 500 subscribers the channel receives active algorithmic promotion (`benchmarks.md` §4); the constraint is not reach, it is not yet having a format that repeats | Find one repeatable format and stop producing anything that cannot be made again on schedule | None — not yet monetized |
| 500–1K | Expanded YPP at 500 subscribers (`benchmarks.md` §9) opens audience-direct streams, and Shorts can buy reach the format cannot yet earn | Shorts volume as a discovery instrument feeding a long-form format that already works | Audience-direct only, and immaterial at this size |
| 1K–10K | Full YPP at 1,000 subscribers (`benchmarks.md` §9); packaging becomes the dominant variable — the same idea wins or dies on thumbnail and title | A/B test every thumbnail; double down on whatever broke out instead of diversifying away from it | First ad revenue, held down by the Tier 3 RPM band (`benchmarks.md` §9) — reach far outruns earnings in this archetype |
| 10K–50K | Brand deals become reachable at the floor (`benchmarks.md` §9) and typically outearn ads; hero budgets become justifiable for the first time | A rate card, and hero budgets sized to what a sponsor pays rather than to what ads return | Meaningful but not replacement income from ads alone; sponsorship is what makes it material |
| 50K–100K+ | The channel behaves as a media property — sponsorship inventory rather than view count sets income | Sponsorship rate card, and a format durable enough that a sponsor buys a slate rather than a single video | Can reach replacement income, driven almost entirely by sponsorship rather than by the Tier 3 RPM band |

Variance is the format here, not noise around it. One breakout can carry a channel across several tiers while a year of
competent uploads moves it nowhere, which makes this archetype's position the least predictable on the matrix.

> ⚠️ Tier progression is not a timeline. `benchmarks.md` §11 lists growth-timeline and revenue-by-tier as known gaps — no verified data exists. Any revenue figure must be modeled from the creator's own audience size and geography via `references/localization-guide.md`, never read off a table.

---

## 9. Failure Modes

**Thumbnail fatigue.** The layout that produced the breakout is now on twenty consecutive videos.
CTR slides half a point at a time, the creator reads it as audience fatigue with the content, and
changes the content instead of the packaging.
**Fix:** track CTR by thumbnail layout family in a spreadsheet, not by video. When a family's
rolling three-video average falls 0.5 points below its own first three, retire it — and run the
next two videos through native A/B testing with a deliberately different composition as a
variant.

**Escalation without a ceiling.** Each video must out-do the last, so budgets and stunt scale
rise until a single underperformer is financially unrecoverable and the format has nowhere left
to go.
**Fix:** set a fixed per-video budget cap and a separate quarterly hero budget, in writing, before
the next production. Escalate the premise instead of the spend — a new constraint costs nothing
and reads as bigger.

**Format-less variety.** Every video is a different idea, so browse never learns who to serve it
to, the audience never learns what a subscription buys, and no video benefits from the last one.
**Fix:** commit the next 8 videos to one repeatable format with a fixed title structure and
thumbnail family. Run the variety ideas as Shorts, where the cost of a miss is one afternoon.
