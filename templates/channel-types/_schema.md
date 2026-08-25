# Channel Type Classification & Template Schema

Two things live in this file: **how to classify a channel** (multi-axis, not a single bucket)
and **the schema every archetype template follows** (normalized, so agents can read any of them
the same way).

---

## Part 1 — Classification

Real channels are hybrids. A cooking channel run by a named personality that publishes tutorials
and daily Shorts is simultaneously Tutorial, Personal Brand and Shorts-First. Forcing one label
throws away most of what matters.

**Classify on five axes first, then name a primary and an optional secondary archetype.**

### Axis A — Dominant traffic surface
Where do views actually come from? This drives title length, thumbnail strategy and CTR targets
more than any other factor.

`search` · `suggested` · `browse` · `shorts-feed` · `external` · `subscriptions`

### Axis B — Viewer intent
Why is the viewer here? This drives hook framework and video length.

`solve-a-problem` · `learn-a-subject` · `decide-a-purchase` · `be-entertained` ·
`follow-a-person` · `understand-an-event` · `relax-or-accompany`

### Axis C — Format
`tutorial` · `essay` · `review` · `narrative` · `conversation` · `performance` ·
`livestream` · `compilation` · `vertical-short`

### Axis D — Monetization model
Where does the money actually come from? This can invert the entire revenue stack.

`adsense-primary` · `sponsorship-primary` · `product-funnel-primary` ·
`audience-direct-primary` (memberships, Super Chat, Patreon) · `lead-gen-primary` (B2B) ·
`not-monetized`

### Axis E — Production model
`solo` · `small-team` · `studio` · `faceless-automated`

### Then pick archetypes

| Archetype | Typical axis signature |
|---|---|
| `education` | search + suggested · learn-a-subject · essay/tutorial · adsense |
| `tutorial` | search · solve-a-problem · tutorial · adsense |
| `review` | search · decide-a-purchase · review · sponsorship/affiliate |
| `commentary` | browse + suggested · understand-an-event · essay · adsense |
| `entertainment` | browse · be-entertained · narrative/performance · sponsorship |
| `vlog` | subscriptions · follow-a-person · narrative · sponsorship |
| `personal-brand` | browse + external · follow-a-person · mixed · product-funnel |
| `niche-authority` | search · learn-a-subject · essay · product-funnel |
| `shorts-first` | shorts-feed · be-entertained · vertical-short · product-funnel |
| `gaming` | browse + suggested · be-entertained · performance/narrative · adsense |
| `podcast` | suggested + external · understand-an-event · conversation · sponsorship |
| `livestream` | subscriptions · follow-a-person · livestream · audience-direct |
| `faceless` | browse + search · learn-a-subject · compilation/essay · adsense |
| `ambient` | search + suggested · relax-or-accompany · performance · adsense |

**Rules for the orchestrator:**

1. Name a **primary** archetype — the one whose traffic surface and monetization model match.
   Traffic surface breaks ties; it is the single most predictive axis.
2. Name a **secondary** only when a second archetype genuinely describes 25%+ of output.
3. Where primary and secondary conflict, **primary wins**. Say so when passing both to an agent.
4. If nothing fits, use the closest archetype and record the mismatch in the channel profile.
   Never silently force a bad fit — a wrong archetype poisons every downstream benchmark.
5. Persist both to `workspace/config.json`.

### Channel size tier

Independent of archetype, and it changes what advice is even relevant. Record it separately.

| Tier | Subscribers | What changes |
|---|---|---|
| `new` | < 1,000 | Not yet monetized. Volume and positioning beat optimization. |
| `growing` | 1K–10K | YPP reached. Packaging and consistency are the levers. |
| `established` | 10K–100K | Sponsorships viable. Format and series thinking matter. |
| `authority` | 100K+ | Off-platform revenue and team leverage dominate. |

**An `authority`-tier channel must never be handed a growth ladder it already finished.**
Agents read the tier and skip irrelevant stages.

---

## Part 2 — Template schema

Every file in `templates/channel-types/` follows this exact structure. Agents rely on it —
do not reorder or rename sections.

### Frontmatter (machine-readable)

```yaml
---
archetype: education
display_name: Education
axes:
  traffic: [search, suggested]
  intent: learn-a-subject
  format: [essay, tutorial]
  monetization: adsense-primary
  production: [solo, small-team]
benchmarks:
  ctr_target: "4.5% average, aim 6%+"
  retention_target: "40%+ AVD (ahead of ~83% of channels, benchmarks §2)"
  length_min: 8
  length_max: 15
  cadence_solo: "2/week"
  cadence_team: "3/week"
  shorts_per_week: "2-3"
  rpm_range_usd: "8-15"
  evergreen_share: "80%+"
traffic_mix:
  search: 40
  suggested: 30
  browse: 20
  shorts: 10
---
```

`traffic_mix` percentages must sum to 100. All benchmark values must exist in
`references/benchmarks.md` or be marked `unavailable`.

### Body sections — all nine, always, in this order

| § | Section | Contents |
|---|---|---|
| 1 | **Channel DNA** | One paragraph: what this archetype fundamentally is, which surface it wins on, which signals the algorithm rewards for it, and its revenue character. |
| 2 | **Content Mix** | Hub / Hero / Help table with percentage ranges summing to 100, plus the evergreen-vs-trending split. |
| 3 | **Cadence & Length** | Table: `Setup \| Long-form \| Shorts \| Notes` with rows for solo and small-team. Then the optimal length band and the mid-roll note. |
| 4 | **Title Patterns** | Exactly 10 numbered fill-in formulas using `[BRACKET]` placeholders, then the character-count rule for this archetype's dominant traffic source, closing with one line telling a non-English channel to re-derive the formulas from local search behaviour rather than translate them (`references/localization-guide.md` §5). |
| 5 | **Thumbnail Formula** | Face / text word count / colors / composition / what to avoid / target CTR. |
| 6 | **Hook Style** | Primary and secondary hook framework, named from `references/hook-library.md`, each with a worked example line, plus the timing rule. |
| 7 | **Monetization Stack** | All 7 streams ranked 1–7 in a `Rank \| Stream \| Why This Position` table. Rank order is what differentiates archetypes. |
| 8 | **Growth Trajectory** | 5-row table, always these tiers: `0–500 \| 500–1K \| 1K–10K \| 10K–50K \| 50K–100K+`, with `What Changes \| Key Lever \| Revenue Character`. **§8 contains no dollar figures and no time estimates, because neither growth timeline by tier nor revenue by tier exists as verified data — `benchmarks.md` §11 lists both as known gaps.** Only qualitative description and genuine monetization thresholds (YPP levels, the brand-deal floor, the archetype's RPM band) may appear. Normalized so archetypes can be compared side by side. |
| 9 | **Failure Modes** | Exactly 3. Each: bolded failure name, the diagnosis, and a **Fix:** line that is a specific action, not advice. |

### Hard rules

- **No dollar figure appears here that is not in `benchmarks.md`.** Templates reference; they
  do not originate data.
- All revenue figures are **US baseline**. Any agent using them for a non-US channel must
  apply `references/localization-guide.md` first. Every template says this in §7.
- Growth-trajectory tiers are identical across all 14 templates. Do not invent new tiers.
- Section 4's 10 title formulas are **placeholders to instantiate**, not blanks to fill in the
  template file itself.
- Templates are **read-only reference**. Nothing writes to them. The creator's own filled-in
  document is `workspace/channel-profile.md`.

### Which agents read templates

Every agent that produces channel-specific output reads the archetype template. Specifically:

| Section | Consumed by |
|---|---|
| Frontmatter benchmarks | every agent |
| §2 Content Mix | `ideation-agent`, `calendar-agent`, `channel-strategist` |
| §3 Cadence & Length | `calendar-agent`, `script-agent`, `shorts-agent` |
| §4 Title Patterns | `seo-agent`, `metadata-agent`, `ideation-agent` |
| §5 Thumbnail Formula | `thumbnail-agent` |
| §6 Hook Style | `script-agent` |
| §7 Monetization Stack | `monetization-agent`, `channel-auditor` |
| §8 Growth Trajectory | `channel-strategist`, `channel-auditor`, `analytics-agent` |
| §9 Failure Modes | `channel-auditor`, `channel-strategist` |
