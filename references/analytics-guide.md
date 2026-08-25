# Analytics Guide

**Purpose.** How to read channel data and turn it into a single decision — the metric hierarchy, the impressions funnel, the arithmetic written out, a full diagnostic matrix, and a repeatable monthly review.

**Numbers live in `benchmarks.md`** — CTR bands are §1, retention shapes are §2, the metric hierarchy and channel-health thresholds are §10, RPM bands are §9, API limits are §10. §11 lists A/B significance thresholds and cold-start targets as **known gaps**: say unavailable rather than estimating.

**Contents:** 1 The metric hierarchy and why it ranks that way · 2 The impressions funnel · 3 The arithmetic · 4 Baselines: compare to the right thing · 5 The full diagnostic matrix · 6 Reading a retention curve, shape by shape · 7 Traffic-source health patterns · 8 Cohorts and returning viewers · 9 A/B testing at small scale · 10 The monthly channel review procedure · 11 Collecting data with no API access · 12 Vanity metrics and reporting hygiene · 13 Decision rules

## 1. The metric hierarchy and why it ranks that way

The ranked order is in `benchmarks.md` §10. The reasoning behind the order is what makes it usable:

| Rank | Metric | Why it sits here | What it cannot tell you |
|---|---|---|---|
| 1 | Watch time | It is the objective the system optimizes; every other metric is an input to it | Whether the watch time was *satisfying* |
| 2 | CTR | It gates whether distribution expands at all — an unclicked impression produces nothing | Whether the click was honest |
| 3 | AVD / retention | It determines whether distribution *keeps* expanding after the click | Anything about reach |
| 4 | Traffic sources | Tells you *which* of the three systems you are winning — what makes every other number interpretable | Absolute performance |
| 5 | Subscribers per video | A lagging trust indicator; useful for direction, too slow for diagnosis | Anything about a single video's fate |

**Rates vs totals.** CTR and AVD are *rates* — meaningful at low volume, and therefore the only honest signals for a small or cold-start channel. Watch time and subscribers are *totals* — meaningful only at volume, misleading below it.

**The order is a debugging order, not an importance order.** Diagnose down the funnel: impressions → CTR → retention → satisfaction → subscribers. Fixing downstream while upstream is broken produces no measurable change and burns a publishing cycle.

## 2. The impressions funnel

`Impressions ──CTR──▶ Views ──AVD──▶ Watch time ──satisfaction──▶ more impressions.` Each arrow is a multiplier and the loop is what makes early performance compound. Phase-by-phase CTR bands are in `benchmarks.md` §1 and §10.

| Phase | What is happening | Expected CTR behavior | Misread to avoid |
|---|---|---|---|
| Launch | Served to the warm core audience | Highest of the video's life (`benchmarks.md` §1) | Treating the launch number as the video's real CTR |
| Expansion | Impressions scale to colder viewers | Declines, by design | Panicking at a declining CTR |
| Sustained | Steady-state distribution | Settles into a band (`benchmarks.md` §10) | Comparing sustained CTR to launch CTR |

**Rule:** a falling CTR alongside rising impressions is healthy expansion. A falling CTR alongside *flat* impressions is a real problem.

## 3. The arithmetic

Written out because agents are asked to produce estimates and must not improvise formulas.

### Core identities

| Quantity | Formula |
|---|---|
| Views | `impressions × CTR` |
| CTR | `views from impressions ÷ impressions` |
| Watch time (minutes) | `views × average view duration in minutes` |
| AVD as a percentage | `average view duration ÷ video length` |
| RPM | `total revenue ÷ views × 1000` |
| Estimated revenue | `views ÷ 1000 × RPM` |
| Subscriber conversion | `subscribers gained ÷ views` |
| End-screen CTR | `end-screen clicks ÷ end-screen impressions` |

### Worked chain — from a view target backwards

For a target of `V` views on a browse-dominant video: (1) take the browse CTR expectation from `benchmarks.md` §1; (2) `impressions needed = V ÷ CTR`; (3) test plausibility — if that impression count is several times anything the channel has received, the target is a topic-demand problem, not a packaging one; (4) `projected watch time = V × (video length × target AVD)`, AVD target from `benchmarks.md` §2 or the archetype template; (5) `projected revenue = V ÷ 1000 × RPM`, band from `benchmarks.md` §9.

### Revenue estimation protocol

1. Take the RPM **band** from `benchmarks.md` §9 — never a point estimate.
2. **Non-US audience → apply `localization-guide.md` before quoting anything.** Unadjusted US RPM on an emerging market is wrong by an order of magnitude (`benchmarks.md` header).
3. Compute low and high ends separately and present a range.
4. Adjust down for videos below the mid-roll threshold (`benchmarks.md` §3); adjust for season if the window includes Q4 or January (`benchmarks.md` §9).
5. State the assumptions in one line alongside the number.

**Never** average an RPM band into a single figure. **Never** apply long-form RPM to Shorts views — separate bands, `benchmarks.md` §9.

### Sanity checks that catch most errors

| Check | Rule |
|---|---|
| RPM vs CPM | RPM must be lower than CPM. An RPM above CPM is arithmetically impossible. |
| AVD vs length | AVD in minutes can never exceed video length. |
| Retention percentages | Retention at a later timestamp cannot exceed retention at an earlier one. |
| Views vs impressions | Browse/suggested views cannot exceed impressions; external and direct views arrive without impressions. |
| Shorts vs long-form views | Do not compare view counts across the March-2025 counting change (`benchmarks.md` §8). |

## 4. Baselines: compare to the right thing

**The single most common analytics error is comparing a video to the wrong baseline.** Distribution decisions are made against a prediction derived from *this channel's* history, so that is the comparison that matters.

| Comparison | When it is valid | When it misleads |
|---|---|---|
| Video vs channel average (last 10–20 uploads) | Almost always — this is the default | Only if the channel recently changed format or cluster |
| Video vs channel average *within its own traffic source* | Best available comparison | Requires enough videos per source |
| Video vs a niche average | Setting a channel-level target | Diagnosing a single video — `benchmarks.md` §1 says to use the traffic-source table instead |
| This month vs last month | Only with equal upload counts | Any month with a break, a holiday, or an outlier video |
| This month vs the same month last year | Best for seasonality questions | Channels younger than ~18 months |

**Constructing the baseline:** take the last 10–20 uploads, exclude the top and bottom outlier, and compute the **median** (not mean) CTR, AVD and views — median resists one viral video distorting every later comparison. Recompute quarterly; a stale baseline makes every video look like a decline. **An outlier is not "the new normal"** — study it for packaging and topic lessons, exclude it from the baseline.

## 5. The full diagnostic matrix

The compact version is in `benchmarks.md` §10. This is the working version — four inputs, a diagnosis, and the specific next action. Read impressions, CTR and AVD against the channel baseline from §4, not against absolutes.

| Impressions | CTR | AVD | Dominant source | Diagnosis | Action |
|---|---|---|---|---|---|
| Low | — | — | any | Distribution never started: topic demand or layer-1 stall | Change topic selection. Packaging work is wasted here |
| Low | High | High | Search | Working but small: real query, low volume | Keep the format, target higher-volume adjacent queries |
| Low | High | High | Suggested | Strong satisfaction, no cold reach | Build session initiators (`algorithm-guide.md` §5) |
| Low | Low | — | any | Wrong topic *and* wrong packaging | Rebuild the idea; do not iterate on the title |
| High | Low | — | Browse | Packaging is the bottleneck | Thumbnail and title. Nothing else until CTR clears the tier in `benchmarks.md` §1 |
| High | Low | — | Suggested | Weak contextual fit to source videos | Retitle toward the source videos' language and topic |
| High | High | Low | any | Metadata mismatch — promise not paid | Rebuild the first minute, or retitle to what the video actually delivers |
| High | High | Mid | Browse | Healthy — expand it | Make more in this cluster; consider a series |
| High | Mid | High | Search | Ranking well, packaging soft | Title/thumbnail A/B test (§9) |
| Rising | Falling | Stable | any | Normal expansion to a colder audience | Do nothing. Continue monitoring |
| Falling | Stable | Stable | any | Freshness decay or seasonality | Compare year-over-year before acting |
| Falling | Falling | Falling | any | Real decline across the funnel | Full audit — start with cluster consistency (`algorithm-guide.md` §6) |
| High | High | High | External | Off-platform driven, not algorithmically endorsed | Diversify; external traffic builds no prediction prior |
| Volatile | Volatile | — | Shorts | Expected — Shorts variance is structurally high | Judge on completion and swipe-away instead (`benchmarks.md` §8) |

## 6. Reading a retention curve, shape by shape

The shape catalogue and its associated benchmarks are in `benchmarks.md` §2. Here is how to *read* a curve in practice, in the order you should look at it.

| Step | Where to look | What it verdicts |
|---|---|---|
| 1 | First 15 seconds | The **hook**, and nothing else. Compare to the thresholds in `benchmarks.md` §2. A cliff here means the opening broke the packaging's promise — nothing further down matters until it is fixed |
| 2 | The 30-second mark | **Promise clarity.** Healthy at 15s but collapsing by 30s means viewers stayed for the attention grab and left once the real subject became clear — a topic/packaging alignment failure, not a hook failure |
| 3 | Slope of the body | Read *steepness*, not direction — every curve declines. A steep body means thin pattern-interrupt density or lost pacing momentum (`retention-scripting-guide.md`) |

**Step 4 — local features.** Map each to a timestamp, then open the script at that timestamp.

| Feature | Read | Script-level cause |
|---|---|---|
| Sharp drop mid-video | A segment lost the audience | Digression, weak transition, or a resolved loop with nothing opened after it |
| Valley that does not recover | Dead weight | Cut it entirely |
| Spike | Rewatching | Identify what it was and build more of it |
| Suspension bridge | Open loops holding the middle | Keep using loops |
| Cliff *before* the end | The payoff never arrived, or came too late | Move the payoff earlier |

**Step 5 — the absolute AVD.** Only now. Channel baseline first, then `benchmarks.md` §2. When comparing two videos' curves, overlay them only at equal length and format — percentage retention is length-normalized and systematically flatters the shorter video.

## 7. Traffic-source health patterns

| Pattern | Interpretation | Risk | Action |
|---|---|---|---|
| Search-dominant, low suggested | Ranking works, engagement does not carry beyond the query | Medium | Improve retention and session continuation |
| Subscriptions-dominant | Growth is capped at the existing audience | High | Build session initiators |
| External-dominant | The channel is a distribution endpoint, not an algorithmic entity | High | Diversify before scaling anything else |
| Shorts-feed-dominant with long-form goals | A structural mismatch, not a failure (`benchmarks.md` §8) | Medium | Reset expectations; treat them as separate businesses |
| Any single source above the concentration threshold in `benchmarks.md` §10 | Fragile — one ranking change removes the channel's traffic | High | Deliberate diversification plan |

**Concentration is the risk, not the source** — any single source can be removed by a ranking change, a season, or a policy. One source = one failure mode; three = a shock absorber. **Reading a *change* in the mix:** a source's share can fall while its absolute number rises, so check absolutes before concluding a source declined.

## 8. Cohorts and returning viewers

Per-video metrics hide the question that determines whether a channel compounds: **do the same people come back?**

| Signal | Where | What it tells you |
|---|---|---|
| Returning vs new viewers | Audience tab | Whether the channel is accumulating an audience or renting attention |
| Unique viewers vs views | Audience tab | Views per viewer — how much each person consumes |
| "Other videos your audience watched" | Audience tab | Adjacency map — the practical definition of the channel's cluster |
| When your viewers are on YouTube | Audience tab | Publish timing for the cold-start window (`algorithm-guide.md` §7) |

**Approximating cohorts.** Studio exposes none, so track three series: returning-viewer *count* (not share) month over month — rising means the channel compounds; views-per-unique-viewer — rising means deeper consumption; and subscribers-gained-per-1,000-views by video, which normalizes for reach and isolates trust. **The interpretation that matters:** growing views with flat returning viewers = renting reach, every video restarting from zero. Flat views with growing returning viewers = building an asset. The second is healthier and looks worse on a dashboard.

## 9. A/B testing at small scale

Native thumbnail testing exists with the parameters and constraints in `benchmarks.md` §7 — including which content types it cannot be used on.

**What it optimizes for.** Watch-time share, not CTR. A variant can win with a lower CTR because it attracts better-matched viewers. Do not overrule a verdict because a different variant had higher clicks.

**When NOT to trust a result:**

| Situation | Why it is untrustworthy |
|---|---|
| Verdict returned "Inconclusive" or "Same" | The platform is telling you the difference is noise. Accept it. |
| Total impressions in the low thousands | Any difference is within noise for a small channel |
| Variants differ in more than one dimension | You learn nothing transferable — you cannot tell which change did it |
| A creator's own before/after with no control | Confounded by time, topic and freshness. This is not a test |

**Testing discipline for a small channel.** Change **one** variable per test (face vs no face, text vs no text, one color scheme vs another). Run the platform's full duration (`benchmarks.md` §7) and never stop early. Record the hypothesis in writing *before* the test. Accumulate across many videos — at small scale the pattern across ten tests is evidence, a single test is not.

> **Known gap.** There is no established significance threshold for small-scale creator A/B tests (`benchmarks.md` §11). If asked for one, answer *benchmark unavailable* and fall back to the platform's own verdict plus the accumulation rule above.

**Title testing** follows the same discipline. Title and thumbnail must never be changed simultaneously — the result becomes uninterpretable.

## 10. The monthly channel review procedure

A repeatable pass that ends in at most three decisions. Run it on a fixed date, not reactively.

| Step | Do | Output |
|---|---|---|
| 1 | Recompute the baseline: median CTR, AVD and views over the last 10–20 uploads, outliers excluded (§4) | Current baseline block |
| 2 | Rank every video published this period as above / at / below baseline on each of CTR and AVD | A 3×3 grid of videos |
| 3 | For each below-baseline video, run the diagnostic matrix (§5) | One diagnosis per video |
| 4 | For each above-baseline video, identify *why* — topic, packaging, format, or timing | A reusable lesson per outlier |
| 5 | Pull the traffic-source mix for the period and compare to last period's **absolute** values (§7) | Concentration verdict |
| 6 | Pull returning viewers, unique viewers, and subs per 1,000 views (§8) | Compounding verdict |
| 7 | Read the retention curves of the best and worst video only (§6) | Two script-level lessons |
| 8 | Check for platform-level explanations before concluding anything channel-level (`benchmarks.md` §5 timeline) | Confounder check |
| 9 | Write **at most three** changes for next period, each naming the metric it should move, and archive the baseline | Decision list + snapshot |

**Discipline rules.** More than three changes per period makes attribution impossible. Never change format, cadence and packaging in the same period. Give every change at least three uploads before judging it.

## 11. Collecting data with no API access

When there is no API or OAuth access, request specific screens and fields. Vague requests produce vague data.

| Studio screen | Path | Fields to request |
|---|---|---|
| Reach | Analytics → Content → Reach | Impressions, impressions CTR, views, unique viewers, traffic-source breakdown |
| Engagement | Analytics → Content → Engagement | Average view duration, average percentage viewed, top videos by watch time |
| Audience | Analytics → Audience | Returning vs new, unique viewers, when viewers are online, other channels/videos watched, top geographies, age/gender |
| Per-video retention | Video → Analytics → Engagement | The retention curve screenshot, plus AVD and average percentage viewed |
| Revenue | Analytics → Revenue | RPM, CPM, estimated revenue, revenue by month — **request the geography split too** |
| Advanced mode | Analytics → Advanced mode | Per-video table with any dimension; best single export for bulk analysis |

**The minimum viable data request** — when you can only ask once, ask for exactly these six: a screenshot of Analytics → Content → Reach for the last 28 days; retention-curve screenshots for their best and worst recent video; the traffic-source breakdown; their last 10 video titles with views, CTR and average percentage viewed; subscriber count plus country if not US; and whether they are in the Partner Program.

**Ask for absolute numbers alongside every percentage** — a percentage with no denominator cannot be diagnosed. **With API access,** the metrics, dimensions and hard limits (query result cap, reporting window, daily quota) are in `benchmarks.md` §10.

## 12. Vanity metrics and reporting hygiene

| Metric | Why it misleads | Report this instead |
|---|---|---|
| Subscriber count alone | Subscribers are permission, not distribution | Views per video and returning viewers |
| Total lifetime views | Dominated by one old video | Median views per video over the last period |
| Likes | Cheap and non-diagnostic | Shares and saves (`algorithm-guide.md` §4) |
| Raw impressions | Impressions can inflate on a video nobody is clicking | Impressions × CTR = views |
| A single viral video | Not repeatable evidence | Median performance, with the outlier studied separately |
| Watch hours on a small channel | Too total-driven to mean anything at low volume | CTR and AVD, which are rates |

**Reporting hygiene:** every number an agent reports carries (1) its period, (2) its baseline, (3) its traffic-source context. A CTR figure with none of the three is not a finding.

## 13. Decision rules

- **If** diagnosing a single video → compare to the channel baseline (§4) and the traffic-source table in `benchmarks.md` §1. Never to a niche or platform average.
- **If** the funnel has multiple broken stages → fix in funnel order: impressions, CTR, retention, satisfaction. One at a time.
- **If** CTR is falling while impressions rise → do nothing. Normal expansion (§2).
- **If** CTR is falling while impressions are flat → packaging is the bottleneck. Nothing else matters yet.
- **If** CTR is high and retention is low → metadata mismatch. Rebuild the first minute or retitle (`algorithm-guide.md` §9).
- **If** asked for a revenue estimate → use the RPM **band** from `benchmarks.md` §9, apply `localization-guide.md` for non-US audiences, present a range, and state the assumptions.
- **If** an RPM comes out above its CPM, or an AVD above the video length → the input is wrong. Recheck before reporting.
- **If** views are up but returning viewers are flat → say the channel is renting reach, not compounding (§8).
- **If** a single traffic source exceeds the concentration threshold (`benchmarks.md` §10) → raise it as a structural risk regardless of current performance.
- **If** an A/B test returns "Same"/"Inconclusive", ran on low volume, or changed more than one variable → report no difference.
- **If** asked for an A/B significance threshold or a first-24h view target → answer *benchmark unavailable* (`benchmarks.md` §11).
- **If** a whole-channel decline appears → check the platform timeline (`benchmarks.md` §5) and year-over-year seasonality first.
- **If** the creator supplies only percentages → request absolute views and impressions before any diagnosis.
- **If** a monthly review produces more than three changes → cut it to three. Attribution is impossible beyond that.
- **If** comparing Shorts numbers across the March-2025 counting change → refuse the comparison and explain why (`benchmarks.md` §8).
