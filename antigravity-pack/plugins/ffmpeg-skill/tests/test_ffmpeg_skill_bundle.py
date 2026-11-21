import json
import os
import re
import subprocess
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(PLUGIN_ROOT, "skills", "ffmpeg-skill", "SKILL.md")
LINK_RX = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class FfmpegSkillPluginBundle(unittest.TestCase):
    def test_manifest_and_template(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "ffmpeg-skill")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)
        tpl = os.path.join(PLUGIN_ROOT, "mcp_config.template.json")
        cfg = os.path.join(PLUGIN_ROOT, "mcp_config.json")
        self.assertTrue(os.path.isfile(tpl) or os.path.isfile(cfg))

    def test_skill_frontmatter_and_links(self):
        with open(SKILL_MD, encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        self.assertIsNotNone(m)
        self.assertIn("name: ffmpeg-skill", m.group(1))
        for lm in LINK_RX.finditer(text):
            raw = lm.group(1).strip()
            if not raw or raw.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
                continue
            target = raw.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(SKILL_MD), target))
            self.assertTrue(os.path.exists(resolved), f"Broken link {raw} -> {resolved}")

    def test_mcp_server_lists_core_tools(self):
        server = os.path.join(PLUGIN_ROOT, "mcp", "server.py")
        res = subprocess.run([sys.executable, server, "--list"], capture_output=True, text=True, check=False)
        self.assertEqual(res.returncode, 0, res.stderr)
        lines = [ln for ln in res.stdout.splitlines() if ln.strip()]
        self.assertGreaterEqual(len(lines), 10)


if __name__ == "__main__":
    unittest.main()
