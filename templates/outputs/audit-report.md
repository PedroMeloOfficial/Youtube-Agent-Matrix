# Channel Audit — `{CHANNEL_NAME}` · `{DATE}`

> Fill in OUTPUT LANGUAGE. Section headings may be translated.

**Archetype:** `{PRIMARY}` (`{SECONDARY_OR_NONE}`) · **Tier:** `{TIER}` · **Market:** `{MARKET}`
**Sample:** `{N}` videos, `{DATE_RANGE}` · **Source:** `{STUDIO / PUBLIC / PASTED}`

## Overall score

**Overall: `{X}` / 100 — `{CRITICAL / WEAK / FUNCTIONAL / STRONG}`**

| Lens | Weight | Score | Band | One-line read |
|---|---|---|---|---|
| Packaging & SEO | `{%}` | `{X}` | `{BAND}` | `{READ}` |
| Performance | `{%}` | `{X}` | `{BAND}` | `{READ}` |
| Content & strategy | `{%}` | `{X}` | `{BAND}` | `{READ}` |
| Monetization | `{%}` | `{X}` | `{BAND}` | `{READ}` |

## ▶ The single highest-leverage fix

> ### `{THE_FIX_IN_ONE_SENTENCE}`
>
> **Why this one:** `{WHY_IT_OUTRANKS_EVERYTHING_ELSE}`
> **Evidence:** `{METRIC_AND_NUMBER}` vs `{BENCHMARK}` (`benchmarks.md` §`{N}`)
> **Effort:** `{HOURS}` · **Expected effect:** `{WHAT_MOVES}`
> **First action, today:** `{CONCRETE_STEP}`

Everything below is secondary to this.

## Lens 1 — Packaging & SEO

| Item | Observed | Benchmark (§1 / §6 / §7) | Verdict |
|---|---|---|---|
| CTR (channel median) | `{X}%` | `{BENCH}` | `{PASS/FAIL/NO DATA}` |
| Title length vs traffic source | `{X}` chars → `{SOURCE}` | §6 | `{VERDICT}` |
| Keyword inside first 40–50 chars | `{X}` of `{N}` | §6 | `{VERDICT}` |
| Thumbnail consistency | `{OBSERVATION}` | §7 | `{VERDICT}` |
| First 150 description chars used | `{X}` of `{N}` | §6 | `{VERDICT}` |
| Chapters present | `{X}` of `{N}` | §6 | `{VERDICT}` |

**Evidence:** `{SPECIFIC_VIDEOS_OR_PATTERNS}`

## Lens 2 — Performance

| Item | Observed | Benchmark (§1–§4) | Verdict |
|---|---|---|---|
| AVD / average % viewed | `{X}%` | `{BENCH}` | `{VERDICT}` |
| Retention at 30s | `{X}%` | §2 | `{VERDICT}` |
| Median views vs own baseline | `{X}` | — | `{VERDICT}` |
| Upload cadence | `{X}`/month | §4 | `{VERDICT}` |
| Traffic mix vs archetype | `{MIX}` | template frontmatter | `{VERDICT}` |
| Top `{N}` outliers | `{WHAT_THEY_SHARE}` | — | — |

**Evidence:** `{RETENTION_NUMBERS}`

## Lens 3 — Content & strategy

| Item | Observed | Verdict |
|---|---|---|
| Positioning legible from the last 10 uploads | `{YES/NO}` | `{VERDICT}` |
| Pillar balance vs target | `{DELTA}` | `{VERDICT}` |
| Evergreen share | `{X}%` vs `{TARGET}` | `{VERDICT}` |
| Series / recurring formats | `{N}` | `{VERDICT}` |
| Archetype failure modes present (template §9) | `{WHICH}` | `{VERDICT}` |

**Evidence:** `{EXAMPLES}`

## Lens 4 — Monetization

> Non-US market: adjusted per `references/localization-guide.md`. Applied: `{YES/NO}`

| Item | Observed | Benchmark (§9) | Verdict |
|---|---|---|---|
| YPP status | `{STATUS}` | §9 | `{VERDICT}` |
| Active revenue streams | `{LIST}` | template §7 | `{VERDICT}` |
| Mid-roll eligible uploads (8:00+) | `{X}` of `{N}` | §3 | `{VERDICT}` |
| Cheapest unexploited stream | `{STREAM}` | — | — |

## Insufficient data

| Missing | Blocks | What would resolve it |
|---|---|---|
| `{METRIC}` | `{LENS_ITEM}` | `{EXACT_STUDIO_SCREEN_OR_EXPORT}` |
| | | |

Any row here means the related score reads `insufficient data` — never an estimate.

## Prioritized actions — impact over effort

| # | Action | Lens | Impact | Effort | Ratio | Do by |
|---|---|---|---|---|---|---|
| 1 | `{ACTION}` | `{LENS}` | `{H/M/L}` | `{H/M/L}` | `{SCORE}` | `{DATE}` |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

**Explicitly not doing now:** `{DEPRIORITIZED}` — because `{REASON}`.

## Self-check

- [ ] Every number traces to `benchmarks.md` (§ noted) or is marked `insufficient data`
- [ ] Market adjustment applied before any revenue figure (`localization-guide.md`)
- [ ] Compared against the **archetype's** targets, not generic ones
- [ ] The highest-leverage fix is one sentence and names a first action
- [ ] Every verdict cites specific videos or numbers, never an impression
- [ ] Actions ordered by impact-over-effort with a ready first step
- [ ] Advice irrelevant to the size tier removed (`channel-types/_schema.md`)
- [ ] No score estimated where the underlying data is missing
