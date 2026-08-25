# Markets — Index and Schema

**Purpose.** `benchmarks.md` holds platform mechanics that are the same everywhere — CTR bands,
retention thresholds, character limits, YPP requirements, API quotas. **None of that changes by
country.** What changes by country is *economics and culture*: what a view is worth, when
advertisers spend, how people phrase a search, who pays for sponsorship and in what currency,
what the law requires you to disclose.

That is what a market file holds.

---

## Available markets

| Code | File | Status |
|---|---|---|
| `BR` | `br.md` | Full |
| `US` | `us.md` | Full — this is the baseline `benchmarks.md` is written against |

**No file for the market you need?** Fall back to `../localization-guide.md`, which carries a
directional RPM multiplier table covering ~20 markets. A multiplier is a rough approximation of
one dimension; a market file is the real thing across all of them. Say which one you used.

---

## How markets are configured

`workspace/config.json` carries an audience mix, not a single country:

```json
"markets": {
  "mix": [
    { "code": "BR", "share": 80 },
    { "code": "US", "share": 20 }
  ],
  "source": "declared"
}
```

- **`share` percentages must sum to 100.**
- **`source`** is `declared` (the creator told us at setup) or `analytics` (measured from
  YouTube Analytics → Audience → Geography). `analytics` always wins over `declared`.
- The orchestrator asks for this at `/yt setup`, right after the language question, and the
  `analytics-agent` corrects it the first time it sees real geography data.

### The rule that matters most

**What counts is where the *audience* is, not where the creator is.**

A creator living in Toronto whose viewers are Brazilian has a `BR` channel. Advertisers bid on
the viewer's market, not the uploader's. Getting this backwards produces revenue estimates wrong
by an order of magnitude, and it is the single most common mistake in this whole system.

---

## Computing a blended figure

For any market-dependent number — RPM above all — compute a **weighted average across the mix**:

```
blended = Σ ( market_value × share )
```

Worked example. A channel in the Education niche, audience 80% BR and 20% US:

```
US Education RPM band          = $8–15        (benchmarks.md §9)
BR Education RPM band          = see br.md §2
blended_low  = (BR_low  × 0.80) + (8  × 0.20)
blended_high = (BR_high × 0.80) + (15 × 0.20)
```

Always show the arithmetic and state the mix you used. **Never present a blended figure as a
single number** — it is a range built on `C`-confidence inputs, so it is presented as a range
with its assumptions named. See the README's *How to read the numbers*.

Where the mix has a **long tail** (many markets under 5%), fold the tail into whichever named
market is economically closest and say you did.

---

## File schema

Every market file follows this structure. Agents rely on the section numbers — do not reorder.

### Frontmatter

```yaml
---
market: BR
display_name: Brazil
currency: BRL
primary_languages: [pt-BR]
rpm_multiplier_vs_us: "…"      # directional, for quick sanity checks only
confidence: C
last_reviewed: YYYY-MM-DD
---
```

### Body sections

| § | Section | Contents |
|---|---|---|
| 1 | **Market snapshot** | What makes this market structurally different for a creator. One dense paragraph plus the headline facts. |
| 2 | **Revenue** | RPM/CPM by niche *in this market*, plus how the curve differs in shape from the US baseline — not just in level. |
| 3 | **Seasonality** | Month-by-month demand and CPM pattern, local events that move it, what to schedule when. |
| 4 | **Search and discovery** | How people actually phrase queries, high-volume local modifiers, what does not translate. |
| 5 | **Sponsorship landscape** | Who buys, in what currency, typical deal structures, how local and global brands differ. |
| 6 | **Off-platform monetization** | Payment rails, course and membership platforms, affiliate networks that actually operate here. |
| 7 | **Disclosure and legal** | Advertising regulation, data protection, what the platform's own toggle does not satisfy. |
| 8 | **Publishing rhythm** | Timezones, when the audience is online, weekly pattern. |
| 9 | **Competitive landscape** | Saturated categories, underserved ones, notes on what travels from other markets. |
| 10 | **Decision rules** | Compact if-then rules an agent can act on directly. |

### Hard rules for market files

- **Every figure carries a confidence tag and a source.** Market data is volatile and mostly
  `C`. Tag honestly; a `C` labelled `B` is worse than no number.
- **Mark `unavailable` rather than deriving.** If no source gives Gaming RPM for this market, say
  so. Do not multiply the US figure and present the result as market data — that is exactly the
  fabrication this system is built to prevent.
- **Do not restate platform mechanics.** CTR bands, retention thresholds, character limits and
  YPP requirements live in `benchmarks.md` and are cited, never copied.
- **State the review date.** Revenue figures decay within a year.
- Written in English, like every reference file. Deliverables are translated; references are not.

---

## Which agents read market files

| Agent | Uses |
|---|---|
| `monetization-agent` | §2, §5, §6, §7 — **mandatory**, before quoting any figure |
| `analytics-agent` | §2 for revenue interpretation; corrects `markets.mix` from Geography data |
| `calendar-agent` | §3 seasonality, §8 publishing rhythm |
| `seo-agent` | §4 search behaviour |
| `metadata-agent` | §4, and §7 when a video is sponsored |
| `channel-strategist` | §1, §9 for positioning and niche selection |
| `channel-auditor` | §2 to calibrate the monetization lens |
| `competitor-analyst` | §9 |

---

## Decision rules

- **Mix has a market with a file → read the file.** Do not fall back to the multiplier table when
  a dedicated file exists.
- **Mix has a market with no file → use `localization-guide.md`'s multiplier**, and say in the
  deliverable that a directional multiplier was used rather than market data.
- **`source: analytics` exists → use it and ignore `declared`.**
- **No mix configured at all → say so, ask once, and proceed with `US` baseline** clearly labelled
  as an assumption. Never silently assume US.
- **Any revenue figure crossing markets → show the weighted arithmetic**, never a bare number.
- **Creator's country ≠ audience's country → the audience wins**, every time.
