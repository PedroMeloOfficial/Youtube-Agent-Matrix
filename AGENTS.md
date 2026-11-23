# AGENTS.md

Guidance for OpenAI Codex (and other agents that read `AGENTS.md`) when working **on this repository**.

- The maintainer guide is [`CLAUDE.md`](CLAUDE.md). Read it before changing anything: its rules apply here
  unchanged.
- **The Claude Code files are the single source of truth**: `agents/*.md`, `skills/*/SKILL.md`,
  `commands/yt.md`, `.claude-plugin/`. Never change them to suit Codex.
- Everything under `codex/agents/`, `codex/skills/`, `.codex-plugin/` and `.agents/plugins/` is
  **generated** by `python3 codex/build_codex.py`. Never edit those files by hand. Edit the Claude source,
  rebuild, and check with `python3 codex/build_codex.py --check`.
- Using the plugin (not developing it) in Codex: see "Using it in OpenAI Codex" in `README.md`.
