# Monetization Plan — `{CHANNEL_NAME}` · `{DATE}`

> Fill in OUTPUT LANGUAGE. Section headings may be translated.

**Archetype:** `{PRIMARY}` · **Tier:** `{TIER}` · **Market:** `{MARKET}` · **Localized:** `{YES/NO}`,
multiplier `{X}`. Every figure in `benchmarks.md` §9 is **US baseline** — none is quoted unadjusted.

## 1. YPP status and the shortest path

| Field | Value |
|---|---|
| Current status | `{NOT_ELIGIBLE / EXPANDED_YPP / FULL_YPP}` |
| Subscribers · watch hours (12mo) · Shorts views (90d) | `{N}` · `{N}` · `{N}` |
| Next threshold · gap to close | `{THRESHOLD}` (`benchmarks.md` §9) · `{GAP}` |

| Step to the next threshold | Action | Contributes | By when |
|---|---|---|---|
| 1 | `{ACTION}` | `{HOURS_OR_SUBS}` | `{DATE}` |
| 2 | | | |

**Arithmetic:** `{N}` videos × `{N}` views × `{MM:SS}` AVD = `{N}` h/month → threshold in `{N}` months.

## 2. Revenue stack — ranked for this archetype

| Rank | Stream | Status | Why this position here | Activation cost | Next action |
|---|---|---|---|---|---|
| 1 | `{STREAM}` | `{ACTIVE/DORMANT/UNAVAILABLE}` | `{REASON}` | `{COST}` | `{ACTION}` |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |

Rank order comes from the archetype template §7; every deviation is explained in the table.

## 3. Revenue projection — market-adjusted

> **Not a forecast.** Arithmetic on stated assumptions — change one and the number changes.

| Assumption | Value | Source |
|---|---|---|
| Monthly long-form views · monetized playback share | `{N}` · `{X}%` | `{CHANNEL_DATA}` |
| US baseline RPM for this niche | `${X}–${Y}` | `benchmarks.md` §9 |
| Market multiplier for `{MARKET}` | `{X}` | `localization-guide.md` |
| **Adjusted RPM** | `${X}–${Y}` | derived |
| Mid-roll eligible share (8:00+) | `{X}%` | `benchmarks.md` §3 |

```
{N} views × {X}% monetized = {N} monetized views
{N} / 1,000 × ${X} adjusted RPM = ${X}  (low)
{N} / 1,000 × ${Y} adjusted RPM = ${Y}  (high)
+ {STREAM}: {CALCULATION} = ${Z}
= ${LOW}–${HIGH} per month at current volume
```

| Scenario | Monthly | Annual | What has to be true |
|---|---|---|---|
| Current volume | `${X}` | `${X}` | nothing changes |
| Committed cadence | `${X}` | `${X}` | `{CONDITION}` |
| Next tier reached | `${X}` | `${X}` | `{CONDITION}` |

**Seasonality:** `{HIGH_AND_LOW_MONTHS}` (`benchmarks.md` §9 Seasonality).

## 4. Unexploited streams

| Stream | Why unexploited | Activation requirements | Realistic first revenue | Worth it? |
|---|---|---|---|---|
| `{STREAM}` | `{REASON}` | `{REQUIREMENTS}` | `{TIMELINE}` | `{YES/NO — WHY}` |

**Explicitly not pursuing:** `{STREAM}` — `{REASON}` (revisit at `{TIER_OR_CONDITION}`).

## 5. Sponsorship

| Field | Value |
|---|---|
| Average views per video (last `{N}`) | `{N}` |
| Rate range for this size and market | `${X}–${Y}` (`benchmarks.md` §9, adjusted `{X}`) |
| Integration types and pricing | `{PRE-ROLL / MID-ROLL / DEDICATED}` — `${X}` / `${Y}` / `${Z}` |
| Floor — never accept below · categories refused | `${X}` · `{CATEGORIES}` |

**Media kit contents**

- [ ] Channel one-liner and positioning sentence
- [ ] Audience: size, geography, age/gender split, top traffic sources
- [ ] Performance: median views, CTR, AVD — 90-day window
- [ ] Past integrations and results (or "first partnership available")
- [ ] Formats offered with pricing · turnaround, exclusivity, revisions
- [ ] Contact and preferred process

## 6. Disclosure obligations — `{MARKET}`

| Requirement | Applies when | How it is met | Source |
|---|---|---|---|
| Platform paid-promotion toggle | `{WHEN}` | `{HOW}` | `benchmarks.md` §9 |
| Verbal disclosure in video · written in description | `{WHEN}` | `{HOW}` | `{REGULATOR}` |
| Local market rule | `{WHEN}` | `{HOW}` | `localization-guide.md` |

Non-compliance risk: `{CONSEQUENCE}`.

## Self-check

- [ ] Every US baseline figure adjusted via `localization-guide.md` before being quoted
- [ ] Projection is labeled arithmetic on assumptions — never called a forecast
- [ ] Every assumption listed with a source; the calculation shown line by line
- [ ] YPP thresholds quoted exactly from `benchmarks.md` §9
- [ ] Stream ranking matches the archetype template §7, with deviations explained
- [ ] Sponsorship rates given as a range with a stated floor
- [ ] Disclosure obligations reflect the channel's actual market, not US rules by default
- [ ] No figure appears that is absent from `benchmarks.md` — unavailable is said, never estimated
