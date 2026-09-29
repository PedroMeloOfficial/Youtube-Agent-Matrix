# Research Report Standard

**Purpose.** Defines what `research-report-agent` may publish under the creator's name. This is
the one deliverable in the matrix meant to leave the pipeline entirely — a stranger with no
context reads it, judges the creator's rigor by it, and may cite it themselves. That is a
different bar than every other file here, including `research-dossier.md`, which only ever has to
survive contact with another agent.

**Contents:** 1 What this is, and is not · 2 Structure · 3 Citation format · 4 Source tiers and
what may be cited · 5 Length and depth · 6 Voice · 7 Before publishing

---

## 1. What this is, and is not

It is **not** a scientific paper: no abstract written for peer reviewers, no literature-review
throat-clearing, no methodology section justifying a sample size. Nobody is defending a thesis to
a committee.

It **is** a structured, sourced, citable document — the kind a serious blog or a trade
publication runs, built to the same evidentiary standard as `research-dossier.md` (§ *Standards*
in `agents/research-agent.md`) but written for a reader who was never going to open that dossier.
Every number has a date. Every claim that isn't common knowledge has a citation. A reader can
follow any citation back to a real, checkable source.

**Its job is to survive being wrong in public.** The dossier's errors get caught by the script
agent or the creator before anyone outside the channel sees them. This document's errors are the
creator's error, permanently, in a document that outlives the video.

## 2. Structure

Fixed skeleton, in this order. `templates/outputs/research-report.md` carries the exact
placeholders.

1. **Title and byline** — working title of the report (not necessarily the video's title),
   creator's name or channel name, date, output language.
2. **Summary** (120–180 words) — what the report argues and why it matters, written so it stands
   alone if someone reads nothing else. Not an academic abstract: no "this paper examines,"
   just the claim and its stakes.
3. **Body sections**, one `##` per angle the creator asked for. Each section is itself sourced and
   dated; each closes with the one sentence connecting it back to the report's central argument,
   so a reader skimming headers still gets the throughline.
4. **Discussion** — where the sections meet. This is where the report is allowed a point of view:
   the creator's own argument, built from the sourced material above it, stated plainly. Opinion
   is allowed here and only here, and it must be legible as the creator's read of the evidence,
   not presented as another sourced fact.
5. **Conclusion** — the claim restated in one paragraph, plus what would change the creator's mind
   about it. A report that cannot say what would falsify its own argument is not a research report.
6. **References** — every source cited above, alphabetical by author or organization, full
   citation per § 3. Nothing appears here that wasn't cited in the body; nothing is cited in the
   body that isn't here.

No table of contents field — the document is short enough that headings alone navigate it, and a
manually-numbered ToC drifts the moment a section is edited.

## 3. Citation format

**APA-style, author–date, adapted for the mix of source types this actually involves.** Real APA
(7th edition) assumes journal articles and books; most of what feeds this report is web content,
so use the APA web/organization conventions throughout rather than forcing a journal template
onto a blog post.

**In-text:** `(Author or Organization, Year)`. Two authors: `(Smith & Lee, 2023)`. No named author:
use the organization or publication (`(Deadline, 2022)`), never "Anonymous." No year found: `(n.d.)`
— and treat that as a flag to look harder before accepting the source at all.

**Reference-list entry, by type:**

- **Web article / news:** `Author or Organization. (Year, Month Day). Title of the article.
  Publication Name. URL`
- **Company or platform report:** `Organization. (Year). Title of the report. URL`
- **Video (interview, documentary, official statement):** `Creator or Channel. (Year, Month Day).
  Title of the video [Video]. Platform. URL`
- **Court record, filing, official document:** `Issuing body. (Year). Title or docket identifier.
  URL`
- **Book:** `Author, A. A. (Year). Title of the book. Publisher.`
- **Academic article, when one genuinely applies:** `Author, A. A. (Year). Title of the article.
  Journal Name, Volume(Issue), pages. DOI or URL`

List entries alphabetically by the first element (author or organization), not by citation order.
Every entry needs a live or archived URL — a citation with no way to verify it is not a citation,
it is an assertion wearing a citation's clothes.

## 4. Source tiers and what may be cited

Reuses `research-agent`'s three tiers, applied at publication strictness rather than dossier
strictness:

- **Documented fact** — cite it, state it as fact.
- **Widely believed** — cite the strongest source making the claim, but the prose must say
  "reportedly" or "according to `<source>`," never assert it as settled.
- **Fan theory or speculation** — may be *described* as existing discourse ("some fans argue...",
  cited to where that argument lives) but never presented as this report's own claim.

**A source with no fixed publication date is a source you keep looking past**, not one you cite
with `(n.d.)` as a shrug. Use it only when nothing better exists, and say so.

**Wikipedia is a map to sources, never a source.** Follow its citations to the primary material
and cite that instead. If a fact only exists on Wikipedia with no traceable citation, mark it
`⚠️ unverified — Wikipedia only, no primary source found` in the body and either cut it or keep
the marker in the published text; do not launder it into an unmarked claim.

**Never invent a citation to fill a gap.** A claim with no real source gets `⚠️ unverified` in the
body (visible to the reader, not hidden) or gets cut. A fabricated reference is the single worst
failure this document can produce — worse than an admitted gap, because it is undetectable until
someone checks.

## 5. Length and depth

Target **1,200–2,500 words of body text** (summary through conclusion; references don't count).
That is genuinely multi-page once formatted — four to eight pages depending on section count —
without becoming the "elaborate scientific paper" the creator explicitly does not want. Depth
comes from source density and the sharpness of the discussion section, not from word count; a
2,000-word report with twenty checkable sources beats a 5,000-word one with three.

Section count follows the number of angles the creator actually asked for — three angles in the
brief means three body sections, not a padded five.

## 6. Voice

Written in the third person, plainly, for a reader who has never seen the video. Do not write
"in this video I argue" — the report stands on its own and may be read by someone who never
clicks through. It may reference the video once, near the top, as where the argument is presented
in full ("this report supports the analysis in `<video title>`"), and nowhere else.

Match `output_language`. Citations and source titles stay in their original language, same rule as
`research-dossier.md`.

## 7. Before publishing

- [ ] Every claim traces to a citation, or is marked `⚠️ unverified` visibly in the text
- [ ] Every reference-list entry has a live or archived URL
- [ ] No citation invented to cover a gap
- [ ] Documented fact / widely believed / speculation are distinguishable in the prose, not just
      internally
- [ ] Discussion section states the creator's own read, legibly separated from the sourced facts
      above it
- [ ] Conclusion names what would change the argument's mind
- [ ] Word count sits in the 1,200–2,500 band, or the deviation is explained in the return summary
- [ ] Nothing contradicts `research-dossier.md` for the same video; a real contradiction is
      reported, not silently resolved
- [ ] Written entirely in `output_language`
