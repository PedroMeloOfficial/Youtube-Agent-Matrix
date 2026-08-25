# YouTube Agent Matrix

A complete YouTube pre-production system for [Claude Code](https://claude.com/claude-code): an
orchestrator that routes work to **14 specialized subagents** covering strategy, audits,
competitor intelligence, research, ideation, calendars, hooks, scripts, thumbnails, SEO, upload
metadata, Shorts, repurposing, monetization and analytics. It works for any channel, any niche
and any language, with three human approval gates and no required API keys.

---

## Install

The plugin is self-contained. Pick either path.

### As a local plugin marketplace (recommended)

```
/plugin marketplace add /path/to/YoutubeAgents_Pipeline
/plugin install youtube-agent-matrix@youtube-agent-matrix
```

The marketplace manifest lives in `.claude-plugin/marketplace.json`, so the folder registers as
its own single-plugin marketplace. Updating is `git pull` plus `/plugin marketplace update`.

### As a symlink into `~/.claude/`

```bash
ln -s /path/to/YoutubeAgents_Pipeline/skills/orchestrator ~/.claude/skills/orchestrator
ln -s /path/to/YoutubeAgents_Pipeline/agents/*.md         ~/.claude/agents/
```

Convenient while editing the matrix itself, since your changes are live with no reinstall.

**Requirements:** Claude Code. That is the whole list. Python 3.9+ and
`google-api-python-client` are needed *only* if you want the optional live-data scripts in
`execution/`.

---

## First run

The first time you invoke the matrix it asks **two** questions, once each. First:

```
Before we start — what language should I work in?

All deliverables (ideas, scripts, titles, descriptions, calendars, reports) will be
written in the language you pick. I'll save it so you're only asked once.

  1. English      3. Español     5. Deutsch     7. 日本語
  2. Português    4. Français    6. Italiano    8. Other — just tell me which
```

Your answer is saved to `workspace/config.json` and you are never asked again. From then on
**every deliverable is written in that language** — ideas, hooks, scripts, titles, descriptions,
tags, calendars, audits, analytics reports, and the conversation itself. Change it any time by
saying so.

**One exception: thumbnails.** The `thumbnail-agent` always writes its deliverable in **English**,
whatever your output language is, because image-generation models are trained predominantly on
English and produce materially worse images from other languages. Two fields inside that English
document stay in *your* language, because viewers actually read them:

| Field | Language | Why |
|---|---|---|
| `overlay_text` | Yours | The words rendered on the thumbnail image |
| `paired_title` | Yours | The video title the thumbnail is designed against |
| Everything else | English | Composition, subject, lighting, colour direction, the generation prompt |

So you get an English prompt you can paste into any image generator, carrying your own words for
the parts the audience sees.

### The second question: your market

Right after the language question it asks one more, also once:

```
And where is your audience? Not where you live — where the people watching are.

  1. Brazil          3. Mixed — e.g. "80% Brazil, 20% US"
  2. United States   4. I don't know yet
```

**Where your audience is, not where you are.** Advertisers bid on the viewer's market, not the
uploader's. A creator living in Canada whose viewers are Brazilian has a Brazilian channel, and
getting this backwards produces revenue estimates wrong by an order of magnitude.

Your answer loads `references/markets/br.md` or `us.md` — researched files covering what a view
is actually worth in that market, when advertisers there spend, how people phrase searches, which
payment rails and course platforms actually operate, and which disclosure regime binds you (CONAR
in Brazil, FTC in the US — and neither is satisfied by YouTube's own "paid promotion" checkbox).

Markets without a dedicated file fall back to a directional multiplier in
`references/localization-guide.md`, and the deliverable says so.

If you answer "I don't know", it assumes your market matches your language and **corrects itself**
the first time the `analytics-agent` sees your real Audience → Geography data.

---

After both questions, the orchestrator loads `workspace/channel-profile.md`. If that file
does not exist yet, it says so in one line and routes you to `channel-strategist`, whose entire
job is writing it. Everything downstream is sharper once it exists.

---

## Quick start

Just say what you want. The orchestrator picks the entry point and tells you which one it chose,
in one line.

```
> Set up my channel — I make short documentaries about urban history
> My channel stopped growing three months ago, what's wrong?
> I want to make a video about why old buildings get demolished
> Turn last week's video into Shorts and a LinkedIn post
```

Explicit commands, when you already know what you want:

| Command | Runs |
|---|---|
| `/yt setup` | Language + market config → `channel-strategist` → channel profile + summary |
| `/yt strategy` | `channel-strategist` |
| `/yt audit` | `channel-auditor` (4 analysis lenses, parallel where supported) |
| `/yt competitor [channel]` | `competitor-analyst` (4 analysis lenses, parallel where supported) |
| `/yt research <topic>` | `research-agent` |
| `/yt ideate [topic]` | `research-agent` → `ideation-agent` |
| `/yt calendar` | `calendar-agent` |
| `/yt hook <topic>` | `script-agent` in `hooks-only` mode |
| `/yt script <idea>` | `script-agent` |
| `/yt thumbnail <video>` | `thumbnail-agent` |
| `/yt seo <topic>` | `seo-agent` |
| `/yt metadata <video>` | `metadata-agent` |
| `/yt shorts` | `shorts-agent` |
| `/yt repurpose <video>` | `repurpose-agent` |
| `/yt monetize` | `monetization-agent` |
| `/yt analyze` | `analytics-agent` |
| `/yt video <topic>` | **The full production chain** — see below |

These are phrases the orchestrator recognizes, not registered slash commands — type them in the
conversation. Natural language works identically.

---

## The full production chain

`/yt video <topic>` runs the whole pre-production pipeline from a topic to a package you can
record. Three gates, not seven, and everything that can run in parallel does.

```
                          research-agent
                                │
                                ▼
                          ideation-agent
                                │
                                ▼
                       6 ranked idea cards
                                │
    ┌───────────────────────────▼───────────────────────────┐
    │  ◆ GATE 1 — you approve one idea                      │
    └───────────────────────────┬───────────────────────────┘
                                │
                                ▼
                            seo-agent
                     (title direction, so the
                      hook can pay its promise)
                                │
                                ▼
                          script-agent
                     (hooks, then full scripts)
                                │
                                ▼
         3 variants: narrative / instructional / argumentative
                                │
    ┌───────────────────────────▼───────────────────────────┐
    │  ◆ GATE 2 — you pick one variant                      │
    └───────────────────────────┬───────────────────────────┘
                                │
                     script-agent (recording mode)
                     └─▶ script-recording.md — the version you read on camera
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
   thumbnail-agent       metadata-agent          shorts-agent   (parallel)
          └─────────────────────┼─────────────────────┘
                                ▼
    ┌───────────────────────────────────────────────────────┐
    │  ◆ GATE 3 — you approve the package                   │
    └───────────────────────────┬───────────────────────────┘
                                ▼
                      production package
           workspace/videos/YYYY-MM-DD_<slug>/
```

At a gate the orchestrator stops, presents the options, **recommends one with a one-line reason**,
and waits. Rejecting something re-runs only the rejected stage with your feedback passed through
verbatim — never the whole chain.

---

## The 14 agents

| Agent | Owns |
|---|---|
| `channel-strategist` | Positioning, content pillars, audience definition, voice — writes the channel profile every other agent reads, plus the one-page summary you read |
| `channel-auditor` | Scored channel health across SEO, performance, content and monetization, with the single highest-leverage fix named |
| `competitor-analyst` | The competitive landscape: keyword gaps, format gaps, audience gaps, and which of their videos are outliers |
| `research-agent` | Verified substance for one video — facts with sources, angle gaps, current discourse, sourceable visuals |
| `ideation-agent` | Ranked, pitchable video ideas as idea cards, scored against the channel's own pillars |
| `calendar-agent` | The publishing calendar: cadence, production windows, pillar balance, seasonality |
| `script-agent` | Hook options across multiple frameworks, three full retention-engineered script variants, and the clean recording script for the one you approve |
| `thumbnail-agent` | Thumbnail concepts and image-generation prompts (**English output**, see First run) |
| `seo-agent` | Keyword strategy, title candidates, and a realistic ranking approach for this channel's size |
| `metadata-agent` | The copy-paste upload package: title, description, tags, chapters, cards, end screens |
| `shorts-agent` | Shorts strategy, specs, hooks and series design |
| `repurpose-agent` | Long-form into Shorts and cross-platform distribution |
| `monetization-agent` | The revenue stack: YPP path, sponsorship rates, product funnel |
| `analytics-agent` | Metric interpretation, diagnosis, and what to change next |

Each agent loads only the reference files it needs and writes its output to a file. The
orchestrator summarizes in a couple of lines and points you at it — it never pastes a full
deliverable into the conversation.

---

## Folder map

```
YoutubeAgents_Pipeline/
├── .claude-plugin/
│   ├── plugin.json              # plugin manifest
│   └── marketplace.json         # lets this folder register as its own marketplace
├── skills/
│   └── orchestrator/
│       └── SKILL.md             # startup sequence, routing, gates, state model
├── agents/                      # the 14 subagent definitions, one file each
├── references/                  # 13 knowledge files + market files, loaded on demand
│   ├── benchmarks.md            # SINGLE SOURCE OF TRUTH for every number
│   ├── algorithm-guide.md       ├── analytics-guide.md
│   ├── retention-scripting-guide.md
│   ├── hook-library.md          ├── seo-playbook.md
│   ├── thumbnail-ctr-guide.md   ├── shorts-playbook.md
│   ├── monetization-guide.md    ├── repurposing-guide.md
│   ├── community-guide.md       ├── localization-guide.md
│   ├── data-sources.md          # integrations and their fallbacks
│   └── markets/                 # what a view is WORTH, by market
│       ├── _index.md            # schema + how to blend a multi-market audience
│       ├── br.md                ├── us.md
├── templates/
│   ├── channel-types/           # _schema.md + 14 channel archetypes
│   └── outputs/                 # deliverable formats agents write into
├── execution/                   # optional Python layer for live YouTube data
│   ├── fetch_channel_data.py    # channel stats + recent videos (cheap path)
│   ├── fetch_video_analytics.py # private analytics, OAuth, own channel only
│   ├── fetch_transcript.py      # captions as timed segments
│   ├── search_competitor_videos.py  # keyword search (expensive — 100 units/call)
│   └── utils/
│       ├── youtube_auth.py      # API key + OAuth, credentials never in this folder
│       └── quota_tracker.py     # daily quota ledger and pre-flight checks
└── workspace/                   # everything the matrix produces about YOUR channel
    ├── config.json              # language, market, channel type (created on first run)
    ├── channel-profile.md       # written by channel-strategist — the full spec
    ├── channel-summary.md       # the same thing in one readable page, for you
    ├── calendar.md, competitors.md, audit-<date>.md, monetization-plan.md
    └── videos/
        └── 2026-08-24_my-video-slug/    # one folder per video, dated on entry
            ├── _state.json              # where this video is in the pipeline
            ├── _handoff.md              # decisions made and rejected so far
            ├── _log.md                  # append-only trail of what each agent did
            ├── research-dossier.md      ├── idea-cards.md
            ├── hooks.md                 ├── script-a-narrative.md
            ├── script-b-instructional.md├── script-c-argumentative.md
            ├── script-recording.md      # the clean version you read on camera
            ├── seo-package.md           ├── thumbnail-brief.md
            ├── metadata-package.md      ├── shorts-plan.md
            └── production-package.md    # the final deliverable
```

### One folder per video

Every video gets one folder named `YYYY-MM-DD_<slug>`, and **everything about that video lives
inside it**. The date is when the video entered the pipeline, not its publish date — publish
dates move, this one doesn't, and it keeps the list in chronological order.

### File ownership

**Every file has exactly one agent allowed to write it.** No file is ever written by two agents,
which is what makes it impossible for one to silently overwrite another's work. Any agent may
read anything; writing outside its own file is a defect. If an agent thinks another's output is
wrong, it says so in its summary and you decide.

Three files are the orchestrator's alone — `_state.json`, `_handoff.md` and the final
`production-package.md`. Subagents never touch them; they return results and the orchestrator
persists. `_log.md` is the one shared file, and it is append-only: agents add lines, nobody edits
existing ones.

### Two versions of the things you actually read

Most files here are written for the agents: dense, structured, full of markers and tables,
because that is what makes them unambiguous to parse. That is deliberate and it stays.

But two of those files are also files **you** have to use — one with a camera running, one while
deciding whether an idea fits your channel. Density is a defect there. So each of them ships in
two versions:

| What the agents read | What you read |
|---|---|
| `script-a/b/c-*.md` — timestamps, `[B-ROLL:]`, `[INTERRUPT]`, beat claims, evidence traces | `script-recording.md` — what the scene is, then exactly what to say. No markup, no jargon. |
| `channel-profile.md` — the full specification, every field, every test | `channel-summary.md` — one page of plain prose, under 500 words |

The agent-facing file is always the source of truth. The readable one restates it and never
decides anything on its own, both are written by the same agent in the same run, and the recording
script is generated only for the variant you actually approve at Gate 2 — not for all three.

### Why `_handoff.md` and `_log.md` exist

A subagent starts with **no memory of your conversation**. It knows only what the orchestrator
put in its prompt. The classic failure in a system like this is an agent producing something
technically fine but misaligned with a decision you made three stages ago — a thumbnail concept
built on the script variant you already rejected.

`_handoff.md` is the briefing that prevents it: what was approved, **what was rejected and why**,
your own words wherever you expressed a preference, and anything an agent must not do. The
orchestrator rewrites it before every delegation and every agent reads it first.

`_log.md` is the trail: one line per agent, appended when it finishes.

```
2026-08-24 14:02 · research-agent · wrote research-dossier.md · 3 angles found, no timing hook
2026-08-24 14:35 · orchestrator · GATE 1 passed · approved #3, rejected #1 as "too broad"
2026-08-24 15:10 · script-agent · wrote hooks.md + 3 variants · used hooks 2/5/7 · recommends C
```

That is what lets you come back to a video weeks later without reconstructing the reasoning.

`workspace/` is yours and is git-ignored. Everything else is the plugin.

---

## Optional integrations

**None of these are required.** The matrix is designed to run with zero credentials, and the
common case is exactly that.

| Integration | Adds | Without it |
|---|---|---|
| YouTube Data API v3 (`YOUTUBE_API_KEY`) | Channel stats, video lists, public counts, competitor search | Ask the creator for the channel URL, subscriber count, and the last 10 titles with view counts and dates |
| YouTube Analytics API (OAuth) | Private analytics for a channel they own: impressions, CTR, retention, traffic sources, revenue | Ask for five numbers off the Studio Overview screen, and a screenshot of the retention curve |
| DataForSEO MCP | *Optional enhancement, only if such a tool is present in the session:* replaces the demand proxies with real search volume, keyword difficulty and SERP composition | **The default path.** WebSearch plus the free demand proxies in `seo-playbook.md` §3 — qualitative, never presented as measured volume |
| Image-generation MCP | *Optional enhancement, only if such a tool is present in the session:* also renders the concepts as 16:9 images saved beside the brief, to compare and iterate on | **The default path, and the normal case.** The English generation prompts are the deliverable — complete and usable in any generator |
| WebSearch | Current facts, competitor context, trend signals | Reason from the reference files and mark the file `⚠️ unverified` |

Setup for each is in `references/data-sources.md`. To enable the Python layer:

```bash
pip install google-api-python-client google-auth-oauthlib
export YOUTUBE_API_KEY="your-key"                     # Data API, public data
python execution/utils/youtube_auth.py --authorize    # Analytics API, your own channel
python execution/utils/youtube_auth.py --check all    # verify without printing anything secret
```

Credentials live in environment variables and your own config directory
(`~/.config/youtube-agent-matrix/`) — **never** inside the plugin folder, never in a deliverable,
never in the chat.

> ### The golden rule
> **Nothing ever blocks on a missing integration.** Detection is by attempting the call. If it
> fails, the matrix falls back, says so in one line, and finishes the deliverable. An agent that
> stops to demand an API key has failed; an agent that asks for three numbers off a Studio screen
> and then ships the full deliverable has succeeded.

---

## How to read the numbers

Every benchmark in this matrix carries a **confidence tag** — `A`, `B` or `C`. It appears next to
tables and figures throughout `references/benchmarks.md` and in the market files.

**The tag is not a measure of how sure the system is. It describes the quality of the evidence
behind the number.**

| Tag | What it means | How much weight it holds |
|---|---|---|
| **`A`** | Multiple independent sources agree, or a single study with a large sample | Solid. Plan around it. |
| **`B`** | One credible source — an industry report, a platform announcement, a vendor's dataset | Usable. Verify before a big commitment. |
| **`C`** | Directional only — anecdotal, a single case study, or a structural heuristic rather than a measurement | A hint, not a fact. |

**The practical rule: never make an irreversible decision on a `C`.** A `C` is good enough to
choose between two experiments. It is not good enough to quit a job over, quote to a sponsor as a
rate, or build a revenue forecast on. When an agent hands you a projection built on `C` figures, it
must present it as a modelled range with its assumptions stated — never as a prediction.

Some things are honest about being unknown. `benchmarks.md` §11 keeps a **known gaps** list — for
instance, nobody has verified data on how long each subscriber tier takes to reach, or what a
channel of a given size typically earns per month. When an agent needs one of those, the correct
answer is "benchmark unavailable" plus what it would take to find out. That is working as
designed, not a failure.

**Two honest caveats about the tags themselves.** First, they reflect what each source claims
about its own methodology — this is not an independent audit of primary research. Second,
`references/localization-guide.md` is `C` throughout, by its own admission: regional revenue
multipliers move constantly and should be re-verified against your own Analytics before you rely
on them.

---

## Design principles

**One file owns every number.** Every benchmark — CTR ranges, retention targets, RPM figures,
title length limits, quota costs — has exactly one home: `references/benchmarks.md`. Other files
cite it by section, and may quote a value inline **alongside that citation** so the reader is not
forced to open a second file. What no file may ever do is **originate** a benchmark, or state one
that **contradicts** `benchmarks.md`. The citation is what makes an inline number legitimate; an
uncited one is a defect. When a figure changes it changes in one place, every citation points
there, and nothing in the system is permitted to disagree with itself.

**Never fabricate a statistic.** If a number an agent needs is not in `benchmarks.md`, the correct
output is "benchmark unavailable" plus what it would take to find out. A plausible invented figure
is the single worst thing this system could produce, because it looks exactly like a real one.
Search results and API responses are evidence; they never become benchmarks.

**Gates are never skipped.** Three approval points, and the matrix stops at each one. It always
recommends an option with a reason — a gate is for your approval, not for offloading the thinking
onto you. Loose approvals are accepted ("go with C", "yeah do it"); ambiguity is asked about once,
briefly.

**Graceful degradation everywhere.** Every integration is optional, every failure has a named
fallback, and the fallback is specific: not "give me your data" but "Studio → Analytics →
Overview, last 28 days, these five numbers." Degraded analysis is stated as degraded rather than
quietly shipped as complete.

**Dense for machines, readable for you.** The files agents parse and the files a person reads
have opposite requirements, and trying to satisfy both in one document fails at both. So the
script and the channel profile each ship twice — the full specification the agents consume, and a
stripped, plain-language view for the human who has to act on it. The second is always derived
from the first, never a second source of truth.

**Markets are researched, not multiplied.** Every revenue figure in `benchmarks.md` is
US-baseline. Rather than scaling it by a single fudge factor, each supported market gets its own
researched file — because the difference is not only *level* but *shape*. Brazil's RPM curve is
flatter than the US one, which means "pick a high-RPM niche" buys far less there than the US data
implies. Seasonality inverts too: back-to-school is February in Brazil, and Carnaval is a trough
that has no US equivalent. A multiplier captures none of that. Markets without a file still get
the directional multiplier from `references/localization-guide.md`, and the deliverable says
which one it used.

**Channel type drives the output.** A generic system produces generic advice. Classification
against `templates/channel-types/_schema.md` loads an archetype carrying its own cadence, length,
CTR target, retention target, title patterns, hook frameworks and monetization stack — that is
how the same matrix produces different, specific answers for a tutorial channel and an ambient
channel.

---

## Not covered

This is a **pre-production and channel-operations** system. It ends where the camera starts.

- **Recording** — no capture, no lighting, no audio engineering.
- **Editing** — no cuts, no colour, no sound design, no rendering.
- **Publishing** — nothing is uploaded on your behalf. The metadata package is copy-paste ready;
  you paste it.
- **Thumbnail rendering** — the deliverable is the concepts and their English generation
  prompts; rendered images only if an image-generation tool happens to be available in the
  session. Final compositing and overlay text happen in your editor.
- **Community management at scale** — the matrix advises on comments, Community tab and
  collaborations; it does not post for you.

What it does own: everything from "I have a channel" to "I have a script, a title, a description,
a thumbnail brief and a Shorts plan sitting in a folder, approved and ready to shoot."

---

## Credits

Inspired by [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) (MIT),
which was used as a knowledge base while designing this matrix.

No code was copied — every file here was written from scratch against a different architecture —
but that project mapped the problem space first, and several of its choices shaped this one: a
skill routing to specialized workers, benchmark-grounded output, channel archetypes as the
mechanism for turning generic advice into specific advice, and graceful degradation when an
integration is missing.

Where this matrix diverges: one file owns every benchmark and the contradictions between sources
are reconciled explicitly; archetypes are classified on five axes instead of picked from nine
mutually exclusive buckets, and every agent reads them rather than only two; hooks have a named
taxonomy; markets and languages are first-class instead of assumed to be US English; and the
system carries approval gates with explicit state.

---

## License

MIT — see [LICENSE](LICENSE).
