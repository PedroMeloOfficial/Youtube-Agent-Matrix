"""
Checks for the generated OpenAI Codex version.

    python3 -m unittest discover -s codex/tests
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "no frontmatter"
    out = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


class CodexBuild(unittest.TestCase):
    def test_generated_files_are_up_to_date(self):
        r = subprocess.run([sys.executable, str(ROOT / "codex" / "build_codex.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_one_codex_agent_per_claude_agent(self):
        claude = sorted(p.stem for p in (ROOT / "agents").glob("*.md"))
        codex = sorted(p.stem for p in (ROOT / "codex" / "agents").glob("*.toml"))
        self.assertEqual(claude, codex)

    @unittest.skipIf(tomllib is None, "tomllib needs Python 3.11+")
    def test_agent_toml_is_valid_and_complete(self):
        for f in (ROOT / "codex" / "agents").glob("*.toml"):
            data = tomllib.loads(f.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], f.stem, f)
            self.assertTrue(data["description"], f)
            body = (ROOT / "agents" / f"{f.stem}.md").read_text(encoding="utf-8").split("---", 2)[2].strip()
            self.assertIn(body[:200].replace("youtube-agent-matrix:", ""), data["developer_instructions"], f)
            self.assertIn("__PLUGIN_ROOT__", data["developer_instructions"], f)

    def test_skills_have_valid_frontmatter(self):
        names = {p.parent.name for p in (ROOT / "codex" / "skills").glob("*/SKILL.md")}
        self.assertEqual(names, {"orchestrator", "editor", "yt"})
        for name in names:
            meta = frontmatter((ROOT / "codex" / "skills" / name / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(meta["name"], name)
            desc = json.loads(meta["description"])  # quoted, so colons cannot break YAML
            self.assertTrue(0 < len(desc) <= 1024, name)

    def test_manifests_follow_the_claude_version(self):
        claude = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        codex = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((codex["name"], codex["version"]), (claude["name"], claude["version"]))
        self.assertEqual(codex["skills"], "./codex/skills/")
        market = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(market["plugins"][0]["name"], claude["name"])

    def test_claude_sources_are_not_touched(self):
        for f in list((ROOT / "agents").glob("*.md")) + list((ROOT / "skills").glob("*/SKILL.md")):
            self.assertNotIn("Running in OpenAI Codex", f.read_text(encoding="utf-8"), f)

    def test_install_writes_the_plugin_root_and_uninstalls(self):
        with tempfile.TemporaryDirectory() as home:
            env = {**os.environ, "CODEX_HOME": home, "PATH": "/usr/bin:/bin"}
            mine = Path(home) / "agents" / "my-own.toml"
            mine.parent.mkdir()
            mine.write_text("name = \"mine\"\n")
            r = subprocess.run(["bash", str(ROOT / "codex" / "install.sh")], env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            files = list((Path(home) / "agents").glob("youtube-agent-matrix__*.toml"))
            self.assertEqual(len(files), len(list((ROOT / "agents").glob("*.md"))))
            for f in files:
                text = f.read_text(encoding="utf-8")
                self.assertNotIn("__PLUGIN_ROOT__", text)
                self.assertIn(str(ROOT), text)
            r = subprocess.run(["bash", str(ROOT / "codex" / "install.sh"), "--uninstall"], env=env,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            self.assertEqual(list((Path(home) / "agents").glob("youtube-agent-matrix__*.toml")), [])
            self.assertTrue(mine.exists(), "uninstall must leave the creator's own agents alone")


if __name__ == "__main__":
    unittest.main()
