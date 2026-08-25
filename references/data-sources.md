# Data Sources and Integrations

**Purpose.** Every live-data integration this matrix can use, how to set it up, and — more importantly — exactly what to do when it is absent. All integrations are **optional**.

> ## The golden rule
> **Never block a workflow because an integration is missing.**
> Detect by attempting the call. If it fails, fall back, say so in **one line**, and continue.
> An agent that stops to ask for an API key has failed. An agent that asks the creator to paste
> three numbers from a Studio screen and then delivers the full deliverable has succeeded.

**Quota numbers live in `benchmarks.md` §10.** This file describes mechanics, not figures.

**Contents:** 1 Capability map · 2 YouTube Data API v3 · 3 YouTube Analytics API · 4 DataForSEO MCP · 5 Image-generation MCP · 6 WebSearch · 7 Execution scripts · 8 Task → source decision table · 9 Troubleshooting · 10 Data hygiene · 11 Decision rules

## 1. Capability map

| Source | Auth | Cost | Gives | Fallback |
|---|---|---|---|---|
| YouTube Data API v3 | API key | Free within quota | Public channel/video stats, uploads lists, search, comments, captions metadata | Creator pastes Studio numbers, or a channel URL to inspect manually |
| YouTube Analytics API | OAuth | Free | Private analytics for a channel the creator owns | Creator pastes or screenshots Studio metrics |
| DataForSEO MCP *(optional enhancement, rarely present)* | Account credentials | Per call | Upgrades the default proxies to real search volume, keyword difficulty, intent, YouTube SERP, trends | **The default: WebSearch** plus the §3 demand proxies — sufficient for every decision the matrix makes |
| Image-generation MCP *(optional enhancement, rarely present)* | Varies | Varies | Additionally renders the concepts as 16:9 images saved beside the brief | **The default, and the normal case: the English text prompts**, complete and usable in any generator |
| WebSearch | None | Free | Current facts, competitor context, trend signals | The creator's own knowledge; mark the file `⚠️ unverified` |

**Zero integrations configured is a fully supported state.** The matrix is designed to run on WebSearch plus what the creator can tell you.

## 2. YouTube Data API v3

**What it gives.** Public data only: channel statistics, the uploads playlist, video metadata and public counts, search results, public comment threads, and available caption tracks. **It never gives** retention, CTR, impressions, revenue or traffic sources — for any channel, including the creator's own. Those live in the Analytics API (§3).

**Setup.** Create a project in the Google Cloud console → enable *YouTube Data API v3* → create an API key under Credentials → restrict the key to that API. Then:

```bash
export YOUTUBE_API_KEY="..."
```

Put the export in the shell profile so it persists. The execution layer reads `YOUTUBE_API_KEY` from the environment.

**Quota model.** A daily unit budget that resets at midnight Pacific — the exact figures are in `benchmarks.md` §10. Two things matter operationally:

| Call | Relative cost | Guidance |
|---|---|---|
| `search.list` | **Expensive** (two orders of magnitude above a read) | The single biggest quota risk. Avoid in loops. |
| `videos.list`, `channels.list`, `playlistItems.list`, `commentThreads.list`, `captions.list` | Cheap reads | Use freely |

**The uploads-playlist pattern — use this instead of search.** To list a channel's recent videos, do *not* call `search.list` with a channel filter. Instead: `channels.list` to get the uploads playlist ID → `playlistItems.list` to get video IDs → `videos.list` (batched, up to 50 IDs per call) for statistics. This costs a handful of cheap reads instead of one expensive search, and it is the difference between analyzing a few channels a day and analyzing dozens.

Batch aggressively (`videos.list` accepts many IDs per call), cache within a session and never re-fetch the same channel twice, and warn the creator before an operation that will consume a large share of the day's budget.

**Fallback when the key is absent.** Ask for exactly what you need — never a generic "give me your data":

| Needed | Ask for |
|---|---|
| Channel size and shape | Subscriber count, total videos, and the channel URL |
| Recent performance | "Studio → Content, sorted by views: the last 10 video titles with their view counts and publish dates" |
| A specific video | The video URL and its public view/like/comment counts |
| Competitor data | The competitor's channel URL — then read the public page or use WebSearch |
| A transcript | Paste the transcript, or use the transcript panel under the video |

## 3. YouTube Analytics API

**What it gives.** The private metrics that actually drive the matrix's diagnostics: impressions, CTR, average view duration, audience retention curves, traffic sources, audience geography and demographics, subscriber gain/loss per video, and revenue where monetized.

**Only for a channel the creator owns or manages.** There is no path — via this API or any other — to a competitor's private analytics. If a creator asks for a competitor's retention or RPM, the honest answer is that it is not obtainable, and the workaround is inference from public signals plus the diagnostic matrix in `benchmarks.md` §10.

**OAuth flow, at a high level.** Create OAuth 2.0 client credentials (desktop application type) in the same Cloud project → download the client secrets JSON → store it **outside the plugin folder** (§10) → the first run opens a browser consent screen → the resulting token is cached locally and refreshed automatically.

**Scopes needed:** read-only YouTube Analytics access, plus read-only YouTube account access for channel identification. Monetary metrics require the monetary-readonly Analytics scope; request it only if revenue reporting is actually needed — asking for more scope than necessary makes creators refuse consent.

**Reporting limits** (results per query, video-group sizes, the Reporting API's granularity and window) are in `benchmarks.md` §10.

**Fallback when OAuth is not set up.** This is the *common* case, and the matrix works well without it. Ask for a small, specific set — creators can read these off a Studio screen in a minute:

> From Studio → Analytics → Overview, for the last 28 days: views, watch time, average view duration, impressions, and impressions CTR. Then Audience → your top 5 countries with percentages, and returning vs new viewers.
> For a single video, open it → Analytics → Engagement and tell me the retention at 30 seconds and where the biggest drop-off is.

A screenshot of the retention curve is worth more than any of the numbers — accept it gladly. State plainly which analysis is degraded by the missing data rather than silently producing a weaker deliverable.

## 4. DataForSEO MCP (optional)

**The default path is WebSearch and the free demand proxies in `seo-playbook.md` §3.** This MCP is an optional enhancement that is usually *not* present; nothing waits on it.

**What it adds when it is present.** Real search-volume figures, keyword difficulty scores, search-intent classification, YouTube SERP composition for a keyword, and trend time series. It moves SEO and ideation work from *reasoned* to *measured*.

**Detection by attempt.** There is no capability list to consult. Attempt the call you need. If the tool is not present or the call errors, fall back to WebSearch and note it in one line. Do not probe with a throwaway call first — that costs money for no output.

**Cost awareness.** DataForSEO bills per call. Rules: batch keywords into one call wherever the endpoint accepts an array (twenty keywords in one call costs what one does); never re-fetch data already retrieved this session; keep list limits modest; and warn the creator before a large sweep.

**Interpretation cautions that matter more than the setup:**
- Google search volume is a strong *proxy* for YouTube demand, not a measurement of it. Some topics skew heavily to YouTube (tutorials, gaming, repair) and others to Google.
- Trend series are relative indices, not absolute volumes — always pair with volume data.
- SERP data may be cached and hours old; pair with trend data for anything time-sensitive.
- Ad CPC correlates loosely with RPM. It is a directional signal about a topic's commercial value, never a revenue estimate — revenue figures come from `benchmarks.md` §9 through `localization-guide.md`.
- Localize `location` and `language` parameters to the *target market*, not to the default. A US-English query is the wrong question for a non-US channel (`localization-guide.md` §5).

**Fallback: WebSearch.** Search the keyword and read the actual YouTube results — how many videos rank, their view counts, their ages, their title patterns, the Shorts-to-long-form ratio. This is qualitatively weaker than volume data but sufficient for every decision the matrix makes. Never present a search-derived impression as a volume figure.

## 5. Image-generation MCP (optional)

**The default deliverable is the text prompt, and that is the normal case.** The thumbnail agent's output is complete without any image tool. This MCP is an optional enhancement that is usually *not* present; nothing waits on it.

**What it adds when it is present.** Rendered thumbnail images *alongside* the prompts, so a concept can be evaluated visually and iterated in the session.

**Recommended settings for YouTube thumbnails:** 16:9 aspect ratio, generated at the recommended resolution and kept under the file-size cap — all of those specs are in `benchmarks.md` §7; read them there and set the generator to match. Generate 2–3 variants per concept so there is something to compare. Design constraints (one focal point, two or three primary colours, generous negative space, minimal text) also live in §7 and should be written into the prompt itself, not applied afterward.

**Text on generated images is unreliable.** Image models misspell. The dependable workflow is: generate the *image* with no text, then add the overlay text in an editor. If the model must render text, keep it to one or two short words, verify the spelling character by character, and regenerate rather than accepting "close enough."

**Language note:** the thumbnail agent writes its prompts in English regardless of the channel's output language, because image models perform materially better in English. Only the `overlay_text` and `paired_title` fields stay in the creator's language — see the orchestrator skill.

**Fallback.** Deliver the prompt as text, formatted so the creator can paste it into any image generator, plus a plain-language description of the composition (subject, framing, expression, background, colour direction, where the overlay text goes and what it says). This is the *default* deliverable — a working prompt is genuinely useful output, not a consolation prize. Say "here's the prompt to paste into your generator," not "I couldn't make the image."

## 6. WebSearch — the universal baseline

Always available, no setup, and the fallback for nearly everything else. Use it for: current facts and their sources during research, competitor context and recent news, what is trending in a niche, platform policy changes, live SERP inspection, and verifying any claim before it enters a script.

**Limits to respect:** results are a snapshot, not a dataset — never aggregate them into a statistic. Nothing from a search becomes a benchmark; benchmarks come from `benchmarks.md` only. Prefer primary sources (platform documentation, official help pages) over creator-blog summaries, which propagate outdated figures for years.

**When there is no web access at all:** proceed with reasoning from the reference files, and mark the deliverable `⚠️ unverified` at the top so nobody mistakes it for researched work.

## 7. Execution scripts

The `execution/` folder wraps the APIs above in a small, predictable command-line surface, so agents call scripts rather than constructing API requests.

| Script | Purpose | Needs |
|---|---|---|
| `fetch_channel_data.py` | Channel stats plus recent videos, via the cheap uploads-playlist path | API key |
| `search_competitor_videos.py` | Topic or channel search — uses the expensive `search.list` call | API key |
| `fetch_transcript.py` | Transcript retrieval, with a cascade of methods and graceful failure | API key or a local extractor |
| `fetch_video_analytics.py` | Private metrics for an owned channel | OAuth |
| `utils/youtube_auth.py` | Resolves the API key and the OAuth token | — |
| `utils/quota_tracker.py` | Tracks unit consumption and warns before exhaustion | — |

**Behaviour to rely on:** every script returns structured JSON, including on failure, where the error object names the problem and the fix. Check quota before an expensive run. Prefer `fetch_channel_data.py` over `search_competitor_videos.py` whenever the channel is known — it is dramatically cheaper for the same information.

## 8. Task → source decision table

| Task | Best available | Second | Fallback |
|---|---|---|---|
| Channel size and recent videos | Data API (`fetch_channel_data.py`) | Public channel page via WebSearch | Ask the creator |
| Competitor video list | Data API, uploads-playlist path | `search.list` (expensive) | Ask for the channel URL, inspect manually |
| Competitor private metrics | **Not obtainable** | — | Infer from public signals; say plainly it is unavailable |
| Own channel retention / CTR / traffic | Analytics API (OAuth) | Studio screenshot | Ask for the five headline numbers (§3) |
| Audience geography | Analytics API | Studio → Audience, pasted | Ask; never infer (`localization-guide.md` §4) |
| Keyword search volume | DataForSEO | — | WebSearch the SERP and read it qualitatively |
| Keyword difficulty | DataForSEO | — | Count and assess the ranking videos manually |
| YouTube SERP composition | DataForSEO | WebSearch | Ask the creator to search and describe the first page |
| Trend direction | DataForSEO trends | WebSearch | Say the signal is unavailable |
| Transcript | `fetch_transcript.py` | Studio captions | Creator pastes the transcript panel |
| Video comments | Data API `commentThreads.list` | — | Creator pastes a sample (`community-guide.md` §8) |
| Thumbnail image | Image MCP, if present | — | **Default:** the text prompt, ready for any generator |
| Current facts for a script | WebSearch | — | Mark `⚠️ unverified` |
| Any benchmark figure | `benchmarks.md` | — | "Benchmark unavailable." Never estimate. |

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| "API key not found" | `YOUTUBE_API_KEY` unset in this shell | Export it, or use the §2 fallback and continue |
| 403 `accessNotConfigured` | The API is not enabled on the Cloud project | Enable YouTube Data API v3 for that project |
| 403 `quotaExceeded` | Daily units exhausted | Wait for the Pacific-midnight reset, or use fallbacks today. Check whether `search.list` in a loop caused it. |
| 403 with a key that worked yesterday | Key restrictions too narrow, or the key was rotated | Check API and referrer restrictions on the key |
| Quota drains within minutes | `search.list` being used where the uploads-playlist path would work | Switch to `fetch_channel_data.py` |
| OAuth consent screen loops | Unverified app, or a missing scope | Add the account as a test user; re-check requested scopes |
| Analytics returns empty rows | The channel is not monetized, the range predates the channel, or the metric does not apply to the video type | Narrow the metric set; confirm the date range |
| Analytics 403 on a valid channel | Token is for a different account than the channel owner | Re-authenticate as the channel's owning account |
| Revenue metrics missing | The monetary scope was not requested | Re-consent with the monetary-readonly scope, or use the §3 fallback |
| DataForSEO tool not found | MCP not configured for this session | Fall back to WebSearch; say so in one line |
| DataForSEO returns zero volume | Wrong location or language code for the market | Set them to the target market (`localization-guide.md` §5) |
| Transcript fetch fails | Captions disabled, or no extractor available | Ask the creator to paste from the transcript panel |
| Generated thumbnail text is misspelled | Expected — image models misspell | Generate without text; add the overlay in an editor |
| Numbers disagree between sources | Different definitions or windows (for example view-counting changed — `benchmarks.md` §5, §8) | Name the discrepancy; never average them |

## 10. Data hygiene

**Credentials.**
- Never write an API key, OAuth token, client secret or password into the plugin folder. Not in a config file, not in a script, not in a comment, not in an example.
- The API key comes from the `YOUTUBE_API_KEY` environment variable. OAuth client secrets and cached tokens live in the user's own configuration directory, outside the plugin.
- Never echo a credential into conversation, a log, a deliverable or a committed file — including partially masked. If one appears in output, treat it as compromised and tell the creator to rotate it.
- Never ask a creator to paste a key into the chat. Tell them where to set the environment variable instead.
- If the plugin folder is under version control, credential files must be ignored; the safer answer is that they are never in that folder at all.

**What may be written to the workspace.** Channel profile and configuration (no credentials), video-stage artifacts and state, calendars, audits, competitor notes built from public data, and pasted analytics the creator explicitly provided for this purpose.

**What may not.** Credentials of any kind, raw API responses containing tokens, personal data about commenters or third parties beyond what the analysis needs, and anything the creator shared for one task and did not agree to have stored.

**Retention.** Cached API responses are a convenience, not a record — treat them as disposable and re-fetch rather than trusting stale data for a decision. Analytics the creator pasted should be dated in the file, because a metric with no date is unusable three weeks later.

## 11. Decision rules

- **If** an integration is missing → fall back, say so in one line, and finish the deliverable. Never stop to request setup.
- **If** you need to know whether an integration exists → attempt the call. Do not ask the creator, and do not probe with a throwaway paid call.
- **If** the fallback is "ask the creator" → ask for the *specific* screen and the *specific* numbers, never for "your data".
- **If** listing a channel's videos → use the uploads-playlist path, never `search.list`.
- **If** a search-type call is unavoidable → check quota first and warn the creator if the run is large.
- **If** asked for a competitor's retention, CTR or revenue → say plainly it is not obtainable by any means, then infer from public signals.
- **If** DataForSEO is present → localize the location and language parameters to the target market before querying.
- **If** using search volume → present it as a proxy for YouTube demand, never as YouTube volume, and never as a revenue estimate.
- **If** generating a thumbnail → 16:9, no rendered text, English prompt, 2–3 variants. Without the MCP, deliver the prompt as the finished output and say so confidently.
- **If** two sources disagree → name the discrepancy and its cause. Never average conflicting figures.
- **If** a number is needed → it comes from `benchmarks.md`, converted through `localization-guide.md` for non-US audiences. If it is not there, say "benchmark unavailable."
- **If** working without web access → proceed and mark the deliverable `⚠️ unverified`.
- **If** a credential would need to be stored → it goes in an environment variable or the user's own config directory. Never in the plugin folder, never in chat, never in a deliverable.
