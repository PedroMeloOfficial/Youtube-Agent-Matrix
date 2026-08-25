---
archetype: livestream
display_name: Livestream
axes:
  traffic: [subscriptions]
  intent: follow-a-person
  format: [livestream]
  monetization: audience-direct-primary
  production: [solo, small-team]
benchmarks:
  ctr_target: "unavailable — live streaming benchmarks are a documented gap (benchmarks §11); diagnose VOD and clips against the traffic-source table (benchmarks §1)"
  retention_target: "unavailable — no published live retention benchmark (benchmarks §11); track concurrent viewers and average session length instead"
  length_min: unavailable
  length_max: unavailable
  cadence_solo: "3-5 sessions/week at a fixed start time"
  cadence_team: "5-7 sessions/week, plus 2-3 edited VOD uploads"
  shorts_per_week: "5-7 (cut from stream VODs)"
  rpm_range_usd: "unavailable for live — no live-specific RPM is published (benchmarks §11); VOD follows the niche table (benchmarks §9)"
  evergreen_share: "under 20%"
traffic_mix:
  subscriptions: 45
  shorts: 20
  browse: 15
  suggested: 15
  search: 5
---

# Livestream Channel

> Revenue comes from a small number of people who show up, not from a large number who scroll
> past. Everything about this archetype follows from that.

---

## 1. Channel DNA

Livestream channels are the clearest case of **depth beating reach**. The monetization stack
inverts completely against every other archetype: memberships and Super Chat/Thanks sit at the
top and AdSense drops to third, because income scales with how much a committed minority values
being present rather than with how many strangers were served an impression. A mid-size channel
sees $50–500/month in Super Chat alone and membership conversion of around 1% is considered
meaningful (`benchmarks.md` §9) — which sounds bleak until you notice that 1% of a live audience
paying monthly outearns the AdSense on views the same channel could never have reached. The
algorithmic consequence is harsh: **live discovers badly**. A stream is unfinished while it is
running, has no retention curve to evaluate, no thumbnail history, and nothing for the browse
ranker to rank, so almost all live viewers are people who already subscribed and were notified.
Discovery therefore has to be manufactured after the fact by chopping VODs into clips and
Shorts — that is where new people come from, not from the stream itself. **Schedule reliability
matters more than content quality** here than in any other archetype, because appointment
viewing is the product; a merely fine stream at the usual time beats an excellent one nobody
knew about. Moderation is a production requirement, not an afterthought: chat is the show's
second channel and an unmoderated one drives away exactly the paying minority the economics
depend on. The trap is that streaming hours *feel* like work — four hours live is genuinely
exhausting — while producing almost nothing discoverable, so a creator can stream 20 hours a
week for a year and have no growing catalog to show for it.

---

## 2. Content Mix

| Type | Share | Purpose |
|---|---|---|
| **Hub** (the regular scheduled stream) | 65–75% | The appointment. Same day, same time, same format. This *is* the channel. |
| **Help** (Q&A, requests, community sessions) | 15–20% | Direct interaction — the sessions that convert viewers into members. |
| **Hero** (marathons, milestones, collaborations, events) | 10–15% | The only live format that reliably reaches beyond the existing audience. 4–8 per year. |

**Evergreen vs trending:** under 20% evergreen. Live VOD decays fast and reruns rarely earn.
Accept it and plan for it — the evergreen layer of this archetype is the **edited output**
(clips, Shorts, highlight cuts), not the streams themselves. If you want a compounding catalog,
you have to build it out of the recordings deliberately.

---

## 3. Cadence & Length

| Setup | Long-form | Shorts | Notes |
|---|---|---|---|
| Solo | 3–5 live sessions/week + 1 edited VOD | 5–7/week | The edited upload is what keeps the channel alive on non-stream days |
| Small team (2–3) | 5–7 live sessions/week + 2–3 edited VODs | 8–12/week | A dedicated editor and a dedicated moderator, not one person doing both |

**Optimal length:** **unavailable.** No published benchmark covers live session length
(`benchmarks.md` §11 lists live streaming and premiere performance as a known gap). Do not
import the long-form length bands — they measure a different behaviour. The practical
constraints are your own stamina and a start time your audience can predict. Judge a session by
average concurrent viewers, chat messages per active viewer, and how many people return to the
next one.

**Mid-roll:** the 8:00 threshold (`benchmarks.md` §3) is irrelevant to a multi-hour stream —
you clear it immediately. Ad density on live is a trade against Super Chat and membership
conversion, which outrank AdSense here (§7), so err toward fewer breaks. The mid-roll decision
that actually matters is on the **edited VOD**, where the 8:00 minimum applies normally and the
~50% revenue increase is real.

**Pattern interrupts:** live runs at roughly every **2–3 minutes**, versus ~30 seconds for
pre-recorded long-form (`benchmarks.md` §2). Reading a chat message, changing activity, or
addressing an arrival all count.

---

## 4. Title Patterns

1. `[ACTIVITY] Until [CONDITION IS MET]`
2. `LIVE: [ACTIVITY] — Day [N]`
3. `[GOAL] or [CONSEQUENCE]`
4. `Answering Your [TOPIC] Questions Live`
5. `[ACTIVITY] With [COMMUNITY NAME]`
6. `Attempt [N] at [DIFFICULT GOAL]`
7. `[N]-Hour [ACTIVITY] Stream`
8. `Reacting Live to [EVENT]`
9. `First Time [DOING SOMETHING] — Live`
10. `[BEST MOMENT] — [ACTIVITY] Stream Highlights` *(VOD re-title, see below)*

**Length rule:** the dominant surface is the subscriptions feed and the notification, both of
which truncate hard, so keep live titles **under 50 characters** and front-load the activity and
the stake inside the first **40–50** (`benchmarks.md` §6). Note the notification cap of **3 per
user per 24 hours** (`benchmarks.md` §4) — a channel that streams daily and also uploads is
already spending that budget, so titles have to earn the notification they consume. **Non-English channel:** the formulas are structural only — the live-title conventions a target-language audience recognizes have to come from local channels streaming the same thing, not from a translation of the English (`references/localization-guide.md` §5).

**Re-title every VOD after the stream ends.** The live title sells a moment in time ("LIVE:
Day 4"); the VOD title has to sell the recording to someone who wasn't there, which is a
completely different promise. Same for the thumbnail. A VOD left with its live title and
auto-thumbnail is a dead asset.

---

## 5. Thumbnail Formula

This is the section where the conventional advice applies least. Most live viewers arrive from
a notification or the subscriptions feed, where the decision is "is my person on?" rather than
"is this thumbnail good" — so **thumbnail work barely moves live attendance**. It moves the VOD,
the clips, and the small share of browse traffic, which is where you should spend the effort.

- **Face:** yes, and expressive. Faces carry a **+20–30% CTR** lift (`benchmarks.md` §7), and the
  parasocial draw is the whole proposition of this archetype.
- **Text:** ≤5 words, 3 ideal (`benchmarks.md` §7). For live, the stake or the goal. For the VOD, the
  outcome — what actually happened.
- **Colors:** 2–3, and keep them fixed across the channel. Recognition in a crowded subscriptions
  feed is worth more than novelty per stream.
- **Composition:** 1 focal point, 30–40% negative space. A live-state marker (a consistent badge
  or colour bar) helps returning viewers distinguish live from VOD at a glance.
- **Avoid:** auto-generated stream frames, mid-blink captures, cluttered gameplay or screen-share
  captures with no subject, and re-using the live thumbnail on the VOD.
- **Target CTR:** **unavailable** for live (`benchmarks.md` §11). Judge VODs and clips against
  the traffic-source table (`benchmarks.md` §1) — browse 3.5%, suggested 9.5% — and judge live
  sessions by concurrents and returning-viewer rate instead.

---

## 6. Hook Style

Live has no single hook window, because **viewers arrive continuously throughout the stream**
rather than all at the start. The hook is therefore recurring rather than one-time: re-establish
what is happening and what is at stake roughly every 10–15 minutes, so someone who joins at
minute 90 gets the same orientation as someone who joined at minute 2.

**Primary — Stakes Framing.** Open the session, and each re-hook, on what could be won or lost
in this specific stream.
> "If this doesn't work in the next two hours, the whole run resets and we start from zero."

**Secondary — Direct Challenge.** Give the chat something to do that changes the stream.
> "Chat decides the next one. If you pick it, I have to finish it — no restarts."

**Timing:** the first 60 seconds of the *VOD* still obey normal rules — 55% of viewers are lost
in the first 60 seconds and 20% in the first 10 (`benchmarks.md` §2) — so the edited VOD must
open on the best moment, not on "hey everyone, let me get set up". Live pattern interrupts run
every 2–3 minutes (`benchmarks.md` §2).

Full taxonomy in `references/hook-library.md`.

---

## 7. Monetization Stack

> All figures are **US baseline**. Apply `references/localization-guide.md` before quoting
> revenue for a non-US channel.

**This ranking inverts the mainstream archetypes and that inversion is the point.** Reach-based
streams sit at the bottom; presence-based streams sit at the top.

| Rank | Stream | Why This Position |
|---|---|---|
| 1 | Memberships | Recurring, predictable, and the natural fit for appointment viewing: $0.99–$499.99/mo, 25 tiers available, YouTube takes 30%, and ~1% conversion is already meaningful (`benchmarks.md` §9) |
| 2 | Super Chat / Thanks | The format's native mechanic — paying to be seen in the moment. 70/30 split, $1–$500 per message, mid-size channels $50–500/mo (`benchmarks.md` §9) |
| 3 | AdSense | Demoted, not absent: hours of watch time generate real revenue, but ad density trades directly against the two streams above it |
| 4 | External funnels | Merch, Patreon and community platforms convert well against a parasocial audience; Patreon takes 10% plus payment fees (`benchmarks.md` §9) |
| 5 | Brand deals | Harder than for edited archetypes — no edit control, unpredictable runtime, and live reads cannot be re-cut if they go wrong. Real, but priced below the $1,000+ edited floor per equivalent reach |
| 6 | Shopping affiliate | Live product links work in the moment but the catalog earns nothing between streams; 5–20% commission (`benchmarks.md` §9) |
| 7 | Shorts ad share | The discovery engine and almost none of the income — long-form RPM runs 10–100× Shorts RPM (`benchmarks.md` §9). Judge Shorts here on reach, never on revenue |

Note that **Expanded YPP (500 subs) unlocks memberships and Super Chat/Thanks before full YPP
unlocks ad revenue** (`benchmarks.md` §9). For this archetype that means the top two income
streams arrive at 500 subscribers, not 1,000 — the earliest monetization of any archetype.

---

## 8. Growth Trajectory

| Tier | What Changes | Key Lever | Revenue Character |
|---|---|---|---|
| 0–500 | Reach is not the problem — the schedule is; the tier goes to proving the creator will show up whether or not anyone is watching | Fix the schedule and never miss it; stream to an empty room on purpose | None — not yet monetized |
| 500–1K | Expanded YPP at 500 subscribers (`benchmarks.md` §9) unlocks memberships and Super Chat, and this archetype monetizes them earlier and harder than any other | Turn memberships and Super Chat on the day they unlock — this is the primary stack, not a supplement to ads | First real income, and it comes from the audience rather than from advertising |
| 1K–10K | Full YPP at 1,000 subscribers (`benchmarks.md` §9) adds ads, but live content is structurally weak at discovery, so clips become the growth engine | Clip and Short every session; this is where new viewers actually come from | Meaningful but not replacement income; audience-direct still outweighs ads by a wide margin |
| 10K–50K | The community becomes a structure with roles rather than a chat — tiers, rituals and moderation are what make the income durable | Tiered memberships, community rituals, and a named moderator team | Can support part-time focus; income tracks how much a small group values access, not audience size |
| 50K–100K+ | Events, collaborations and off-platform community become viable, and brand deals reach the floor (`benchmarks.md` §9) | Events and an off-platform community the audience follows regardless of platform | Replacement-income territory, driven by audience-direct depth rather than by any RPM band |

This archetype earns earlier and smaller than the others, and depends far more on how much a small group values access
than on audience size — two channels of identical size can differ enormously here, which makes any size-to-income
mapping meaningless for livestreams.

> ⚠️ Tier progression is not a timeline. `benchmarks.md` §11 lists growth-timeline and revenue-by-tier as known gaps — no verified data exists. Any revenue figure must be modeled from the creator's own audience size and geography via `references/localization-guide.md`, never read off a table.

---

## 9. Failure Modes

**Hours streamed, nothing produced.** Twenty hours a week live, no clips, no edited VODs, no
Shorts. The work is real and exhausting and the channel has no discoverable surface, so growth
stops at whoever already found it and the back catalog is a wall of 4-hour recordings nobody
will ever start.
**Fix:** treat every stream as raw footage with a fixed deliverable attached — within 24 hours,
3 clips and 1 re-titled, re-thumbnailed VOD, or the stream doesn't count as done. Timestamp
moments live as they happen so the editor isn't scrubbing four hours to find them.

**Schedule drift.** Start times slide, sessions get skipped, the calendar becomes "whenever I
feel like it". Concurrents fall, and because the only reliable traffic source is the
subscriptions feed, there is no algorithmic floor to catch the channel — a publishing break
costs 2–3 weeks of momentum to rebuild (`benchmarks.md` §4).
**Fix:** commit to a smaller schedule you will actually hit — three fixed slots beats five
aspirational ones — publish those slots on the channel banner and in the Community tab, and go
live at that time even on a low-energy day rather than moving it.

**Chat left unmoderated.** The creator is busy performing and cannot read chat and moderate it
at once, so the tone is set by whoever is loudest. The engaged minority who would have paid
quietly leave, and they are exactly the top two revenue streams in §7.
**Fix:** before the next stream, appoint at least one moderator who is not the streamer, write a
three-line rule set into the channel description, and configure automated filters plus
slow-mode/members-only thresholds you can escalate to mid-stream without stopping the show.
