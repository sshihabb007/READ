import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(PLUGIN_ROOT, "skills", "whisper-captions")
SCRIPT = os.path.join(SKILL_DIR, "scripts", "whisper_captions.py")


class WhisperCaptionsPluginBundle(unittest.TestCase):
    def test_manifest_and_frontmatter(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "whisper-captions")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        self.assertIsNotNone(m)
        self.assertIn("name: whisper-captions", m.group(1))

    def test_doctor_and_from_words_export(self):
        doc = subprocess.run([sys.executable, SCRIPT, "--doctor"], capture_output=True, text=True, check=False)
        self.assertEqual(doc.returncode, 0, doc.stderr)
        info = json.loads(doc.stdout)
        self.assertIn("backends", info)

        sample_words = {
            "words": [
                {"word": "Watch", "startMs": 0, "endMs": 280},
                {"word": "this", "startMs": 290, "endMs": 520},
                {"word": "insane", "startMs": 540, "endMs": 950},
                {"word": "escape!", "startMs": 980, "endMs": 1450},
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            words_path = os.path.join(tmp, "demo.json")
            with open(words_path, "w", encoding="utf-8") as fh:
                json.dump(sample_words, fh)
            res = subprocess.run(
                [sys.executable, SCRIPT, "--from-words", words_path, "--aspect", "9:16", "--style", "viral-pop", "--formats", "srt,vtt,json,ass", "--out-dir", tmp],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res.returncode, 0, res.stderr)
            out = json.loads(res.stdout)
            self.assertEqual(out["word_count"], 4)
            for fmt in ("srt", "vtt", "json", "ass"):
                self.assertTrue(os.path.isfile(out["outputs"][fmt]), fmt)
            with open(out["outputs"]["ass"], encoding="utf-8") as fh:
                ass_txt = fh.read()
            self.assertIn("&H001DE1FF", ass_txt)
            self.assertIn("PlayResX: 1080", ass_txt)


if __name__ == "__main__":
    unittest.main()
