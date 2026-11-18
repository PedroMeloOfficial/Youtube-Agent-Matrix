---
description: Route to the YouTube Agent Matrix orchestrator — the full pre-production pipeline
argument-hint: "[setup|strategy|brand|audit|competitor|research|research-report|voice|ideate|calendar|hook|script|recording|thumbnail|seo|metadata|shorts|repurpose|monetize|analyze|video|edit] [args]"
---

Load the `youtube-agent-matrix:orchestrator` skill and act as the orchestrator described there.

Arguments received: $ARGUMENTS

Parse the first word of the arguments as the verb and route it exactly as the orchestrator's
routing table specifies (`setup`, `strategy`, `brand`, `audit`, `competitor`, `research`, `research-report`,
`voice`, `ideate`, `calendar`, `hook`, `script`, `recording`, `thumbnail`, `seo`, `metadata`, `shorts`,
`repurpose`, `monetize`, `analyze`, `video`, `edit`). Everything after the verb is the argument to that
route (a topic, an idea, a video folder, a channel to analyze, etc.).

If no arguments were given at all, and `workspace/config.json` does not exist yet, run the setup
flow (`/yt setup`): ask the language question, then the market/audience question, then hand off
to `channel-strategist` if there is no channel profile yet.

If no arguments were given and setup is already complete, ask the creator what they want to work
on next rather than guessing.

`edit` hands over to the `youtube-agent-matrix:editor` skill (`skills/editor/SKILL.md`), passing the
rest of the arguments (`setup`, `test`, `return <file>`, `learnings`, `style`, `intro`, or a video).

Follow every rule in the orchestrator skill exactly — approval gates, file ownership, the
`_handoff.md`/`_log.md` mechanics, and never inventing benchmark numbers.
