import json
import os
import re
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PLUGIN_ROOT, "skills")

EXPECTED_SKILLS = [
    "remotion-best-practices",
    "remotion-captions",
    "remotion-create",
    "remotion-docs",
    "remotion-interactivity",
    "remotion-license",
    "remotion-maps",
    "remotion-markup",
    "remotion-multimedia",
    "remotion-render",
    "remotion-saas",
    "remotion-studio",
    "remotion-upgrade",
]

LINK_RX = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    return (m.group(1) if m else ""), text


class RemotionPluginBundle(unittest.TestCase):
    def test_expected_thirteen_skills_present(self):
        found = sorted(
            d
            for d in os.listdir(SKILLS_ROOT)
            if os.path.isdir(os.path.join(SKILLS_ROOT, d))
            and os.path.isfile(os.path.join(SKILLS_ROOT, d, "SKILL.md"))
        )
        self.assertEqual(found, sorted(EXPECTED_SKILLS))

    def test_frontmatter_and_no_stub_symlinks(self):
        for skill in EXPECTED_SKILLS:
            skill_dir = os.path.join(SKILLS_ROOT, skill)
            fm, _ = parse_frontmatter(os.path.join(skill_dir, "SKILL.md"))
            norm_fm = fm.replace("\r\n", "\n") + "\n"
            self.assertIn("name: %s\n" % skill, norm_fm, skill)
            self.assertRegex(norm_fm, r"description:\s+\S", skill)
            # Ensure no git symlink text-stub files survived
            for entry in os.listdir(skill_dir):
                full = os.path.join(skill_dir, entry)
                if os.path.isfile(full) and entry.startswith("remotion-"):
                    self.fail("Unexpected symlink stub file left in %s: %s" % (skill, entry))

    def test_all_local_markdown_links_resolve(self):
        broken = []
        for dirpath, _, filenames in os.walk(SKILLS_ROOT):
            for fn in filenames:
                if not fn.endswith((".md", ".mdx")):
                    continue
                md_path = os.path.join(dirpath, fn)
                with open(md_path, encoding="utf-8") as fh:
                    content = fh.read()
                for m in LINK_RX.finditer(content):
                    raw = m.group(1).strip()
                    if not raw or raw.startswith("#"):
                        continue
                    target = raw.split()[0].strip("<>")
                    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                        continue
                    path_part = target.split("#", 1)[0].split("?", 1)[0]
                    if not path_part:
                        continue
                    resolved = os.path.normpath(os.path.join(dirpath, path_part))
                    if not os.path.exists(resolved):
                        broken.append((os.path.relpath(md_path, SKILLS_ROOT), raw, os.path.relpath(resolved, SKILLS_ROOT)))
        self.assertEqual(broken, [], f"Broken local markdown links: {broken}")

    def test_plugin_manifest_valid(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "remotion-suite")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)


if __name__ == "__main__":
    unittest.main()
