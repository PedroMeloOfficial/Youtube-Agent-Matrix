---
market: US
display_name: United States
currency: USD
primary_languages: [en-US]
rpm_multiplier_vs_us: "1.0 — this market is the baseline"
confidence: B
last_reviewed: 2026-08-24
---

# United States — Market File

> **This file exists for what `benchmarks.md` leaves out.** `benchmarks.md` is written against this market, so every platform mechanic and every RPM band in it is *already* the US figure. None of it is repeated here. This file carries variation *inside* the US, the US ad calendar, US search phrasing, the US sponsorship market, US payment rails, and US disclosure law.

## 1. Market snapshot

"Baseline" means three structural things at once, and they cut both ways. **Highest advertiser competition.** More advertisers bid per viewer than in any other market — which is why `benchmarks.md` §9 is the ceiling other markets are measured against, not an average. Nothing here raises those bands; what moves US revenue is *which* US audience and *when*.

**Deepest sponsorship market.** US influencer marketing spend: **$10.5B (2025) → $13.7B (2027)**, `B` — [eMarketer](https://www.emarketer.com/content/influencer-marketing-set-surpass--13-billion-by-2027). An agency layer, settled contract norms and dedicated brand budgets let a small US channel transact at a professionalism level absent from most markets. Sponsorship, not ads, is where US scale pays. **Most saturated creator supply.** The same conditions attract creators: a US-targeting channel competes with the highest production budgets on the platform in nearly every category (§9).

| Structural fact | Implication |
|---|---|
| Baseline for all `benchmarks.md` figures | Never apply a multiplier to a US channel |
| USD, paid via AdSense | Payout mechanics: `monetization-guide.md` §12 |
| Federal disclosure regime, per-violation penalties | §7 — usually the strictest regime in any mix |
| 20 state privacy laws in force (2026) | §7 — rising, not settled (`B`, [MultiState](https://www.multistate.us/insider/2026/2/4/all-of-the-comprehensive-privacy-laws-that-take-effect-in-2026)) |
| Contiguous 48 states span 4 timezones | §8 — no single national prime time |

## 2. Revenue

**The numbers live in `benchmarks.md` §9 and are not restated.** RPM by niche, Shorts RPM, splits, membership and tip mechanics, brand-deal floors and the Q4/January headline are all US figures already. Applying a multiplier to them for a US channel is a bug, not a refinement. What §9 does not cover:

**2a. Regional variation inside the US — sub-national RPM is `unavailable`.** No public source gives RPM by state, region or DMA, and Analytics reports revenue only at country level though it reports *views* down to city level. Do not derive one.

| Known structurally | Conf. | Use |
|---|---|---|
| Advertisers bid on geography and audience segment, not on channels | `B` | Identical US view counts can carry materially different RPM |
| Political spend concentrates geographically (§3) | `B` | A regionally concentrated audience is more exposed in even years |
| Low-income-signal segments attract lower-value bids | `C` | Inference only — never quote a number for it |

Rule: treat "US" as one market for estimation, because that is the resolution the data exists at, and flag regional concentration as an unquantified risk instead of adjusting a figure.

**2b. US-resident vs US-*targeted* audience.**

| Case | Analytics geography | Who's paying |
|---|---|---|
| Viewers physically in the US, creator anywhere | United States | US bids — §9 applies in full |
| Creator in the US, viewers elsewhere | The other market | That market's rates; creator location is irrelevant (`_index.md`) |
| en-US content aimed at the US, watched abroad | Split | Split economics — blend per `_index.md` |

The third case is the trap — making content *for* the US does not make it a US channel; being watched in the US does. An en-US channel commonly lands 40–60% US with the rest spread across UK/CA/AU/IN — a long tail `_index.md` says to fold into the nearest market and disclose.

**2c. Why the same niche pays differently under B2B vs consumer framing.** §9 splits Tech into B2B/SaaS and consumer reviews; the mechanism behind that split generalises and is not in §9.

| Lever | Effect | Same topic, reframed |
|---|---|---|
| Buyer is a business with a budget line | Higher advertiser LTV per conversion | "best laptop" → "best laptop for a dev team of 10" |
| Viewer holds purchase authority | Higher | consumer how-to → practitioner workflow |
| Content sits near a decision, not near entertainment | Higher | "reacting to X" → "choosing between X and Y" |
| Audience is hobbyist / entertainment-seeking | Lower | any Tier-1 topic covered as commentary |

This is how a channel moves between §9 tiers without changing subject. It is a positioning decision (`channel-strategist`), not a revenue estimate. **`C` — structural heuristic, no measured US data. Never quote a tier change as projected revenue.**

## 3. Seasonality — the US ad calendar

§9 gives the Q4/Q1 headline. Below is the mechanism and the dates.

| Period | Driver | Effect on inventory | Conf. |
|---|---|---|---|
| January | Budgets reset, retail spent out | Cheapest of the year (§9) | `B` |
| Jan 26 – Apr 15 | Filing season opened **Jan 26 2026**, deadline **Apr 15 2026** | Finance/tax/software bid hard | `A` — [IRS](https://www.irs.gov/newsroom/irs-opens-2026-filing-season) |
| Feb–Apr | Spring retail, home improvement | Recovery toward baseline | `C` |
| May–Jun | Graduation, summer travel booking | Travel and consumer firm up | `C` |
| Jul–Aug | **Back-to-school** — second-largest US retail season | Education, tech, apparel rise | `B` |
| Sep–Oct | Product cycles, pre-holiday brand building | Building toward Q4 | `C` |
| **Late Nov** | Thanksgiving → Black Friday → Cyber Monday | Peak commercial bidding | `A` |
| Nov 1 – Dec 31 | US online holiday spend **$257.8B** in 2025, +6.8% YoY | This *is* the §9 Q4 peak | `B` — [Adobe](https://news.adobe.com/news/2026/01/adobe-holiday-shopping-season) |
| Late Dec | Spend holds, attention fragments | High CPM, softer view volume | `C` |

**Cyber Week magnitudes** (`B`, Adobe, 2025): Thanksgiving→Cyber Monday **$44.2B** online (+7.7%) · Cyber Monday **$14.25B**, the largest US e-commerce day · Black Friday **$11.8B** (+9.1%). These are *retail* figures — the demand signal producing the §9 CPM peak. Never cite them as CPM data. **The political-advertising cycle (even years).** Verified, not folklore. US federal elections fall in even years; 2026 is a midterm.

| Fact | Value | Conf. |
|---|---|---|
| Projected 2026 cycle political ad spend | **$11.07B**, +21.4% vs the 2022 midterm | `B` — [eMarketer](https://www.emarketer.com/content/11b-midterm-ad-race-may-drive-record-cpms-key-battlegrounds) |
| Independent projection, same cycle | **$10.8B**, "most expensive midterm on record" | `B` — [AdImpact](https://adimpact.com/political-projections-26) |
| Digital share | **$3.84B** digital, **$2.70B** of it CTV (+194% vs 2022) | `B` — eMarketer |
| Mechanism | Campaigns are deadline-bound and price-inelastic; they **outbid commercial advertisers** for programmatic, social and streaming inventory before Election Day | `B` — eMarketer |
| Concentration | Battlegrounds absorb it disproportionately (one state projected >$1B) | `B` — eMarketer |
| Election Day 2026 | Tue **Nov 3 2026**; squeeze peaks in the ~8 preceding weeks | `A` |

**The collision:** the political peak (Sep–early Nov, even years) lands immediately *before* the commercial Q4 peak, so Aug–Dec is bid-competitive end to end. Displacement raises CPM as a side effect — it does not lower it — but it tightens brand-side sponsorship budgets in those weeks because brands are being priced out of paid media. **Creator-side magnitude: `unavailable`. Do not quantify it.** **Scheduling** (for `calendar-agent`): high-monetization and sponsored content → Oct–Dec · experiments and format tests → January · finance/tax → published *before* Jan 26, harvested through mid-April · education and family → Jul–Aug · sponsor outreach → Aug–Sep for Q4 slots (Q4 budgets commit weeks ahead) and January for annual-budget conversations.

## 4. Search and discovery — US English

`seo-playbook.md` mechanics apply unchanged; phrasing is what's US-specific. All rows `C` — linguistic patterns, not measured volume.

| Modifier pattern | Form | Intent |
|---|---|---|
| Comparison | `X vs Y`, `X or Y`, `is X worth it` | Pre-purchase |
| Superlative | `best X for Y`, `top X`, `X ranked` | Category entry |
| Year-stamped | `X in 2026`, `2026 X guide` | Freshness filter — refresh annually |
| Beginner | `how to X for beginners`, `X 101`, `X explained` | Education |
| Speed / effort | `X in 5 minutes`, `easy X`, `X without Y` | Low commitment |
| Skeptical | `does X actually work`, `X honest review`, `is X a scam` | Trust-seeking, high retention |
| Problem-first | `why is my X doing Y`, `how to fix X` | Support, evergreen |
| Cost | `how much does X cost`, `X on a budget` | Commercial |

**US vs UK/AU divergence** — targeting the US in UK/AU vocabulary silently splits search volume, and the on-screen term must match the query:

| US | UK / AU | US | UK / AU |
|---|---|---|---|
| `-ize`/`-yze` (organize, analyze) | `-ise`/`-yse` | `college` | `uni` |
| `color`, `favorite`, `traveling` | `colour`, `favourite`, `travelling` | `résumé` | `CV` |
| `math` | `maths` | `soccer` | `football` |
| `cell phone` | `mobile` | `fall` | `autumn` |
| `vacation` | `holiday` | `candy`, `cookie` | `sweets`, `biscuit` |
| `apartment` | `flat` | `check` (payment) | `cheque` |
| `gas` | `petrol` | `aluminum` | `aluminium` |

**US-only institution terms** — using them signals US targeting and captures US-only volume: `401(k)`, `IRS`, `W-2`, `1099`, `HSA`, `Medicare`, `HOA`, `DMV`, `ZIP code`, `Black Friday`, `back to school`, `spring break`. **Rules:** pick one spelling convention per channel and hold it (mixed matches neither market) · put the US term in the title, the alternate in the description only if the mix justifies it · never localise a US institution term — `401(k)` has no British equivalent and translating it destroys the query · year-stamped titles need an annual refresh pass (`repurposing-guide.md`).

## 5. Sponsorship landscape

**Pricing mechanics are `monetization-guide.md` §5** — CPM basis, deliverable multipliers, rights and exclusivity multipliers — and negotiation is §6 there. Not restated. Below is the US market structure those mechanics run inside. No sponsorship rate figures appear in this file; `benchmarks.md` §9 holds the only brand-deal numbers this system quotes. Currency USD, invoiced; net-30 is the reasonable ask and agency procurement opens at net-60 or later.

| Channel | Represents | Character | Creator posture |
|---|---|---|---|
| Direct brand, in-house creator team | Itself | Fast decisions, visible budget, brand owns the relationship | Best margin; needs a media kit and an inbound business email |
| Talent / influencer agency | The **creator** | Commission on deals it sources | Worth it only above the volume a solo creator can service |
| Media / buying agency | The **brand** | Standard briefs, procurement timelines, net-30 to net-60 | Expect contracts and insurance questions; slower payment |
| Creator marketplace | Neither | Low floor, high volume, price-compressed | Fine for a first deal; never a rate anchor |
| Affiliate → sponsorship escalation | — | Creator proves conversion first | Strongest position available to a small channel |

**Media kit** (contents: `monetization-guide.md` §7). US-specific expectations on top — one-page PDF · **median** views, labelled as median, because a US buyer will ask · audience geography broken out, since a US-only advertiser buys only the US share · explicit brand-safety posture (categories refused) · business email on a real domain · turnaround and revision policy, asked for in the first procurement email.

**Usage-rights norms** (priced in `monetization-guide.md` §5):

| Term | US expectation | Watch for |
|---|---|---|
| Organic-only integration | Default unless stated | Contract silence is not "organic only" |
| Whitelisting / paid amplification | Common, expected to be paid separately | Ad rights granted with no fee named |
| Perpetual worldwide all-media | Routinely requested by large brands | A buyout in disguise — price it or time-limit it |
| Category exclusivity | Standard ask, 3–12 months typical | Vertical-wide exclusivity, which is unpriceable |
| Creator controls disclosure wording | **Non-negotiable** — liability is the creator's (§7) | Brand-supplied "approved" disclosure copy |

## 6. Off-platform monetization — US rails

**Headline take-rates already in `benchmarks.md` §9** (Patreon, Substack, Amazon Associates, YouTube memberships and Shopping) are cited, not restated. Below: the rails §9 does not carry, and the fee *mechanics* it omits. Publicly stated vendor pricing at the review date; decays fast, re-verify before quoting.

| Rail | Published US terms | Conf. | Source |
|---|---|---|---|
| Stripe, standard online card | 2.9% + $0.30 · +1.5% international cards · +1% currency conversion | `A` | [stripe.com/pricing](https://stripe.com/pricing) |
| PayPal Checkout, domestic commercial | 3.49% + $0.49 | `A` | [PayPal fees](https://www.paypal.com/us/business/paypal-business-fees) |
| PayPal standard card payments | 2.99% + $0.49 · micropayments 4.99% + $0.09 · +1.50% international | `A` | PayPal fees |
| Gumroad, direct / profile sales | **10% + $0.50** per transaction | `A` | [gumroad.com/pricing](https://gumroad.com/pricing) |
| Gumroad, Discover marketplace sales | **30%** per transaction | `A` | Gumroad |
| Gumroad, tax posture | Merchant of record since Jan 1 2025; collects and remits sales tax at no extra cost | `B` | Gumroad |
| Patreon, standard plan (pages created after Aug 4 2025) | 10% platform fee | `A` | [Patreon](https://support.patreon.com/hc/en-us/articles/11111747095181-Creator-fees-overview) |
| Patreon, legacy plans still in force | Founders 5% · Pro 8% · Pro + Merch 11% | `A` | Patreon |
| Patreon processing, USD | Card/Apple Pay 2.9% + $0.30 · PayPal/Venmo US 2.9% + $0.30, non-US 3.9% + $0.30 | `A` | Patreon |
| Patreon payout, USD | $0.25 per direct deposit · PayPal 1%, min $0.25, cap $20 | `A` | Patreon |
| Substack, on top of its cut | Stripe 2.9% + $0.30 **plus a 0.7% recurring-billing fee** | `A` | [Substack](https://support.substack.com/hc/en-us/articles/360037607131-How-much-does-Substack-cost) |
| Kajabi | Basic $179/mo · Growth $249/mo · Pro $499/mo (−20% annual); processing 2.7–2.9% + $0.30 by plan | `B` | [kajabi.com/pricing](https://kajabi.com/pricing) |
| Teachable | Starter $39/mo with **7.5%** transaction fee · Builder $89/mo 0% · Growth $189/mo 0%; processing separate | `B` | [teachable.com/pricing](https://teachable.com/pricing) |
| Kit (ex-ConvertKit) | Newsletter free to 10,000 subs · Creator $33/mo · Pro $66/mo at 1,000 subs; commerce fee **3.5% + $0.30** | `B` | [kit.com/pricing](https://kit.com/pricing) |
| Amazon Associates | Category-fixed schedule, not negotiated: Luxury Beauty 10% · Books & Kitchen 4.5% · Toys/Home/Sports 3% · TVs 2% · Grocery & Health 1% · gift cards 0% | `A` | [Fee schedule](https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ) |

**What the tables teach.** Fees stack: a Substack subscription pays Substack *and* Stripe *and* the recurring-billing fee; a Teachable Starter sale pays 7.5% *and* processing. Compare rails on **net per dollar collected**, never on headline percentage. A flat-monthly platform beats a percentage platform above a volume crossover — compute it with the creator's real numbers using `monetization-guide.md` §10 before recommending a migration. Amazon's schedule is why §9's affiliate range is so wide: the rate is set by *product category*, so niche selection decides affiliate economics before a link is ever placed.

## 7. Disclosure and legal

**Placement, timing, the three required surfaces and the penalty figure are in `benchmarks.md` §9; the comparative-regime table is `monetization-guide.md` §11.** Neither restated. This is the mechanics US creators get wrong.

**Material connection** — a relationship a "significant minority of consumers would not expect" that could affect how they weigh the endorsement (`B` — [FTC Endorsement Guides FAQ](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking)). Not limited to cash:

| Triggers disclosure | Note |
|---|---|
| Cash, or free / discounted product | Any free product, including low-value items |
| Affiliate commission | Including an unused link left in an old description |
| Employment or business relationship | Listing an employer on a profile page is **not** sufficient |
| Family or close personal relationship | Material however obvious it seems to the endorser |
| Creator's own product, or equity in the brand | Ownership is a material connection |
| Contest entry, press trip, event access, loaned gear | Anything of value received |

**"Clear and conspicuous."** The 2023 revised Guides define it by **placement** (where viewers actually look), **readability** (legible, contrasting, on screen long enough) and **clarity** (plain words an ordinary viewer understands) — "easily noticeable, easily understandable, and hard to miss" (`B`, FTC FAQ). Operationally: visual content requires a visual disclosure, audio requires an audible one, both together is the safe form · an end-of-video disclosure is presumptively missable · live content needs periodic repetition because viewers arrive mid-stream · a hashtag alone, an abbreviation or a term of art is not plain language. **Platform toggle:** It supplements and never replaces a disclosure — the FTC places "the ultimate responsibility … on the influencer and the brand, not the platform" (`B`, FTC FAQ). Rule zero in `monetization-guide.md` §11; the US is where it carries a per-violation penalty (`benchmarks.md` §9). Brand and creator are both liable, and a contract cannot assign the creator's liability away — which is why brand control of disclosure wording is a walk-away term (§5).

**COPPA and made-for-kids:**

| Fact | Detail | Conf. |
|---|---|---|
| Audience setting | Mandatory per channel and per video; declared, not inferred from intent | `A` |
| Consequence of MFK | Personalised ads off; comments, notifications, end screens and several monetization surfaces restricted — hence the MFK gap in `benchmarks.md` §11 | `B` |
| Thumbnail A/B testing | Unavailable for MFK content (`benchmarks.md` §7) | `A` |
| Amended COPPA Rule | Effective June 2025; **full compliance deadline Apr 22 2026** — now in force | `B` — [Finnegan](https://www.finnegan.com/en/insights/articles/coppas-amended-rule-is-now-in-full-effect-what-operators-need-to-know.html) |
| Mislabelling | Risk runs both ways; labelling kid-directed content as general-audience is the enforcement exposure | `B` |

Determination is about the *content* — subject matter, characters, animation style, music, activities. A channel does not escape MFK by asserting an adult audience. **State privacy laws:** **20 states** have comprehensive consumer privacy laws on the books in 2026; Indiana, Kentucky and Rhode Island took effect Jan 1 2026, more on Jul 1 2026 (`B`, [MultiState](https://www.multistate.us/insider/2026/2/4/all-of-the-comprehensive-privacy-laws-that-take-effect-in-2026)). Most thresholds sit above a solo creator, but exposure begins the moment there is an **email list, a course platform or a storefront** collecting personal data — the §6 rails, not the channel. Rhode Island shows how low a bar can sit: 35,000 consumers, or 10,000 if >20% of revenue comes from selling personal data. Age-appropriate design codes are a stricter separate overlay wherever a product touches minors. **Not legal advice:** Tell the creator to verify with counsel before a first paid deal, before launching a list or storefront, and before publishing anything kid-directed.

## 8. Publishing rhythm

| Zone | Share of US population | Offset from ET |
|---|---|---|
| Eastern | ~47% | — |
| Central | ~33% | −1h |
| Pacific | ~14% | −3h |
| Mountain | ~5% | −2h |
| Alaska + Hawaii | ~1% | −4h / −5h |

*`C` — commonly cited population-share breakdown ([RPS](https://www.rpsrelocation.com/blog/data-visualization/american-cities-by-time-zone/)). Directional, not a scheduling formula.*

ET and CT together are ~80% of the population and sit one hour apart, so one slot serves both; the Pacific coast is three hours behind and cannot be served by the same slot. The standard compromise is publishing early enough to be live before the Eastern morning and still fresh for the Pacific evening. **Publish at one fixed local time and hold it** — the first distribution wave (`benchmarks.md` §5 testing cascade) fires against a warm audience whose habit you are training, and consistency is worth more than a theoretically optimal hour. **DST:** US DST runs second Sunday in March → first Sunday in November (2026: **Mar 8 → Nov 1**) (`A`). Two complications: most of Arizona and all of Hawaii do not observe it, so their offset from the rest of the country changes twice a year; and the US and Europe switch on *different dates*, giving a mixed US/EU audience two multi-week windows a year where the gap is off by an hour. Automated scheduling must use a fixed **local** zone (`America/New_York`), never UTC — a UTC-fixed schedule silently shifts the audience-facing time twice a year.

| Weekly window | Character | Conf. |
|---|---|---|
| Tue–Thu | Highest routine consumption; default for evergreen and search content | `C` |
| Fri | Attention turns to the weekend; lighter formats | `C` |
| Sat–Sun | Longer sessions, more TV-surface viewing; favours long-form | `C` |
| Mon | Weakest slot in most niches | `C` |
| Mid-Nov → early Jan | Travel and gatherings fragment weekday patterns | `C` |

Directional priors only. **The creator's own "when your viewers are on YouTube" report overrides every row above** (`analytics-guide.md`).

## 9. Competitive landscape

The most saturated market on the platform, with two consequences pointing opposite ways.

**Against the creator:** a US-targeting channel competes with the highest production budgets in the world. In the best-paying §9 categories — finance, business, B2B tech, legal, real estate — incumbents include funded media companies, agency-run creator brands, and firms treating YouTube as customer acquisition where the video need not be profitable on ad revenue at all. Beating that on production value is not a plan. **For the creator:** saturation is a *broad-level* phenomenon. It thins fast with specificity, and US market depth means a narrow segment is still large enough to sustain a channel — the structural advantage this market offers a small creator.

| Category | Saturation | Where room remains |
|---|---|---|
| Personal finance, general | Extreme | A named situation: one profession, one life stage, one system |
| Business / entrepreneurship | Extreme | Operator-level specifics instead of motivation |
| Consumer tech reviews | Extreme (production-cost war) | Long-term ownership, repair, niche workflows |
| Gaming | Extreme | Format innovation, not title selection |
| Health & fitness | High | Constraint-specific programming; credentialed depth |
| Education | High | Curriculum- or exam-aligned series |
| DIY / home improvement | Moderate | Regional building conditions, real cost accounting |
| B2B software / practitioner tooling | Moderate | Role-specific workflows — smallest audience, best §9 tier |
| Local / regional US topics | Low | Geography as the moat; sponsorship is local but real |

*All `C` — structural judgement, no saturation index measured. `competitor-analyst` validates against live search results before any positioning recommendation.* **Notes:** format arbitrage — a format proven in another market or category brought to a US niche that has not seen it — is the cheapest edge and needs no budget · a credential or a job the audience cannot get elsewhere beats production value · the highest-RPM §9 tiers are highest *because* they are most contested, so the tier table is a competition map as much as a revenue map · a channel that cannot win on production competes on specificity, cadence (`benchmarks.md` §4), or access.

## 10. Decision rules

- **US channel → never apply an RPM multiplier.** `benchmarks.md` §9 is already the US figure; applying `localization-guide.md` double-counts.
- **Any US revenue figure → cite `benchmarks.md` §9.** This file holds no RPM, CPM or brand-deal numbers, by design.
- **Audience geography decides, not creator location** (`_index.md`). "Made for the US" is not a US channel; "watched in the US" is.
- **Sub-national US revenue asked for → `unavailable`.** No state, region or DMA data exists. Flag regional concentration as unquantified risk; never derive a figure.
- **Q4 monetization → sponsor outreach lands Aug–Sep**, because Q4 budgets commit weeks before the spend. January is for experiments (§3).
- **Finance or tax content → publish before Jan 26**, so it is indexed when filing season opens (§3).
- **Even-numbered year, Sep–early Nov → warn about political displacement** (§3), and attach no number to the creator-side effect.
- **Sponsored video → three surfaces, plain language, before the endorsement** (`benchmarks.md` §9); the toggle never counts as one of them (§7).
- **Brand wants to control disclosure wording → walk** (`monetization-guide.md` §6). US liability is the creator's and cannot be contracted away.
- **Free product, affiliate link, family tie or creator-owned product → disclose.** Cash is not the trigger; material connection is (§7).
- **Kid-directed content → MFK applies on content, not intent**, and it removes monetization and packaging surfaces (§7).
- **Creator runs a list, course or store → state privacy law is in scope** (§7). Recommend counsel; do not assess thresholds in a deliverable.
- **Comparing off-platform rails → compare net per dollar collected**, never headline take-rate (§6); run `monetization-guide.md` §10 before recommending a migration.
- **Scheduling → one fixed local publish time, never UTC** (§8); the creator's own Analytics overrides every prior here.
- **US spelling and vocabulary → one convention, held** (§4). Never localise a US institution term.
- **Mix includes the US alongside other markets → apply the strictest disclosure regime in the mix.** In most mixes that is the US.
