import json
import os
import re
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(PLUGIN_ROOT, "skills", "ghost-editor")


class GhostEditorPluginBundle(unittest.TestCase):
    def test_manifest_valid(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "ghost-editor")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)

    def test_skill_frontmatter_and_core_assets(self):
        skill_md = os.path.join(SKILL_DIR, "SKILL.md")
        self.assertTrue(os.path.isfile(skill_md))
        with open(skill_md, encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        self.assertIsNotNone(m)
        fm = m.group(1)
        self.assertIn("name: ghost-editor", fm)
        self.assertRegex(fm, r"description:\s+\S")
        for rel in [
            "scripts/build.mjs",
            "scripts/transcribe.py",
            "scripts/face_track.py",
            "references/reel-json.md",
            "references/take-selection.md",
            "docs/PLAYBOOK.md",
            "recipes/clean-os",
        ]:
            self.assertTrue(os.path.exists(os.path.join(SKILL_DIR, rel)), rel)


if __name__ == "__main__":
    unittest.main()
