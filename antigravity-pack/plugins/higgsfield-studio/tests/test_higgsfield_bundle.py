import json
import os
import re
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PLUGIN_ROOT, "skills")

EXPECTED_SKILLS = [
    "editorial-motion-graphics",
    "higgsfield-brandkit",
    "higgsfield-faceless-video",
    "higgsfield-generate",
    "higgsfield-marketplace-cards",
    "higgsfield-product-photoshoot",
    "higgsfield-soul-id",
    "higgsfield-video-explainer",
    "higgsfield-websites",
    "higgsfield-youtube-thumbnail",
]


class HiggsfieldPluginBundle(unittest.TestCase):
    def test_manifest_and_mcp_config(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "higgsfield-studio")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)
        with open(os.path.join(PLUGIN_ROOT, "mcp_config.json"), encoding="utf-8") as fh:
            mcp = json.load(fh)
        self.assertEqual(
            mcp["mcpServers"]["higgsfield-mcp"]["serverUrl"],
            "https://mcp.higgsfield.ai/mcp",
        )

    def test_all_ten_skills_present_with_valid_frontmatter(self):
        found = sorted(
            d
            for d in os.listdir(SKILLS_ROOT)
            if os.path.isdir(os.path.join(SKILLS_ROOT, d))
            and os.path.isfile(os.path.join(SKILLS_ROOT, d, "SKILL.md"))
        )
        self.assertEqual(found, sorted(EXPECTED_SKILLS))
        for skill in EXPECTED_SKILLS:
            with open(os.path.join(SKILLS_ROOT, skill, "SKILL.md"), encoding="utf-8") as fh:
                text = fh.read()
            m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
            self.assertIsNotNone(m, skill)
            self.assertIn(f"name: {skill}", m.group(1), skill)


if __name__ == "__main__":
    unittest.main()
