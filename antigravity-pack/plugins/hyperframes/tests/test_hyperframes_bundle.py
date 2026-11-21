import json
import os
import re
import subprocess
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PLUGIN_ROOT, "skills")

EXPECTED_SKILLS = [
    "figma",
    "hyperframes",
    "hyperframes-cli",
    "hyperframes-registry",
    "media-use",
    "remotion-to-hyperframes",
    "reverse-any-video",
    "slideshow",
    "style-sampling",
]


class HyperFramesPluginBundle(unittest.TestCase):
    def test_manifest_and_apache_license(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "hyperframes")
        self.assertEqual(manifest["version"], "0.9.77")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)
        with open(os.path.join(PLUGIN_ROOT, "LICENSE"), encoding="utf-8") as fh:
            self.assertIn("Apache License", fh.read())

    def test_all_nine_skills_present_with_frontmatter(self):
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

    def test_plugin_cli_recognizes_manifest_version(self):
        cli_url = "file:///" + os.path.join(SKILLS_ROOT, "hyperframes", "scripts", "plugin-cli.mjs").replace("\\", "/")
        code = f"import {{pluginVersion}} from '{cli_url}'; console.log(pluginVersion(undefined, process.env.TEMP || '/tmp'));"
        res = subprocess.run(["node", "--input-type=module", "-e", code], capture_output=True, text=True, check=False)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), "0.9.77")


if __name__ == "__main__":
    unittest.main()
