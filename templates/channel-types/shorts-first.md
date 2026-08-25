---
archetype: shorts-first
display_name: Shorts-First
axes:
  traffic: [shorts-feed]
  intent: be-entertained
  format: [vertical-short]
  monetization: product-funnel-primary
  production: [solo, small-team, faceless-automated]
benchmarks:
  ctr_target: "not applicable — Shorts rank on completion, not clicks. Track Viewed vs Swiped Away: 75%+ good, below 60% rewrite the hook now"
  retention_target: "70%+ completion rate triggers aggressive promotion"
  length_unit: seconds
  length_min: 15
  length_max: 60
  cadence_solo: "1/day (30/month)"
  cadence_team: "2/day (60/month)"
  shorts_per_week: "7-14"
  rpm_range_usd: "0.01-0.07 typical per 1K views (Finance $0.05-0.30 · Comedy/Lifestyle $0.01-0.05)"
  evergreen_share: "effectively 0% — deprioritized after ~28-30 days"
traffic_mix:
  shorts: 85
  browse: 6
  search: 5
  suggested: 2
  external: 2
---

# Shorts-First Channel

> Fastest audience growth on the platform, worst revenue per view on the platform. Both are
> the same fact.

---

## 1. Channel DNA

A Shorts-first channel is the platform's **fastest subscriber-acquisition machine and its worst
revenue-per-view business**, and the two facts are inseparable: Shorts are 75% of platform views
(`benchmarks.md` §3), which is why reach is cheap, and long-form RPM runs **10–100× Shorts RPM**
(`benchmarks.md` §9), which is why that reach is nearly worthless on its own. Ranking is by
**completion, not clicks** — CTR plays essentially no role — so packaging discipline moves
entirely into the first 1–3 seconds (`benchmarks.md` §8). The structural problem is that
**nothing compounds**: Shorts are deprioritized after roughly 28–30 days (`benchmarks.md` §5,
§8), so there is no back catalog earning in the background, no annuity, and a publishing break
costs 2–3 weeks of rebuilding momentum immediately (`benchmarks.md` §4) — this archetype is the
one where a pause is most expensive because there is no inventory to carry you. Nor do the
subscribers transfer: **long-form audience overlap is only ~10% and related-video link
conversion is under 1%** (`benchmarks.md` §8), so a 200,000-subscriber Shorts channel does not
have a 200,000-person long-form audience, it has roughly 20,000 people who might watch one. The
characteristic trap follows directly: **mistaking subscriber count for a business**. The number
climbs faster than in any other archetype and buys less, and the only way it converts into
revenue is off-platform — which is why the monetization axis is product-funnel-primary despite
the format being pure entertainment.

---

## 2. Content Mix

| Type | Share | Purpose |
|---|---|---|
| **Hub** (the repeatable format that defines the channel) | 55–65% | The feed learns one recognizable pattern and serves it. Volume lives here. |
| **Help** (fast, useful, saveable) | 20–30% | Saves and shares rank above likes (`benchmarks.md` §5); this is also the only search-visible content. |
| **Hero** (high-effort swings for reach) | 10–15% | One breakout can multiply the channel. Budget for a low hit rate. |

**Evergreen vs trending:** effectively 0% evergreen in distribution terms. A Short can be
timeless in content and still be dead in 30 days. **Plan the calendar as a treadmill, not a
library.**

**Repost with intent, not by default.** The Jul 2025 "Inauthentic content" policy
(`benchmarks.md` §5) makes low-effort re-uploads a monetization risk, not a growth hack.

---

## 3. Cadence & Length

| Setup | Long-form | Shorts | Notes |
|---|---|---|---|
| Solo | 0–1/week (optional) | 7/week (1/day) | Daily is the floor, not the goal; batch 7–10 in one session |
| Small team (2–3) | 1/week | 14/week (2/day) | Two per day is the practical ceiling before quality collapses |

**Optimal length:** 15–60 seconds, bimodal with peaks at ~13s and ~60s. **Avoid the 30–45s dead
zone** (`benchmarks.md` §8). Max length is 3 minutes since Oct 2024 (`benchmarks.md` §5) but
longer runtimes lower completion rate, which is the ranking signal.

**Mid-roll does not apply.** There is no 8-minute threshold in this format; the ~50% mid-roll
revenue increase (`benchmarks.md` §3) is one of the things a Shorts-first channel gives up.

**Pattern interrupts every 2–3 seconds**, versus every 30 seconds in long-form
(`benchmarks.md` §2). Visual change every 3 seconds (`benchmarks.md` §8).

**Notification cap:** max 3 per user per 24 hours (`benchmarks.md` §4) — posting 4+ times a day
does not reach subscribers proportionally.

---

## 4. Title Patterns

1. `[SURPRISING CLAIM] in [NUMBER] Seconds`
2. `Nobody Does [COMMON TASK] Like This`
3. `[NUMBER] [THINGS] You've Been Doing Wrong`
4. `Watch What Happens to [OBJECT]`
5. `Why [THING] Is Actually [OPPOSITE]`
6. `The [ADJECTIVE] Way to [DO THING]`
7. `[ROLE] Reacts to [SITUATION]`
8. `Stop Doing [BEHAVIOR]`
9. `[THING] vs [THING] — Instantly`
10. `This Is Why [OUTCOME] Keeps Happening`

**Length rule:** Shorts-feed archetype, so the title is barely a discovery lever at all — it
truncates at roughly **40 characters** and 4–6 words is optimal (`benchmarks.md` §8). Hashtags:
1–5, 60 characters total for Shorts (`benchmarks.md` §6), the first 3 display above the title.
Description preview is the first 125 characters (`benchmarks.md` §8) — put the funnel link there,
because it is one of the few places a viewer can leave for. **Non-English channel:** the ten formulas are structural examples only — re-derive the wording, and the hashtag convention with it, from what performs in that language's Shorts feed rather than translating the English (`references/localization-guide.md` §5).

---

## 5. Thumbnail Formula

**This section works differently from every other archetype.** In-feed, **the first frame IS the
thumbnail** — the viewer never sees a custom image before the video plays, and Test & Compare is
**not available for Shorts** (`benchmarks.md` §7). A custom thumbnail only appears on the channel
page grid and in search results, so it is a browse-and-catalog asset, not a discovery one.

**The first frame (the real thumbnail):**
- Must contain motion or an unresolved state within the first 1–3 seconds
  (`benchmarks.md` §8) — a static opening frame reads as a paused video and gets swiped.
- Subject centered and large; the vertical 1080 × 1920 frame is close-up territory
  (`benchmarks.md` §8).
- No opening title card. It spends the entire hook window saying nothing.
- Any on-screen text must be readable in under one second (`benchmarks.md` §7) and clear of the
  UI overlays along the bottom and right edges.

**The custom thumbnail (channel page and search only):**
- Text ≤5 words, 3 ideal (`benchmarks.md` §7); 2–3 colors, exactly one focal point, 30–40%
  negative space. 1280 × 720 minimum, 16:9, under 2 MB.
- Its job is to make the channel grid look like one coherent show.

**Target metric instead of CTR:** Viewed vs Swiped Away — **75%+ is good, below 60% means
rewrite the hook now** (`benchmarks.md` §8). Never diagnose a Short with CTR.

---

## 6. Hook Style

**Primary — Shock/Contradiction.** State something that cannot be true, in the first second,
before any setup. The viewer's thumb is already moving; you are interrupting it.
> "This is the wrong way to do it — and it's the way everyone was taught."

**Secondary — Demonstration.** Start mid-action with the outcome already visibly in progress,
so the viewer stays to see it resolve.
> [Frame 1: the thing already failing/transforming on screen, no words yet.]

**Timing:** the hook window is the **first 1–3 seconds** (`benchmarks.md` §8), not 15. A pattern
interrupt in the first 5 seconds is worth +23% retention in long-form (`benchmarks.md` §2); in
Shorts the equivalent interrupt has to be at second one. Open loops matter — the suspension
bridge shape correlates with 68% higher completion (`benchmarks.md` §2) and completion is the
entire ranking signal here.

Full taxonomy in `references/hook-library.md`.

---

## 7. Monetization Stack

> All figures are **US baseline**. Apply `references/localization-guide.md` before quoting
> revenue for a non-US channel.

| Rank | Stream | Why This Position |
|---|---|---|
| 1 | External funnels | The only stream whose value is set by the audience rather than by Shorts economics. Requires no YPP threshold, and it is the only way a large Shorts audience becomes income |
| 2 | Brand deals | Buyers pay for reach and this archetype has reach; floor $1,000+ (`benchmarks.md` §9). Per-view rates are low, so sell audience size and format fit, not CPM |
| 3 | Shorts ad share | Ranked far higher than in any other archetype because it is the format's own revenue — but still only $0.01–0.07 per 1K views typical (`benchmarks.md` §9). Note Oct 2025: Shorts reported to earn more per watch hour than in-stream ads in the US (`benchmarks.md` §5) — per watch *hour*, not per view |
| 4 | Memberships | Reachable via the Shorts YPP path (3M Shorts views/90 days at 500 subs, `benchmarks.md` §9), but a swipe-feed audience is weakly attached; 1% conversion will run low |
| 5 | Shopping affiliate | Fits demo-and-product formats well; 5–20% commission, 30-day attribution (`benchmarks.md` §9) |
| 6 | AdSense (long-form) | Only exists if the channel also publishes long-form — and with ~10% audience overlap (`benchmarks.md` §8), that long-form starts nearly cold |
| 7 | Super Chat / Thanks | Near-zero. The format is not live and builds almost no parasocial attachment |

**Music tax.** Every licensed track splits the revenue pool: no music = 100% of the creator
share, 1 track = 50%, 2 tracks = 33% (`benchmarks.md` §8). At Shorts RPM, halving the share is
the difference between negligible and nothing.

**The YPP path is different here.** Expanded YPP: 500 subs + 3M Shorts views/90 days. Full YPP:
1,000 subs + 10M Shorts views/90 days (`benchmarks.md` §9) — versus 4,000 watch hours for
long-form. Fast to reach, and worth much less on arrival.

---

## 8. Growth Trajectory

| Tier | What Changes | Key Lever | Revenue Character |
|---|---|---|---|
| 0–500 | Reach arrives quickly and means very little; the tier goes to finding a format that repeats rather than a video that worked | Find one repeatable format; publish daily; kill anything below 60% viewed-vs-swiped | None — not yet monetized |
| 500–1K | Expanded YPP becomes reachable at 500 subscribers via the 3M-Shorts-views path (`benchmarks.md` §9); the off-platform capture matters more than the unlock does | Open an off-platform capture immediately — the feed does not hand over an audience, it rents one | Audience-direct only, and immaterial at this size |
| 1K–10K | Full YPP at 1,000 subscribers via the 10M-Shorts-views path (`benchmarks.md` §9); the channel now discovers how little Shorts reach converts — long-form RPM runs 10–100× Shorts RPM (`benchmarks.md` §9) | Double down on the one format that repeats instead of chasing whatever spiked last | First ad revenue, and structurally the lowest per view of any archetype |
| 10K–50K | Reach is large enough to sell, but only once it has been converted into something durable — a list, a product, or long-form | Convert reach into a list or a product; reach alone does not pay | Meaningful but not replacement income at Shorts RPM; brand deals at the floor (`benchmarks.md` §9) do more than ads |
| 50K–100K+ | The audience is the asset and the catalog is not — old Shorts do not compound the way a long-form catalog does | Diversify off the feed entirely | Can reach replacement income, but almost never from Shorts ad revenue alone |

The fastest audience curve and the flattest revenue curve on the matrix: a Shorts-first channel can reach a very large
audience and still earn less than a small niche-authority channel, which is exactly why audience size cannot be used as a
revenue proxy in this archetype.

> ⚠️ Tier progression is not a timeline. `benchmarks.md` §11 lists growth-timeline and revenue-by-tier as known gaps — no verified data exists. Any revenue figure must be modeled from the creator's own audience size and geography via `references/localization-guide.md`, never read off a table.

---

## 9. Failure Modes

**Subscribers with nowhere to go.** The count climbs, the RPM stays at $0.01–0.07 per 1K
(`benchmarks.md` §9), and the creator waits for it to convert into something. It doesn't: the
long-form overlap is ~10% and related-link conversion is under 1% (`benchmarks.md` §8).
**Fix:** ship one off-platform destination this week and put the link in the first 125 characters
of every description (`benchmarks.md` §8), plus a spoken or on-screen call at second 8–12 of
every fourth Short. Measure list additions per 100K views, not subscribers.

**The pause.** A week off, a holiday, a burnout gap. Because Shorts are deprioritized after
~28–30 days (`benchmarks.md` §5), there is no inventory still working, and the restart costs 2–3
weeks of rebuilding momentum (`benchmarks.md` §4) on top of the gap itself.
**Fix:** maintain a 14-Short buffer at all times and treat it as a hard floor — when the buffer
drops below 7, the next work session is a batch-record session and nothing else. Schedule the
buffer to publish through any planned break.

**Scoring everything with licensed music.** Tracks are added by habit for polish. Each one halves
or thirds the revenue pool — 1 track = 50%, 2 tracks = 33% (`benchmarks.md` §8) — and Content ID
music can block Shorts longer than 1–3 minutes in some territories.
**Fix:** audit the last 30 Shorts, count how many carry two or more licensed tracks, and switch
the default to no music or a single cleared track. Reserve licensed music for videos where the
track is the actual premise.
