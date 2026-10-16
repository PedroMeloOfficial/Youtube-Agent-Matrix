# First-run setup — the two questions

> Read by the orchestrator **only on a first run** (no `workspace/config.json` yet), then not again.
> Kept out of `skills/orchestrator/SKILL.md` because it is needed once per channel and that file
> loads on every invocation. Ask both questions exactly as written; translate the second into the
> language the creator picks in the first.

Ask exactly this, and nothing else, as your first message:

```
Before we start — what language should I work in?

All deliverables (ideas, scripts, titles, descriptions, calendars, reports) will be
written in the language you pick. I'll save it so you're only asked once.

  1. English
  2. Português (Brasil)
  3. Español
  4. Français
  5. Deutsch
  6. Italiano
  7. 日本語
  8. Other — just tell me which

Reply with a number or the language name.
```

Then write `workspace/config.json`:

```json
{
  "output_language": "pt-BR",
  "output_language_name": "Português (Brasil)",
  "channel_profile": "workspace/channel-profile.md",
  "channel_type_primary": null,
  "channel_type_secondary": null,
  "markets": {
    "mix": [ { "code": "BR", "share": 100 } ],
    "source": "declared"
  },
  "created_at": "YYYY-MM-DD"
}
```

Then ask the **second and last** setup question, in the language they just chose:

```
And where is your audience? Not where you live — where the people watching are.
This decides what a view is actually worth, when advertisers pay most, and which
disclosure rules apply to you.

  1. Brazil
  2. United States
  3. Mixed — tell me roughly, e.g. "80% Brazil, 20% US"
  4. I don't know yet

If you don't know, say so — I'll assume your audience matches your language and
correct it the first time I see your real Analytics.
```

Write the answer into `markets.mix` with shares summing to 100 and `source: "declared"`.

**Why the audience and not the creator.** Advertisers bid on the viewer's market, not the
uploader's. A creator living in Canada whose viewers are Brazilian has a `BR` channel. Getting
this backwards produces revenue estimates wrong by an order of magnitude — it is the most
expensive mistake available in this system.

If they pick "I don't know", infer from `output_language`, set `source: "declared"`, and say in
one line that you assumed it and will correct it from Analytics later.

Confirm both answers in one line, in the chosen language, then proceed with the original request.
