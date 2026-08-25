# SEO Playbook

Method for finding what an audience searches for, deciding whether a video targets search or browse, and packaging every metadata surface — video-level and channel-level — around that decision, in any language.

> **Every limit, threshold and benchmark lives in `benchmarks.md`.** This file teaches procedure and names the section where each number lives.

**Contents:** [1 Two-Algorithm Decision](#1-the-two-algorithm-decision) · [2 Keyword Research](#2-keyword-research-without-paid-tools) · [3 Demand vs Competition](#3-judging-demand-vs-competition) · [4 Clustering](#4-clustering-one-cluster-one-video) · [5 Titles](#5-title-construction) · [6 Descriptions](#6-description-architecture) · [7 Tags](#7-tags-the-honest-version) · [8 Chapters](#8-chapters) · [9 Hashtags](#9-hashtags) · [10 Captions](#10-captions-and-transcripts) · [11 Channel SEO](#11-channel-level-seo) · [12 Playlists](#12-playlists-as-a-search-surface) · [13 Google & Schema](#13-google-surfaces-and-videoobject-schema) · [14 Localization](#14-localization-and-translated-metadata) · [15 Pinned Comment](#15-pinned-comment-strategy) · [16 Worked Example](#16-worked-example) · [17 Decision Rules](#17-decision-rules)

## 1. The Two-Algorithm Decision

Search and Browse are separate ranking systems (`benchmarks.md` §5). Decide which one a video is for **before** writing the title; everything downstream follows.

| Question | Search-targeted | Browse-targeted |
|---|---|---|
| Would someone type this into a search box? | Yes, in these words | No — they don't know they want it |
| Is the payoff a stated outcome? | Yes ("how to X") | No (story, reveal, opinion) |
| Relevance horizon | Months to years | Often days |
| Title optimises for | Term coverage | Speed of comprehension |
| Thumbnail optimises for | Confirmation ("this is it") | Curiosity gap |

**Hybrid** — a searchable phrase carrying a curiosity clause — is the safe default. Build the search half first: curiosity can be added later, a term nobody searches cannot be retrofitted. Diagnose CTR against the traffic-source table in `benchmarks.md` §1, never against a niche average.

## 2. Keyword Research Without Paid Tools

Paid tools give a score, not a method, and their databases are thin outside major languages. This works anywhere, free. **Step 1 — harvest 30–60 raw seeds:**

| Source | How to mine it | Why it is trustworthy |
|---|---|---|
| YouTube autocomplete | Topic, then topic + each letter a–z; also + "how / why / best / vs / for" | Drawn from real query volume |
| Results sorted by view count | Read the top 20 titles | Phrasing that already wins |
| Related-search chips | Collect every chip | The platform's own intent clustering |
| Competitor titles **and chapter names** | 5–10 channels of similar size | Chapters expose sub-intents |
| Own comments, repeated questions | Take the literal wording | Language the audience actually uses |
| Studio → Research tab | Free demand indicator | First-party platform data |
| Google autocomplete, "People also ask", forum thread titles | Same alphabet-soup method; copy thread titles verbatim | Feeds the Google video surface; unfiltered phrasing |

**Language rule:** harvest in the language the video will be spoken in, from that language's locale. Never translate an English keyword list — translated keywords are frequently not what native speakers type. Where the niche code-switches (English technical terms inside a non-English sentence), keep the code-switched form; that is the real query.

**Step 2 — expand each seed on five axes:** modifier (best / cheapest / free / at home) · audience (for beginners / for professionals) · situation (when X / after X / without X) · comparison (A vs B, alternative to A) · outcome (to do X, in N days). Expect 8–25 survivors per seed. **Step 3 —** log every phrase with its source; judge in §3 against evidence, not intuition.

## 3. Judging Demand vs Competition

Three free proxies replace a paid volume number: **autocomplete depth** (the fewer characters typed before it is suggested, the higher the demand) · **result freshness** (sort by upload date — many recent uploads means live demand, a dead page means a dead term) · **top-result view floor** (the lowest view count in the top 10; a high floor means the term reliably delivers).

**The outlier test — the single most useful signal.** Find videos on the term from channels *smaller* than the creator's that far exceed their own channel average. One such outlier proves the term rewards a small channel. Zero outliers, every winner from a large channel, means the term is won by authority rather than relevance — deprioritise it.

| Score 1–3 per axis, rank by total | 1 | 2 | 3 |
|---|---|---|---|
| Demand evidence | No autocomplete, stale results | Autocomplete only | Autocomplete + fresh results + high floor |
| Winnability | Top 10 all large channels | Mixed | ≥1 small-channel outlier |
| Intent match | Tangential | Adjacent | Exactly what the channel is about |
| Production fit | Needs missing resources | Feasible | Material already exists |
| Durability | Tied to a passing event | Seasonal | Evergreen |

**Long-tail selection** — take the long-tail variant when **any two** hold: the head term's top 10 is dominated by channels 10× larger; the head term is ambiguous; the channel has no authority on the topic; the phrase names a specific pain, tool, model, situation or number. A long-tail phrase no autocomplete confirms is not long-tail — it is invented.

## 4. Clustering: One Cluster, One Video

A cluster is one **primary phrase** (the literal answer the viewer wanted) plus **3–8 secondaries**, each a re-phrasing of the same need and each mapping to one section of the video. If a secondary needs its own video, it is not a secondary — it is the *next* video. Cluster boundary: different outcomes mean different videos, however similar the wording.

Heavy overlap causes self-cannibalisation: two of the creator's videos split the same impressions and neither ranks. Fix by keeping the stronger video, re-titling the weaker toward its distinct secondary, and linking them via playlist and pinned comment. Worksheet fields: primary phrase · search or browse · secondaries (become chapter names) · adjacent phrases deliberately excluded (become the next 2–3 videos).

## 5. Title Construction

Character limits, truncation points, the front-load window and the **title-length reconciliation** are in `benchmarks.md` §6 — read the reconciliation first, because length is chosen from the intended traffic source, not from a global rule. **Order:** (1) write the primary phrase exactly as a person types it; (2) place it inside the front-load window; (3) add one differentiator — number, constraint, timeframe, outcome or named contradiction; (4) delete every zero-information word ("in this video", "tips and tricks"); (5) check against the thumbnail — they must not say the same thing (Information Split Rule, `benchmarks.md` §7).

| Target | Shape | Fits |
|---|---|---|
| Search | `[primary phrase] — [outcome / constraint]` | Tutorials, comparisons, fixes |
| Search | `[primary phrase] ([qualifier])` | Version- or year-sensitive topics |
| Browse | `[unexpected claim]` · `I [did X] and [surprising result]` · `Why [common belief] is wrong` | Opinion, story, reveal, experiment, contrarian |
| Hybrid | `[primary phrase]: [curiosity clause]` | Default when unsure |

**Language adaptation.** Limits count characters, not words. In character-dense scripts (Japanese, Chinese, Korean, Thai) the same budget carries a full clause — use it. In compounding or heavily inflected languages (German, Finnish, Hungarian, Turkish) it carries far less, so cut the differentiator before the keyword. RTL scripts truncate from the opposite side on some surfaces; verify visually on mobile. **Anti-patterns:** ALL CAPS beyond one word · more than one exclamation · a claim the video does not deliver (metadata-mismatch penalty, `benchmarks.md` §5) · keyword repeated twice · empty brackets.

## 6. Description Architecture

Limits, preview length and keyword placement: `benchmarks.md` §6.

| Block | Purpose | Rule |
|---|---|---|
| 1 Hook paragraph | All that shows before "Show more" — treat as ad copy | Primary phrase early, payoff stated, no links |
| 2 Expansion | Restate the promise fully | Secondaries appear naturally; no stuffing |
| 3 Chapters | Timestamps, first at `0:00` | Doubles as a scannable outline |
| 4 Resources | What was mentioned | Label every link; never a bare URL |
| 5 Related content | 1–3 own videos or a playlist | Feeds session continuation |
| 6 Channel line, social, contact | Fixed block, stable across uploads | Channel-level keyword surface; kept last |
| 7 Disclosures + hashtags | Sponsorship, affiliate, AI; then §9 | Placement rules in `benchmarks.md` §9 |

```
Fixing a slow laptop usually takes ten minutes, not a new machine. This walkthrough
shows the four checks that recover most of the lost speed, in the order that finds
the cause fastest — and the one "fix" that makes things worse.

Everything here works on a standard install with no extra software. If your machine
is still slow after step three, chapter 4 explains how to tell whether the problem
is storage, memory, or heat, and what each one costs to solve.

0:00 The four checks, in order        6:05 Check 3 — background processes
1:12 Check 1 — startup load           9:18 Check 4 — heat and throttling
3:40 Check 2 — storage headroom      12:02 The "fix" that backfires
```

Mechanics of that example: primary phrase in sentence one, a payoff, an open loop surviving the fold, secondaries carried by chapter names instead of a keyword list. (Timestamps are one per line in the real description.)

## 7. Tags: The Honest Version

Tags carry minimal ranking value (`benchmarks.md` §6). They are not zero and they are cheap, so the policy is a strict time-box, not abstinence.

| Situation | Bother? | Enter |
|---|---|---|
| Common misspellings, or a topic name ambiguous across fields | Yes | The misspellings; disambiguating terms |
| Brand-new channel, no topical history | Yes | Primary + 3–5 secondaries |
| Non-English content, weak auto-transcription for the language | Yes | Primary phrase and its transliteration |
| Established channel, unambiguous evergreen topic | No | Skip entirely |

Never spend real time here — nothing in the tag field rescues a weak title, and viewers never see it.

## 8. Chapters

Start time, minimum count, minimum length and the retention effect: `benchmarks.md` §6. **Deriving from a script:** mark every point where the *subject* changes (not the delivery); merge any segment under the minimum into its neighbour; name each chapter by what is in it; fold in a secondary keyword only where it is the honest description.

| Function-named (weak) | Content-named (strong) |
|---|---|
| Intro / Background | The four checks, in order · Why laptops slow down after two years |
| Step 3 | Check 3 — background processes |
| Conclusion | What to do if none of this worked |

Chapter names surface on Google's key-moments display, so each must read as a standalone phrase, not a fragment that only makes sense in sequence. Omit end matter — thanks and outros rarely deserve a chapter.

## 9. Hashtags

Counts, cap and the all-or-nothing failure mode: `benchmarks.md` §6. Slot 1 = broad topic, the category the channel lives in · slot 2 = specific topic, closest to the primary phrase · slot 3 = channel or series tag, identical on every upload.

The first hashtags display above the title, so humans read them. **Convention is language-specific:** some languages hashtag in local script, some in Latin transliteration, and many niches hashtag in English regardless of the spoken language. Copy the convention from top-performing videos in that language; an invented hashtag nobody follows is an empty slot.

## 10. Captions and Transcripts

Watch-time effect and audience composition: `benchmarks.md` §6. Manual captions beat auto captions for six reasons: auto-transcription mangles **proper nouns** (product names, jargon, places — the high-value terms); auto captions **run on** with no readable segmentation, hurting comprehension and dwell; **quality varies sharply by language** and for many languages is poor or absent; auto systems **degrade badly on accents and code-switching**; a clean transcript is a **clean text index** of the video; and a correct source transcript is a **prerequisite for any translated track**.

Procedure: generate auto captions → download → correct → re-upload as the manual track. Correcting costs a fraction of transcribing from scratch. Say the primary phrase aloud naturally in the video — spoken content is transcribed and read.

## 11. Channel-Level SEO

Ignored constantly, and it compounds across every upload.

| Surface | Rule | Failure mode |
|---|---|---|
| Channel name | Readable, pronounceable, memorable; a topic word only if the channel will never widen | Locks the channel into a topic it outgrows |
| Handle | Matches the name, identical across platforms | Split brand searches |
| Channel description + keywords | Description first lines: who it's for, what they get, plus the 2–3 terms the channel should own. Keywords: small topic set, disambiguation only | A keyword list no human would read; stuffing |
| Trailer / featured video | Trailer under a minute for new visitors (promise + cadence); featured = best current video for returning ones | Generic welcome; featured left unset for years |
| About links, banner | Links ordered by what converts; banner readable at mobile size, stating promise or schedule | Twelve unprioritised links; banner text outside the safe area |
| Home-tab sections | Trailer → current series → best playlists → the rest | Default "Uploads" only |
| Localised channel metadata | Translated name and description for a multilingual audience | One language for a bilingual audience |

Channel identity is what tells the system what a *new* video is about before that video has any performance data of its own.

## 12. Playlists as a Search Surface

Playlists rank in search independently of their videos and drive session continuation, a top satisfaction signal (`benchmarks.md` §5).

| Element | Method |
|---|---|
| Title | Written for a phrase broader than any single video ("everything about X", "X for beginners") |
| Description | §6 blocks 1–2; it is indexed |
| Order | Teaching: prerequisite order, strongest first only if it stands alone. Bingeing: strongest first, then descending by retention, so the session survives video two |
| Grouping | One playlist per series; cross-cluster playlists grouped by viewer *goal*, never by upload date |
| Maintenance | Remove videos that break the title's promise — a weak middle ends sessions |

Add every video to at least one playlist at publish, and put the *playlist* link (not the video link) in description block 5 when the goal is session length.

## 13. Google Surfaces and VideoObject Schema

YouTube ranks on satisfaction and retention; Google ranks on information delivery and page authority — a video can win one and lose the other. Google-surface presence and AI-overview citation rates: `benchmarks.md` §6.

**Video-trigger keyword taxonomy** — query classes that reliably surface video in general web search: *procedural* (how to, step by step, tutorial — motion shows sequence) · *demonstrative* (review, unboxing, test — seeing the object matters) · *comparative* (X vs Y, best X for Y — side-by-side is visual) · *diagnostic* (why is my X doing Y, fix, error — recognition by sight) · *explanatory* (explained, what is — diagrams and pacing) · *performative* (recipe, workout, walkthrough — timing must be watched). A phrase in none of these classes will get little Google video traffic; plan for YouTube-internal discovery only.

**JSON-LD for an embedding page** (rich results require the video to be the page's main content):

```html
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "VideoObject",
  "name": "Video title exactly as published",
  "description": "One-paragraph summary matching the video's actual content.",
  "thumbnailUrl": ["https://example.com/thumb-1920x1080.jpg"],
  "uploadDate": "2026-01-15T09:00:00+00:00", "duration": "PT12M40S",
  "contentUrl": "https://example.com/media/video.mp4",
  "embedUrl": "https://www.youtube.com/embed/VIDEO_ID", "inLanguage": "en",
  "publisher": { "@type": "Organization", "name": "Channel name",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" } },
  "hasPart": [ { "@type": "Clip", "name": "Check 1 — startup load", "startOffset": 72,
      "endOffset": 220, "url": "https://example.com/page#t=72" } ],
  "potentialAction": { "@type": "SeekToAction",
    "target": "https://example.com/page?t={seek_to_second_number}",
    "startOffset-input": "required name=seek_to_second_number" } }
</script>
```

Add one `Clip` per chapter. Set `inLanguage` to the spoken language and publish one block per localised page rather than listing languages in one. An invalid ISO 8601 `duration` suppresses the rich result silently.

## 14. Localization and Translated Metadata

The largest under-used growth surface, and the one most often skipped.

| Layer | Effect | Cost | When |
|---|---|---|---|
| Translated subtitles + translated title and description | Watchable *and* **findable** in that language | Low | As soon as a second language appears in geography — always together; subtitles alone are rarely discovered |
| Multi-language audio track | Native narration on the same video, sharing all performance history | High | When one foreign language is already a large share of views |
| Localised thumbnail text and channel metadata | Removes the last barrier at the click decision; channel reads natively | Low–medium | Thumbnails only where the surface supports it; channel metadata once two languages are established |

**Procedure:** (1) pick the target language from audience geography and the subtitle-language report, not by guess; (2) correct the source transcript first — every translation inherits its errors; (3) translate subtitles and have a native speaker check terminology, not just grammar; (4) **re-run §2 keyword research in the target language** — a translated title contains translated words, a researched title contains what that language's speakers actually type; (5) enter the researched title and a rewritten description in the localisation panel; (6) track that language separately — one that does not grow after three localised videos is the wrong second language. Never publish a machine-translated title unreviewed: a mistranslated promise is a metadata mismatch in that language, with the same penalty exposure as clickbait (`benchmarks.md` §5).

## 15. Pinned Comment Strategy

A free, editable metadata slot sitting where attention already is. Use it for exactly one of: a **correction** ("at 4:10 I said X; it's actually Y" — protects trust and pre-empts a pile-on) · a **question prompt** (one specific question, never "what do you think?" — drives comment volume, `benchmarks.md` §5) · a **next step** (link to the follow-up video or playlist, for session continuation) · the **resource** everyone asks for · a **timestamp map** where chapters were not enough.

Pin within the first hours, while early comments set the tone. One purpose per pin — a pin doing three jobs does none. Write it in the spoken language, and add a two-line translation beneath when a second language is a large share of the audience.

## 16. Worked Example

**Topic:** beginner explainer, home-tech niche, small channel with no topical authority.

| Stage | Output |
|---|---|
| Seeds, then expanded | "slow laptop", "laptop slow fix", "speed up laptop", "why is my laptop slow", "laptop slow after update" — expanded with "without buying a new one", "for beginners", "free", "after 2 years" |
| Demand / winnability | Autocomplete confirms 4 of 10; results fresh; high top-10 view floor; two small-channel outliers on the long-tail variant, none on the head term |
| Decision | Long-tail, **search-targeted** · primary: "why is my laptop slow" |
| Secondaries | startup programs · storage full · background processes · overheating · when to upgrade instead |
| Excluded (next videos) | "best budget laptop" · "how to reinstall the OS" |

**Title candidates** — search-targeted, so the longer band per the reconciliation in `benchmarks.md` §6:

| # | Candidate | Verdict |
|---|---|---|
| 1 | Why Is My Laptop Slow? 4 Checks That Fix It in 10 Minutes | Primary phrase verbatim and front-loaded, number differentiator — **selected** |
| 2 | Why Is My Laptop Slow — And The One Fix That Makes It Worse | Strong curiosity, weaker coverage — keep as the A/B alternate |
| 3 | Speed Up A Slow Laptop (Without Buying A New One) | Different primary phrase — that is video two |
| 4 | 4 Reasons Your Laptop Is Slow | Primary phrase broken — weakest, discard |

**Description** = the worked blocks in §6, then resources, one playlist link, the channel line, three hashtags. **Chapters** = the six content-named chapters shown in §6. **Tags** = the new-channel exception in §7: primary, three secondaries, one common misspelling, time-boxed under a minute.

## 17. Decision Rules

- Phrase absent from autocomplete in the target language → **do not build a video on it**; it is invented demand.
- No channel smaller than the creator's in the top 10 → **take the long-tail variant**.
- Two of the creator's videos on one primary phrase → **re-title the weaker** toward a distinct secondary and link them.
- Nobody would type the phrase into a search box → **treat it as browse-targeted** and stop optimising for term coverage.
- Search-targeted → **longer title band**; browse-targeted → **shorter** (`benchmarks.md` §6 reconciliation).
- Primary phrase does not fit the front-load window → **cut the differentiator, never the keyword**.
- Thumbnail and title carry the same information → **rewrite one** (`benchmarks.md` §7).
- A link appears before a promise in the description's first lines → **rewrite them**; that space is ad copy.
- Chapter named for its function → **rename it for its content**; end matter gets no chapter at all.
- Established channel, unambiguous topic → **skip tags entirely**; hashtags over the cap → **cut to three**, since exceeding voids all of them.
- Only auto-captions exist → **correct and re-upload** before considering any translation.
- A second language is a meaningful share of the audience → **localise title and description with the subtitles**, never subtitles alone.
- Localised title produced by translation rather than research → **do not publish it**.
- Video is not the embedding page's main content → **do not add VideoObject schema**; it cannot produce a rich result.
- Video has no playlist → **it is not finished being published**.
- Pinned comment doing more than one job → **split it and pin the more valuable half**.
