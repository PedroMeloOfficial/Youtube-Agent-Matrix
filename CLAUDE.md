# CLAUDE.md — Maintainer Guide

Guidance for anyone (human or agent) editing this plugin. The user-facing document is
`README.md`; this one is about how the thing is built and how to keep it coherent.

---

## Architecture: three layers

```
  Layer 1   skills/orchestrator/SKILL.md
            Routing, startup sequence, state, gates, delegation contract.
            Holds no domain knowledge and writes no deliverable.
                        │  delegates with an explicit prompt
                        ▼
  Layer 2   agents/*.md
            14 subagents. Each owns its deliverable — two of them also own a
            derived creator-facing view of it, see below. Agents do not call
            each other; the orchestrator fans them out and collects results.
                        │  loads, on demand, only what it needs
                        ▼
  Layer 3   references/*.md  +  templates/channel-types/*.md  +  templates/outputs/*
            Knowledge and shape. Inert: nothing here decides anything.
            execution/*.py sits beside this layer as optional live data.
```

The separation is the point. Routing logic that leaks into an agent makes the agent unusable on
its own. Domain knowledge that leaks into the orchestrator gets loaded on every single request.
Benchmarks that leak into either one start drifting the moment the platform changes.

**Which layer does a change belong in?**

| The change is… | It goes in |
|---|---|
| When something runs, in what order, who approves | `skills/orchestrator/SKILL.md` |
| How one deliverable is produced and what it must contain | `agents/<agent>.md` |
| A fact, a rule, a framework, a mechanic | `references/<topic>.md` |
| A number | `references/benchmarks.md`, and nowhere else |
| Archetype-specific targets and patterns | `templates/channel-types/<type>.md` |
| The shape of a written deliverable | `templates/outputs/` |
| Talking to an API | `execution/` |

---

## Hard authoring rules

**1. `SKILL.md` stays under 500 lines.** It loads on every invocation. Anything that is not
routing, state or gates belongs in a reference file. If it is growing, something has leaked down
from Layer 3 or up from Layer 2.

**2. Reference files stay under ~260 lines.** They are loaded selectively and read in full when
loaded. Past that, split by topic rather than letting one file become the place everything lands.

**`references/benchmarks.md` is exempt from this limit**, and it is the only exemption. Holding
every number in the system in one file is the whole point of rule 3 below — splitting it by topic
would manufacture exactly the second home for a number that rule 3 exists to prevent, and the
first time the two copies drifted the system would start quoting a stale figure with full
confidence. Its length is a consequence of the design, not a symptom of neglect. Keep it
organized by numbered section instead: agents load it by section reference, not by reading it end
to end.

**3. All benchmark numbers live only in `references/benchmarks.md`.** This is the rule the whole
system's credibility rests on. No agent, no template, no other reference restates a CTR range, a
retention target, an RPM figure, a character limit or a quota cost — they point at
`benchmarks.md` instead. Two files holding the same number means one of them is already wrong;
you just do not know which yet.

Grep before you commit:

```bash
grep -rniE '[0-9]+(\.[0-9]+)?\s*%|RPM|CPM' agents/ references/ templates/ \
  --include='*.md' | grep -v 'references/benchmarks.md'
```

Percentages that survive that filter should be structural (a weighting, a split, a share of a
score), never platform data.

**4. Kebab-case filenames throughout.** `hook-library.md`, `channel-auditor.md`,
`niche-authority.md`. Python files stay `snake_case.py` — a module name has to be importable.

**5. Agent frontmatter.** Every file in `agents/` opens with:

```yaml
---
name: agent-name          # MUST equal the filename stem: agents/agent-name.md
description: One sentence on what it owns, then one on when to use it. This is
             what the orchestrator matches against — write it for routing, not for a
             catalogue entry.
tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch   # only what it needs
model: opus               # or sonnet for the lighter agents
---
```

`name` mismatching the filename is the most common breakage: the orchestrator delegates by name
and the agent silently does not exist.

**6. Python scripts output JSON and degrade gracefully.** Every script in `execution/`:

- has a module docstring covering purpose, cost, credentials and usage examples;
- exposes `--help` via `argparse`;
- prints JSON to **stdout** on success (`{"ok": true, ...}`) and on failure
  (`{"ok": false, "error": {"code", "message", "fix"}}`), exiting non-zero on failure;
- **never emits a stack trace** — `install_excepthook()` from `utils/youtube_auth.py` converts
  anything uncaught into a JSON error object;
- names the manual fallback in the error when a credential is missing, so the workflow continues
  without it;
- reads credentials from environment variables and the user config directory
  (`~/.config/youtube-agent-matrix/`) only. Never from, and never written to, the plugin folder.
  Never printed — not in full, not masked;
- checks `utils/quota_tracker.py` before an expensive call and records what it spent;
- depends on nothing beyond the standard library plus `google-api-python-client` /
  `google-auth-oauthlib`.

Compile-check before committing:

```bash
python3 -m py_compile execution/*.py execution/utils/*.py
```

**7. Everything is written in English.** Source files, comments, docstrings, agent prompts. The
creator's chosen language governs *deliverables at runtime*, never the repository.

**8. Stay generic.** No person's name, no real channel, no assumed niche, no assumed market
anywhere in the plugin. Examples use placeholders. A channel-specific detail in a template is a
bug — it will be wrong for every other user.

---

## Adding a new agent

1. **Check it earns a slot.** Does it own a deliverable no existing agent owns? Overlapping
   agents make routing ambiguous, and ambiguous routing is worse than a missing agent.
2. Create `agents/<agent-name>.md` with `name: <agent-name>` matching the filename stem.
3. Write the `description` for routing: what it owns, then when to use it. The orchestrator reads
   this and nothing else when deciding.
4. Grant the minimum `tools`. Only agents that fan out internally need `Agent`. Only agents that
   run the execution layer need `Bash`.
5. Name the reference files it should load, specifically. "Load what you need" makes an agent
   load all thirteen.
6. State its output contract: exact filename, exact sections, where it writes in
   `workspace/videos/<slug>/` or `workspace/`.
7. Register it in three places, or it is invisible:
   - the agents table in `skills/orchestrator/SKILL.md`
   - the routing tables in `skills/orchestrator/SKILL.md` (command and/or natural language)
   - the agents table in `README.md`
8. If it belongs in the production chain, update the chain diagram in **both** `SKILL.md` and
   `README.md`, and decide explicitly whether it sits before, after or inside an existing gate.
   Do not add a fourth gate without a strong reason — gate count is a design budget.
9. Cite no numbers of its own. It reads `benchmarks.md`.

---

## Adding a new channel archetype

Read `templates/channel-types/_schema.md` first — it defines both the five classification axes
and the normalized section order every archetype file follows. Agents read any archetype the same
way, and that only holds if the schema is followed exactly.

1. Confirm it is a genuine archetype, not a niche. "Gaming" is an archetype (different traffic
   surface, cadence, format, monetization). "Cooking" is a niche — it is served by Tutorial or
   Personal Brand.
2. Copy the section order from `_schema.md`. Do not reorder, rename or drop sections.
3. Fill in what makes it *different*: traffic surface, viewer intent, cadence, typical length,
   title and hook patterns, monetization stack, production model.
4. Numbers still come from `benchmarks.md`. If the archetype needs a target that is not there,
   either add it to `benchmarks.md` with a date and a source, or say the benchmark is unavailable.
   Do not invent one to fill the template.
5. Add it to the archetype list in `_schema.md` and to the folder map in `README.md`.
6. Sanity-check the classifier: describe two real-feeling channels of that type and confirm the
   five axes actually land on it rather than on an existing archetype.

---

## Updating a benchmark

The value of `benchmarks.md` is that it is the only place a number lives. Protect that.

1. Change the number **in `benchmarks.md` only**.
2. Update its date and source on the same line or in the section's source note. A number with no
   date is unusable within a year.
3. Set the confidence tag honestly: `A` multi-source or large-N, `B` single credible source,
   `C` directional or anecdotal. Downgrading a tag is a legitimate edit on its own.
4. Grep the repository to make sure no second file picked the figure up:

   ```bash
   grep -rn '<the old number>' . --include='*.md' --include='*.py'
   ```

   Any other file holding it is the bug — remove it there, point at `benchmarks.md` instead.
5. If the number no longer exists in a trustworthy form, move it to §11 *Known gaps* rather than
   keeping a stale value. "Benchmark unavailable" is a correct answer; a stale figure presented
   as current is not.
6. Never let a competing figure survive in an agent, a template or another reference. One number,
   one home.

The one legitimate exception: the per-call quota costs in `execution/utils/quota_tracker.py`.
Those are operational constants the code spends against, not figures the matrix cites. The
headline quota numbers agents quote still come from `benchmarks.md` §10.

---

## Adding a new market

Market files live in `references/markets/`, one per market code, plus `_index.md`. **Read
`references/markets/_index.md` before writing one** — it is the schema: the frontmatter fields,
the fixed ten-section body, the `workspace/config.json` → `markets.mix` config shape, the
weighted-blending method, and the table of which agent reads which section. Agents cite section
numbers, so **do not reorder or renumber sections.**

The hard rules, which are not negotiable:

1. **Every figure carries a confidence tag and a source.** Market data is volatile and mostly
   `C`. A `C` labelled `B` is worse than no number at all.
2. **Write `unavailable` rather than deriving.** If no source gives that niche's RPM for this
   market, say so. Multiplying the US figure and presenting the result as market data is exactly
   the fabrication this system exists to prevent — that is what the multiplier table is for, and
   it must be labelled as a multiplier.
3. **Never restate platform mechanics.** CTR bands, retention thresholds, character limits, YPP
   requirements and quota costs live in `benchmarks.md` and are cited, never copied. A market file
   holds only what actually changes by country: economics, culture, law, rhythm.
4. **State the review date** in `last_reviewed`, and date individual figures where they differ.
5. Written in English, like every reference. Deliverables are translated; references are not.

Then: add the market to the *Available markets* table in `_index.md`, and — if it supersedes a row
in `localization-guide.md` §2 — mark that row superseded rather than deleting it.

**Market files decay faster than any other reference in this repo.** Ad rates, sponsorship norms,
payment rails and disclosure regimes all move within a year, and a stale market file is quoted
with the same confidence as a fresh one. **Re-review every market file at least yearly**, and
downgrade a confidence tag or write `unavailable` rather than letting a figure look current when
it is not.

---

## Localization rule

**Every revenue figure in `benchmarks.md` is US-baseline.** RPM, CPM, sponsorship rates, product
pricing — all of it is United States, English-language, long-form unless a line says otherwise.

Any agent producing a revenue figure for a non-US channel or a non-English audience must adjust it
first: through `references/markets/<code>.md` where that market has a file, and only otherwise
through `references/localization-guide.md`'s directional multiplier table, saying which it used. Unadjusted US RPM applied to an emerging market
is wrong by five to twenty times, and a revenue projection wrong by that much is worse than no
projection at all.

This applies to authoring too: when adding a revenue number to `benchmarks.md`, label the market
it came from. If it is not US, say so on the line — otherwise the conversion is applied twice.

CTR and retention data are **not** regionally adjusted in this matrix. There is no reliable
non-US dataset for them; `benchmarks.md` §11 lists that as a known gap, and it should stay listed
rather than being filled in with guesses.

---

## Derived creator-facing files

Two deliverables ship in two versions, and the distinction is load-bearing:

| Source of truth (agents read this) | Derived view (the creator reads this) | Owner |
|---|---|---|
| `script-{a\|b\|c}-*.md` | `script-recording.md` | `script-agent`, `recording` mode |
| `workspace/channel-profile.md` | `workspace/channel-summary.md` | `channel-strategist` |

Rules when touching either pair:

1. **Only the source is ever read by an agent.** Nothing in the system may depend on a derived
   file. If you find an agent reading one, that is the bug.
2. **Same agent, same run.** Never split the pair across two agents or two invocations — that is
   how they drift.
3. **Derived files originate nothing.** Every statement traces to the source. A fact that exists
   only in the derived view is a gap in the source; fill it there.
4. **The formatting rules in the derived templates are functional requirements, not style.** No
   asterisks, backticks, bracket markers, bold, or internal vocabulary. The templates state why.
5. `script-recording.md` is generated **only for the variant approved at GATE 2**, never for all
   three. Generating three would triple the cost of the most expensive agent in the matrix for
   two files the creator will never open.

Adding a third pair is a real decision, not a freebie: every derived file is another thing that
can fall out of sync. Do it only when asked.

## Maintenance

**Platform numbers decay.** YouTube changes what it counts, how it counts it and what it rewards,
and creator-blog figures propagate outdated numbers for years after the fact. Treat anything
tagged **2024 or earlier as directional**, not as a measurement — safe for framing a decision,
not safe for a projection a creator will act on.

A sensible review pass:

- Re-check §1 CTR, §2 retention and §9 monetization against primary sources annually. Prefer
  platform documentation and official help pages over roundups.
- Re-check §10 analytics and quota limits whenever a script starts failing in a new way.
- When a figure cannot be re-verified, downgrade its confidence tag or move it to §11 rather than
  leaving it looking fresh.
- Keep §11 *Known gaps* honest and current. An accurate list of what the system does not know is
  worth more than a complete-looking list of half-sourced numbers, because it is what stops an
  agent from inventing one.

Before any release, the short checklist:

```bash
python3 -m py_compile execution/*.py execution/utils/*.py   # scripts compile
wc -l skills/orchestrator/SKILL.md                          # under 500
wc -l references/*.md                                       # each around 260 or less;
                                                            # benchmarks.md exempt (rule 2)
grep -L 'name:' agents/*.md                                 # every agent has frontmatter
```

Then confirm each agent's `name` still equals its filename stem, and that any agent added or
renamed appears in the orchestrator's tables and in `README.md`.
