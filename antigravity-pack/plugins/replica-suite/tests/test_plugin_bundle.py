import json
import os
import re
import unittest

from _load import PLUGIN_ROOT, ROOT

SKILLS = [
    "replica-recon",
    "replica-architect",
    "replica-design",
    "replica-build",
    "replica-backend",
    "replica-test",
    "replica-diff",
    "replica-entrepreneur",
    "replica-brand",
    "replica-launch",
    "replica-deploy",
]


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    return (m.group(1) if m else ""), text


class ReplicaPluginBundle(unittest.TestCase):
    def test_eleven_skill_folders_under_skills_dir(self):
        found = sorted(
            d
            for d in os.listdir(ROOT)
            if os.path.isfile(os.path.join(ROOT, d, "SKILL.md"))
        )
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(ROOT, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm.replace("\r\n", "\n") + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 200, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_antigravity_plugin_manifest_valid(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "replica-suite")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, plugin["logo"])))
        self.assertLessEqual(len(plugin.get("suggestedPrompts", [])), 3)

    def test_no_em_dashes_anywhere(self):
        bad = []
        for dirpath, dirnames, filenames in os.walk(PLUGIN_ROOT):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for fn in filenames:
                if fn.endswith((".md", ".py", ".json", ".ts", ".csv")):
                    path = os.path.join(dirpath, fn)
                    with open(path, encoding="utf-8") as fh:
                        if chr(0x2014) in fh.read():
                            bad.append(os.path.relpath(path, PLUGIN_ROOT))
        self.assertEqual(bad, [])


if __name__ == "__main__":
    unittest.main()
