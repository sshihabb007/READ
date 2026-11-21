import json
import os
import re
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(PLUGIN_ROOT, "skills", "claude-shorts")


class ClaudeShortsPluginBundle(unittest.TestCase):
    def test_manifest_valid(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "claude-shorts")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)

    def test_skill_and_pipeline_assets(self):
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        self.assertIsNotNone(m)
        self.assertIn("name: claude-shorts", m.group(1))
        for rel in [
            "scripts/transcribe.py",
            "scripts/snap_boundaries.py",
            "scripts/compute_reframe.py",
            "references/scoring-rubric.md",
            "references/caption-styles.md",
            "remotion/render.mjs",
        ]:
            self.assertTrue(os.path.isfile(os.path.join(SKILL_DIR, rel)), rel)


if __name__ == "__main__":
    unittest.main()
