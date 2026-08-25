# Benchmarks — Single Source of Truth

> **Every number cited anywhere in this matrix comes from this file.** No other reference,
> agent, or template restates a benchmark. They link here.
>
> If a number an agent needs is not in this file, the correct answer is **"benchmark
> unavailable"** — never an estimate presented as data.

**Baseline:** United States, English-language, long-form unless stated.
**Non-US channels:** adjust before quoting any revenue figure. Read `references/markets/<code>.md`
first — that is the researched market data. Only where a market has no file, fall back to the
multiplier table in `references/localization-guide.md` and say so. Unadjusted US RPM applied to an
emerging market is wrong by 5–20×.

**Confidence key** — describes the **quality of the evidence**, not how sure the system is:

| Tag | Evidence | Weight |
|---|---|---|
| `A` | Multiple independent sources, or a single large-N study | Solid — plan around it |
| `B` | One credible source | Usable — verify before a big commitment |
| `C` | Directional: anecdotal, single case study, or a structural heuristic | A hint, not a fact |

**Never make an irreversible decision on a `C`.** Any projection built on `C` figures must be
presented as a modelled range with stated assumptions, never as a prediction. Full explanation for
the creator in `README.md` → *How to read the numbers*.

---

## 1. Click-through rate

CTR depends more on **traffic source** than on niche. Use the source table to diagnose a
specific video; use the niche table to set a channel-level target.

### By traffic source

| Source | Typical CTR | Why |
|---|---|---|
| Search | 12.5% | Viewer already has intent |
| Suggested | 9.5% | Contextual match to what they just watched |
| Browse (home feed) | 3.5% | Cold, competing with everything |
| External | 2.8% | Off-platform, low intent |

*Source: Focus Digital, Dec 2025. Confidence `B`.*

### Performance tiers (blended, all sources)

| Range | Assessment |
|---|---|
| < 3% | Packaging is the bottleneck — fix before anything else |
| 4–6% | Average |
| 7–10% | Good |
| 10%+ | Exceptional |

*Confidence `A`.*

### By niche (blended average)

| Niche | Average CTR |
|---|---|
| Gaming | 8.5% |
| Health & Fitness | 8.0% |
| Tech & Reviews | 7.5% |
| Beauty & Fashion | 6.5% |
| Entertainment | 6.0% |
| Finance & Business | 5.5% |
| Education | 4.5% |

*Source: Focus Digital, Dec 2025. Confidence `B`.*

> ⚠️ **Reconciliation.** Niche averages skew high relative to the tier table because they are
> blended across sources and weighted toward search and suggested traffic. A browse-dominant
> video at 4% is healthy even in a niche whose average reads 8%. **Always diagnose against the
> traffic-source table, not the niche table.**

### CTR lifecycle
- Peak in the first **24 hours** (served to subscribers and warm audience first)
- Sustained healthy: **4–8%**
- A **0.5 percentage-point** difference is significant at scale

---

## 2. Retention and view duration

| Metric | Value | Confidence |
|---|---|---|
| Average AVD across all videos | 23.7% | `B` (Retention Rabbit, 150M+ minutes) |
| Videos exceeding 50% AVD | 16.8% | `B` |
| Below 40% AVD | Actively deprioritized | `B` |
| Retention above 40% | Ahead of ~83% of channels | `B` |
| 15%+ above channel average | ~2.3× more algorithmic promotion | `C` |
| +10 percentage points retention | 25%+ impression increase | `C` |
| AI/synthetic narration | ~70% lower retention | `C` |

### The first 60 seconds

| Metric | Value |
|---|---|
| Viewers lost in first 60s | 55% |
| Viewers lost in first 10s | 20% |
| Value proposition stated within 15s | +18% retention at the 1-minute mark |
| Retention at 10–15s below 50% | Hook is failing |
| Retention at 30s: 70%+ | Solid |
| Retention at 30s: 80%+ | Exceptional |

*Confidence `B`.*

### Pattern interrupts

| Context | Frequency |
|---|---|
| Pre-recorded long-form | Every ~30 seconds |
| Live | Every 2–3 minutes |
| Shorts | Every 2–3 seconds |

- Interrupt within the first 5 seconds: **+23% retention** (`C`)
- Interrupts placed at known drop-off points: **15–22% re-engagement** (`B`, Wistia)

### Retention curve shapes

| Shape | Diagnosis | Fix |
|---|---|---|
| Sharp cliff (20%+ lost in first 15s) | Hook broke the title's promise | Rewrite the first 15 seconds |
| Steady decline | Normal — only a problem if slope is steep | Increase interrupt density |
| Mid-video valley (dip at 40–60%) | A segment is dead weight | Cut it or move it earlier |
| Spikes | Viewers rewatching something | Do more of that |
| Suspension bridge (open loops) | Healthy — **68% higher completion** | Keep using loops |
| Sawtooth | Rhythmic re-engagement — **43% higher completion** | Keep the cadence |

*Confidence `C` on the two lift figures.*

---

## 3. Video length

| Format | Optimal length |
|---|---|
| Shorts | 15–60s (bimodal peaks at ~13s and ~60s) |
| Tutorials | 7–15 min |
| Entertainment / Vlogs | 8–12 min |
| Product reviews | 8–15 min |
| Gaming (edited) | 10–20 min |
| Educational / video essay | 15–25 min |
| Documentary / deep-dive | 20–45 min |
| Podcasts / interviews | 30–90 min |

| Fact | Value |
|---|---|
| Peak average retention band | 5–10 min (31.5%) |
| Share of total watch time from 20+ min videos | 57% |
| Shorts share of platform views | 75% |
| **Mid-roll ad threshold** | **8:00 minimum → ~50% revenue increase** |
| Spoken-word pacing | ~140 words/minute (130–150 typical) — **English baseline only** |

*Confidence `B`. The 8-minute mid-roll threshold is `A` — it is a platform rule, not a study.*

*The pacing figure is drawn from this file's United States, English-language sample and **does not transfer to other languages** — syllable-timed and mora-timed languages differ substantially from it, and for languages that compound heavily or are written without spaces, words are the wrong unit altogether. For any non-English script take the rate from `localization-guide.md` §7, which also gives the timing test that produces the creator's own measured rate.*

---

## 4. Upload cadence

| Cadence | Effect |
|---|---|
| 12+ uploads/month | 8× faster view growth, 3× subscriber growth |
| Long-form + Shorts together | 40–60% faster growth than either alone |

*Source: vidIQ, 5.08M channels. Confidence `B`.*

- Notification cap: **max 3 per user per 24 hours**
- Channels under **500 subscribers** receive active algorithmic promotion
- A publishing break costs **2–3 weeks** of rebuilding momentum (`C`)

---

## 5. Algorithm mechanics

**Three independent ranking systems:** Browse · Search · Shorts. A video ranks separately in
each; failing one does not mean failing the others.

**Testing cascade** — each layer must perform to unlock the next:
1. Core audience (subscribers, frequent viewers)
2. Expanded (similar interest profiles)
3. Broader (wider demographic or topic)
4. High authority (trending surfaces)

**Satisfaction signals, ranked:**
Shares > Repeat viewing > Session continuation > Saves > Survey responses > Likes > Comments

**Engagement:** replying to 50+ comments within 2 hours correlates with **15–20% higher
reach** (`C`).

### Platform timeline

| Date | Change |
|---|---|
| Mid-2024 | Native thumbnail A/B testing ("Test & Compare") |
| Oct 2024 | Shorts max length raised to 3 minutes |
| Late 2024 | Clickbait/metadata-mismatch penalty; title A/B testing |
| Jan 2025 | LLMs integrated into recommendations |
| Mar 2025 | View-counting change; `engagedViews` introduced |
| Apr 2025 | `engagedViews` official in Analytics API |
| Jul 2025 | "Repetitious content" policy renamed **"Inauthentic content"** |
| Sep 2025 | Shorts older than ~28–30 days deprioritized |
| Oct 2025 | Shorts reported to earn more per watch hour than in-stream ads (US) |

---

## 6. SEO limits and rules

| Element | Rule |
|---|---|
| Title hard limit | 100 characters |
| Title — desktop truncation | ~60–70 characters |
| Title — mobile truncation | ~40–50 characters |
| Title — front-load window | First 40–50 characters carry the hook and keyword |
| Description max | 5,000 characters |
| Description — visible before "Show more" | First 150–200 characters |
| Description — keyword placement | Primary keyword in first 25 words |
| Description body | 200–350 words, keyword 2–4× |
| Tags | 500 characters total; minimal ranking value |
| Chapters | Must start at `0:00`, minimum 3, minimum 10s each |
| Hashtags — long-form | 3–5 optimal, **15 max (exceeding makes ALL hashtags ignored)** |
| Hashtags — Shorts | 1–5, 60 characters total |
| First 3 hashtags | Displayed above the title |
| End screen | Last 15–20 seconds; CTR 2%+ healthy, 4%+ strong |

> ⚠️ **Title length reconciliation.** Three published figures conflict. They are not
> contradictory once separated by traffic source:
> - **Search-targeted video** → longer titles (60–70 chars) carry more matchable terms.
>   The "70–100 characters outperform by 10–14%" finding (10xCreator, 3M+ videos, `B`) is
>   dominated by search traffic.
> - **Browse-targeted video** → shorter titles (under 50 chars) read faster in a scrolling
>   feed. This is the MrBeast rule and it applies to home-feed content.
> - **Universal** → the hook and the primary keyword live in the first 40–50 characters,
>   because that is all mobile shows.
>
> Decide title length from the video's intended traffic source, not from a global rule.

**Other SEO facts:**
- Numbers in titles: **+20–30% CTR** (`C`)
- Chapters: **+4% AVD** (`B`, Backlinko); up to 50% higher retention (`C`, HubSpot)
- Captions: **+12% watch time**; 80% of caption users are not deaf or hard of hearing (`B`)
- VideoObject schema on an embedding page: **+30% CTR** in Google results (`B`)
- 29.5% of Google AI Overviews cite YouTube (`B`, BrightEdge mid-2025)
- 25%+ of Google results include video snippets (`B`)

---

## 7. Thumbnails

| Rule | Specification |
|---|---|
| Minimum resolution | 1280 × 720 |
| Recommended | 1920 × 1080 (TV surfaces) |
| Aspect ratio | 16:9 |
| Max file size | 2 MB |
| Formats | JPG, PNG, GIF, BMP |
| Text overlay | 5 words max, 3 ideal |
| Primary colors | 2–3 |
| Focal points | Exactly 1 |
| Negative space | 30–40% |
| Viewer decision time | Under 1 second |
| Mobile share of views | 70%+ |

- Faces: **+20–30% CTR** (`B`, vidIQ)
- Custom thumbnails on **90%** of top-performing videos (`B`)
- **Information Split Rule:** thumbnail carries the visual/emotional hook, title carries the
  keyword and the promise. **They must never say the same thing.**

### Native A/B testing ("Test & Compare")

| Parameter | Value |
|---|---|
| Variants | Up to 3 |
| Optimizes for | Watch-time share |
| Duration | Up to 2 weeks |
| Verdicts | Winner / Same / Inconclusive |
| Setup | Desktop only |
| **Not available for** | **Shorts, made-for-kids content** |
| Documented CTR gains | 37% – 110% (`C`) |

### Policy strikes
First violation = warning (expires after 90 days). Same policy again within 90 days = strike.
**3 strikes = channel termination.** Pornographic thumbnails = immediate termination, no
warning.

---

## 8. Shorts

**Ranking is by completion, not clicks.** CTR plays essentially no role.

| Priority | Signal | Benchmark |
|---|---|---|
| 1 | Completion rate | **70%+ triggers aggressive promotion** |
| 2 | Loop / replay rate | >100% average viewed = loopable |
| 3 | Comments and shares | Weighted above likes |
| 4 | **Viewed vs Swiped Away** | **75%+ good · below 60% = rewrite the hook now** |
| 5 | Satisfaction (surveys, long-press) | — |

> ⚠️ **Threshold reconciliation.** "70%" and "75%" and "60%" measure *different things*.
> Completion rate ≥70% is the promotion trigger. Viewed-vs-Swiped-Away ≥75% is a healthy hook.
> Viewed-vs-Swiped-Away below 60% is the emergency threshold — rewrite the opening immediately.
> Never compare these numbers to each other.

| Spec | Value |
|---|---|
| Max length | 3 minutes |
| Sweet spot | 15–60s (peaks at ~13s and ~60s) |
| Dead zone to avoid | 30–45s |
| Aspect ratio | 9:16 |
| Resolution | 1080 × 1920 |
| Visual change every | 3 seconds |
| Hook window | First 1–3 seconds |
| Title visible before truncation | ~40 characters (4–6 words optimal) |
| Description preview | First 125 characters |
| Freshness window | Deprioritized after ~28–30 days |

**Music and revenue:** every licensed track splits the revenue pool.
No music = creator keeps 100% of their share · 1 track = 50% · 2 tracks = 33%.
Content ID music blocks Shorts longer than 1–3 minutes in some territories.

**Long-form relationship:** audience overlap is only **~10%**; "related video" link conversion
is **under 1%**. Shorts build reach, not directly a long-form audience. Channels running both
grow **40–60% faster** (`B`).

**View counting (Mar 2025):** any playback counts as a view, loops count again. Totals inflated
roughly **30%** versus the old method — do not compare pre/post-March-2025 numbers.

---

## 9. Monetization

### YouTube Partner Program

| Tier | Requirements | Unlocks |
|---|---|---|
| **Expanded** | 500 subs · 3 public uploads in last 90 days · (3,000 watch hours/12mo **OR** 3M Shorts views/90 days) | Memberships, Super Chat/Thanks/Stickers, Shopping |
| **Full** | 1,000 subs · (4,000 watch hours/12mo **OR** 10M Shorts views/90 days) | Ad revenue, Premium revenue share |

Both require 2-step verification, no active strikes, a linked AdSense account. Review takes
roughly one month.

### RPM by niche (US baseline, long-form)

RPM is what the creator actually receives. CPM is what advertisers pay. **YouTube keeps 45%**
of ad revenue on long-form, **55%** on Shorts.

| Tier | Niche | RPM |
|---|---|---|
| **1** | Personal Finance / Investing | $20–40+ |
| **1** | Legal / Real Estate | $20–35 |
| **1** | Business / Entrepreneurship | $15–30 |
| **1** | Tech & Software (B2B/SaaS) | $15–25 |
| **1** | Digital Marketing | $12–25 |
| **2** | Health & Fitness | $8–15 |
| **2** | Education | $8–15 |
| **2** | DIY / Home Improvement | $8–14 |
| **2** | Consumer Tech / Reviews | $6–12 |
| **2** | Food / Cooking | $6–12 |
| **2** | Travel | $6–12 |
| **3** | Beauty | $5–8 |
| **3** | Lifestyle | $3–6 |
| **3** | Gaming | $2–5 (US median $3.50) |
| **3** | Entertainment / Commentary | $2–5 |
| **3** | Music | $1–3 |

*Confidence `B`.*

> ⚠️ **Two reconciliations applied here.** (1) "Tech" appeared with two different ranges in
> the source material; it is split above into B2B/SaaS ($15–25) and consumer tech reviews
> ($6–12), which is what the divergent figures actually described. (2) Education was published
> as "CPM $5–12, RPM $8–15" — an RPM above CPM is arithmetically impossible. Education CPM is
> $8–20, RPM $8–15.

### Shorts RPM

| Niche | RPM per 1K views |
|---|---|
| Finance | $0.05–0.30 |
| Typical | $0.01–0.07 |
| Comedy / Lifestyle | $0.01–0.05 |

**Long-form RPM runs 10–100× Shorts RPM.** Shorts are a reach instrument, not a revenue one.

### Other revenue streams

| Stream | Key numbers |
|---|---|
| **Memberships** | $0.99–$499.99/mo · max 25 tiers · YouTube takes 30% · 1% conversion is meaningful · start with 2–3 tiers |
| **Super Chat / Thanks** | 70/30 split · $1–$500 per message · $2,000/user/week cap · mid-size channels $50–500/mo |
| **Shopping affiliate** | 5–20% commission (median ~15%) · up to 60 products/video · 30-day attribution · limited country availability |
| **Premium revenue** | ~55% creator share · 15–30% of total revenue for Premium-leaning channels |
| **Brand deals** | Floor $1,000+ · 5K–15K avg views → $1,000–1,500/video · 50K–250K views → $1,250–6,250 · Gaming ~$0.037/view · Lifestyle ~$0.023/view |
| **External (courses, Patreon)** | Patreon 10% + payment fees · Ko-fi free tier · Substack 10% · Amazon Associates 1–10% · digital-product networks 20–75% |

### Seasonality
Q4 CPMs run **30–60% higher** than average. January is the cheapest month. Plan
high-monetization content for Q4 and experimental content for Q1.

### FTC disclosure (US)

| Method | Requirement |
|---|---|
| Verbal | Within the first 15–30 seconds |
| On-screen text | Displayed 10+ seconds |
| Written | In the first 2 lines of the description |
| YouTube's paid-promotion toggle | **Not sufficient on its own** |

Penalty up to **$53,088 per violation**. Both brand and creator are liable. Non-US markets have
their own regimes — see `localization-guide.md`.

---

## 10. Analytics

### Metric hierarchy

| Priority | Metric | Why |
|---|---|---|
| 1 | Watch time | The objective the algorithm optimizes |
| 2 | CTR | Drives ~80% of initial distribution decisions |
| 3 | AVD | 50%+ makes a video ~3× more likely to be recommended |
| 4 | Traffic sources | Tells you *which* algorithm you're winning |
| 5 | Subscribers per video | Lagging indicator of trust |

### Impressions funnel

| Phase | CTR range |
|---|---|
| Launch (warm audience) | 12%+ |
| Sustained healthy | 4–8% |

### Diagnostic matrix

| Impressions | CTR | AVD | Diagnosis |
|---|---|---|---|
| High | Low | — | Thumbnail/title problem |
| High | High | Low | Clickbait — packaging over-promised |
| Low | High | — | Too niche, or topic has no demand |
| Low | Low | — | Wrong topic *and* wrong packaging |
| Falling over time | Stable | Stable | Freshness decay or seasonal |

### Channel health

| Signal | Healthy | Struggling |
|---|---|---|
| CTR | 4–8% | Under 3% |
| Retention | Above 40% | Dropped 40%+ vs baseline |
| Traffic concentration | Diversified | 80%+ from one source |

### Analytics API limits
- 200 results per query · video groups up to 500 videos
- Reporting API: 24-hour granularity, 60-day window
- `engagedViews` official since April 2025; for long-form it equals `views`

### YouTube Data API v3 quota
- **10,000 units/day**, resets at midnight Pacific
- `search.list` costs **100 units** → maximum 100 searches/day
- Most read calls cost 1–5 units

---

## 11. Known gaps

Honest inventory. When an agent needs one of these, the answer is "benchmark unavailable":

- Cold-start velocity (first 24h/48h view targets by channel size)
- Impressions-per-subscriber ratios
- Retention benchmarks segmented by video length or traffic source
- Statistical significance thresholds for A/B tests at small scale
- Live streaming and premiere performance benchmarks
- Community tab engagement benchmarks
- Non-US CTR and retention data (only revenue has regional adjustment)
- Playlist performance beyond the "5–10 videos, +40% watch time" figure (`C`)
- Made-for-kids / COPPA-restricted monetization figures
- Growth timeline by subscriber tier (how long each tier typically takes)
- Revenue by subscriber tier (monthly earnings at a given channel size)

---

## 12. Maintenance

Platform numbers decay fast. Anything tagged 2024 or earlier should be treated as directional.

When updating: change the number **here only**, note the date and source, and never let another
file in this matrix hold a competing figure. The value of this file is that it is the only
place a number lives.
