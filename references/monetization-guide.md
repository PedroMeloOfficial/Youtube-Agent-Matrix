# Monetization Guide

**Purpose.** Method for building a revenue stack: sequencing toward the Partner Program, pricing a sponsorship instead of guessing, placing mid-rolls, designing membership tiers, doing product-funnel arithmetic.

**Benchmark numbers live in `benchmarks.md` §9** — RPM bands, YPP thresholds, splits, penalties. This file never restates *benchmark* data. It does originate a small number of **structural pricing heuristics** — the deliverable, rights and exclusivity multipliers in §5 and the funnel conversion rates in §10. Those are reasoning scaffolds, not measurements, and each is labeled `Confidence: C` where it appears. For any non-US audience, convert §9 through `localization-guide.md` first; §9 is US-baseline.

**Contents:** 1 Revenue stack · 2 Sequencing to YPP · 3 Ad mechanics · 4 Mid-rolls · 5 Sponsorship pricing · 6 Contracts & negotiation · 7 Media kit · 8 Memberships · 9 Affiliate · 10 Funnel arithmetic · 11 Disclosure law · 12 Payouts · 13 Readiness checklist · 14 Decision rules

## 1. Revenue stack

Seven streams. **Their ranking inverts by archetype** — the most misunderstood thing in creator monetization. A commentary channel and a B2B tutorial channel with identical views have near-inverted income statements.

| # | Stream | Revenue driver | Scales with |
|---|---|---|---|
| 1 | Ad revenue | Advertiser demand for the audience | Views × RPM |
| 2 | Sponsorship | Trust + audience buying power | Views × niche rate |
| 3 | Memberships / patron platforms | Parasocial attachment | Superfan count |
| 4 | Tips (Super Chat / Thanks) | Live presence, personality | Live hours |
| 5 | Affiliate | Purchase intent while watching | Commercial-intent views |
| 6 | Own product | A viewer problem you can solve | Email list size |
| 7 | Services / speaking | Authority | Reputation, not views |

Rank 1 = largest expected share. Use it to decide what to build first, not as a forecast.

| Archetype | 1st | 2nd | 3rd | Weak / skip |
|---|---|---|---|---|
| Tutorial / educational (search intent) | Own product | Affiliate | Ads | Tips |
| B2B / software / finance | Sponsorship | Ads | Own product | Tips, memberships |
| Entertainment / commentary | Ads | Memberships | Sponsorship | Affiliate |
| Gaming / live | Tips | Memberships | Sponsorship | Ads (low RPM) |
| Vlog / lifestyle | Sponsorship | Affiliate | Ads | Own product |
| Review / consumer tech | Affiliate | Sponsorship | Ads | Memberships |
| Documentary / video essay | Memberships | Ads | Sponsorship | Affiliate |
| Faceless / compilation | Ads | Affiliate | — | Memberships, tips (no parasocial hook) |

**Why it inverts.** Ads pay per view regardless of relationship; memberships and tips pay per *relationship* regardless of views; products pay per *problem solved*. Ask whether the viewer feels they know the creator or that the creator solved something — the ranking falls out of the answer.

### 1a. Taxonomy and precedence

This guide and the 14 archetype templates use **two different names for the same seven streams**.
They are the same taxonomy; map them one-to-one before comparing anything.

| This guide (§1) | Archetype template §7 label | Note |
|---|---|---|
| Ad revenue | AdSense | Long-form ad revenue only — Shorts is broken out separately, see below |
| Sponsorship | Brand deals | Same stream |
| Memberships / patron platforms | Memberships | Same stream |
| Tips (Super Chat / Thanks) | Super Chat / Thanks | Same stream |
| Affiliate | Shopping affiliate | Same stream |
| **Own product** | **External funnels** | *(see below — one template label covers two guide rows)* |
| **Services / speaking** | **External funnels** | *(same — merged into External funnels)* |
| *(sub-line of ad revenue here)* | **Shorts ad share** | Promoted to a peer stream in the templates |

**Two deliberate mismatches:**

- **"External funnels" covers both "Own product" and "Services / speaking."** The templates merge
  them because they share one mechanism — moving the viewer off-platform to something the creator
  owns — and one prerequisite: an email list or a direct channel. "Services / speaking" therefore
  has no separate row in any template; it lives inside External funnels.
- **"Shorts ad share" is broken out from AdSense in the templates** because its economics differ by
  roughly an order of magnitude (`benchmarks.md` §9). Folding it into ad revenue, as §1 does, hides
  the single most common revenue miscalculation in this system. The two are separate lines in a
  template ranking and are **not** double-counted: AdSense means long-form ad revenue, Shorts ad
  share means the Shorts pool.

**Precedence — which ranking wins.**

> **The archetype template's §7 ranking is authoritative for a specific channel.** The §1 table
> above is a **coarse default**, for use only when no archetype has been classified yet.

The §1 table's rows are broad categories ("Gaming / live", "Entertainment / commentary") that
collapse several archetypes into one line; a template's §7 is written against one archetype, with
its actual volume, RPM band and production model in view. **Where the two disagree, the template
wins.** Do not renumber a template to match this table.

**Gaming is the clearest example.** §1 marks ads "weak / skip" for *Gaming / live*, while
`gaming.md` §7 ranks AdSense **#1**. The template is right: gaming sits in the lowest RPM band
(`benchmarks.md` §9), so per-view value genuinely is poor — but an enormous volume of
mid-roll-eligible watch time against that low band still makes ad revenue the **largest single
line** for the archetype. A weak *rate* and the largest *total* are not a contradiction. The §1
row is really describing a live-first channel, where watch hours are concentrated in streams and
tips dominate.

## 2. Sequencing toward YPP

Thresholds for both tiers: `benchmarks.md` §9. The tiers are a sequence, not a gate to wait at.

| Phase | Goal | Do this |
|---|---|---|
| Pre-Expanded | Reach tier 1 | Publish volume. Very small channels get real algorithmic promotion (§4) — spend it. |
| Expanded reached | Turn on non-ad streams | Memberships, tips, Shopping. None need the Full tier. |
| Between tiers | Pick the faster path | Watch-hours vs Shorts-views — choose one and optimize deliberately. |
| Full reached | Turn on ads | Mid-rolls only past the length threshold (§3–4). |
| Post-YPP | Diversify off-platform | Ads are the least controllable stream. Build email + product early. |

**Choosing the path.** Watch-hours if AVD is above channel norm, a long-form catalogue exists, capacity favours low volume / high polish, and the post-YPP plan is ads or product. Shorts-views if vertical clips already exist, turnaround is fast, and the plan is sponsorship or funnelling to long-form. **Warn explicitly:** the Shorts path satisfies YPP but generates very little ad revenue afterward (§9 Shorts RPM) — reaching Full tier via Shorts and expecting long-form income is the most common disappointment in this system.

**Hygiene.** Both tiers need 2-step verification, no active strikes, linked AdSense. Review takes about a month — keep publishing through it. Usual rejection causes: reused or templated content, no original commentary, metadata that misrepresents the video.

## 3. Ad revenue mechanics

| Format | Placement | Skippable | Creator control |
|---|---|---|---|
| Skippable in-stream | Pre / mid / post | After ~5s | On/off + mid-roll positions |
| Non-skippable in-stream | Pre / mid | No | On/off |
| Bumper | Pre / mid | No, short | On/off |
| In-feed / discovery | Search + suggested | n/a | On/off |
| Shorts feed ads | Between Shorts | Swipe | Pool-based, no placement control |

Enable every format initially. Disable non-skippables only if retention shows a drop exactly at an ad position, and only on that video.

**Limited ads is a classification, not a penalty.** Usual causes, with the script moment they enter through: strong profanity in the opening line; graphic recounting of a crime, injury or accident; sexual content even discussed clinically; ongoing conflict, tragedy or sensitive events; unsafe stunts, DIY or challenges; firearms handling or modification; recreational drug depiction.

**Avoidance, in script order:** (1) keep the first 30 seconds clean — early profanity carries outsized classification weight; (2) use the clinical word, not the slang; (3) keep the shocking detail out of title, description and thumbnail — that is what the classifier reads first; (4) isolate an unavoidable segment so it can be cut for a re-upload.

**Self-certification.** Answer honestly on every upload. Accurate certification builds a channel-level trust record and speeds reviews; misreporting permanently costs the benefit of the doubt. If a video is limited and certification was accurate, request review — accurate creators win reviews often.

## 4. Mid-roll placement strategy

Mid-rolls unlock past the length threshold in `benchmarks.md` §3, which also holds the revenue effect of crossing it.

| Video length | Mid-rolls | Rationale |
|---|---|---|
| Under threshold | 0 (unavailable) | — |
| Threshold to ~10 min | 1 | One break is nearly free in retention terms |
| 10–15 min | 2 | Space them, do not cluster |
| 15–25 min | 3–4 | Roughly one per 5–6 min |
| 25 min+ | One per 5–7 min | Past ~6 breaks, complaints outpace revenue |

**Spacing:** never under ~3 minutes apart, never in the first 3 minutes, never in the last 60 seconds. Automatic placement violates all three — switch to manual on any video worth the effort.

**Where in the script.** Put a break **immediately after a resolution and immediately before an open loop.** A viewer who just got a payoff and has been promised the next one sits through an ad; a viewer interrupted mid-explanation leaves.

| Good position | Bad position |
|---|---|
| After a section conclusion | Mid-sentence or mid-demonstration |
| Right after a cliffhanger line | Anywhere in the hook |
| At a hard visual transition / before a new chapter | On an emotional peak, or inside a step-by-step sequence |

**Workflow:** mark candidates in the script as `[AD BREAK]` while writing (instruct the script agent to do this), then align to timestamps in the editor. Never place mid-rolls off a waveform.

**The tradeoff, honestly.** A break earns its place when marginal revenue exceeds watch-time loss × downstream algorithmic value. Search-driven evergreen: be conservative — it earns for years and retention protects its ranking. One-off trending video earning out in 72 hours: be aggressive. Check the retention curve (§2) — a break sitting on an existing drop-off charges you for that drop twice.

## 5. Sponsorship: pricing a deal

Never quote a number the brand suggested first, and never quote from a rate calculator. Price from a defensible CPM basis.

```
Base price = (expected views ÷ 1,000) × sponsor CPM
```

- **Expected views** = *median* of the last 10 comparable videos over 90 days. Median, not mean — one outlier inflates the quote and you underdeliver.
- **Sponsor CPM ≠ ad CPM.** It is what a brand pays per thousand delivered views for an endorsement, set by niche buying power. Anchor from the channel's ad RPM band in §9; sponsor CPMs sit at a multiple of it because the brand buys trust, not impressions. Any deal the creator actually closed beats every derivation.
- **Delivery window:** quote against 30-day views and say so in the contract. A brand wanting lifetime views counted is asking for a discount.

**Deliverable multipliers** (compound onto base):

| Deliverable | Multiplier | Note |
|---|---|---|
| Shorts mention only | 0.3–0.5× | Low dwell, low intent transfer |
| 30–60s integration | 1.0× | The baseline |
| 90s+ integration with demonstration | 1.3–1.6× | Real production work |
| Dedicated video | 2.5–4× | The whole video is the ad; costs goodwill |
| Multi-video package | −10 to −20% | Volume for guaranteed slots |
| Pinned comment, description link, community post | +5–10% each | Cheap to give — never give free |

**Rights and exclusivity multipliers** — where creators lose the most money by not charging:

| Term | Multiplier | Why |
|---|---|---|
| Organic only | 1.0× | Baseline |
| Whitelisting / paid amplification | +30–100% | They are buying media now, not content |
| Perpetual usage rights | +50–100% | The asset never expires — price it as a buyout |
| Usage capped at 6–12 months | +10–25% | Reasonable, cheap |
| Category exclusivity, 3 mo / 12 mo | +20% / +50–100% | Price as lost competitor revenue, explicitly |
| Broad vertical exclusivity | Usually decline | Unpriceable for a growing channel |
| Right to re-cut your footage | +25% | Your face in someone else's edit |
| Likeness in the brand's own ads | +50%+ | Talent licensing, not sponsorship |

**Confidence: C — directional heuristic, not measured data. Re-verify against current market rates before quoting a creator.** Both multiplier tables above are structural
heuristics originated in this file — they encode *what to charge for*, not what the market
currently pays. They are not in `benchmarks.md` and no measurement backs the specific
percentages. Present them to a creator as a range with the assumptions stated, never as a quoted
rate.

**Worked example (structure, not a rate card).** Median 30-day views 40,000 → base = 40 × sponsor CPM. Brand wants a 90-second integration (×1.4), 6-month whitelisting (×1.5), 6-month category exclusivity (×1.2). Combined **×2.52**. Quote that, then negotiate down by removing rights — never by cutting the base.

## 6. Contracts and negotiation

| Red-flag clause | Problem | Response |
|---|---|---|
| Payment per click/sale only | Creator takes all risk, brand all upside | Flat fee + bonus |
| Net-90 or later | Cash-flow killer for a solo creator | Net-30; 50% upfront on large deals |
| Perpetual worldwide all-media rights, unpriced | A buyout disguised as sponsorship | Price it or time-limit it |
| Unlimited revisions | Uncapped labour | Cap at 2 rounds, extras billed |
| Pre-publish approval, no deadline | Your calendar becomes theirs | 5-business-day window, deemed approved after |
| Broad indemnification of the brand | You insure their product claims | Limit to your own conduct |
| Guaranteed views or engagement | You cannot control the algorithm | Refuse, or make-good on the *next* video |
| Brand controls disclosure wording | Disclosure liability is yours (§11) | Non-negotiable — creator controls it |

**Sequence.** (1) Let them name a budget: "What range are you working with?" (2) Quote a range; the low end is a stripped deliverable. (3) Concede scope, not price. (4) Bundle upward: "below my rate for one video, but it works as a three-video package." (5) Get the timeline before agreeing — rush fees (+20–30%) are legitimate.

**Walk when:** the creator would not use the product or cannot verify its claims; the brand insists on controlling disclosure; the fee is below the goodwill cost and they will not move; terms exceed net-60 with nothing upfront; the category conflicts with a stated channel value. One misaligned deal costs more trust than the fee is worth — and trust is the input to every other stream in §1.

## 7. The media kit

One page, PDF, refreshed quarterly. **Positioning** — one sentence on who the channel serves and what they get. **Audience** — age/gender split, top countries, interests, taken from Analytics and never guessed. **Reach** — subscribers, monthly views, and *median* views per video, labelled as the median. **Engagement** — comment and like rates, average view duration. **Past partners** — logos, or "available on request"; never fabricate. **Case study** — one deal with a measured result. **Packages** — 2–3 named packages with price *ranges*, not one number. **Process** — turnaround, revision policy, approval window. **Contact** — a business email, not a form.

**Exclude** RPM and ad revenue; they tell a buyer what you would settle for. **Feature** audience geography prominently: a brand selling in one market is buying that market's share of the audience, not the total (`localization-guide.md`).

## 8. Memberships and tier design

Splits, price range and maximum tier count: `benchmarks.md` §9.

**Why 2–3 tiers beats many.** Each extra tier adds a decision, and decision cost suppresses conversion more than price does. It also multiplies perk-delivery work — the failure mode of memberships is not low sign-ups, it is a creator drowning in promised monthly perks across five tiers (`community-guide.md`, sustainability). Three is the ceiling for a solo creator.

| Tier | Price posture | What belongs behind it | Delivery cost |
|---|---|---|---|
| 1 — Support | Lowest | Badge, emoji, name in credits, members-only posts | Near zero |
| 2 — Access | ~3× tier 1 | Early access, substantive members-only posts, monthly Q&A or stream, behind-the-scenes | Bounded, batchable |
| 3 — Proximity | ~10× tier 1 | Direct channel, priority questions, topic input, occasional group call | Caps out fast — cap the seats |

Tier 1 must be purely symbolic (any real work makes it unprofitable at scale) · never move existing free content behind a tier — add, don't subtract · never surface members-only content to non-members · cap the top tier's seats explicitly ("20 spots" is scarcity *and* self-protection) · perks that scale beat perks that don't.

## 9. Affiliate strategy

Commission ranges: §9. The strategy question is placement and intent, not rate.

| Video intent | Fit | Approach |
|---|---|---|
| "Best X for Y" / comparison | Highest | Link every option, including the one not chosen |
| Tutorial using tools | High | Link only what appears on screen |
| Single-product review | High | Link, and disclose before the verdict |
| Entertainment, commentary, news, opinion | Low | Do not force it |

Link only what the creator actually uses — one bad recommendation poisons the whole list. Put links where intent peaks: top of description *and* pinned comment. Maintain one evergreen gear/tools page and link to it, so a discontinued product means editing one page rather than 200 descriptions. Attribution windows make evergreen videos the best affiliate assets — another reason to refresh them (`repurposing-guide.md`). Affiliate links require disclosure (§11), not just cash deals.

## 10. Product funnel arithmetic

The most common monetization mistake is planning a product without this arithmetic. Write it out with the creator's real numbers.

```
Monthly views                                V
  × description-CTA click rate    c₁         (typical 0.5%–2%)
= landing page visits             V·c₁
  × landing-page opt-in rate      c₂         (typical 20%–40%)
= new emails per month            V·c₁·c₂
List size L × launch purchase rate c₃        (typical 1%–3%)
  × price P  = launch revenue     L·c₃·P
```

**Confidence: C — directional heuristic, not measured data. Re-verify against current market rates before quoting a creator.** The three conversion ranges (`c₁`, `c₂`, `c₃`) are
directional defaults for making the arithmetic runnable before real data exists. They are not in
`benchmarks.md` and are not measurements of this channel. Replace each with the creator's own
observed rate as soon as one exists, and label any projection built on the defaults as an
assumption.

**Worked example.** 100,000 monthly views · 1% CTA click = 1,000 visits · 25% opt-in = **250 emails/month** = 3,000/year. On a 3,000 list, 2% purchase at $200 = 60 × $200 = **$12,000 per launch**, twice a year.

What it teaches: the bottleneck is almost always `c₁`, which is a *scripting* problem (a spoken, specific CTA at a moment of demonstrated value), not a product problem · list size, not views, is the revenue variable — a 100k-view channel with no list has no product business · price is a multiplier, so a higher-priced offer to a smaller list usually wins, but only if the audience has the problem · run it *backwards* from a revenue goal to find the required list size before building anything.

**Gate before building:** can the creator name 10 specific viewer comments describing the exact problem the product solves? If not, demand is assumed, not observed. Mine comments first (`community-guide.md`).

## 11. Disclosure law

**Rule zero: the platform's paid-promotion toggle is not sufficient in any jurisdiction.** It supplements a disclosure; it never replaces one.

US FTC placement, timing and penalty: `benchmarks.md` §9. The method is to disclose **clearly, conspicuously, and before the endorsement**, in the medium the audience is consuming.

| Region | Regime character | Practical implication |
|---|---|---|
| United States | FTC Endorsement Guides, per-violation penalties | Verbal + on-screen + written |
| United Kingdom | Advertising regulator + consumer law, published influencer guidance | Prominent label at the start; specific accepted wordings |
| European Union | Consumer-protection directives applied nationally; some states stricter | Varies by member state — "the EU" is not one rule |
| Brazil | Advertising self-regulation + consumer-protection code | Explicit advertising labelling expected |
| Canada / Australia | Consumer regulators with influencer guidance | Similar in substance to the US |
| Elsewhere | Assume a regime exists | Verify before publishing |

Always: plain words in the audience's language (not a hashtag alone, not an abbreviation) · before the endorsement · on all three surfaces · apply the strictest rule among the markets the audience actually comes from, judged by *audience* geography not creator location (`localization-guide.md`) · tell the creator to verify local law and never present this file as legal advice · disclose affiliate links, gifted products and creator-owned products, not only cash deals · synthetic or AI content carries its own disclosure obligation *in addition*.

## 12. Payout mechanics

| Item | What to tell the creator |
|---|---|
| Payment account | Ad revenue pays through a linked AdSense account, verified by mailed PIN before any payment |
| Threshold & schedule | Earnings accumulate to a minimum balance, then pay monthly after a finalization period; below threshold they roll over indefinitely |
| Currency | Paid in the account's currency; cross-border conversion and intermediary bank fees are routinely underestimated |
| Tax forms | A US tax form is required of **all** creators regardless of country, because payments route through a US entity; without it, maximum withholding applies |
| Withholding | Applied to the US-viewer share of earnings; a valid treaty claim usually reduces it substantially |
| Other streams | Memberships, tips and Shopping pay through the same account with their own splits (§9). Affiliate networks, patron platforms and product sales each have separate thresholds, schedules and fees — track separately, never blend |

File the tax form and treaty claim *before* the first payout; retroactive correction is slow. Separate business and personal accounts from the first dollar.

## 13. Readiness checklist by size tier

| Size | Enable now | Build now | Not yet |
|---|---|---|---|
| Pre-Expanded | Nothing | Publishing consistency; email capture; an audience-problem list from comments | Sponsor outreach, product |
| Expanded | Memberships (2 tiers), tips, Shopping if available | Media kit v1; affiliate links on high-intent videos | Ads (unavailable), dedicated sponsor videos |
| Full, small | Ads + mid-rolls past threshold; self-certification discipline | Inbound sponsorship email; a rate anchored on §5 | Discounting below floor to land a first deal |
| Full, mid | All the above; third tier if capacity allows | Funnel arithmetic (§10); first digital product | Perpetual rights; broad exclusivity |
| Established | Full stack | A second income surface independent of the algorithm | Relying on ads as the majority stream |

**Diagnostic:** any single stream above ~60% of revenue is the channel's biggest risk, at any size.

## 14. Decision rules

- **If** below the Expanded tier → discuss publishing volume, not revenue splits. Nothing else matters yet.
- **If** asked "how much will I make" → require niche, audience geography and median views; convert §9 through `localization-guide.md`; give a range, never a point estimate.
- **If** the archetype is high-attachment / low-view → lead with memberships and tips, not ads. **If** high-intent and search-driven → lead with product and affiliate; ads are a byproduct.
- **If** the video is under the mid-roll length threshold → do not discuss mid-roll strategy; discuss whether the content honestly justifies crossing it.
- **If** placing mid-rolls → after a resolution, before an open loop; never in the first 3 minutes; never on an existing retention drop. Search-driven evergreen gets fewer breaks; trending and short-lived gets more.
- **If** pricing a sponsorship → median 30-day views × sponsor CPM, then deliverable and rights multipliers. Never quote before the brand names a budget. Whitelisting, perpetual rights and exclusivity are priced line items, never free add-ons.
- **If** negotiating down → remove scope and rights, never cut the base rate. **If** the brand wants disclosure control, performance-only payment, or guaranteed views → walk.
- **If** designing membership tiers → 2 to start, 3 maximum; tier 1 symbolic; cap the top tier's seats. **If** the creator wants a product → run §10 first and require 10 real comments naming the problem. No comments, no product.
- **If** anything monetized is placed → spoken + on-screen + written, before the endorsement, in the audience's language, to the strictest applicable market's standard.
- **If** the audience is majority non-US → no §9 figure leaves the room without `localization-guide.md` applied.
- **If** a needed figure is absent from `benchmarks.md` → "benchmark unavailable." Never estimate revenue and present it as data.
