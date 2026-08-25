---
market: BR
display_name: Brazil
currency: BRL
primary_languages: [pt-BR]
rpm_multiplier_vs_us: "0.05–0.15 — sources disagree by ~3×; see §2 before quoting"
confidence: C
last_reviewed: 2026-08-24
---

# Brazil (BR)

Economics and culture only. Platform mechanics live in `benchmarks.md` and are cited, never restated; `benchmarks.md` §9 is the US RPM baseline §2 contrasts against. This file **supersedes** `localization-guide.md`'s BR multiplier row (0.10–0.22, `C`) wherever it carries a sourced figure. **FX:** USD/BRL 2026 high 5.52 (1 Jan), low 4.91 (11 May), average **5.16** — `B`, [exchange-rates.org](https://www.exchange-rates.org/exchange-rate-history/usd-brl-2026). AdSense pays in USD and converts, so BRL revenue moves with FX independently of views.

## 1. Market snapshot

Brazil is a **volume market with a compressed monetization curve**: an enormous, near-universally reachable audience at one of the lowest per-view ad rates of any large economy, and — the part that actually changes strategy — a *far narrower spread between well-paid and badly-paid niches than the US* (§2). Ad revenue is therefore rarely a primary stream at any channel size, and "pick a high-RPM niche" buys much less here. The compensating advantage is unusually mature off-platform infrastructure: instant payments (Pix), a large domestic infoproduct economy, and a R$3.5bn influencer-marketing market. Sponsorship and product monetize a Brazilian audience roughly an order of magnitude better than ads do (§5 vs §2).

| Fact | Value | Conf. | Source |
|---|---|---|---|
| Internet users | 185M, 86.9% penetration (end 2025) | `B` | [DataReportal 2026 BR](https://datareportal.com/reports/digital-2026-brazil) |
| YouTube ad-reachable audience | **150M** — 70.4% of population, 81.1% of internet users | `B` | same |
| Mobile connections | 217M (102% of population) | `B` | same |
| Median mobile download | 239.43 Mbps (Aug 2025), +228% YoY | `B` | same |
| Digital ad spend 2025 | R$42.7bn, +12.7% YoY; **video = 49%** | `B` | [IAB Brasil/Kantar via Conversion](https://www.conversion.com.br/blog/iab-brasil-publicidade-digital-42-bilhoes-2025) |
| Programmatic share of digital buying | ~70% | `C` | [AdSeleto citing IAB/Kantar](https://adseleto.com/mercado-programatico-no-brasil-em-2026/) |
| 2026 ad-market growth forecast | 9.1% vs 5.1% global — fastest of 12 major markets (Dentsu) | `C` | [AdSeleto](https://adseleto.com/mercado-programatico-no-brasil-em-2026/) |
| CTV reach 2024 | 64% of population (Comscore) | `C` | [AdSeleto](https://adseleto.com/mercado-programatico-no-brasil-em-2026/) |
| Influencer-marketing market 2026 | R$3.5bn | `C` | [Estado de Minas](https://www.em.com.br/trends/2026/06/7442820-quanto-custa-contratar-um-influencer-no-brasil-veja-a-tabela-de-precos.html) |
| Rank in global YouTube audience | **`unavailable`** — widely asserted 2nd/3rd; no primary source located | — | — |
| BR-specific mobile share of views | **`unavailable`** (`benchmarks.md` §7's 70%+ is global) | — | — |

**Connection quality is no longer a constraint** at the median — "optimize for low bandwidth" is stale advice for the mainstream BR audience. Mobile *share* of consumption still governs packaging.

## 2. Revenue

**Sources disagree by ~3×, and that disagreement is the finding.**

| Source | BR CPM | BR RPM | Ratio to that source's own US figure | Conf. |
|---|---|---|---|---|
| [Lenos](https://www.lenostube.com/en/youtube-cpm-rpm-rates/) (upd. Apr 2026) | $1.14 | $0.58 (self-labelled estimate) | US $32.75 / $10.81 → **0.054** | `C` |
| [TubeAnalytics](https://www.tubeanalytics.net/benchmarks/brazil) (rev. Jun 2026) | $2.80 avg | $1.40 avg | no US table given | `C` |
| [Fluxnote](https://fluxnote.io/guides/youtube-cpm-brazil) (2026) | $1.50–4.00 typical | — | — | `C` |
| [Unclik](https://unclik.com.br/conteudos/quanto-ganha-um-youtuber/) (Feb 2026) | R$1–5 | — | — | `C` |
| `localization-guide.md` §2 (superseded) | — | — | 0.10–0.22 | `C` |

No source publishes sample size or method; TubeAnalytics explicitly calls its figures "directional editorial benchmarks, not official YouTube averages". **Do not average these into one number.**

**The one measured data point located.** A Brazilian creator publishing full AdSense screenshots for calendar 2025 — ≈17k subs, creator-education niche, BR audience, 1.5M monetized views May–Dec — [Criadores em Ação](https://criadores.vip/quanto-ganhei-com-o-youtube-2025-shorts-videos-longos/):

| Metric | Value | Conf. |
|---|---|---|
| Long-form RPM | **R$7.89** (≈US$1.53 at 5.16) | `C` — single self-reported case |
| Shorts RPM | **R$0.29** (≈US$0.06) | `C` — same |
| Gross / net 2025 | R$673.27 / R$553.21 | `C` |
| Long-form ÷ Shorts | **27×** — inside `benchmarks.md` §9's 10–100× band | `C` |

Shorts economics are **not** materially worse in BR than globally — Shorts rates are floor-bound nearly everywhere, so the market multiplier matters much less for a Shorts-heavy channel.

**Niche curve — single source (TubeAnalytics 2026), `C` throughout.**

| Niche | BR CPM | BR RPM | US RPM band (`benchmarks.md` §9) |
|---|---|---|---|
| Finance & Investing | $4.50 ↑ | $2.40 | $20–40+ |
| Technology | $3.80 ↑ | $2.00 | $15–25 B2B / $6–12 consumer |
| Education | $2.80 → | $1.50 | $8–15 |
| Health & Wellness | $2.50 → | $1.30 | $8–15 |
| Beauty & Fashion | $2.30 → | $1.20 | $5–8 |
| Food & Cooking | $2.00 → | `unavailable` | $6–12 |
| Entertainment | $1.60 ↓ | `unavailable` | $2–5 |
| Gaming | $1.30 ↓ | $0.70 | $2–5 |

**`unavailable` for Brazil in every source found:** Legal/Real Estate, Digital Marketing, DIY/Home Improvement, Travel, Lifestyle, Music, and Business/Entrepreneurship as distinct from Finance.

**Shape, not level.** Within the TubeAnalytics table, BR Finance RPM ÷ BR Gaming RPM = **3.4×**. The equivalent US midpoint ratio in `benchmarks.md` §9 is ≈**8.6×**. *This compares two ratios inside their own sources; it is not a derived Brazilian figure.* Read directionally: the **BR niche curve is flat** — Gaming→Finance buys ~3× RPM in Brazil vs ~9× in the US; **low-tier niches are relatively less punished**, with BR Gaming and Entertainment sitting near the BR average rather than being the outlier disaster the US tier-3 label implies; and the **trends split**, Finance and Tech rising while Entertainment and Gaming fall (`C`, single source). The consequence is that niche choice in BR should be driven by **sponsorship CPM and product fit** (§5, §6), because ad RPM barely discriminates.

> **Never multiply a `benchmarks.md` §9 US band by a BR multiplier and present the result as Brazilian market data.** Where this file says `unavailable`, the answer is "unavailable". A multiplier may be quoted only *as a labelled multiplier*.

## 3. Seasonality

Not the US calendar with translated month names. The retail anchors differ, and the Southern-Hemisphere summer puts the vacation trough in **January**, on top of the post-Q4 budget reset. All rows `C`; CPM behaviour from [AdSeleto](https://adseleto.com/sazonalidade-cpm-publishers-guia-completo-2025/), dates from [Tray calendário comercial 2026](https://tray.com.br/escola/calendario-comercial/).

| Month | Demand | Drivers |
|---|---|---|
| Jan | **Floor of the year** | Budget reset + summer holidays + school break. AdSeleto: "queda de 30–40%", CPMs at "50–70% dos valores de novembro e dezembro" with traffic unchanged |
| Feb | Low, volatile | **Carnaval** (movable) — "padrões dramáticos de tráfego", desktop down / mobile up. A second national pause |
| Feb–Mar | Slow recovery | **Volta às aulas** — the school year starts in **February**, so back-to-school spend lands in Q1, the inverse of the US |
| Mar | Rising | **Dia do Consumidor (15/03)** — a real BR commercial date with no US analogue |
| Apr–May | Solid | **Dia das Mães (2nd Sun of May)** — top-3 retail date; AdSeleto flags it as a secondary CPM peak |
| Jun | Moderate | **Dia dos Namorados = 12 June, not 14 February.** Festas Juninas (24/06) |
| Jul | Trough | Winter school break; Q3 low point |
| Aug | Recovering | Dia dos Pais (2nd Sun of Aug) |
| Sep–Oct | Building | Dia das Crianças (12/10); Black Friday warm-up — "CPMs sobem 15–25% comparado a setembro" |
| **Nov** | **Peak** | **Black Friday** (last Fri). Desktop CPMs +~40% from mid-Nov; BF weeks "dobrem ou até triplicarem" vs annual average |
| Dec | High → collapse | Elevated through roughly the first three weeks, then near-total collapse after ~20 Dec |

> ⚠️ **AdSeleto reads partly translated from US publisher material** — "summer slump" for July, USD publisher revenue, June fiscal-year-ends that are not the Brazilian norm. Its *Brazilian* items (Carnaval, Dia das Mães, Black Friday) are credible; its Northern-Hemisphere framing is not.

**Contradiction to report.** AdSeleto claims an annual swing of "até 300% entre janeiro e novembro" (`C`). IAB Brasil/Kantar's 2025 AdSpend study reports the opposite trend — **seasonality flattening**, H1 and H2 near-balanced (20.8% vs 21.9% of annual spend as reported) — [Conversion](https://www.conversion.com.br/blog/iab-brasil-publicidade-digital-42-bilhoes-2025). The two are not strictly incompatible, since spend can shift channel rather than volume, but **do not quote 300% as fact**. Defensible statement: November peaks, January floors, magnitude disputed.

**Black Friday BR ≠ Black Friday US.** It is a **month-long** event ("esquenta" / "Black November"), not a weekend — publish buying-guide content from **late October**. Consumer distrust is deep and durable: a Reclame Aqui survey, n=23,500, found **48.8% call it "Black Fraude"**, with 27% of complaints in the referenced year being "propaganda enganosa" — [Serasa](https://www.serasa.com.br/premium/blog/black-friday-ou-black-fraude-pesquisa-aponta-desconfianca-do-consumidor/) (`C`, survey date not stated). Price-verification and "is this actually a discount" framings therefore outperform hype, and the high-intent research window opens in **September–October** ("um ou dois meses antes"). No Thanksgiving means no US-style pre-holiday lull and no Wed/Thu pattern.

**Scheduling rule:** high-monetization content Oct–Dec and Apr–May; experimental and evergreen Jan–Feb and Jul. Same principle as `benchmarks.md` §9 but with a **second trough in July** and a **Q1 back-to-school peak** the US calendar does not have.

## 4. Search and discovery

**No Brazilian YouTube keyword-volume dataset was located.** Everything below is structural and linguistic, confidence `C`, to be validated against pt-BR autocomplete and the local SERP (`localization-guide.md` §5). Comparative search volume for specific pt-BR phrases: **`unavailable`**.

| Modifier | Literal | Intent | Note |
|---|---|---|---|
| **"vale a pena"** | is it worth it | Purchase decision | Highest-commercial-intent BR modifier; no clean EN query equivalent |
| **"como fazer"** | how to make/do | Tutorial | The dominant how-to form; bare "como" splits across intents |
| **"passo a passo"** | step by step | Tutorial, beginner | Very common as a *title* term |
| **"do zero"** | from scratch | Beginner series | Standard BR course/tutorial convention; no EN title analogue |
| **"explicado" / "explicando"** | explained | Explainer | Direct analogue of EN "explained" |
| **"na prática"** | in practice | Applied demo | Signals "not theory" |
| **"o que é"** | what is | Definition | |
| **"antes de comprar"** | before you buy | Pre-purchase | Pairs with the Sep–Oct window (§3) |
| **"funciona mesmo?"** | does it really work | Skeptical verification | Ties to the distrust pattern in §3 |
| **"2026"** | — | Recency | Year-in-title at least as strong as in the US |

**review vs resenha vs análise.** **"review"** is a fully naturalized loanword and the standard term for product and tech video reviews — **do not translate it**. **"resenha"** carries an academic/literary connotation (a book or film critique, a school assignment) and pulls a different intent and audience. **"análise"** reads technical and in-depth — games, finance. Comparative volumes **`unavailable`**; structural note only (`C`), cf. [Pensata](https://pensata.medium.com/resenha-ou-review-8d376d6e56dd).

| English SEO advice | Why it fails in pt-BR |
|---|---|
| "Translate your keyword" | `review`, `setup`, `gameplay`, `marketing`, `mindset`, `home office` stay English *inside* pt-BR queries; translating produces a phrase nobody types |
| "Use the exact keyword string" | pt-BR is heavily inflected — gender and number agreement fragment one intent across many surface forms |
| "Front-load 40–50 chars" (`benchmarks.md` §6) | Still true, but pt-BR runs **15–30% longer** than the same EN sentence (`localization-guide.md` §6), so the mobile window holds less. Cut articles (`o/a/os/as`) and connectives |
| "Users type accents" | **Many do not**: `vídeo/video`, `você/voce`, `análise/analise`, `não/nao`. Accented form in the title, unaccented variant in the description |
| "One national spelling" | Wide regional and register variation; the informal register wins in search while dictionaries return the formal word |
| "Questions start with a question word" | pt-BR search often drops it — `melhor notebook custo benefício`, not `qual é o melhor…`. And pt-PT is not interchangeable with pt-BR |

Hashtags: copy the convention from top local channels rather than translating EN tags; limits unchanged (`benchmarks.md` §6).

## 5. Sponsorship landscape

**"Publi"** (from *publicidade*) is the settled Brazilian word for a sponsored piece, used by brands, creators and audiences alike — "fazer uma publi". `#publi` is also CONAR's canonical disclosure marker (§7). Use the word; it reads native.

YouTube-specific rate card, `C` — [Veeras, Mar 2026](https://veeras.com.br/blog/quanto-custa-contratar-influenciador-digital) (practitioner interviews, with Statista/HypeAuditor for market context):

| Tier | Integration (60–90s) | Dedicated video |
|---|---|---|
| Micro (10–50k) | R$1,500–6,000 | R$4,000–12,000 |
| Mid (50–200k) | R$5,000–20,000 | R$12,000–40,000 |
| Macro (200k–1M) | R$15,000–60,000 | R$40,000–120,000 |
| Mega (1M+) | R$60,000+ | R$120,000+ |

Cross-platform tiers, `C` — [Estado de Minas, Jun 2026](https://www.em.com.br/trends/2026/06/7442820-quanto-custa-contratar-um-influencer-no-brasil-veja-a-tabela-de-precos.html), which discloses AI assistance and names no research agency, so treat it as the weaker source: nano ≤10k Reels/TikTok R$300–2,000; micro 10k–100k Reels/TikTok R$2,000–8,000, with **finance-niche micro R$3,000–6,000 vs lifestyle R$1,500–3,000**; macro R$5,000–20,000/post; mega R$20,000+.

**Campaign CPM R$15–35**, reported independently by both sources (`C`). That is the *sponsor's* CPM — roughly an order of magnitude above the platform ad CPM in §2, and the entire argument for sponsorship-led monetization in Brazil. **Guaranteed minimums of R$2,000–5,000 per creator regardless of views** are reported at mid and macro tier (`C`, Veeras): Brazilian deals are more often flat-fee than view-indexed.

| | Local BR brands | Global brands buying BR |
|---|---|---|
| Currency | BRL, always | Often USD/EUR — **ask** |
| Level | The R$ tables above | Closer to their global rate; frequently a multiple of local for the same slot (`C`, structural — `localization-guide.md` §8) |
| Route | Direct or via a local agency | Global agency or local affiliate office |

**Payment terms are the defining friction:** market standard is **45–90 days post-publication**, with a reported worst case of 180 days; escrow platforms compress this to 24–48h after approval (`C` — [Veeras payments guide](https://veeras.com.br/pagamentos-influenciadores)). Materially worse than typical US terms — price the delay in. Deal rails: **Pix** (instant, 0–1% fee), TED above ~R$50k.

Invoicing structure determines take-home, not just admin (`C`, same source; not tax advice). **MEI** — simple nota fiscal but a hard **R$81,000** annual ceiling many creators outgrow. **PJ (LTDA/SLU)** — no ceiling, accepted by all brands, monthly compliance. **Pessoa física** — the payer withholds up to **27.5% IR + 11% INSS** via RPA, the worst net outcome. **Permuta** (gifted product) — no cash moves, but the stated value can be taxable and CONAR still treats it as advertising (§7).

## 6. Off-platform monetization

Brazil's off-platform stack is unusually strong, and it is the market's compensating advantage for §2.

| Infoproduct platform | Producer fee | Payout | Notes | Conf. |
|---|---|---|---|---|
| **Hotmart** | **9.9% + R$1.00/sale**; **20%** under R$10 | 30d free; **D+2 at 3.59%**, D+14 at 2.19% | Player fee R$2.49/txn (R$2.49 first + R$0.50 recurring). Card installment 3.49%/mo. Largest affiliate marketplace | `C` — [Tactus](https://tactus.com.br/taxas-da-hotmart-para-produtor/) |
| **Kiwify** | **8.99% + R$2.49/sale** | Pix/boleto **2d**; card ≤15d | **R$3.67 per withdrawal**, charged even on failed attempts. No monthly fee. Negotiable above R$50k/mo | `C` — [InvestFinance](https://investfinance.com.br/taxas-kiwify-para-2026-para-produtor-ou-afiliado/) |
| **Eduzz** | **`unavailable`** | — | Established, smaller than Hotmart | — |
| **Monetizze** | **`unavailable`** | — | Skews physical-product affiliate | — |
| **Braip** | **`unavailable`** | — | Skews physical/nutra affiliate; reputational risk in some verticals | — |

**Read the fee shape, not the headline.** Kiwify's lower percentage is offset by a higher fixed fee (R$2.49 vs R$1.00) plus a per-withdrawal charge — **Hotmart wins on low-ticket, Kiwify on high-ticket**. Compute per product; the crossover depends on price.

| Membership rail | Fee | Notes | Conf. |
|---|---|---|---|
| **Apoia.se** (recurring) | **13%** = 5% payment + 8% platform; creator keeps 87%; charged only if supported | The BR-native Patreon analogue; BRL, local payment methods | `B` — [Apoia.se](https://suporte.apoia.se/hc/pt-br/articles/219814327-Quanto-custa-usar-a-APOIA-se) |
| **Catarse** (project) | **13%**, of which ~4% payment/anti-fraud | Campaign-based, not recurring; funding model not stated on the fee page | `B` — [Catarse](https://crowdfunding.catarse.com.br/nossa-taxa) |
| **Patreon** | 10% + payment fees (`benchmarks.md` §9) | USD-denominated; international-card friction is a real conversion drag on a BR audience | `C` |
| **YouTube Memberships** | 30% (`benchmarks.md` §9) | Native, but the worst cut of the set | — |

**Rule:** a BRL-denominated, Pix-accepting rail converts a BR audience better than a USD/card rail even at a higher headline fee — Apoia.se at 13% typically out-earns Patreon at 10% here (`C`, structural).

**Payments.** **Pix** is the default consumer rail — instant, effectively free for individuals, universally expected; a checkout without Pix loses BR conversions. Current Banco Central adoption statistics: **`unavailable`** (source fetch failed at review). **Mercado Pago** is the dominant local gateway/wallet and the default in Mercado Livre flows. **Boleto** persists for the underbanked and for higher-ticket B2C. **Card installments ("parcelado")** drive purchase decisions in a way they do not in the US — R$1,200 priced as "12× R$100" converts materially better; the producer either absorbs ~3.5%/mo or shifts it to the buyer.

**Affiliates.** *Amazon Associados Brasil*: cookie **24 hours**, payout minimum **R$30**, paid monthly from around the 27th with a **2-month lag** (earned month A → paid month C); **category commission table `unavailable`** (`C` — [leandroabreu.com.br](https://leandroabreu.com.br/programa-de-afiliados-da-amazon/)). *Mercado Livre afiliados*: commission rates **`unavailable`** — searches surface seller-side *selling*-fee tables, which are a different thing entirely; do not confuse them. *Hotmart/Kiwify affiliate side*: commission is producer-set, and on Kiwify the affiliate is paid net of the producer's platform fee. The 24-hour Amazon BR cookie is short, so affiliate content must convert **in the first session** — which favours "vale a pena / antes de comprar" formats (§4) over awareness content.

## 7. Disclosure and legal

Three overlapping layers. **All three bind; the platform toggle satisfies none of them.**

**CONAR — Guia de Publicidade por Influenciadores.** Self-regulation, but with real teeth (public reprimand, mandated removal) and increasingly cited by PROCON and the courts as the diligence standard.

| Rule | Detail | Conf. |
|---|---|---|
| Version | Updated **May 2026**, effective **1 June 2026**, replacing the 2020 edition | `B` — [Abratel](https://abratel.org.br/conar-atualiza-guia-de-publicidade-por-influenciadores-digitais/), [Migalhas](https://www.migalhas.com.br/depeso/456129/guia-do-conar-de-publicidade-de-influenciadores-o-que-precisam-saber) |
| Trigger | **Editorial control removed as a criterion.** Now any **"compromisso recíproco"** between brand and creator, direct or via a representative. **Non-monetary incentives count — gifted product is advertising** | `B` — Migalhas |
| Affiliate links | Performance pay (clicks, sales) **does not** remove the advertising character; trackable links and commission coupons must be disclosed | `B` — Migalhas |
| Marker | **`#publi`** is canonical; also used in practice: `#publicidade`, `#parceriapaga`, `#ad`, or plain *"este conteúdo é patrocinado por…"* | `C` — Abratel, [Jurismenteaberta](https://jurismenteaberta.com.br/responsabilidade-de-influencers-e-youtubers-publicidade-disfarcada-e-vendas/) |
| Placement | Before the product is discussed (Instrução 22/2020 framing). **Precise 2026 placement/duration spec: `unavailable`** — obtain the PDF guide directly | `C` |
| Responsibility | **Shared** across brand, agency and creator; non-delegable | `B` — Migalhas |
| AI | Virtual influencers, avatars, animal personas and CGI characters **expressly covered**; AI-generated claims must be verified | `B` — Abratel, Migalhas |
| Minors | **"Hipertransparência"** required; judicial authorization referenced for minor influencers online; cross-references **ECA Digital (Lei 15.211/2025)** | `B` — Abratel, Migalhas |

**CDC — Código de Defesa do Consumidor** (statute, not self-regulation). All from [Jurismenteaberta](https://jurismenteaberta.com.br/responsabilidade-de-influencers-e-youtubers-publicidade-disfarcada-e-vendas/). **Art. 36** (`B`) — *"toda informação publicitária deve ser apresentada de forma clara e ostensiva"*: advertising must be immediately recognizable as such. **Art. 37** (`B`) — prohibits *publicidade enganosa e abusiva*; undisclosed commercial ties create a false impression of spontaneity and breach it. **Art. 49** (`B`) — 7-day right of withdrawal on online purchases, relevant to anything the creator sells directly. **Responsabilidade solidária** (`C`, single secondary source — verify before relying): courts have held creators **jointly liable** with the seller for harm from products they promoted, on the basis that profiting from a recommendation imports a *dever de diligência*; cited precedent **TJSP Apelação nº 1001234-89.2021.8.26.0100**. Enforcement (`C`): PROCON warnings, fines and mandated public retraction, plus civil damages both material and moral.

**This is the sharpest divergence from the US.** Under the CDC a Brazilian creator carries *product* liability exposure, not merely *disclosure* exposure. Promoting a defective or fraudulent product — a failing course, a bad supplement, an unlicensed financial offer — is a materially larger risk than the US FTC regime implies.

**LGPD (Lei 13.709/2018)** engages the moment the creator collects personal data directly: email lists, *sorteio* entries, community sign-ups, forms, WhatsApp lists. All `C`; general framing [Pora](https://www.usepora.com.br/blog/compliance-lgpd-marketing-influencia). A lawful basis is required, normally **specific informed consent** for marketing lists — no pre-ticked or bundled consent. Purpose must be stated at collection and the data not reused for another. Data-subject rights (access, correction, deletion) must be honoured. Sharing a list with a sponsor is a **transfer** and needs its own basis. Sanctions run to **2% of Brazilian revenue, capped at R$50m per infraction**. Not legal advice.

**Why YouTube's "paid promotion" toggle is not sufficient here.** (1) It renders a generic overlay only in the **first seconds** of playback, while CONAR requires identification clear *to that audience*, in Portuguese, where the commercial claim is actually met. (2) It does not appear in the **description**, in **community posts**, or in **clips and re-uploads**. (3) It is invisible to a viewer who joins mid-video or watches muted. (4) **It does not trigger at all** for the cases CONAR now expressly covers: affiliate links, commission coupons, and gifted product with no cash payment. (5) It is a platform feature, not a legal act — on its own it does not meet CDC art. 36's *clara e ostensiva* standard, and CONAR treats responsibility as shared and non-delegable.

**Minimum compliant practice:** toggle **on** + verbal pt-BR disclosure in the first 15–30s + on-screen `#publi` or *"Publicidade"* held ≥10s + a disclosure line in the **first two lines** of the description — in Portuguese, in every audio and subtitle track (`localization-guide.md` §9).

## 8. Publishing rhythm

| Fact | Value | Conf. |
|---|---|---|
| Population-centre timezone | **UTC−3** ("Horário de Brasília") — SP, Rio, Brasília, the Northeast, the South | `A` |
| Other zones | UTC−4 (AM, MT, MS, RO, RR), UTC−5 (Acre, western AM), UTC−2 (Fernando de Noronha) | `A` |
| **Daylight saving** | **Abolished in 2019 (Decreto 9.772/2019) and not reinstated — Brazil does not observe DST** | `A` |
| Scheduling rule | Schedule everything in **UTC−3**: the overwhelming majority of the audience is there and the offset never shifts | `A` |

**Often missed:** because Brazil dropped DST while the US and Europe kept it, the **BR↔US offset changes twice a year**. A mixed BR/US channel cannot hold one fixed publish time that suits both — pick the dominant market and let the other drift.

**Best publish hour: `unavailable` as measured BR data.** Every source located either restates US HubSpot data with the timezone swapped, or is a 2012-era Brazilian usage study far too old to use. The commonly cited *horário nobre* of **19h–22h BRT** is a broadcast-TV convention that plausibly transfers to online video, but it is `C` and unverified for YouTube specifically. **Weekly pattern for BR: `unavailable`** — check the channel's own data for two structural distortions before assuming a US-style week: Carnaval (a movable multi-day national pause) and the *feriado prolongado* culture around midweek public holidays. The reliable instrument is Studio → Analytics → Audience → "When your viewers are on YouTube". Cadence effects are platform mechanics and do not vary by market (`benchmarks.md` §4).

## 9. Competitive landscape

**No published saturation study of Brazilian YouTube was located.** Everything below is `C`, assembled from category-level commentary and structural reasoning — hypotheses for `competitor-analyst` to test against real search results, not findings.

| Category | State | Reasoning |
|---|---|---|
| Gaming / gameplay | Heavily saturated | Historically the largest BR category; decade-deep incumbent catalogues. §2 also marks CPM falling |
| Humour / entertainment / reaction | Saturated, monetizes worst | High supply, lowest CPM (§2), and falling |
| Podcast / long-form interview | Rapidly crowding | The 2023–2026 BR growth format; supply has caught demand. Viable, no longer empty |
| "Marketing digital / ganhar dinheiro online" | Saturated and low-trust | Huge infoproduct-driven supply against a skeptical audience (§3) |
| Beauty / lifestyle vlog | Saturated at top, fragmented below | Sponsorship-rich (§5) but the weakest micro-tier rates in the Estado de Minas table |
| Personal finance / investing | Competitive but expanding | Best BR CPM and rising (§2); micro finance creators command ~2× lifestyle sponsorship rates. Room in **sub-topics**, not general finance |
| **B2B / SaaS / professional software in pt-BR** | **Underserved** | High CPM tier, thin pt-BR supply, buyers with budgets. Clearest RPM-vs-competition gap in the market |
| **Regulated-professional explainers** (tax, labour, benefits, licensing, compliance) | **Underserved** | BR regulation changes constantly; content dates fast, which suppresses supply and rewards cadence. High intent, no competition from translated content |
| **Regional / non-Southeast** | **Underserved** | Production concentrates in SP/Rio; the North, Northeast and Centre-West are large audiences with thin native supply |
| **Trades, repair, agro, logistics** | **Underserved** | Large economic sectors, technical audiences, minimal video supply |
| **"Vale a pena" decisions on BR-available products** | **Underserved** | Global review content covers products not sold in Brazil, at prices and specs that do not apply — non-substitutable |

**Travels:** format structures and hook frameworks (`localization-guide.md` §12); universal problems (money, health, skill, time); numbers, demonstrations, before/after; software and SaaS tutorials. **Does not travel:** product recommendations, since BR availability, pricing and specs differ; anything tax, legal, benefits or regulatory — *and that is exactly the moat*; US/EU price points and salaries without purchasing-power framing; and payment or banking workflows, since Pix, boleto and parcelado have no foreign analogue.

**Structural opening for a small channel:** a flat ad-RPM curve (§2) plus a sponsorship CPM an order of magnitude above ad CPM (§5) means a small, *specific*, high-intent BR audience is worth far more to a sponsor than its ad revenue suggests. **Depth of niche beats breadth of reach in Brazil more than it does in the US.**

## 10. Decision rules

- **If** the mix contains BR → read this file, not `localization-guide.md`'s BR row. Say which you used.
- **If** quoting a BR RPM → give a **range**, tag `C`, name the source, and state that sources disagree by ~3× (§2). Never a point estimate.
- **If** the niche is not in §2's table → answer **"unavailable for Brazil"**. Do **not** multiply a `benchmarks.md` §9 US band by a multiplier and present the product as BR data; a multiplier may be quoted only *as a labelled multiplier*.
- **If** the channel is monetized → its realized Studio RPM replaces this entire section.
- **If** asked "which niche pays best in Brazil" → the BR ad-RPM curve is **flat (~3.4× top-to-bottom vs ~8.6× in the US)**; drive niche choice from sponsorship CPM and product fit, not ad RPM.
- **If** a BR channel is ad-revenue-led → flag it. BR sits below `localization-guide.md`'s 0.25 threshold on every source found: **ads are not a viable primary stream.** Lead with §5 and §6.
- **If** planning the calendar → high-monetization content **Oct–Dec** and **Apr–May**; experimental and evergreen **Jan–Feb** and **Jul**.
- **If** producing Black Friday content → start **late October**, treat it as month-long, and lead with price-verification framing (48.8% call it "Black Fraude").
- **If** the brief says "back to school" → that is **February** in Brazil. **If** it says "Valentine's" → **Dia dos Namorados is 12 June**; February is Carnaval.
- **If** doing keyword research → never translate the EN keyword; use pt-BR autocomplete and the local SERP. Keep naturalized loanwords (`review`, `setup`, `gameplay`) in English.
- **If** writing a title → front-load harder than the EN rule implies (pt-BR runs 15–30% longer); accented form in the title, unaccented variant in the description.
- **If** the topic is a product decision → prefer **"vale a pena"**, **"antes de comprar"**, **"funciona mesmo"**, and **"review"** over **"resenha"**.
- **If** pricing sponsorship → BRL to local brands, hard currency to global brands; assume **45–90 day** terms and price the delay in; prefer a **guaranteed minimum** over pure view-indexing, which is the local norm.
- **If** the creator is invoicing → flag the **MEI R$81,000 ceiling** and the ~38.5% withholding on *pessoa física* payments. Recommend a contador; give no tax advice.
- **If** the deal is **gifted product only**, or the video carries an **affiliate link or commission coupon** → it is advertising under CONAR's 2026 "compromisso recíproco" test. Disclose.
- **If** anything is sponsored → toggle **on** *and* verbal pt-BR disclosure in the first 15–30s *and* on-screen `#publi` ≥10s *and* description lines 1–2. The toggle alone is never enough.
- **If** the creator promotes a third-party product → warn about **responsabilidade solidária** under the CDC; this exposure is larger than the US equivalent.
- **If** the creator collects emails, runs a *sorteio*, or shares a list with a sponsor → LGPD applies: specific informed consent, stated purpose, honoured deletion.
- **If** choosing a course platform → compute **Hotmart (9.9% + R$1.00)** against **Kiwify (8.99% + R$2.49 + R$3.67/withdrawal)** at the actual ticket price. Low ticket favours Hotmart.
- **If** choosing a membership rail for a BR audience → prefer **Apoia.se (13%, BRL, local payments)** over Patreon (10%, USD) despite the higher headline fee.
- **If** selling to a BR audience → **Pix is mandatory**, and **parcelado** materially lifts conversion at higher tickets.
- **If** scheduling → use **UTC−3**, no DST; take the publish hour from Studio → Audience → "When your viewers are on YouTube". The 19h–22h *horário nobre* convention is `C` and unverified.
- **If** the mix is BR + US → no single fixed publish time serves both; the offset shifts twice a year.
- **If** positioning a small channel → go narrower. Underserved: pt-BR B2B/SaaS, regulated-professional explainers, regional non-Southeast, trades/agro, BR-specific purchase decisions. Avoid gaming, reaction/humour, and generic "ganhar dinheiro online".
- **If** any figure here is challenged → concede it is `C`, name the source, and offer to re-verify. Revenue figures decay within a year of `last_reviewed`.
