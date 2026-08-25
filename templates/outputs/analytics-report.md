# Analytics Report — `{SCOPE}` · `{DATE_RANGE}`

> Fill in OUTPUT LANGUAGE. Section headings may be translated.

**Channel:** `{CHANNEL_NAME}` · `{TIER}` · `{PRIMARY_ARCHETYPE}` · `{MARKET}`
**Data source:** `{ANALYTICS_API / STUDIO_EXPORT / SCREENSHOT / PASTED}`

**Every observation below terminates in an action.** An observation with no action is deleted,
not kept as a note.

## 1. Data availability — read this first

| What we have | Granularity | What's missing | Blocks | What would resolve it |
|---|---|---|---|---|
| `{METRIC}` | `{DAILY/TOTAL}` | `{METRIC}` | `{WHICH_ANALYSIS}` | `{EXACT_STUDIO_SCREEN_OR_EXPORT}` |
| | | | | |
| | | | | |

**Confidence in this report:** `{HIGH / MEDIUM / LOW}` — because `{REASON}`.
Anything blocked above is marked `insufficient data` below, never inferred.

## 2. Diagnostic matrix

| Impressions | CTR | AVD | Diagnosis (`benchmarks.md` §10) | Observed here | Action |
|---|---|---|---|---|---|
| `{LOW/OK/HIGH}` | `{LOW/OK/HIGH}` | `{LOW/OK/HIGH}` | `{DIAGNOSIS}` | `{YES/NO}` | `{ACTION}` |
| | | | | | |
| | | | | | |

**Primary diagnosis:** `{THE_ONE_THAT_FITS}` — evidence: `{NUMBERS}`.

## 3. Retention curve

| Feature | Where | Cause | Fix | Applies to |
|---|---|---|---|---|
| `{DROP / PLATEAU / SPIKE / SLOW_BLEED}` | `{MM:SS}` | `{CAUSE}` | `{SPECIFIC_FIX}` | `{THIS_VIDEO / ALL_FUTURE}` |
| | | | | |
| | | | | |

| Checkpoint | Observed | Benchmark (`benchmarks.md` §2) | Verdict |
|---|---|---|---|
| 30-second retention | `{X}%` | `{BENCH}` | `{PASS/FAIL}` |
| 60-second retention | `{X}%` | `{BENCH}` | `{PASS/FAIL}` |
| AVD / average % viewed | `{X}%` | archetype target `{X}%` | `{PASS/FAIL}` |
| Curve shape | `{SHAPE}` | §2 Retention curve shapes | `{HEALTHY/UNHEALTHY}` |

## 4. Baseline comparison — against this channel's own median

Never compared to other channels. The channel's own median is the only fair baseline.

| Metric | This period | Channel median | Delta | Direction |
|---|---|---|---|---|
| Views per video | `{N}` | `{N}` | `{±%}` | `{↑/↓/FLAT}` |
| CTR | `{X}%` | `{X}%` | `{±pp}` | `{↑/↓}` |
| AVD | `{X}%` | `{X}%` | `{±pp}` | `{↑/↓}` |
| Subs per video | `{N}` | `{N}` | `{±%}` | `{↑/↓}` |
| Comments per 1k views | `{N}` | `{N}` | `{±%}` | `{↑/↓}` |

**Is the change real or noise?** `{ASSESSMENT}` — sample size `{N}` videos.

## 5. Traffic-source health

| Source | Share | Prior period | Archetype expectation | Verdict | Action |
|---|---|---|---|---|---|
| Search | `{X}%` | `{X}%` | `{X}%` | `{VERDICT}` | `{ACTION}` |
| Suggested | | | | | |
| Browse | | | | | |
| Shorts feed | | | | | |
| External | | | | | |

**Impressions funnel** (`benchmarks.md` §10): impressions `{N}` → clicks `{N}` (`{X}%`) →
watch time `{N}`h. Where it leaks: `{STAGE}` → action: `{ACTION}`.

## 6. Outliers

| Video | Views vs median | CTR | AVD | Traffic source | What made it different |
|---|---|---|---|---|---|
| `{TITLE}` | `{X}×` | `{X}%` | `{X}%` | `{SOURCE}` | `{FACTOR}` |
| | | | | | |
| `{TITLE}` (under) | `{X}×` | | | | |

**What the over-performers share:** `{PATTERN}` → **repeat by** `{ACTION}`
**What the under-performers share:** `{PATTERN}` → **stop by** `{ACTION}`
**Is the pattern real?** `{N}` of `{N}` outliers show it — `{CONVINCING / COINCIDENCE}`.

## 7. Prioritized changes — impact over effort

| # | Change | Fixes which observation | Impact | Effort | Ratio | Measure by | Recheck |
|---|---|---|---|---|---|---|---|
| 1 | `{CHANGE}` | `{§N}` | `{H/M/L}` | `{H/M/L}` | `{SCORE}` | `{METRIC}` | `{DATE}` |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

**Change nothing about:** `{WHAT_IS_WORKING}` — `{WHY}`.
**Next review:** `{DATE}`, after `{N}` more uploads.

## Self-check

- [ ] Data-availability table comes first and names what would resolve each gap
- [ ] Every benchmark cited traces to `benchmarks.md` (§1, §2, §4, §10) with the section noted
- [ ] Comparisons use the channel's own median, never another channel's numbers
- [ ] Retention features each terminate in feature → cause → fix
- [ ] Traffic mix compared against the archetype's expected mix, not a generic one
- [ ] Outlier patterns tested against sample size — coincidence called out as coincidence
- [ ] Every observation in every section has a corresponding row in §7
- [ ] Changes ordered by impact-over-effort, each with a metric and a recheck date
- [ ] Missing data marked `insufficient data` — never filled with an estimate
- [ ] What is working is explicitly protected from change
