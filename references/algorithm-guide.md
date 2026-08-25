# Algorithm Guide

**Purpose.** A working mental model of YouTube distribution an agent can reason with — the three ranking systems, the testing cascade, session value, clustering, cold start, and a procedure for diagnosing which system a video is actually failing.

**Numbers live in `benchmarks.md`** — CTR by traffic source is §1, retention thresholds are §2, cadence effects are §4, the cascade and satisfaction ranking are §5, Shorts signals are §8. §11 lists cold-start velocity as a **known gap**: say it is unavailable rather than inventing a figure.

**Contents:** 1 The core reframe · 2 Three independent ranking systems · 3 The testing cascade and what failing a layer looks like · 4 Satisfaction signals and how to design for each · 5 Session initiation vs session continuation · 6 Topical clustering and niche discipline · 7 The cold-start problem · 8 Context weighting: device, surface, format · 9 The metadata-mismatch penalty · 10 Diagnostic procedure: which system are you failing? · 11 Misattribution: what creators blame on "the algorithm" · 12 Decision rules

## 1. The core reframe

The recommendation system is a **per-viewer prediction engine**. It does not rank videos globally. For each viewer, on each surface, at each moment, it predicts: *will this specific person click this, watch it, and be glad they did?*

Three consequences follow, and almost every strategic error comes from ignoring one of them:

| Consequence | What it means in practice |
|---|---|
| There is no global ranking | "My video was suppressed" is almost never true. It was predicted to underperform *for the viewers it was offered to*. |
| Prediction is relative to a baseline | The system compares a video to what it expected from *this channel*, *this topic*, *this surface* — not to the platform average. |
| Satisfaction outranks consumption | Watch time that a viewer later regrets is worth less than watch time they act on. The system infers regret from downstream behavior. |

**The operative substitution:** replace the word "algorithm" with "audience." Every distribution question becomes a behavioral question — why would this person click, why would they stay, why would they tell someone. This substitution is not a motivational slogan; it is a debugging technique. If a hypothesis about the algorithm cannot be restated as a hypothesis about human behavior, it is not a real hypothesis.

## 2. Three independent ranking systems

Browse, Search and Shorts are separate systems with separate signal hierarchies (`benchmarks.md` §5). A video is ranked in each one independently. Failing one says nothing about the others.

| | **Browse** | **Search** | **Shorts** |
|---|---|---|---|
| Viewer state | No intent, scrolling | Explicit query, high intent | No intent, high tolerance for skipping |
| Question it answers | "What should this person watch now?" | "What best answers this query?" | "Will this person watch to the end?" |
| Entry signal | Thumbnail + title against a personalized feed | Query–metadata match, then engagement | First frame; clicks do not exist |
| Ranking driver | Predicted satisfaction and session value | Relevance × satisfaction on that query | Completion and replay (`benchmarks.md` §8) |
| Decay profile | Fast — front-loaded, then long tail if satisfaction holds | Slow — compounds for months or years | Fastest — a hard freshness window (`benchmarks.md` §8) |
| CTR expectation | Lowest of the three (`benchmarks.md` §1) | Highest of the three (`benchmarks.md` §1) | Not applicable |

### How strategy differs per system

| Decision | Browse-first | Search-first | Shorts-first |
|---|---|---|---|
| Topic selection | Broad emotional appeal, timeliness, curiosity | Existing query demand with beatable competition | Format repeatability; a template you can run weekly |
| Title | Short, readable at a glance (`benchmarks.md` §6 reconciliation) | Longer, keyword-bearing (same section) | Barely visible; write for the ~40-char cut (`benchmarks.md` §8) |
| Thumbnail | Everything. The single highest-leverage asset | Matters, but relevance gates it first | Irrelevant — the first frame replaces it |
| Hook | Must justify a click made on impulse | Must confirm the query is answered here | Must stop a swipe before the viewer decides |
| Success horizon | Days | Months | Hours to days |
| Failure signal | Impressions rise, CTR collapses | Impressions never rise at all | Swipe-away rate (`benchmarks.md` §8) |

**Rule:** never diagnose a video against a benchmark from a system it is not competing in. A browse-dominant video judged against search CTR looks broken when it is healthy — `benchmarks.md` §1 states this reconciliation explicitly.

## 3. The testing cascade and what failing a layer looks like

Distribution expands in layers (`benchmarks.md` §5). Each layer must meet the prediction set for it before the next unlocks. The cascade is invisible in Studio, but its failures have distinct fingerprints.

| Layer | Audience | Analytics fingerprint of success | Fingerprint of failing *here* |
|---|---|---|---|
| 1 · Core | Subscribers and frequent viewers | Sharp early impression spike; CTR at its lifecycle peak (`benchmarks.md` §1) | Impressions plateau within hours and never expand; CTR fine, volume tiny |
| 2 · Expanded | Similar interest profiles | Impressions keep climbing on day 2–3; traffic source mix widens beyond Subscriptions | Impressions stall on day 2 while retention looks acceptable — usually a topic-demand ceiling |
| 3 · Broader | Wider demographic or adjacent topics | Suggested traffic appears and grows; new-viewer share rises | Suggested never appears; the video is trapped inside the subscriber base |
| 4 · Authority | Trending and high-reach surfaces | Non-linear impression growth days after publish | Rare and mostly outside a creator's control — do not plan for it |

**How to read a stall.** The layer you failed is the last one whose fingerprint you achieved. A video that never left layer 1 has a *packaging or topic* problem within its own audience. A video that reached layer 2 and stopped has a *satisfaction* problem — the expanded audience clicked and left.

**What advances a layer:** performance *against prediction*, not against absolutes. A modest video that beats its own low prediction can advance further than a strong video that falls short of a high one. This is why a channel's own recent performance sets the difficulty of its next upload.

## 4. Satisfaction signals and how to design for each

The ranked order is in `benchmarks.md` §5. What that ranking does not tell you is how to *cause* each signal. That is this table.

| Signal | What it proves to the system | How a script or package causes it | Design tell |
|---|---|---|---|
| Shares | The viewer staked social capital on the video | Give one transferable idea, framing, or moment a viewer can repeat in a sentence | If nobody can summarize your video in one line, it will not be shared |
| Repeat viewing | The content had reference or rewatch value | Dense reference segments, a payoff worth re-seeing, a chapter worth returning to | Retention spikes (`benchmarks.md` §2) mark rewatched seconds — build more of what caused them |
| Session continuation | The video kept the viewer on-platform | End on a question the next video answers; end screens and playlists pointing inward | A video that resolves *everything* is a session terminator |
| Saves | Deferred intent — the viewer plans to act | Actionable, list-shaped, or tool-shaped content | Tutorials and resource videos are save-generators by construction |
| Survey responses | Direct satisfaction measurement | Cannot be engineered; only earned by not over-promising | — |
| Likes | Cheap positive signal | Ask once, after a value delivery, never before | Asking in the first seconds costs retention and gains little |
| Comments | Time investment | Ask a specific question with a low-effort answer; take a stakeable position | "Let me know what you think" produces nothing; "which of the three would you pick?" produces threads |

Two amplifiers worth naming:

- **Quality click ratio.** The system distinguishes a click that converts into satisfied viewing from a click that converts into an immediate exit. Raw CTR is a means; quality clicks are the end. This is the mechanism behind §9.
- **Early comment replies.** Replying quickly correlates with higher reach (`benchmarks.md` §5). The plausible mechanism is comment volume and recency feeding engagement prediction during the layer-1/layer-2 window, not a reward for creator effort.

## 5. Session initiation vs session continuation

Every video plays one of two roles, and the role changes which topics are worth making.

| | **Session initiator** | **Session continuer** |
|---|---|---|
| Role | The video that starts a viewing session | The video watched second, third, fourth |
| Typical entry | Notification, search, home feed, external link | Suggested sidebar, autoplay, end screen |
| What it must do | Be clickable cold, from nothing | Be the obvious next thing after a related video |
| Topic character | Broad, timely, high-curiosity, low prerequisite | Adjacent, deeper, part of a series or cluster |
| Packaging emphasis | Thumbnail and title carry the entire load | Relevance to the *previous* video carries most of the load |
| Rewarded because | It brings a session into existence — high platform value | It extends a session — also high platform value, cheaper to earn |

**Why this changes topic choice.** A channel made entirely of initiators burns effort on cold clicks for every single upload. A channel made entirely of continuers never starts a session and depends on other creators' videos to feed it. Healthy channels run both deliberately.

| Channel state | What to make more of |
|---|---|
| High browse traffic, low suggested | More continuers — deepen existing topics, build series, cross-link |
| High suggested, low browse or search | More initiators — broader, more clickable, more timely topics |
| High search, low everything else | Continuers that follow a search video's natural next question |
| New channel, no cluster yet | Continuers around a single tight topic — you cannot win cold clicks yet |

**Practical construction:** an initiator ends by opening the question its continuer answers — an open loop (see `retention-scripting-guide.md`) applied across videos instead of within one.

## 6. Topical clustering and niche discipline

The system builds a representation of what a channel is about, and of which videos and channels sit near each other in topic space. Two things follow.

**For the channel.** Consistent topics make prediction easier, and easier prediction means faster, wider layer-2 and layer-3 expansion. Erratic topics force the system to re-learn the channel's audience with every upload, which lands each new video back at layer 1 with a weak prior.

**For the video.** A video is suggested alongside topically near videos — including competitors'. Being *legible* as part of a cluster is what gets you into somebody else's sidebar.

| Behavior | Effect on clustering | Verdict |
|---|---|---|
| Tight, repeated topic with varied formats | Strong cluster; formats add variety without confusing the topic model | Best case |
| Varied topics with one repeated format | Weak cluster; the channel is legible as a *style*, not a *subject* | Works only for personality-led archetypes |
| Adjacent expansion (a neighbouring topic, deliberately) | Cluster stretches; some short-term cost, new reach if it lands | Do this on purpose, one step at a time |
| Random pivots | Cluster resets | Worst case |

**The adjacency test before any new topic:** would a viewer who watched our best-performing video plausibly want this next? If yes, it is adjacent expansion. If no, it is a pivot, and it should be planned as one — accepting a rebuild period rather than being surprised by it.

**Niche discipline is not topic narrowness.** It is *audience* narrowness. A channel can cover many subjects if one recognizable person or problem connects them. It cannot serve two unrelated audiences from one upload feed without paying for it in prediction quality.

## 7. The cold-start problem

Cold start applies to a new channel, a channel returning from a break (`benchmarks.md` §4), and any channel entering a new cluster. In all three the system has a weak prior and expands cautiously.

**What the creator actually controls in the first 24 hours:**

| Controllable | Not controllable |
|---|---|
| Packaging quality at the moment of publish | How many impressions layer 1 grants |
| Whether the first minutes deliver the packaged promise | Which viewers are selected |
| Publishing when the core audience is awake | Whether layer 2 unlocks |
| Replying to early comments inside the reach-correlated window (`benchmarks.md` §5) | Anything about layer 4 |
| Whether an end screen or playlist points somewhere | The absolute view count |
| Not deleting/re-uploading, not swapping the title mid-test | — |

**Cold-start priorities, in order:**

1. A hook that pays the packaging's promise.
2. Packaging a *cold* viewer understands with no channel context.
3. Publishing into the audience's active hours.
4. Early comment engagement, inside the reach-correlated window.
5. An inward-pointing next step — end screen, playlist, or a stated follow-up.

**Never** judge a cold-start video on absolute views. Judge CTR and retention against `benchmarks.md` §1–§2 — the only signals meaningful at low volume.

> **Known gap.** There are no reliable first-24h or first-48h view targets by channel size. `benchmarks.md` §11 lists this explicitly. An agent asked for one must answer *benchmark unavailable* and diagnose from rate metrics instead.

## 8. Context weighting: device, surface, format

The same minute of watch time is not worth the same everywhere. Weighting adapts to context (`benchmarks.md` §5), and the practical read is:

| Context | Weighting character | What it changes |
|---|---|---|
| TV / connected-TV | Higher — lean-back, deliberate, long sessions | Favors longer formats, readable-at-distance thumbnails, higher-resolution assets (`benchmarks.md` §7) |
| Mobile | Lower per minute, but dominant in volume (`benchmarks.md` §7) | Title and thumbnail must survive mobile truncation (`benchmarks.md` §6) |
| Desktop | Middle; highest for search and reference use | Chapters, timestamps and descriptions do real work here |
| Long-form audio-led formats | Higher — sustained sessions | Length bands in `benchmarks.md` §3 can be pushed upward |
| Background/ambient consumption | Lower per minute | Optimize for session length, not per-video retention |

**Design implication:** know the dominant surface before optimizing anything. A majority-TV channel should not obsess over thumbnail micro-detail; a majority-mobile channel should not write titles that only read at desktop width.

## 9. The metadata-mismatch penalty

A clickbait penalty exists (`benchmarks.md` §5, late-2024 entry). It is widely misunderstood as a punishment for *exciting* packaging. It is not.

**What actually triggers it:** a gap between what the packaging promised and what the video delivers, measured through viewer behavior — high CTR followed by fast abandonment, low satisfaction, negative survey and feedback signals. The trigger is the *behavioral aftermath*, not the wording of the title.

| Packaging | Delivery | Outcome |
|---|---|---|
| Bold claim | Claim addressed in the first minute | Fine. This is good packaging. |
| Bold claim | Claim addressed at minute 9 | Penalized in effect — the abandonment happens before the payoff |
| Bold claim | Claim never addressed | Penalized, and it damages the channel's prediction prior |
| Mild claim | Strong delivery | Not penalized, but under-distributed — a different failure |
| Question in title | Answer withheld as a retention device | High risk; withholding beyond the first minutes reads as mismatch |

**How to keep aggressive packaging safe:**

1. Deliver the headline promise inside the first minute, then escalate beyond it.
2. Keep the title's claim *literally* true and let the thumbnail carry the emotion — the Information Split Rule (`benchmarks.md` §7).
3. If the title asks a question, answer it early and spend the video on *why*, not on *whether*.
4. Retitle a video that is winning clicks and losing viewers rather than defending the title.

**Diagnostic signature:** high impressions, high CTR, low retention — the "clickbait" row of the diagnostic matrix in `benchmarks.md` §10.

## 10. Diagnostic procedure: which system are you failing?

Run this before proposing any fix. Two inputs: the traffic-source breakdown and the impressions/CTR/retention triad.

| Symptom | Failing system / layer | Most likely cause | Change this |
|---|---|---|---|
| Impressions never rise past the first hours | Browse, layer 1 | Core audience did not click, or topic has no pull for them | Packaging first; then topic fit to the existing audience |
| Impressions rise, CTR collapses as they rise | Browse, layer 2 | Package works on warm viewers, not cold ones | Rewrite title/thumbnail for someone with no channel context |
| High CTR, retention falls off a cliff early | All systems, satisfaction | Hook does not pay the promise | Rebuild the opening (`retention-scripting-guide.md`, `hook-library.md`) |
| Good retention, impressions still flat | Layer 2 topic ceiling | Nobody is looking for this | Change topic demand, not packaging |
| No search traffic at all on an evergreen topic | Search | Query mismatch, or the query is saturated | Keyword and title work (`seo-playbook.md`) |
| Search traffic but no suggested traffic | Search fine, Browse/Suggested failing | Weak session continuation; no cluster | Series, end screens, adjacent follow-ups |
| Suggested traffic collapsed after a topic change | Clustering | Pivot reset the topic model | Return to the cluster or commit to a rebuild period |
| Shorts get views, long-form does not move | Shorts fine, Browse untouched | Expected — audience overlap is low (`benchmarks.md` §8) | Stop expecting Shorts to feed long-form directly |
| Shorts die in the first seconds | Shorts | First frame and first seconds (`benchmarks.md` §8) | Rebuild the opening frame, not the whole video |
| Retention strong, but no shares or saves | Satisfaction depth, not distribution | Nothing transferable to repeat; no deferred intent | Give one line-sized idea and one actionable takeaway (§4) |
| A pivot video did well, the next three did not | Clustering | The system cannot predict the channel's audience any more | Commit to one cluster for several uploads before judging (§6) |
| Everything fell at once, across all videos | Usually none of the above | Seasonality, a view-counting change, or an audience-wide shift | Compare year-over-year and check the timeline in `benchmarks.md` §5 before acting |

**Sequencing rule:** fix in funnel order — impressions, then CTR, then retention, then satisfaction. Fixing retention on a video nobody is being shown wastes the effort.

## 11. Misattribution: what creators blame on "the algorithm"

| Creator's claim | What it usually is | How to confirm |
|---|---|---|
| "I'm shadowbanned" | Layer-1 stall — the core audience did not click | Impressions exist but are small; CTR is the tell |
| "The algorithm changed" | Their topic mix or packaging changed | Compare the last N videos' topics and CTR against the prior N |
| "Views dropped for no reason" | Seasonality, a metric-definition change, or a strong prior video raising the prediction bar | Year-over-year comparison; check `benchmarks.md` §5 timeline |
| "Subscribers aren't being shown my videos" | Subscribers are a permission, not a distribution guarantee; notification caps apply (`benchmarks.md` §4) | Check the Subscriptions share of traffic and returning-viewer counts |
| "Small channels can't grow" | Small channels receive active promotion (`benchmarks.md` §4) | Diagnose packaging against the CTR tiers instead |
| "My retention is fine, so it must be the algorithm" | Retention is fine *for them*, not against the traffic source it needs | Compare to `benchmarks.md` §2, and to their own channel average |
| "The video is too good for the audience" | Almost always packaging or topic demand | Retitle/rethumbnail and re-measure before accepting this |

**The governing statement:** distribution problems are packaging problems, topic-demand problems, or satisfaction problems — in that order of frequency. "The algorithm" is a description of the symptom, never a diagnosis.

## 12. Decision rules

- **If** a video underperforms → identify the traffic source first, then diagnose against that source's benchmarks in `benchmarks.md` §1–§2. Never against a global average.
- **If** impressions are flat → the problem is topic or layer-1 packaging. Do not touch retention yet.
- **If** CTR is high and retention is low → treat it as metadata mismatch (§9). Fix the first minute or retitle; do not add more hype.
- **If** CTR falls as impressions rise → this is normal expansion. Only act if it falls below the sustained band in `benchmarks.md` §1.
- **If** the channel has no suggested traffic → build session continuers and a tighter topic cluster (§5, §6).
- **If** the creator proposes a topic outside the cluster → apply the adjacency test (§6). If it fails, plan it as a deliberate pivot with a stated rebuild period.
- **If** the channel is in cold start → optimize only the six controllables in §7 and judge by rate metrics, never absolute views.
- **If** asked for a first-24h view target → answer *benchmark unavailable* (`benchmarks.md` §11) and diagnose from CTR and retention.
- **If** Shorts perform and long-form does not → do not treat Shorts as a long-form funnel (`benchmarks.md` §8). Set the expectation explicitly with the creator.
- **If** the creator says "shadowban," "suppressed," or "the algorithm changed" → run §11 before accepting the premise.
- **If** a channel returns from a publishing break → treat it as cold start, expect a rebuild period (`benchmarks.md` §4), and do not diagnose the first upload back as a content failure.
- **If** the audience is majority TV or majority mobile → adjust packaging and length priorities per §8 before optimizing anything else.
- **If** two systems' benchmarks conflict in a diagnosis → the dominant traffic source for that specific video wins. Always.
