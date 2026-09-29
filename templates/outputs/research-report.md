# ⟨REPORT TITLE — can differ from the video's title⟩

> Fill in OUTPUT LANGUAGE. Section headings may be translated.
>
> **The deliverable is `research-report.docx`, not this file.** You write this Markdown, run
> `execution/build_reader_doc.py` on it, and the Markdown is deleted. What the creator publishes
> and links from the video description is the Word document.
>
> Standard: `references/research-report-standard.md`. Read all of it before writing — the thesis
> and claim map (§2), data discipline (§4), evidence strength (§5) and the citation audit (§8) are
> there, not repeated here.

## How the converter reads this file

| You write | The reader sees |
|---|---|
| `# Title` | Document title |
| `## Heading` / `### Sub-heading` | Section headings |
| plain paragraph | Body text |
| `**word**` / `*word*` | Real bold / italics (italicise standalone titles in references) |
| `- item` / `1. item` | Real bullets / numbered list |
| `\| a \| b \|` | A real table with a header row — use for every set of 3+ comparable figures |

No `>` lines in this document — that convention belongs to the recording script. No images or
charts: the converter cannot embed them, so data goes in tables.

---

⟨Creator or channel name⟩ · ⟨Date⟩ · Accompanies the video "⟨video working title⟩"

**Thesis:** ⟨One declarative, falsifiable sentence.⟩

## Summary

⟨150–250 words: the thesis, the two or three strongest pieces of evidence with their numbers, and
the main limitation. A reader who stops here has the argument.⟩

## Background

⟨Only what a stranger needs to follow the argument.⟩

| Date | Event | Why it matters here | Source |
|---|---|---|---|
| ⟨YYYY-MM⟩ | ⟨event⟩ | ⟨one line⟩ | ⟨(Author, Year)⟩ |

*(Keep the chronology table only when history is part of the argument.)*

## ⟨Evidence section — named for the claim it establishes⟩

**Claim:** ⟨the supporting claim this section establishes⟩

⟨Sourced prose. Every figure: value, unit, currency, period, reported/measured/estimated, scope.
Direct evidence, proxy and inference visibly distinct.⟩

| ⟨Metric⟩ | ⟨Period A⟩ | ⟨Period B⟩ | Status | Source |
|---|---|---|---|---|
| ⟨…⟩ | ⟨value + unit⟩ | ⟨value + unit⟩ | ⟨reported / estimated by X⟩ | ⟨(Author, Year)⟩ |

**What this establishes:** ⟨one line for the thesis⟩ — **and what it does not:** ⟨one line⟩

*(Repeat per supporting claim in the claim map.)*

## Case study: ⟨subject⟩

*(Only when the brief names one.)*

⟨Context · the decision taken · the measurable outcome, with numbers · what it demonstrates · what
it cannot demonstrate.⟩

## Counterarguments

### ⟨Objection 1, stated at full strength⟩

⟨Who makes it, cited. Then the evidence that answers it — or an explicit concession.⟩

### ⟨Objection 2⟩

⟨Same.⟩

## Discussion

⟨The inference chain: how the sections add up to the thesis, each step labelled as direct
evidence, proxy or inference. The creator's own reading lives here, legibly as interpretation.⟩

## Conclusion and limits

⟨The thesis restated at the strength the evidence earned. What data was unavailable. What finding
would overturn it.⟩

## References

- ⟨Author or Organization. (Year, Month Day). Title. *Publication*. URL⟩

## Appendix: data notes

*(Only when any figure was derived.)*

⟨Arithmetic behind every computed figure; inflation index and base year; why each proxy was chosen.⟩

---

## Self-check — run before converting, then delete this section

- [ ] Thesis is one falsifiable sentence; each evidence section maps to one supporting claim
- [ ] Every figure has value, unit, currency, period, status and scope
- [ ] Every set of 3+ comparable figures is a table
- [ ] Cross-year money comparisons inflation-adjusted, index and base year named
- [ ] Derived figures show arithmetic in the appendix; proxies named as proxies
- [ ] No causal claim without a source saying so or an explicit inference label
- [ ] Counterarguments are real, cited, at full strength, answered or conceded
- [ ] Citation audit done on every source — each page says exactly what it is cited for
- [ ] No invented citation; gaps marked `⚠️ unverified` or cut
- [ ] Every "What this establishes" line is honest about what it does not establish
- [ ] Body (Thesis through Conclusion) is 2,000–4,500 words, or the deviation is explained
- [ ] Written in OUTPUT LANGUAGE; source titles in their original language
- [ ] Nothing contradicts `research-dossier.md` for this video
