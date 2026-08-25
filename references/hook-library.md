# Hook Library

**Purpose.** The ten canonical hook frameworks with mechanisms, templates and worked lines — plus hook structure, surface-specific rules, a generation drill and a selection table.

**Script structure lives in `retention-scripting-guide.md`. Numbers live in `benchmarks.md`** — early-retention thresholds are §2, Shorts hook and swipe-away thresholds are §8. A Stat Shock hook may only cite a number that exists there, in the creator's analytics, or in verified research.

**Contents:** 1 What a hook is and what it must do · 2 The ten frameworks · 3 The 0–5 / 5–15 / 15–30 structure · 4 Hooks by traffic source · 5 Paying the title's promise · 6 The retitle / rehook loop · 7 Shorts hooks · 8 The 10-hook generation drill · 9 Anti-patterns and fixes · 10 Hook selection decision table · 11 Decision rules

## 1. What a hook is and what it must do

A hook is the opening span of a video whose only job is to convert a click into a viewing. It is a *retention* instrument, not a packaging one — packaging earned the click, the hook keeps it. The share of viewers lost in the opening seconds and minute, and the retention thresholds that mark a working hook, are in `benchmarks.md` §2.

Every hook must do four things, in this order of priority:

| Job | Test |
|---|---|
| **Stop the exit** | Would this stop a scroll if the viewer had no context? |
| **Confirm the promise** | Does the viewer immediately recognize the thing the title/thumbnail promised? |
| **Open a loop** | Is there a stated unanswered question they now want closed? |
| **Establish stakes** | Is it clear what they gain by staying or lose by leaving? |

**A hook is written last.** Write the video, find its most surprising true statement, and build the hook from that. Hooks written first tend to promise something the script does not deliver — which is the mismatch failure in `algorithm-guide.md` §9.

## 2. The ten frameworks

These names are canonical across this plugin — archetype templates and agents reference them by exact name.

### 2.1 Curiosity Gap
**State that something specific and knowable exists, without stating what it is.** An information gap creates discomfort the brain wants to close. The gap must be *narrow and specific* — a vague gap creates no tension.
**Works when:** the payoff is genuinely non-obvious and arrives soon. **Fails when:** the answer is guessable, or withheld too long — then it reads as bait. **Suits:** education, commentary, faceless, niche-authority · browse and suggested traffic.
**Template:** `There's one [THING] that [SURPRISING OUTCOME] — and almost nobody [ACTION].`
**Examples:** "There's one setting in [SUBJECT] that changes everything, and it's off by default." · "Three of these [ITEMS] are fine. One of them is quietly costing you money."

### 2.2 Problem–Agitation
**Name the viewer's problem, then make its cost vivid before offering relief.** Recognition plus urgency. The viewer sees themselves described, and the cost makes waiting feel expensive.
**Works when:** the audience already feels the problem. **Fails when:** the problem is hypothetical, or agitation runs so long it becomes unpleasant. **Suits:** tutorial, education, niche-authority, personal-brand · search traffic above all.
**Template:** `If [SITUATION] keeps happening, it's not [ASSUMED CAUSE] — and it's costing you [COST].`
**Examples:** "If your [PROCESS] keeps breaking at the same step, the problem isn't the step. It's what you did two steps earlier." · "Every week you leave this unfixed, you're redoing work you already paid for."

### 2.3 Shock / Contradiction
**Open with a statement that contradicts what the audience believes.** Expectation violation. A belief that just got challenged must be resolved.
**Works when:** you can actually defend the claim within the video. **Fails when:** the contradiction is semantic sleight-of-hand — audiences punish this hard. **Suits:** commentary, education, review, video essay · browse and suggested.
**Template:** `Everything you've been told about [TOPIC] assumes [ASSUMPTION]. That assumption is wrong.`
**Examples:** "[COMMON PRACTICE] doesn't work. It hasn't for years, and the data was there the whole time." · "The advice everyone repeats about [TOPIC] was true once. The conditions that made it true are gone."

### 2.4 Story Open
**Drop into a specific moment mid-scene, then reveal why it matters.** Narrative transportation. A concrete scene occupies attention before the viewer decides whether to stay.
**Works when:** the story is genuinely yours or genuinely specific. **Fails when:** it is generic, or the connection to the promise is slow. **Suits:** vlog, narrative, personal-brand, entertainment, podcast · browse and subscriptions.
**Template:** `[TIME MARKER], [SPECIFIC VIVID MOMENT]. Here's how that happened.`
**Examples:** "Six hours before the deadline, the entire thing stopped working — and the cause was a single line nobody had touched in a year." · "The first time I tried [ACTION], I got it completely wrong. What I learned from that is the whole video."

### 2.5 Social Proof
**Lead with adoption, scale, or a credible track record.** Herd validation plus authority — it lowers the risk of investing time.
**Works when:** the proof is specific and verifiable. **Fails when:** it is vague ("everyone's talking about this") or reads as bragging without a viewer benefit. **Suits:** review, niche-authority, business/education, personal-brand · search and suggested.
**Template:** `[SPECIFIC NUMBER OR GROUP] have already [ACTION]. Here's what they figured out that most people haven't.`
**Examples:** "After going through this process [N] times, the same three mistakes came up every single time." · "Every practitioner I asked named the same tool — and none of them named the popular one."

### 2.6 Stat Shock
**Open on a single striking, verifiable number.** Concreteness. A number is unambiguous, memorable, and hard to argue with.
**Works when:** the number is real, sourced, and surprising. **Fails when:** it is invented, unsourced, or so large it feels abstract. **Suits:** education, faceless, commentary, niche-authority · search and browse.
**Template:** `[NUMBER + UNIT] of [GROUP] [SURPRISING FACT]. Here's what that actually means for you.`
**Examples:** "[N]% of [GROUP] never get past the first step — and the reason has nothing to do with effort." · "The difference between the top and bottom result was [N]×. Same inputs, same conditions."

> **Sourcing rule.** A Stat Shock hook may only use a number that exists in `benchmarks.md`, in the creator's own analytics, or in a source the research stage verified. Never invent one to make a hook land.

### 2.7 Negative Framing
**Lead with what to stop, avoid, or what is going wrong.** Loss aversion — the threat of a mistake outweighs the promise of a gain.
**Works when:** the mistake is common and the viewer might be making it. **Fails when:** it is used on every video, which makes a channel exhausting. **Suits:** tutorial, education, review, niche-authority · search and browse.
**Template:** `Stop [COMMON ACTION]. It's the reason [BAD OUTCOME], and here's what to do instead.`
**Examples:** "Most people doing [TASK] make the same mistake in the first five minutes, and it can't be fixed later." · "If you're still [PRACTICE], you're solving a problem that stopped existing."

### 2.8 Direct Challenge
**Address the viewer and challenge them to do, prove, or reconsider something.** Personal address plus mild ego threat. Being singled out interrupts passive viewing.
**Works when:** the audience is confident and engaged. **Fails when:** it reads as insulting, or the viewer cannot actually meet the challenge. **Suits:** gaming, entertainment, personal-brand, commentary · browse and Shorts.
**Template:** `You think you [CAPABILITY]? Try [SPECIFIC TEST] and see what happens.`
**Examples:** "Bet you can't explain why [COMMON THING] works. Most people who use it daily can't." · "Try doing [TASK] without [CRUTCH]. That's the whole video."

### 2.9 Demonstration
**Show the result, process or effect immediately — no verbal setup.** Visual proof arrives faster than language and needs no trust.
**Works when:** the subject is visual and the result is impressive at a glance. **Fails when:** the subject is abstract, or the demo needs explanation to be legible. **Suits:** tutorial, review, gaming, entertainment, shorts-first · every traffic source; the strongest hook for Shorts.
**Template:** `[SHOW THE FINISHED RESULT / THE EFFECT IN ACTION] — "this took [TIME/EFFORT]. Here's exactly how."`
**Examples:** "(shot of the finished outcome) That's the end state. Twelve minutes from now you'll have it too." · "(the failure happening on camera) That's what it looks like when it goes wrong. Now watch the fix."

### 2.10 Stakes Framing
**Establish what is at risk, what the constraint is, or what happens if this fails.** Consequence creates investment — outcomes matter only when something is on the line.
**Works when:** the stakes are real and legible fast. **Fails when:** they are manufactured; audiences detect inflated stakes quickly. **Suits:** narrative, entertainment, gaming, documentary, podcast · browse and suggested.
**Template:** `[CONSTRAINT: time / money / one attempt]. If [FAILURE CONDITION], [CONSEQUENCE].`
**Examples:** "One attempt, no do-overs. If this doesn't work, the whole [PROJECT] is wasted." · "Thirty days, a fixed budget, and one rule: [RULE]. Here's how far that got."

## 3. The 0–5 / 5–15 / 15–30 structure

Three windows, three different jobs. Retention thresholds for each are in `benchmarks.md` §2.

| Window | Must accomplish | Must NOT contain |
|---|---|---|
| **0–5s** | The framework fires. Something visually or verbally arresting. In autoplay contexts this window is an extension of the thumbnail — the viewer is deciding while it plays | Greetings, channel branding, logo stings, "in this video", any setup |
| **5–15s** | The promise, stated explicitly: what the viewer will have, know or see by the end. This is the value-proposition window in `benchmarks.md` §2 | Backstory, credentials, sponsor reads, apologies |
| **15–30s** | Stakes and scope: why it matters, what's covered, and the first open loop is left running | Long context, disclaimers that can wait, a second full framework |

**The three windows are not three hooks.** One framework runs through all three — it fires at 0–5, resolves into a promise at 5–15, and gains weight at 15–30. Stacking three frameworks promises three unrelated things. **Scale to length:** a short video compresses all three into the first 10–15 seconds; a documentary or podcast spends the first 60 on the same three jobs. The *order* never changes.

## 4. Hooks by traffic source

The viewer arrives in a different mental state per surface, and the hook must meet that state.

| | **Search** | **Browse / Suggested** | **Shorts** |
|---|---|---|---|
| Viewer state | Has a question, wants confirmation this answers it | No intent, evaluating whether to care | Thumb already moving toward the swipe |
| First job | Confirm relevance *fast* — restate their query in their words | Create interest from nothing | Physically stop the swipe |
| Best frameworks | Problem–Agitation, Negative Framing, Social Proof, Stat Shock | Curiosity Gap, Shock/Contradiction, Story Open, Stakes Framing | Demonstration, Direct Challenge, Shock/Contradiction |
| Curiosity gaps | Use sparingly — the viewer wants an answer, not a puzzle | Core technique | Only if resolvable in seconds |
| Speed | Promise inside the first seconds; searchers abandon fast | Slightly more room, but not much | Instant |
| Common failure | Making them wait for confirmation they're in the right place | Being informative before being interesting | Any setup at all |

**The mismatched-surface rule:** a curiosity-gap hook on a search video withholds the exact thing the viewer searched for; a relevance-confirming hook on a browse video answers a question nobody asked. Both underperform.

## 5. Paying the title's promise

The hook's second job (§1) is a contract obligation. The title and thumbnail made a promise; the hook must visibly begin paying it.

| Packaging promised | Hook must | If it doesn't |
|---|---|---|
| A specific answer | Confirm the answer exists here, and start moving toward it | Immediate exit; the viewer assumes they're in the wrong place |
| A transformation or result | Show or state the result | Retention cliff in the first seconds |
| A revelation or reveal | Confirm the reveal is real and say roughly when it lands | Reads as bait; suppresses satisfaction signals |
| A comparison or verdict | Name the contenders and confirm a verdict is coming | Viewers skip forward, which reads as dissatisfaction |
| A story | Enter the story immediately | Curve collapses through the setup |

**What breaks when the hook doesn't pay:** high CTR with early abandonment — the signature of the metadata-mismatch penalty (`algorithm-guide.md` §9; matrix in `analytics-guide.md` §5). The channel's prediction prior absorbs the damage too. **The reverse failure — under-promising** — is safe but wasteful: a hook far more modest than the packaging makes the viewer downgrade and leave anyway. Match the packaging's register, then exceed it.

## 6. The retitle / rehook loop

Packaging and hook are one system tested together. When performance is wrong, change the cheaper end first.

| Symptom | Change | Why |
|---|---|---|
| Low CTR, healthy retention | **Title/thumbnail** | The hook works; not enough people are reaching it |
| High CTR, early cliff | **Hook first** — then retitle if the hook cannot honestly pay the promise | The click is being earned dishonestly |
| High CTR, cliff, and the video genuinely doesn't deliver the title | **Retitle** to what it actually delivers | Rewriting a hook cannot manufacture content that isn't there |
| Both low | Rebuild the idea | Packaging cannot rescue a topic with no demand (`algorithm-guide.md` §10) |

**On a published video** retitling is possible and rehooking is not, short of a re-upload — which discards the video's accumulated signals. Fix the title to match the existing hook and carry the lesson forward. **On the next video:** write the title first, write the hook to pay *that* title, then confirm the script delivers it. Change one element at a time so the lesson stays attributable (`analytics-guide.md` §9).

## 7. Shorts hooks

Shorts ranking is completion-driven, not click-driven (`benchmarks.md` §8), which changes the hook entirely.

| Constraint | Consequence |
|---|---|
| Hook window is the first 1–3 seconds (`benchmarks.md` §8) | There is no time for a sentence. The first *frame* is the hook |
| No thumbnail, no title read before playback | The opening frame does the packaging job as well as the hook job |
| Swipe-away rate is the primary hook metric (`benchmarks.md` §8) | Diagnose the opening against that threshold, not against CTR |
| Visual change cadence (`benchmarks.md` §8) | The hook is visual before it is verbal |

**Rules:**

1. **Start mid-action** — no intro, no framing, no "so today". The first frame shows something already happening, and it carries the most striking visual you have: the finished result, the failure, the contradiction.
2. **The first spoken words are the payload,** not a preamble. Cut every word before the first meaningful one, and state the promise by second three.
3. **Loop-friendly endings:** an ending that flows back into the opening earns replays, which are ranked (`benchmarks.md` §8).
4. **Best frameworks:** Demonstration first, then Direct Challenge and Shock/Contradiction. Story Open and Stakes Framing rarely work — they need setup time that does not exist.

**Diagnosis:** if swipe-away is above the emergency threshold in `benchmarks.md` §8, rewrite the first three seconds only. Do not rebuild the whole Short.

## 8. The 10-hook generation drill

Run this whenever a hook is needed. It produces range, then selects — never write one hook and defend it. **The counts, end to end: generate 10 raw, shortlist 8 for delivery across at least 5 different frameworks, and return the top 3 with their full 0–5s / 5–15s / 15–30s continuations written out (§3).**

| Step | Do |
|---|---|
| 1 | State the video's single most surprising **true** statement, in one sentence. This is the raw material |
| 2 | Write one hook per framework from §2 — all ten, even the ones that feel wrong for the format |
| 3 | Cross out any hook the script cannot honestly pay off |
| 4 | Cross out any hook that opens with a greeting, the channel name, or a setup clause |
| 5 | Score each survivor: *stops the exit* / *confirms the promise* / *opens a loop* / *fits the traffic source* — one point each |
| 6 | Keep the best **8** survivors, spanning at least **5 distinct frameworks**. If fewer than 8 survive, or fewer than 5 frameworks are represented, go back to step 2 — and if the drill still cannot fill it, the problem is the video's premise, not the hook |
| 7 | Read all 8 aloud. Cut every word before the first interesting one |
| 8 | Deliver all 8 with the framework named for each, then rank them and write the full 0–5s / 5–15s / 15–30s continuation (§3) for the **top 3** only, with a one-line reason for the recommendation |

**Why ten, why eight, why three.** Generating all ten forces frameworks the creator would not have reached, and the winner is frequently one of them; generating three produces three variations on one instinct. Eight is what gets delivered, because a shortlist wide enough to span five frameworks keeps the choice genuinely open. Three get the full continuation, because writing three windows out is expensive and only the contenders earn it. **Word budget:** a hook's budget is `seconds ÷ 60 × the speaking rate for the output language` (`retention-scripting-guide.md` §6, `localization-guide.md` §7) — roughly 70 words for 30 seconds at the ~140 wpm English baseline, and a different number in every other language. A hook that exceeds its window's budget is an intro, not a hook.

## 9. Anti-patterns and fixes

| Anti-pattern | Why it costs retention | Fix |
|---|---|---|
| **Greeting** — "hey guys, welcome back" | Zero information; a measurable drop-off trigger. It signals a channel-first video, not a viewer-first one | Delete it. Start on the framework's first line |
| **Channel name / branding sting** | Branding matters to the creator, not to a viewer deciding whether to stay | Move it to a mid-video lower third, or cut it |
| **"In this video I'm going to…"** | Announces content instead of delivering it — costs seconds and adds nothing | Deliver the thing. "In this video I'll show you X" → "Here's X" |
| **Throat-clearing** — "so", "okay so", "alright", "um, so basically" | The viewer hears hesitation before value | Cut every word before the first meaningful one (§8, step 7) |
| **Delayed promise** | The value proposition arrives after the window in `benchmarks.md` §2 | Move the promise into 5–15s; move backstory after 30s or cut it |
| **Over-promising** | Triggers the mismatch penalty (`algorithm-guide.md` §9) | Promise what the script delivers, then exceed it in the body |
| **Sponsor read in the opening** | Trades the highest-value seconds for a commercial | Move to the first mid-video CTA slot (`retention-scripting-guide.md` §7) |
| **Credentials before value** | Nobody grants authority to a stranger before receiving anything | Demonstrate competence; mention credentials briefly if at all |
| **Vague teasing** — "stick around, it gets crazy" | Opens no specific loop, so nothing is left unresolved | Name the specific unanswered question and when it resolves |
| **Recap of a previous video** | Punishes new viewers, bores returning ones | One clause of context maximum, then forward |
| **Apologizing** — "sorry for the long intro" | Draws attention to a flaw the viewer might have overlooked | Remove the flaw instead of naming it |
| **Stacked frameworks** | Three hooks in a row promise three unrelated things | Pick one framework and run it through all three windows (§3) |

## 10. Hook selection decision table

Primary is the default; secondary is the alternative to test against it.

| Traffic source | Viewer intent | Primary | Secondary |
|---|---|---|---|
| Search | Solve a problem | Problem–Agitation | Negative Framing |
| Search | Learn a subject | Stat Shock | Curiosity Gap |
| Search | Decide a purchase | Social Proof | Demonstration |
| Suggested | Learn a subject | Curiosity Gap | Shock/Contradiction |
| Suggested | Understand an event | Shock/Contradiction | Stakes Framing |
| Suggested | Decide a purchase | Demonstration | Negative Framing |
| Browse | Be entertained | Story Open | Stakes Framing |
| Browse | Understand an event | Shock/Contradiction | Curiosity Gap |
| Browse | Follow a person | Story Open | Direct Challenge |
| Browse | Learn a subject | Curiosity Gap | Stat Shock |
| Shorts feed | Be entertained | Demonstration | Direct Challenge |
| Shorts feed | Learn a subject | Stat Shock | Shock/Contradiction |
| Shorts feed | Solve a problem | Demonstration | Problem–Agitation |
| External | Any | Demonstration | Problem–Agitation |
| Subscriptions | Follow a person | Story Open | Stakes Framing |

**Tie-break rules:** the archetype template's §6 Hook Style overrides this table when they disagree — it is channel-specific and this table is general. Where the video's format is inherently visual, Demonstration outranks whatever the table says. Where the creator's voice is built on a stance, Shock/Contradiction and Direct Challenge outperform their table position.

## 11. Decision rules

- **If** writing a hook → generate all ten frameworks (§8), then select three. Never deliver one option.
- **If** the traffic source is known → select from §10 first, then override only with the archetype template's §6.
- **If** the traffic source is unknown → default to the channel profile's dominant source; if that is unknown too, write one search-shaped and one browse-shaped option.
- **If** the video is search-targeted → confirm relevance immediately. Do not open with a curiosity gap.
- **If** the video is a Short → the first *frame* is the hook. Use Demonstration unless there is a reason not to (§7).
- **If** a hook opens with a greeting, channel name, "in this video", or a throat-clearing word → rewrite it. These are non-negotiable (§9).
- **If** a hook promises something the script does not deliver → change the hook, not the script's honesty. Over-promising triggers the mismatch penalty.
- **If** a Stat Shock hook is proposed → the number must come from `benchmarks.md`, the creator's analytics, or a verified research source. Otherwise pick a different framework.
- **If** the value proposition lands after the window in `benchmarks.md` §2 → the hook fails regardless of how good the opening line is.
- **If** no loop is open by the end of the hook → add one (`retention-scripting-guide.md` §3).
- **If** retention is healthy but CTR is low → do not touch the hook; fix packaging (§6).
- **If** a published video needs a new hook → retitle instead. Never re-upload to fix a hook — it discards the video's accumulated signals.
- **If** CTR is high and retention cliffs early → fix the hook first; retitle only if the video genuinely cannot pay the title.
- **If** fewer than three hook options survive the drill's filters → the premise of the video is the problem, not the hook.
