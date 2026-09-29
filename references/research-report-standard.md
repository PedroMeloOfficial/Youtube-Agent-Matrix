# Research Report Standard

**Purpose.** Defines what `research-report-agent` may publish under the creator's name. This is
the one deliverable in the matrix meant to leave the pipeline entirely — a stranger with no
context reads it, judges the creator's rigor by it, and may cite it themselves. The bar is
therefore higher than `research-dossier.md`, which only has to survive contact with another agent.

**What it is for:** defending **one thesis** with facts and data, in a way a sceptical reader can
check line by line. Not a topic overview. A report that informs but never argues has failed its
brief; a report that argues past its evidence has failed worse.

**Contents:** 1 What this is, and is not · 2 Thesis and claim map · 3 Structure · 4 Data
discipline · 5 Evidence strength · 6 Citation format · 7 Source tiers · 8 Citation audit · 9 Length
· 10 Voice · 11 Before publishing

---

## 1. What this is, and is not

It is **not** a scientific paper: no literature-review throat-clearing, no methodology section
justifying a sample size, no committee to satisfy.

It **is** an argued, sourced, citable document — the register of a serious trade-press long read
or a think-tank brief. Every number has a date and a unit. Every claim that isn't common knowledge
has a citation a reader can follow to a real page that says it.

**Its job is to survive being checked in public.** The dossier's errors get caught before anyone
outside the channel sees them. This document's errors are the creator's, permanently, in a file
that outlives the video.

## 2. Thesis and claim map — before any research

Write these down first; they drive every section after.

1. **The thesis** — one declarative sentence that could be wrong. "The product ignores the model its
   competitors proved works" is a thesis. "An analysis of the industry" is a topic.
2. **The supporting claims** — the 3–5 things that must each be true for the thesis to hold. Each
   becomes one evidence section. Each must be checkable on its own.
3. **For each claim, the evidence that would prove it** — which figures, which documents, which
   statements — and the evidence that would sink it.

**The thesis is allowed to lose.** If the research contradicts a supporting claim, you do not
bend, trim or bury the evidence. You stop and report it, with the narrower thesis the evidence
*does* support. Cherry-picking is the failure mode this whole standard exists to prevent.

## 3. Structure

Fixed skeleton, in this order. `templates/outputs/research-report.md` carries the placeholders.

1. **Title and byline** — report title, creator or channel name, date, the video it accompanies.
2. **Thesis** — the one sentence, stated in bold, before anything else.
3. **Summary** (150–250 words) — the thesis, the strongest two or three pieces of evidence with
   their numbers, and the main limitation. Standalone: a reader who stops here has the argument.
4. **Background** — only what a stranger needs to follow the argument. When history matters to the
   thesis, a **chronology table** (date · event · why it matters · source).
5. **Evidence sections** — one per supporting claim. Each **opens with the claim it establishes**,
   presents the evidence (a data table whenever three or more comparable figures appear), and
   **closes with one line: what this establishes for the thesis — and what it does not.**
6. **Case study** — when the brief names one. Fixed shape: context · the decision taken · the
   measurable outcome, with numbers · what it demonstrates · what it cannot demonstrate.
7. **Counterarguments** — the two or three strongest objections a well-informed critic would raise,
   **found in real discourse and cited**, each stated at full strength, then answered with evidence
   or explicitly conceded. No strawmen. A report with no objections section is advocacy.
8. **Discussion** — the inference chain: how the sections add up to the thesis, with every step
   labelled as direct evidence, proxy or inference (§5). This is where the creator's own reading
   lives, legibly as interpretation.
9. **Conclusion and limits** — the thesis restated at the strength the evidence earned; what data
   was unavailable; what finding would overturn it.
10. **References** — every cited source, per §6. Nothing listed that isn't cited; nothing cited
    that isn't listed.
11. **Appendix: data notes** *(when any figure was derived)* — the arithmetic behind every computed
    number, inflation adjustments, and how proxies were chosen.

No table of contents field — headings navigate a document this length, and a manual ToC drifts.

## 4. Data discipline

Facts argue; numbers prove. Every figure carries all of:

- **Value, unit, currency** — "US$ 3.2 million per episode", never "3.2M".
- **Period** — the year, quarter or date range it describes, which is not the publication date.
- **Status** — *reported* (company filing, official statement), *measured* (a ratings or panel
  provider), or *estimated* (analyst, trade press) — and by whom.
- **Scope** — company-level, segment-level or title-level. Companies rarely disclose per-product or
  per-title figures; never present a segment figure as if it were a single title's.

Rules that follow from that:

- **Money across years** is stated nominally, and — when compared across more than a few years —
  also inflation-adjusted, with the index and base year named (e.g. US CPI, 2025 dollars).
- **Derived figures show their arithmetic**, in the text or the data-notes appendix. A number the
  reader cannot reproduce is an assertion.
- **Proxies are named as proxies** — demand scores, viewing-hour rankings, search interest — with
  one line on why the proxy is a fair stand-in and where it breaks.
- **Comparisons compare like with like**: same period length, same currency, same scope. If they
  can't, say so beside the comparison.
- **"Not publicly disclosed" is a finding**, not a gap to fill. Write it; never estimate your way
  around it without labelling the estimate as yours and showing how.
- Platform mechanics (CTR, retention, RPM) still come only from `references/benchmarks.md`. Topic
  facts — market sizes, budgets, revenues — are sourced here like any other research.

## 5. Evidence strength

Every step of the argument is one of three kinds, and the prose makes it visible which:

- **Direct evidence** — the source states it. ("The company's CFO told investors that…")
- **Proxy** — a measurable stand-in for what can't be observed directly, named as such.
- **Inference** — your reasoning from the evidence. Allowed, and often the point — but written as
  inference ("this suggests", "the pattern is consistent with"), never as established fact.

**Causal claims need direct evidence or an explicit inference label.** "Product X drove sales of
product Y" requires a source saying so, or data showing the link *and* the words
"consistent with" rather than "caused". Correlation presented as causation is the most common way
a well-sourced report still ends up wrong.

## 6. Citation format

**APA 7, author–date, using its web and organization conventions** — most of what feeds this report
is web content, so do not force a journal template onto a news article.

**In-text:** `(Author or Organization, Year)`; two authors `(Smith & Lee, 2023)`; no named author →
the organization or publication (`(Reuters, 2022)`), never "Anonymous". A direct quote adds the
location: `(Reuters, 2023, para. 4)`. No year found: `(n.d.)` — and a reason to look harder.

**Reference-list entry, by type** (titles of standalone works in `*italics*`):

- **News / web article:** `Author. (Year, Month Day). Title. *Publication*. URL`
- **Company report, filing, earnings call:** `Organization. (Year). *Title or document type*. URL`
- **Data from a page that changes:** add `Retrieved Month Day, Year, from URL`
- **Video (interview, official statement):** `Channel. (Year, Month Day). *Title* [Video]. Platform.
  URL`
- **Book:** `Author, A. A. (Year). *Title*. Publisher.`
- **Journal article:** `Author, A. A. (Year). Title. *Journal*, Volume(Issue), pages. DOI or URL`

Alphabetical by first element. Every entry needs a live or archived URL.

## 7. Source tiers — what may be cited, and how

- **Primary** (filings, earnings calls, official statements, court records, the company's own
  data) — preferred for every load-bearing number.
- **Credible secondary** (established trade press, measurement firms, named analysts) — fine,
  labelled as reported/estimated by them.
- **Widely believed** — cite the strongest source making the claim; the prose says "reportedly" or
  "according to", never asserts it as settled.
- **Speculation and fan theory** — may be *described* as existing discourse, cited to where it
  lives, never adopted as the report's own claim.

**Wikipedia is a map to sources, never a source.** Follow its footnotes and cite what they point
to. Aggregators recycling each other are one source, not five.

**Never invent a citation.** A claim with no real source is marked `⚠️ unverified` in the visible
text, or cut. A fabricated reference is worse than an admitted gap — it is undetectable until
someone checks, and then it discredits everything else in the document.

## 8. Citation audit — before converting

Re-open **every** cited source and confirm that page contains the specific claim, figure and date
attributed to it — not a related claim, not the same topic. Fix or cut any mismatch. For sources
behind a paywall you could not read in full, cite only what the visible portion states and say so.
This step is not optional and not sampled; a single mismatched citation is the one a critic finds.

## 9. Length

**2,000–4,500 words of body text** (Thesis through Conclusion; references and appendix excluded) —
roughly six to twelve pages once formatted. Budget about 400–900 words per evidence section and the
case study, 300–600 for counterarguments. Length follows the claim map, never the other way round:
three supporting claims make three evidence sections, not five padded ones.

## 10. Voice

Third person, plain, for a reader who has never seen the video. It may name the video once, near
the top, as where the argument is presented on camera, and nowhere else. Confident where the
evidence is strong, explicit where it is thin — hedging everything reads as weaker than stating
limits once, clearly.

Written in `output_language`; citations and source titles stay in their original language.

## 11. Before publishing

- [ ] Thesis is one falsifiable sentence; every evidence section maps to a supporting claim
- [ ] Every figure has value, unit, currency, period, status and scope
- [ ] Cross-year money comparisons inflation-adjusted, index and base year named
- [ ] Derived figures show their arithmetic; proxies named as proxies
- [ ] Direct evidence, proxy and inference are visibly distinct; no causal claim without either a
      source or an inference label
- [ ] Counterarguments are real, cited, at full strength, and answered or conceded
- [ ] Citation audit done on every source — each page says what it is cited for
- [ ] No invented citation; gaps marked `⚠️ unverified` or cut
- [ ] Conclusion states limits and what would overturn the thesis
- [ ] Nothing contradicts `research-dossier.md`; a real contradiction is reported
- [ ] Body length in the 2,000–4,500 band, or the deviation explained
