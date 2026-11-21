import json
import os
import re
import subprocess
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(PLUGIN_ROOT, "skills", "yt-dlp-media")
SCRIPT = os.path.join(SKILL_DIR, "scripts", "yt_dlp_helper.py")


class YtDlpPluginBundle(unittest.TestCase):
    def test_manifest_and_frontmatter(self):
        with open(os.path.join(PLUGIN_ROOT, "plugin.json"), encoding="utf-8") as fh:
            manifest = json.load(fh)
        self.assertEqual(manifest["name"], "yt-dlp-media")
        self.assertTrue(os.path.isfile(os.path.join(PLUGIN_ROOT, manifest["logo"])))
        self.assertLessEqual(len(manifest.get("suggestedPrompts", [])), 3)
        with open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
        self.assertIsNotNone(m)
        self.assertIn("name: yt-dlp-media", m.group(1))

    def test_doctor_and_dry_run_modes(self):
        doc = subprocess.run([sys.executable, SCRIPT, "--doctor"], capture_output=True, text=True, check=False)
        self.assertEqual(doc.returncode, 0, doc.stderr)
        self.assertIn("yt_dlp", json.loads(doc.stdout))

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s"
        cases = [
            (["video", url, "--max-height", "1080", "--h264", "--dry-run"], "vcodec:h264,acodec:aac,ext:mp4:m4a"),
            (["clip", url, "--start", "00:01:00", "--end", "00:02:30", "--dry-run"], "*00:01:00-00:02:30"),
            (["audio", url, "--audio-format", "wav", "--dry-run"], "wav"),
            (["subs", url, "--langs", "en", "--auto-subs", "--dry-run"], "--write-auto-subs"),
            (["metadata", url, "--dry-run"], "--dump-json"),
        ]
        for argv, expected_token in cases:
            res = subprocess.run([sys.executable, SCRIPT] + argv, capture_output=True, text=True, check=False)
            self.assertEqual(res.returncode, 0, res.stderr)
            data = json.loads(res.stdout)
            self.assertEqual(data["status"], "dry-run")
            self.assertIn(expected_token, data["command"])
            self.assertEqual(data["command"][-1], url)


if __name__ == "__main__":
    unittest.main()
