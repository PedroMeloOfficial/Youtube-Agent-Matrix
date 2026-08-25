---
archetype: tutorial
display_name: Tutorial
axes:
  traffic: [search]
  intent: solve-a-problem
  format: [tutorial]
  monetization: adsense-primary
  production: [solo, small-team]
benchmarks:
  ctr_target: "search traffic runs ~12.5%; 4–6% blended is average"
  retention_target: "40%+ AVD (ahead of ~83% of channels)"
  length_min: 7
  length_max: 15
  cadence_solo: "2/week (8-10/month)"
  cadence_team: "3/week (12+/month)"
  shorts_per_week: "2-3"
  rpm_range_usd: "8-14 DIY/home · 6-12 consumer tech · 15-25 B2B software"
  evergreen_share: "85%+"
traffic_mix:
  search: 55
  suggested: 20
  browse: 15
  shorts: 10
---

# Tutorial Channel

> The most search-driven archetype on the platform. Someone typed a problem. This video is
> the answer.

---

## 1. Channel DNA

A tutorial channel is a **query-answering machine**, and it is the archetype where the back
catalog compounds hardest — search sends 12.5% CTR because the viewer already has intent
(`benchmarks.md` §1), and that intent does not expire when the video does, so a two-year-old
walkthrough of a still-current process keeps converting impressions at a rate no browse-fed
video ever reaches. The format's defining tension is that **the viewer wants to leave**: the
moment their problem is solved, staying is irrational, which means retention here fights the
purpose of the format rather than serving it. That inverts several standard tactics — you show
the finished result inside the first 15 seconds instead of withholding it, because a viewer who
does not believe you can solve their problem leaves at 10 seconds and one who does believe you
stays for the whole procedure. Chapter structure is load-bearing rather than cosmetic: chapters
add ~4% AVD (`benchmarks.md` §6) and, more importantly, they let a returning viewer re-enter
at step 4 instead of abandoning, which converts a one-time visit into repeat viewing — the
second-ranked satisfaction signal (`benchmarks.md` §5). Revenue swings widely by subject rather
than by skill: the same production quality earns $6–12 RPM on consumer tech and $15–25 on B2B
software (`benchmarks.md` §9), so subject choice is a monetization decision made before the
first upload. The characteristic trap is **tool sprawl** — the creator follows their own
curiosity across five unrelated tools, YouTube's search ranking never establishes the channel
as the authority on any single one, and a back catalog that should have compounded stays a pile
of unrelated one-offs instead.

---

## 2. Content Mix

| Type | Share | Purpose |
|---|---|---|
| **Help** (single-problem walkthroughs) | 65–70% | The compounding base. One query, one video, one solution. |
| **Hub** (multi-part series, full builds) | 20–25% | Turns single visits into sessions and playlists. |
| **Hero** (definitive complete guide) | 10% | The tentpole that ranks for the broad head term. 1–2 per year. |

**Evergreen vs trending:** 85%+ evergreen — the highest evergreen share of any archetype.
Trending is only worth chasing when a tool ships a major version, and even then the value is
that the video becomes evergreen for the *new* version.

**Version decay is the tax on this archetype.** A tutorial dies not when interest fades but when
the interface changes. Audit the top 10 performers quarterly; a re-record of a decayed
top-performer is worth more than a new video on an untested topic.

---

## 3. Cadence & Length

| Setup | Long-form | Shorts | Notes |
|---|---|---|---|
| Solo | 2/week (8–10/month) | 2–3/week | Batch by tool — one setup, one screen-capture session, several videos |
| Small team (2–3) | 3/week (12+/month) | 3–5/week | Clears the 12+/month threshold: 8× view growth, 3× subscriber growth (`benchmarks.md` §4) |

**Optimal length:** 7–15 minutes (`benchmarks.md` §3). Length must be dictated by the procedure,
not the ad threshold — a 4-minute fix padded to 8:00 produces the mid-video valley described in
`benchmarks.md` §2 and costs more in suggested-traffic ranking than the mid-roll earns.

**Mid-roll:** clearing 8:00 unlocks mid-rolls for roughly a 50% revenue increase
(`benchmarks.md` §3). Where a procedure genuinely runs long, place the break at a natural step
boundary, never mid-step — a viewer interrupted while following along abandons.

**Shorts:** the single highest-value Shorts use in this archetype is the isolated 20-second fix
lifted from a long-form video. It ranks on completion, not clicks (`benchmarks.md` §8), and a
single-step fix completes.

---

## 4. Title Patterns

1. `How to [SPECIFIC ACTION] in [TOOL] — Step by Step`
2. `[TOOL] Tutorial for Beginners: [OUTCOME] in [TIMEFRAME]`
3. `[SPECIFIC ERROR OR PROBLEM]? Here's the Fix ([TOOL] [YEAR])`
4. `The Fastest Way to [OUTCOME] in [TOOL]`
5. `Complete [TOOL] Guide — Beginner to [LEVEL] in [N] Minutes`
6. `[NUMBER] [TOOL] Features You're Not Using (But Should Be)`
7. `How I [BUILT/MADE] [PROJECT] in [TOOL] — Full Walkthrough`
8. `Stop Doing [COMMON WRONG METHOD] — Do [CORRECT METHOD] Instead`
9. `[TOOL A] to [TOOL B]: How to Migrate Without Losing [THING AT RISK]`
10. `[TASK] in [TOOL], Explained Properly ([YEAR] Update)`

**Length rule:** search-dominant archetype, so run 60–70 characters — longer titles carry more
matchable terms and this is exactly the traffic type the 70–100-character finding was drawn from
(`benchmarks.md` §6). The tool name and the action verb must both sit inside the first 40–50
characters, because that is all mobile shows. Add the year only for software whose interface
changes; on a physical-skill tutorial a year tag ages the video for no benefit. **Non-English channel:** the formulas are English syntax and must be re-derived, not translated — the tool name is often kept in English while the action verb is local, and only the target language's own autocomplete will tell you which (`references/localization-guide.md` §5).

---

## 5. Thumbnail Formula

- **Face:** optional and small. When used, place it in a corner with a satisfied or relieved
  expression — faces lift CTR 20–30% (`benchmarks.md` §7), but the UI or the result must remain
  the focal point.
- **Text:** ≤5 words, 3 ideal (`benchmarks.md` §7). This archetype *prefers* the tight end, 2–3 words — the
  outcome state, not the process. `FIXED`, `IN 5 MIN`, `NO CODE`.
- **Colors:** 2–3 primaries. Borrow the tool's brand color as the accent against a dark or
  neutral field so the subject is recognizable at thumbnail scale.
- **Composition:** exactly one focal point (`benchmarks.md` §7), 30–40% negative space. The
  before/after split is the strongest layout in this archetype — broken state on the left,
  working state on the right — because it states the promise without text. A cropped, enlarged
  UI region with a single arrow beats a full uncropped screenshot every time.
- **Avoid:** full-resolution screenshots (unreadable at 70%+ mobile viewing), more than one
  arrow, menu paths, code that has to be read, exaggerated shock faces — they contradict the
  competence the viewer is shopping for.
- **Target CTR:** 5–7% blended is strong here; the search share of impressions pulls the
  channel average up toward the 12.5% search figure (`benchmarks.md` §1).

---

## 6. Hook Style

**Primary — Demonstration.** Show the finished result in the first 10 seconds. The viewer is
deciding whether you can actually do the thing; proof beats promise, and 20% of viewers are lost
in the first 10 seconds (`benchmarks.md` §2).
> "That's the finished version. It took four minutes. Here's every step."

**Secondary — Problem–Agitation.** Name the exact failure state the viewer arrived with, in
their words, then cut to the fix.
> "You clicked export and got this error. Every answer online tells you to reinstall. You don't
> need to."

**Timing:** state the value proposition within 15 seconds (+18% retention at the 1-minute mark,
`benchmarks.md` §2), then start the procedure immediately — no channel intro, no history of the
tool, no request to subscribe before the problem is solved. Ask for the subscribe at the moment
the result works, not before.

Full taxonomy in `references/hook-library.md`.

---

## 7. Monetization Stack

> All figures are **US baseline**. Apply `references/localization-guide.md` before quoting
> revenue for a non-US channel.

| Rank | Stream | Why This Position |
|---|---|---|
| 1 | AdSense | Search traffic never stops arriving; the catalog earns while the creator sleeps, and mid-rolls are natural at 7–15 min |
| 2 | Shopping affiliate | Every tutorial names a tool, part or material — 5–20% commission, 30-day attribution (`benchmarks.md` §9) — and the recommendation is already implicit |
| 3 | External funnels | A paid course is the same product the channel gives away in pieces; the free tutorials are the proof of teaching ability |
| 4 | Brand deals | Tool vendors pay for demonstrated competence, but the audience is transient and sponsor recall is weak |
| 5 | Memberships | Only converts when the channel offers something the tutorials structurally cannot — support, templates, project files |
| 6 | Super Chat / Thanks | Near-zero. Nobody tips a solved problem; the format is neither live nor parasocial |
| 7 | Shorts ad share | Reach instrument, not revenue — long-form RPM runs 10–100× Shorts RPM (`benchmarks.md` §9) |

---

## 8. Growth Trajectory

| Tier | What Changes | Key Lever | Revenue Character |
|---|---|---|---|
| 0–500 | Nothing ranks yet; the tier exists to build enough coverage of one tool or skill that search has something to choose from | 30+ videos against real queries in ONE tool or skill | None — not yet monetized |
| 500–1K | Expanded YPP at 500 subscribers (`benchmarks.md` §9) opens audience-direct streams, and early videos begin appearing for low-competition queries | Playlists per tool, so one fix leads naturally into the next | Audience-direct only, and immaterial at this size |
| 1K–10K | Full YPP at 1,000 subscribers (`benchmarks.md` §9); search ranking is established and the catalog starts compounding — old fixes keep earning | Complete-guide heroes that own the broad query, supported underneath by the specific ones | First ad revenue, sized by subject — tutorial subjects span several RPM bands on the niche table (`benchmarks.md` §9) |
| 10K–50K | Tool vendors become sponsors, because the audience is people actively using their product | Series and complete-guide heroes; first tool-vendor sponsorships at the brand-deal floor (`benchmarks.md` §9) | Meaningful but not replacement income; unusually steady, because search traffic neither spikes nor vanishes |
| 50K–100K+ | The catalog is an acquisition channel for a course or template product rather than an ad property | Course or template funnel built on top of the catalog | Replacement-income territory, reached at a smaller audience for high-RPM subjects than for low-RPM ones |

Tutorial progression depends far more on query volume and competitor quality in the chosen subject than on anything the
creator controls — the same effort in a saturated tooling niche and in an underserved one produce very different results,
so no single progression describes the archetype.

> ⚠️ Tier progression is not a timeline. `benchmarks.md` §11 lists growth-timeline and revenue-by-tier as known gaps — no verified data exists. Any revenue figure must be modeled from the creator's own audience size and geography via `references/localization-guide.md`, never read off a table.

---

## 9. Failure Modes

**Tool sprawl.** The channel covers five unrelated tools because the creator was curious about
each. Search never establishes it as the authority on any of them, suggested traffic has nothing
to chain to, and the catalog never compounds.
**Fix:** pick one tool or skill and commit the next 20 videos to it exclusively. Move the
off-topic ideas to a written backlog with a date no earlier than 20 videos out.

**Padding to the mid-roll threshold.** A 5-minute procedure is stretched to 8:00 with intro,
context and recap. The mid-roll unlocks, retention drops into a mid-video valley, and the
algorithm stops surfacing the video to the audience it earned.
**Fix:** cut every second before the first real step. If the procedure still cannot honestly
reach 8:00, publish it short and combine three related short fixes into one 12-minute compilation
that earns the mid-roll legitimately.

**Silent version decay.** The top-performing video demonstrates an interface that no longer
exists. Comments fill with "this menu is gone," retention collapses, and the ranking it took a
year to earn is handed to a competitor.
**Fix:** put a quarterly calendar block on auditing the top 10 by views. Any video whose subject
has shipped a major version since publication gets re-recorded and re-uploaded as a new video
that same month, with the old one end-screened to it.
