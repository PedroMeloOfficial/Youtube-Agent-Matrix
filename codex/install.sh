#!/usr/bin/env bash
# Install YouTube Agent Matrix for OpenAI Codex (CLI or desktop app).
#
#   git clone https://github.com/PedroMeloOfficial/Youtube-Agent-Matrix.git
#   cd Youtube-Agent-Matrix && bash codex/install.sh
#
# What it does:
#   1. copies the 24 custom agents into ~/.codex/agents/ (Codex plugins cannot ship agents),
#      with this clone's absolute path written in, so every agent finds references/ and execution/;
#   2. registers this folder as a Codex plugin marketplace (if the `codex` CLI is on PATH).
# Only files named youtube-agent-matrix__*.toml are ever written or removed in ~/.codex/agents/.
#
#   bash codex/install.sh --uninstall   removes those agent files again
#
# After a `git pull`, run it again so the installed agents match the new version.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CODEX_HOME:-$HOME/.codex}/agents"
PREFIX="youtube-agent-matrix__"

if [[ "${1:-}" == "--uninstall" ]]; then
  rm -f "$DEST/$PREFIX"*.toml
  echo "Removed the YouTube Agent Matrix agents from $DEST."
  echo "To remove the plugin too: codex plugin marketplace remove youtube-agent-matrix"
  exit 0
fi

command -v python3 >/dev/null || { echo "python3 is required (it also runs the plugin's scripts)." >&2; exit 1; }

python3 "$ROOT/codex/build_codex.py" --check >/dev/null || {
  echo "The Codex files are out of date with the Claude sources. Run: python3 codex/build_codex.py" >&2; exit 1; }

mkdir -p "$DEST"
rm -f "$DEST/$PREFIX"*.toml
count=0
for f in "$ROOT"/codex/agents/*.toml; do
  python3 - "$f" "$DEST/$PREFIX$(basename "$f")" "$ROOT" <<'PY'
import sys
src, dst, root = sys.argv[1:4]
text = open(src, encoding="utf-8").read().replace("__PLUGIN_ROOT__", root)
open(dst, "w", encoding="utf-8").write(text)
PY
  count=$((count + 1))
done
echo "Installed $count agents in $DEST (plugin root: $ROOT)."

if command -v codex >/dev/null; then
  if codex plugin marketplace add "$ROOT"; then
    echo "Registered the marketplace. Now install 'YouTube Agent Matrix' from the Plugins directory"
    echo "in the Codex / ChatGPT desktop app (or enable it in Codex), then type: \$yt setup"
  else
    echo "Could not register the marketplace automatically. Run: codex plugin marketplace add \"$ROOT\""
  fi
else
  echo "Codex CLI not found on PATH. In the Codex / ChatGPT desktop app, add this folder as a plugin"
  echo "marketplace ($ROOT), install 'YouTube Agent Matrix', then type: \$yt setup"
fi
