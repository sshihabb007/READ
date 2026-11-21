import json
import os
import re
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PLUGIN_ROOT, "skills")
RUNTIME_ROOT = os.path.join(PLUGIN_ROOT, "runtime")
LINK_RX = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class OpenMontagePluginBundle(unittest.TestCase):
    def test_manifest_and_agpl_license(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "openmontage-studio")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)
        with open(os.path.join(PLUGIN_ROOT, "LICENSE"), encoding="utf-8") as fh:
            self.assertIn("GNU AFFERO GENERAL PUBLIC LICENSE", fh.read())

    def test_skills_frontmatter_and_links_resolve(self):
        expected = ["openmontage", "openmontage-reference-analyst"]
        found = sorted(
            d
            for d in os.listdir(SKILLS_ROOT)
            if os.path.isdir(os.path.join(SKILLS_ROOT, d))
            and os.path.isfile(os.path.join(SKILLS_ROOT, d, "SKILL.md"))
        )
        self.assertEqual(found, expected)
        for skill in expected:
            skill_md = os.path.join(SKILLS_ROOT, skill, "SKILL.md")
            with open(skill_md, encoding="utf-8") as fh:
                text = fh.read()
            m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
            self.assertIsNotNone(m, skill)
            self.assertIn(f"name: {skill}", m.group(1), skill)
            for lm in LINK_RX.finditer(text):
                raw = lm.group(1).strip()
                if not raw or raw.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
                    continue
                target = raw.split("#", 1)[0].split("?", 1)[0]
                if not target:
                    continue
                resolved = os.path.normpath(os.path.join(os.path.dirname(skill_md), target))
                self.assertTrue(os.path.exists(resolved), f"Broken link in {skill}: {raw} -> {resolved}")

    def test_runtime_core_components_present(self):
        for rel in [
            "AGENT_GUIDE.md",
            "PROJECT_CONTEXT.md",
            "skills/INDEX.md",
            "pipeline_defs/animated-explainer.yaml",
            "pipeline_defs/documentary-montage.yaml",
            "tools/tool_registry.py",
            "lib/checkpoint.py",
            "backlot",
            "ink-theater",
            "remotion-composer",
        ]:
            self.assertTrue(os.path.exists(os.path.join(RUNTIME_ROOT, rel)), rel)


if __name__ == "__main__":
    unittest.main()
