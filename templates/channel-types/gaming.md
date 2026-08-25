---
archetype: gaming
display_name: Gaming
axes:
  traffic: [browse, suggested]
  intent: be-entertained
  format: [performance, narrative, livestream]
  monetization: adsense-primary
  production: [solo, small-team]
benchmarks:
  ctr_target: "8.5% niche blended average — diagnose browse videos against 3.5%"
  retention_target: "40%+ AVD (beats ~83% of channels)"
  length_min: 10
  length_max: 20
  cadence_solo: "3-4/week (12+/month)"
  cadence_team: "5-7/week (20+/month)"
  shorts_per_week: "5-7"
  rpm_range_usd: "2-5 (US median $3.50)"
  evergreen_share: "30-40% (guide and walkthrough content only)"
traffic_mix:
  browse: 35
  suggested: 35
  search: 15
  shorts: 10
  external: 5
---

# Gaming Channel

> The largest category on the platform, the lowest RPM tier on the platform, and the widest
> format range of any archetype.

---

## 1. Channel DNA

Gaming is a **volume-and-watch-time business fighting a low-RPM ceiling**: $2–5 with a US median
of $3.50 (`benchmarks.md` §9) is the third tier, so the economics only work when hours of watch
time are cheap to produce and plentiful — which is exactly what the format provides. It carries
the **highest blended niche CTR on the matrix at 8.5%** (`benchmarks.md` §1), though that number
is weighted toward search and suggested and a browse-dominant gaming video at 3.5% is still
healthy. The critical thing an agent must not flatten is that **"gaming" is not one economy**:
guide, walkthrough and tips content behaves like Tutorial — it is search-driven, evergreen, and
compounds for as long as the game lives — while let's-play, challenge runs and reaction content
behaves like Entertainment, arriving through browse and suggested and decaying almost
immediately. A channel doing both is running two businesses with two different retention curves,
and should package them as two different things. Production is typically a **livestream-VOD
hybrid**: streams generate raw hours and direct audience revenue, edited highlights and Shorts
harvest the same session for discovery. **Personality carries more weight than the game** —
viewers can get the footage anywhere, so the commentary track, not the gameplay, is the
differentiator, and it is why an established gaming channel survives its flagship game dying.
**Game launches are the discovery events**: a launch window concentrates enormous search and
browse demand into a few days, and being present in it is worth more than months of steady
publishing. The characteristic trap sits right there — **chasing every new release** produces a
channel with no durable identity, an audience that arrived for one game and left with it, and no
compounding catalog to fall back on. Copyright is a live operational risk in this archetype in a
way it is not elsewhere; see §9.

---

## 2. Content Mix

| Type | Share | Purpose |
|---|---|---|
| **Hub** (the recurring series or the main game) | 45–55% | The identity. What subscribers come back for on a schedule. |
| **Help** (guides, walkthroughs, tips, patch breakdowns) | 25–35% | The only compounding content on the channel — search-driven, evergreen while the game lives. |
| **Hero** (launch coverage, challenge runs, high-effort projects) | 15–20% | Reach events. Launch windows belong here. |

**Evergreen vs trending:** 30–40% evergreen — and all of it lives in the Help row. Treat that
percentage as a deliberate hedge against the flagship game declining, not as filler.

**Package the two economies separately.** Guide content wants a keyword-shaped title and a
search-legible thumbnail; let's-play content wants a short browse title and an emotional
thumbnail. Sharing one packaging style across both means neither performs.

---

## 3. Cadence & Length

| Setup | Long-form | Shorts | Notes |
|---|---|---|---|
| Solo | 3–4/week (12+/month) | 5–7/week | Clears the 12+/month threshold — 8× view growth, 3× subscriber growth (`benchmarks.md` §4) |
| Small team (2–3) | 5–7/week (20+/month) | 7–14/week | Editor leverage is what makes daily viable; harvest Shorts from stream VODs |

**Optimal length:** 10–20 minutes for edited gaming (`benchmarks.md` §3). Full VODs are their own
thing — 20+ minute videos supply 57% of total platform watch time (`benchmarks.md` §3), so long
uploads are not inherently wrong, but they must be published as VODs on a separate playlist, not
as the channel's main feed.

**Mid-roll:** clear 8:00 for mid-rolls (~50% revenue increase, `benchmarks.md` §3). Easily met
here, and it matters more than in most archetypes precisely because the RPM is low — mid-rolls
are the main lever available on a $3.50 median.

**Pattern interrupts:** every ~30 seconds in edited long-form, every 2–3 minutes when live
(`benchmarks.md` §2). Notification cap is 3 per user per 24 hours (`benchmarks.md` §4) — daily
uploaders are already at the ceiling.

---

## 4. Title Patterns

1. `I Beat [GAME] With [ABSURD CONSTRAINT]`
2. `[GAME] but [RULE CHANGE]`
3. `The [ADJECTIVE] Ending in [GAME]`
4. `[NUMBER] Things [GAME] Never Tells You`
5. `How to [SPECIFIC TASK] in [GAME]`
6. `[GAME] [PATCH/UPDATE] Changed Everything`
7. `Why [MECHANIC] Is Broken in [GAME]`
8. `First [N] Hours of [GAME] — Honest Take`
9. `Beating [BOSS/LEVEL] Without [RESOURCE]`
10. `[GAME] Speedrun: [SPECIFIC RECORD ATTEMPT]`

**Length rule:** browse-and-suggested dominant, so keep titles **under 50 characters** — they
must read at a glance in a feed (`benchmarks.md` §6). The game name and the hook both belong in
the first 40–50 characters, since that is all mobile shows and 70%+ of views are mobile
(`benchmarks.md` §6, §7). **Exception:** formulas 4, 5 and 7 are search-shaped guide content —
run those to 60–70 characters and lead with the query, not the hook. Numbers in titles carry
+20–30% CTR (`benchmarks.md` §6). **Non-English channel:** re-derive the ten formulas from how that audience searches — including whether the game's name is localized or kept in English, which decides the title's first token. Never translate the English patterns directly (`references/localization-guide.md` §5).

---

## 5. Thumbnail Formula

- **Face:** high value here. Faces carry +20–30% CTR (`benchmarks.md` §7), and because
  personality outweighs the game, a recognizable reaction face is the fastest signal that this
  is *your* version of footage available everywhere. Guide thumbnails are the exception — use
  the in-game artifact instead.
- **Text:** ≤5 words, 3 ideal (`benchmarks.md` §7). Usually the constraint or the stake, never a
  restatement of the title (Information Split Rule).
- **Colors:** 2–3 (`benchmarks.md` §7). Gaming feeds are visually loud — saturation is table
  stakes, so contrast and a consistent channel palette do the actual differentiating.
- **Composition:** exactly one focal point, 30–40% negative space (`benchmarks.md` §7).
  Typically face + one game element. Resist the three-element collage the category defaults to.
- **Avoid:** raw in-game screenshots (they look like every other upload), text over busy HUD,
  and any thumbnail whose promise the video does not deliver — the late-2024
  clickbait/metadata-mismatch penalty applies (`benchmarks.md` §5).
- **Target CTR:** 8.5% is the blended niche average, but diagnose against the traffic source —
  3.5% on browse, 9.5% on suggested, 12.5% on search (`benchmarks.md` §1). Test & Compare gives
  up to 3 variants over 2 weeks (`benchmarks.md` §7); worth running on every hero upload.

---

## 6. Hook Style

**Primary — Stakes Framing.** State the constraint, the goal and the cost of failure in the first
line, so every subsequent second is a question the viewer wants answered.
> "One life. No upgrades. If I die, the save file gets deleted and the run is over."

**Secondary — Shock/Contradiction.** Open on the result or the moment that shouldn't be possible,
then rewind into how it happened.
> "This shouldn't work. The game was never built to allow it, and it just cost me the run."

**Timing:** value proposition within 15 seconds (+18% retention at one minute,
`benchmarks.md` §2). 20% of viewers are gone in the first 10 seconds and 55% within 60
(`benchmarks.md` §2) — so lead with the best moment of the session, not with the game booting up.
Open loops are strongly rewarded: the suspension-bridge retention shape correlates with 68%
higher completion (`benchmarks.md` §2), and a challenge run is naturally shaped like one.

Full taxonomy in `references/hook-library.md`.

---

## 7. Monetization Stack

> All figures are **US baseline**. Apply `references/localization-guide.md` before quoting
> revenue for a non-US channel.

| Rank | Stream | Why This Position |
|---|---|---|
| 1 | AdSense | Lowest RPM tier at $2–5, US median $3.50 (`benchmarks.md` §9), but always-on across an enormous volume of watch time and mid-roll-eligible on nearly every upload. Volume, not rate, is the argument |
| 2 | Brand deals | Gaming pays roughly $0.037/view — the highest per-view rate in the table and ~10× the RPM equivalent (`benchmarks.md` §9). Episodic rather than continuous, which is the only reason it isn't rank 1 |
| 3 | Memberships | Unusually strong: emotes, Discord access and stream perks are native to gaming culture; 1% conversion is meaningful, 2–3 tiers to start (`benchmarks.md` §9) |
| 4 | Super Chat / Thanks | Ranks higher here than in any archetype except livestream, because the VOD-hybrid production model means the channel is actually live; $50–500/mo at mid size, 70/30 split (`benchmarks.md` §9) |
| 5 | Shorts ad share | Ranks above where it sits elsewhere only because gaming clips are exceptionally cheap to harvest from existing footage — the RPM is still $0.01–0.07 per 1K (`benchmarks.md` §9) |
| 6 | Shopping affiliate | Peripherals, hardware and setup gear convert; 5–20% commission (`benchmarks.md` §9). Requires the audience to see the creator as a hardware reference, which not all do |
| 7 | External funnels | Weakest fit on the matrix — a be-entertained audience is not looking to buy a solution. Merch is the exception and behaves more like an audience-direct stream than a funnel |

**Q4 matters disproportionately here.** CPMs run 30–60% above average in Q4
(`benchmarks.md` §9), which lands on top of the holiday game-release calendar — the same weeks
carry the highest launch demand and the highest ad rates.

---

## 8. Growth Trajectory

| Tier | What Changes | Key Lever | Revenue Character |
|---|---|---|---|
| 0–500 | Under 500 subscribers the channel receives active algorithmic promotion (`benchmarks.md` §4); the job is to be findable for one game, not for gaming | Pick one game and one format; publish 3–4/week | None — not yet monetized |
| 500–1K | Expanded YPP at 500 subscribers (`benchmarks.md` §9) opens memberships and Super Chat — this audience pays for access earlier than most | Turn memberships and Super Chat on immediately; they arrive before ad revenue does | Audience-direct only, and immaterial at this size |
| 1K–10K | Full YPP at 1,000 subscribers (`benchmarks.md` §9), but the Tier 3 RPM band (Gaming, `benchmarks.md` §9) means views convert to revenue far more slowly than in Tier 1 niches | Add the guide/Help layer so part of the catalog compounds instead of decaying with the game | First ad revenue, low per view — watch hours, not revenue per video, are the metric that matters |
| 10K–50K | Brand deals become reachable at the floor (`benchmarks.md` §9), and gaming has a published per-view deal rate, so reach converts directly | A named recurring series and a consistent stream schedule, so a sponsor is buying a predictable audience | Meaningful but not replacement income from ads; sponsorship is what changes the picture |
| 50K–100K+ | Identity outgrows the game — the channel can survive a title dying, which is the failure that ends most gaming channels | Editor leverage, merch, and an identity that survives changing games | Can reach replacement income, but needs several times the views of a Tier 1 niche for the same ad revenue |

Gaming produces views cheaply per hour of finished content and converts them to revenue slowly, so judge this archetype
on watch hours and audience-direct income rather than on revenue per video.

> ⚠️ Tier progression is not a timeline. `benchmarks.md` §11 lists growth-timeline and revenue-by-tier as known gaps — no verified data exists. Any revenue figure must be modeled from the creator's own audience size and geography via `references/localization-guide.md`, never read off a table.

---

## 9. Failure Modes

**Content ID exposure treated as background noise.** Gameplay footage, licensed soundtracks,
cutscenes and trailer clips all carry rights the creator does not own. The visible symptoms are
claimed revenue on the best-performing videos, muted or region-blocked VODs, and eventually
strikes — first violation is a warning that expires after 90 days, the same policy again within
90 days is a strike, and **3 strikes terminate the channel** (`benchmarks.md` §7). On Shorts,
Content ID music also blocks longer uploads in some territories (`benchmarks.md` §8).
**Fix:** audit the last 20 uploads in the copyright tab this week; mute or replace every claimed
music segment, cut full cutscene playback in favour of commentary over it, and set a standing
rule that in-game music is disabled at capture and replaced with cleared audio.

**Uploading raw VODs as the main feed.** Streams are long and cheap to publish, so the feed fills
with 3-hour unedited sessions. Browse impressions dry up, AVD falls below 40% where videos are
actively deprioritized (`benchmarks.md` §2), and the drop drags the channel's edited uploads
down with it.
**Fix:** move all raw VODs to a dedicated playlist and stop publishing them to the main feed.
Cut one 10–20 minute highlight and 3–5 Shorts from each stream instead — same footage, three
distribution surfaces, none of them a retention liability.

**Footage without a person.** The channel publishes competent gameplay with thin or absent
commentary. Retention is flat, nothing gets shared, and there is no reason to pick this channel
over the hundred others covering the same game — which is fatal in a category where footage is
the commodity and personality is the product.
**Fix:** commit to a continuous commentary track on the next 10 uploads with a stated reaction or
opinion in the first 15 seconds of each. Compare AVD and shares across those 10 versus the
previous 10 — shares are the top-ranked satisfaction signal (`benchmarks.md` §5) and will move
first.
