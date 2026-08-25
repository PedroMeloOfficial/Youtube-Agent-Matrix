# Localization Guide

> ## ⚠️ Read this first — this guide is the **fallback**, not the primary source
>
> For any market that has a file in `references/markets/` — currently `BR` (`br.md`) and `US`
> (`us.md`) — **that file wins over everything in this guide.** A market file carries researched
> market data across revenue, seasonality, search behaviour, sponsorship, off-platform rails,
> disclosure law, publishing rhythm and competitive landscape. This guide carries a **directional
> multiplier**: one dimension, approximated.
>
> What this guide is for:
>
> - **Language and localization method** — §5 keyword research, §6 character counts by script,
>   §7 speaking rate, §10 audio tracks, §11 channel structure, §12 cultural adaptation. These
>   remain **primary** and are unaffected by market files.
> - **Markets with no dedicated file yet** — the §2 multiplier table, used as a directional
>   approximation and **named as such in the deliverable**.
>
> Schema, config shape and the weighted-blending method: `references/markets/_index.md`.

**Purpose.** `benchmarks.md` is US-baseline. Applying it unadjusted to a non-US audience produces revenue projections wrong by 5–20×, SEO advice that fails in the target language, and titles that truncate in the wrong place. This file is the conversion layer.

> **This is the one file in the matrix permitted to originate numbers**, because `benchmarks.md` holds no regional data. Everything numeric below is **confidence `C` — directional**, assembled from creator-reported figures and public commentary rather than a single measured study. Treat it as a starting multiplier, not a measurement. **It must be re-verified before any figure reaches a creator as a projection**, ideally against that channel's own realized RPM in Analytics, which beats every table here.

**Contents:** 1 Why RPM varies · 2 RPM multiplier table · 3 Computing an adjusted RPM · 4 Finding audience geography · 5 Language-specific SEO · 6 Character counts by script · 7 Speaking rate and script length · 8 Sponsorship by market · 9 Disclosure by region · 10 Audio tracks and subtitles · 11 One channel or several · 12 Cultural adaptation · 13 Decision rules

## 1. Why RPM varies by audience geography

Ad rates are set by **advertiser competition for a viewer**, and that competition is a function of the viewer's market: how much local advertisers can pay, the purchasing power behind each impression, the maturity of the digital ad market, and the seasonal ad budget cycle in that country.

Three consequences that get missed constantly:

1. **The creator's location is irrelevant.** A creator in one country whose audience is 80% in another earns roughly that other market's rates. Payment routing, tax residence and withholding depend on the creator; *rates* depend on the viewer.
2. **Language is a proxy, not the cause.** An English-language channel watched mostly in India earns closer to India's rates than to the US's. Do not infer rates from language.
3. **The mix, not the mode, sets the rate.** A channel with 30% US and 70% low-RPM markets does not earn the low-RPM rate — it earns a weighted blend, and that US 30% may be the majority of the revenue (§3).

Niche multiplies on top of geography. A finance channel in a low-RPM market still out-earns a gaming channel in the same market — the *ratio* between niches in `benchmarks.md` §9 broadly survives the translation even when the absolute level does not.

## 2. RPM multiplier table

Multipliers relative to the US baseline = **1.00**, applied to the niche RPM bands in `benchmarks.md` §9. **Confidence `C` throughout. Directional only. Re-verify before use.**

> **`BR` and `US` now have full market files** (`references/markets/br.md`, `references/markets/us.md`). Their rows below are **superseded** — read the market file's §2 instead, and keep the multiplier only as a sanity check on the blended figure. Use this table for markets with no file yet.

| Market | Multiplier | Confidence | Notes |
|---|---|---|---|
| United States | 1.00 | `C` (baseline) | The reference point for all of `benchmarks.md` §9 |
| Australia | 0.90–1.10 | `C` | Occasionally exceeds the US in some niches |
| Norway / Denmark / Sweden / Finland | 0.85–1.10 | `C` | Small audiences, high ad value; often the best per-viewer market |
| Canada | 0.80–1.00 | `C` | Tracks the US closely |
| United Kingdom | 0.75–0.95 | `C` | Mature market, strong advertiser demand |
| Germany | 0.70–0.90 | `C` | Strongest of the large EU markets |
| Switzerland / Netherlands / Ireland | 0.75–1.00 | `C` | Small, high-value |
| Japan | 0.55–0.80 | `C` | Large market; language barrier limits foreign competition |
| South Korea | 0.45–0.70 | `C` | High digital penetration, strong domestic advertisers |
| France | 0.45–0.65 | `C` | |
| Italy | 0.35–0.55 | `C` | |
| Spain | 0.30–0.50 | `C` | Below the northern-EU cluster |
| Poland | 0.25–0.40 | `C` | Rising; best of the CEE cluster |
| Turkey | 0.10–0.25 | `C` | Currency volatility makes this unstable |
| Mexico | 0.12–0.25 | `C` | Strongest of the Spanish-speaking LATAM markets |
| Brazil | 0.10–0.22 | `C` | Very large audience, low per-view rate — volume market |
| Nigeria | 0.05–0.15 | `C` | |
| Philippines | 0.05–0.12 | `C` | High English fluency, low ad rates |
| Indonesia | 0.04–0.12 | `C` | Enormous audience, very low rates |
| India | 0.03–0.10 | `C` | The widest spread from the US baseline; treat any projection with extreme caution |

**How to read this.** Multiply the niche band in `benchmarks.md` §9 by the market multiplier. A tier-1 niche in a 0.10 market lands near a tier-3 US niche — which is exactly why "just pick a high-RPM niche" is bad advice in a low-RPM market, and why non-ad streams (`monetization-guide.md` §1) matter far more there.

**Known distortions in these figures:** they move with the ad-market cycle and with currency; they vary by several-fold *within* a market by niche; Q4 seasonality (`benchmarks.md` §9) applies on top and is stronger in high-RPM markets; and Shorts RPM compresses the spread — Shorts rates are low nearly everywhere, so the multiplier matters far less for a Shorts-heavy channel.

## 3. Computing an adjusted RPM

Weighted average across the audience geography mix.

```
Adjusted RPM = Σ (audience share in market m × US niche RPM × multiplier for m)
```

**Worked example.** Education channel. `benchmarks.md` §9 Education band, take the midpoint of $8–15 → **$11.50 US baseline**. Audience mix from Analytics:

| Market | Share | Multiplier | Contribution |
|---|---|---|---|
| Brazil | 60% | 0.16 (midpoint) | 0.60 × 11.50 × 0.16 = **$1.10** |
| United States | 15% | 1.00 | 0.15 × 11.50 × 1.00 = **$1.73** |
| Portugal (≈ Spain/Italy band) | 10% | 0.40 | 0.10 × 11.50 × 0.40 = **$0.46** |
| Other / long tail | 15% | 0.20 (conservative) | 0.15 × 11.50 × 0.20 = **$0.35** |
| **Adjusted RPM** | | | **≈ $3.64** |

Two things this example teaches. First: the unadjusted figure ($11.50) is more than **3× wrong**, and a creator planning against it will be badly disappointed. Second: 15% of the audience produces **48%** of the ad revenue. That is why a creator in a low-RPM market should look hard at whether they have a viable high-RPM audience segment — and why sponsorship, products and memberships (`monetization-guide.md` §1) are the primary streams in most non-US markets, not ads.

**Presentation rules:** always give a range, never a point estimate — apply the low and high ends of each multiplier and report both. Always state the confidence (`C`) and that the figures need verification. And always tell the creator that their own Analytics RPM, once they are monetized, replaces this entire calculation.

## 4. Finding audience geography

In YouTube Studio: **Analytics → Audience** for top geographies (and top subtitle/CC languages), and **Analytics → Revenue** for the actual per-market breakdown once monetized. The revenue tab is the ground truth — it shows realized RPM by country and makes every table in this file unnecessary for that channel.

Without Studio access, ask the creator for: top 5 countries with percentages, top subtitle languages, and (if monetized) realized RPM for the last 28 days. That is the minimum input for §3. See `data-sources.md` for the API paths and their fallbacks.

**Do not infer geography** from the creator's location, the channel's language, or the niche. Ask, or read it.

## 5. Language-specific SEO

**Why direct keyword translation fails.** A keyword is a phrase people actually type, not a meaning. Translating an English keyword yields a grammatically correct phrase that may be searched by nobody, because:

| Failure mode | Example shape |
|---|---|
| The market borrows the English term | Technical and product terms often stay English even in non-English queries |
| The natural local phrasing differs | The translated noun phrase is correct but people search a verb phrase, or vice versa |
| Regional variants split the volume | The same language differs across countries — the dominant term in one is unused in another |
| Formal vs colloquial register | Dictionaries return the formal word; searchers type the slang |
| Question structure differs | Some languages front the question word; some drop it entirely in search |
| Diacritics and spelling | Searchers type without accents; both forms need covering |
| Compound-word languages | One long compound may be the real keyword, not the three-word phrase |

**Method for non-English keyword research:**
1. Start from the *concept*, not the English keyword.
2. Get candidate phrasings from a native speaker or from the target language's own autocomplete — type the seed into YouTube search set to that language and read the suggestions.
3. Check the local SERP: search the candidate and see whether ranking videos are actually about that topic. If they are not, the phrase is wrong.
4. Cross-check with search-volume data localized to the *country and language*, not just the language (`data-sources.md`).
5. Look at what the top local channels in the niche actually title their videos — the working keyword set is already visible in the market.
6. Keep both the translated term and any borrowed English term where both are in use; put the dominant one in the title, the other in the description.

**Hashtag conventions differ too:** some markets use English hashtags on non-English content; some have strong local tag conventions; some barely use hashtags. Copy the convention from top-performing local channels rather than translating English tags. Limits stay as in `benchmarks.md` §6 regardless of language.

## 6. Character counts by script and language

Title and description truncation limits in `benchmarks.md` §6 are **character** limits, but characters carry very different amounts of meaning by script. The functional consequences:

| Script / language group | Effect vs English | Practical adjustment |
|---|---|---|
| Chinese, Japanese, Korean | Each character carries far more meaning; a title says much more in the same count | Write shorter; the front-load window holds a complete promise. Do not pad to fill the limit. |
| Japanese mixed scripts | Kana runs longer than kanji for the same meaning | Prefer kanji where natural for compactness |
| German, Dutch | Compounds run notably longer than English | Front-load harder; the keyword may consume most of the mobile-visible window |
| Portuguese, Spanish, Italian, French | Typically ~15–30% longer than the same English sentence | Cut articles and connectives; state the promise first |
| Russian, Polish, other Slavic | Longer, with inflected endings that resist shortening | Lead with the noun that carries the keyword |
| Arabic, Hebrew (RTL) | Similar length; direction affects reading order | Put the hook at the *start* in reading order; verify rendering on mobile |
| Thai, Vietnamese | Diacritics and no-space segmentation affect display | Test truncation on a real device |
| Hindi and other Devanagari | Longer than transliterated Latin | Decide deliberately between native script and Latin transliteration — check what the audience searches in |

**Thumbnail text is the sharper constraint.** The 5-words-max / 3-ideal guidance in `benchmarks.md` §7 is about *reading time under one second*, not word count. In CJK, 3–5 characters can carry what 5 English words do — use fewer marks, larger. In languages that run long, 5 words will not fit legibly at mobile size: cut to 2–3 words and let the image carry more. Never shrink the type to fit more text; that fails the one-second test in every language.

**Always verify by rendering,** not by counting. Preview the title on a phone in the target language before publishing.

## 7. Speaking rate and script length by language

**`~140 words/minute` is the English baseline and nothing more.** It is the figure in `benchmarks.md` §3, and `benchmarks.md` scopes itself to a United States, English-language sample. Applied to any other language it produces a script that is systematically too long or too short, and every downstream estimate built on it — runtime, hook word budget, per-beat allocation, chapter timestamps — inherits the error.

**Why the rate differs.** Languages differ in *rhythm class*. Stress-timed languages (English, German, Russian, Arabic) compress unstressed syllables, so a word carries more time on average. Syllable-timed languages (Spanish, Italian, French, Portuguese, Turkish) give each syllable roughly equal duration and are typically spoken faster in syllables per second. Mora-timed languages (Japanese) are faster still by the same measure. Information density moves in the opposite direction — a faster language usually carries less meaning per syllable — so **two languages can convey the same content in a similar runtime while differing by 30% or more in words per minute.** Runtime converges; word count does not. That is exactly why a word-count formula cannot be shared across languages.

**Word count is the wrong unit for some languages entirely:**

| Language group | Why words fail | Use instead |
|---|---|---|
| German, Dutch, Finnish, Hungarian | Heavy compounding and agglutination — one written "word" can be a full English phrase | Syllable count, or a timed read |
| Japanese, Chinese, Thai, Khmer, Lao | Written without spaces; "word count" is an artefact of whichever tokenizer ran | Characters per minute (kana/hanzi), or a timed read |
| Korean | Spaced, but heavily agglutinative | Either, but verify against a timed read |
| Arabic, Hebrew | Clitics attach to the host word; orthographic words undercount | Syllable count, or a timed read |

**Directional speaking rates — confidence `C — directional, verify by timing a real recording`.** Measured-style narration, neither rushed nor slow. Ranges, never point estimates.

| Language | Rate | Unit | Notes |
|---|---|---|---|
| English | 130–150 | words/min | The `benchmarks.md` §3 baseline |
| Spanish | 150–180 | words/min | Syllable-timed; among the fastest by syllable rate |
| Portuguese | 145–175 | words/min | Brazilian and European variants differ audibly |
| Italian | 145–175 | words/min | |
| French | 140–170 | words/min | Liaison makes word boundaries a poor timing guide |
| Indonesian | 130–155 | words/min | |
| Russian | 120–145 | words/min | Long inflected words; fewer of them per minute |
| Polish | 120–145 | words/min | Consonant clusters slow articulation |
| Turkish | 120–145 | words/min | Agglutinative — few words, each long |
| Hindi | 125–150 | words/min | Devanagari; transliteration inflates counts |
| Arabic | 115–140 | words/min | Orthographic words undercount spoken units |
| German | 110–135 | words/min | Compounds make this the least comparable word figure of any Latin-script language |
| Korean | 110–140 | words/min | Cross-check against ~250–350 characters/min |
| Japanese | 300–400 | characters/min | Mora-timed; count kana, not words |
| Mandarin Chinese | 220–280 | characters/min | Count hanzi; each carries roughly a syllable |

**The reliable method, which beats every row above.** Have the creator read **200 words of their own script** — their real script, in their real delivery, not a sample paragraph — and time it with a stopwatch. Then:

```
personal rate = 200 ÷ (seconds elapsed ÷ 60)
```

Use that number for every length calculation on that channel from then on, and re-derive it if the format or the delivery changes. It absorbs the language, the dialect, the creator's natural pace, and their editing style in one measurement. A creator's own rate commonly sits 20–30% away from any table value, which is larger than the differences between most languages in the table — so **the personal rate is the primary instrument and the table is only the fallback when no recording exists yet.** For a language in the character-count rows, read 200 characters instead and divide the same way.

**Presentation rule:** whenever a rate from the table above reaches a creator, say it is directional confidence `C` and offer the 200-word timing test in the same breath. Never present a table row as a measurement of their channel.

## 8. Sponsorship rates by market

Sponsorship rates diverge by market *less* than ad rates, because a sponsor is buying trust and audience action, not impressions — but they still diverge, and differently.

| Factor | Effect |
|---|---|
| Local brand budgets | Track the local ad market; broadly follow the §2 direction, though usually with a **narrower** spread than ad RPM |
| Global brands targeting a local market | Pay closer to their global rate — often several times what a local brand pays for the same slot |
| Market maturity | In markets where influencer marketing is newer, rates are less standardized: both underpayment and surprisingly high one-off deals are common |
| Audience purchasing power | Brands selling a physical product price by expected conversions, so purchasing power matters directly |
| Currency risk | A deal quoted in a volatile local currency loses value between signature and payment |
| Diaspora and cross-border audiences | A local-language channel with a large audience in a high-income country can charge global rates — this is frequently missed |

**Practical rules:** quote global brands in a hard currency and local brands in local currency; price against *the market the sponsor sells into*, not the channel's home market; when the audience spans both a low-RPM home market and a high-income diaspora, lead the media kit with that segment (`monetization-guide.md` §7); and apply all deliverable and rights multipliers from `monetization-guide.md` §5 unchanged — those are structural, not regional. **But they are directional heuristics, not measured rates** (`monetization-guide.md` §5, Confidence: C): present them to a creator as a range with the assumptions stated, never as a quoted rate. Being region-independent does not make them measurements.

## 9. Disclosure law by region

High-level regional character is in `monetization-guide.md` §11. The localization-specific rules:

- **The audience decides which law applies,** not the creator's residence. A channel based in one country with a large audience in another can be subject to both.
- **Apply the strictest applicable standard.** It is always compliant to over-disclose.
- **Disclose in the language the audience is watching in.** An English disclosure on a non-English video does not disclose to anyone.
- **A multi-language channel needs the disclosure in every audio track and every subtitle track**, not only the original.
- **Local wording matters.** Several regimes have specific accepted terms; a literal translation of an English phrase may not satisfy them.
- **The platform's paid-promotion toggle is insufficient everywhere.** No exceptions.
- **Verify locally and say so.** Never present this file, or `monetization-guide.md`, as legal advice.

## 10. Multi-language audio tracks and translated subtitles

The strongest growth lever available to an already-produced catalogue, because production cost is sunk.

| Lever | Cost | Upside | Risk |
|---|---|---|---|
| Corrected captions in the original language | Low | Accessibility, indexing, and the base for every translation downstream | None — do this first, always |
| Translated titles and descriptions | Low | Discovery in the target language; frequently the single highest-return step | Keyword translation failure (§5) — research, do not translate |
| Translated subtitle tracks | Low–medium | Reach in subtitle-tolerant markets | Machine translation of humour and idiom reads badly |
| Multi-language audio tracks | Medium–high | Native listening on the *same* video, keeping its accumulated authority and watch time | A poor dub damages trust more than no dub |
| Fully localized separate uploads | High | Maximum per-market control | Fragments catalogue, audience and analytics (§11) |

**Sequence:** correct the original captions → translate titles and descriptions for the one or two markets already visible in Analytics → subtitles for those markets → audio tracks only where the data justifies it. Localize toward audiences that already exist; never on a hunch. Multi-language audio is strictly better than a separate re-upload when available, because one video keeps all the signal instead of splitting it.

**Dub quality gate:** a dub must preserve pacing and emphasis, not just words. If the dubbed track cannot hold the hook's energy in the first 15 seconds, it will fail the retention curve regardless of translation accuracy.

## 11. One multi-language channel or several

| Choose ONE channel with multi-language tracks when | Choose SEPARATE channels when |
|---|---|
| The content is identical across languages | Content genuinely differs per market (local examples, local regulation, local products) |
| The catalogue is small or the creator is solo | There is a dedicated person or team per language |
| You want each video to keep all its accumulated authority | Branding, thumbnails and cadence must differ per market |
| Analytics should stay interpretable in one place | Sponsors are local and want a single-market channel |
| Cadence would collapse if split | Each language can independently sustain the cadence |

**Default: one channel.** Splitting divides watch time, subscribers and algorithmic signal across two cold starts, and most creators cannot sustain two cadences. The strongest argument for splitting is not language — it is that the *content itself* must differ. If the same video works in both markets, keep one channel.

**Middle path:** one main channel with multi-language audio, plus a clips channel per language if Shorts volume justifies it. Lower risk than a full split and reversible.

## 12. Cultural adaptation of hooks and humour

| Travels well | Travels poorly |
|---|---|
| Curiosity gaps and open loops | Sarcasm and irony — frequently read as sincere |
| Numbers, results, before/after | Wordplay and puns — untranslatable by construction |
| Visible demonstration | Pop-culture and celebrity references |
| Universal problems (money, time, health, skill) | Regulatory, tax and legal specifics |
| Stakes and risk | Regional politics and history |
| Emotional reaction shots | Local measurement units, currencies, date formats |
| Direct statements of benefit | Self-deprecation — read as low status in some cultures |
| Contrarian claims about a shared belief | In-group slang and generational references |

**Adaptation rules:** localize the *example*, keep the *structure* — a hook framework transfers even when its content does not. Replace units, currency and dates with local equivalents every time. Check directness calibration: a hook that reads as confident in one culture reads as arrogant in another, and one that reads as polite in a second reads as weak in the first. Never translate a pun — replace it with a different device that does the same job. And test with one native speaker before committing a series to a framing; a single reader catches most of these.

## 13. Decision rules

- **If** the audience is not majority US → no `benchmarks.md` §9 revenue figure is quoted without applying §2–3 of this file first.
- **If** audience geography is unknown → get it before any revenue estimate. Ask for the top 5 countries with percentages. Never infer it from creator location, language or niche.
- **If** the channel is already monetized → its realized RPM in Studio replaces every table here. Use it.
- **If** quoting an adjusted RPM → give a range from the low and high multipliers, state confidence `C`, and say it needs verification.
- **If** a small high-RPM segment produces most of the revenue → say so explicitly; it usually changes the content strategy.
- **If** the market multiplier is below roughly 0.25 → ad revenue is not a viable primary stream. Lead with sponsorship, product and memberships (`monetization-guide.md` §1).
- **If** doing keyword research in a non-English market → never translate the English keyword. Start from the concept and use local autocomplete, the local SERP, and local channels' titles.
- **If** writing a title in a language that runs longer than English → cut connectives and front-load harder; the mobile-visible window has not grown.
- **If** writing thumbnail text in CJK → fewer marks, larger. **If** in a long-running language → 2–3 words, not 5. Never shrink the type.
- **If** pricing a sponsorship → price against the market the sponsor sells into, not the creator's home market; quote global brands in a hard currency.
- **If** the channel has a high-income diaspora audience → lead the media kit with it and charge accordingly.
- **If** disclosing → in the audience's language, in every audio and subtitle track, to the strictest applicable market's standard.
- **If** localizing content → correct the original captions first, then titles and descriptions, then subtitles, then audio. Follow existing audience signal, never a hunch.
- **If** asked one channel or several → default to one with multi-language audio; split only when the content itself must differ per market.
- **If** adapting a hook → keep the structure, replace the example, localize units and currency, never translate a pun, and have a native speaker read it.
- **If** any figure from this file is challenged → concede immediately that it is directional confidence `C` and offer to verify. Never defend it as measured data.
