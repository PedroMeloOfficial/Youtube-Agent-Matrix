# Contributing

Pull requests are welcome — bug fixes, new reference material, better agents, translations of the
docs.

1. **Read [`CLAUDE.md`](CLAUDE.md) first.** It explains the three layers (orchestrator → agents →
   references), which file a change belongs in, and the rules that keep the system coherent — above
   all: every number lives in `references/benchmarks.md`, and every file has one writer.
2. **Edit the Claude Code files only.** `agents/`, `skills/`, `commands/` and `.claude-plugin/` are the
   source of truth. The OpenAI Codex version (`codex/`, `.codex-plugin/`, `.agents/plugins/`) is
   generated: after your change, run `python3 codex/build_codex.py` and commit the result.
3. **Run the checklist** at the end of `CLAUDE.md` before opening the PR. The `validate` workflow
   runs the same checks on every push; a PR is merged only when it passes.
4. **Never weaken a test or a check to make something pass.** If a check is wrong, say why in the PR.
5. One topic per PR, with a short description of what changed and why.

Bugs and ideas: open an [issue](https://github.com/PedroMeloOfficial/Youtube-Agent-Matrix/issues).
