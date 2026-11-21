#!/usr/bin/env python3
"""Safe cross-platform yt-dlp helper (stdlib-only, shell=False execution)."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def check_doctor() -> Dict[str, Any]:
    yt = shutil.which("yt-dlp")
    ff = shutil.which("ffmpeg")
    yt_ver = None
    if yt:
        r = subprocess.run([yt, "--version"], capture_output=True, text=True, check=False)
        if r.returncode == 0:
            yt_ver = r.stdout.strip()
    return {
        "yt_dlp": yt,
        "yt_dlp_version": yt_ver,
        "ffmpeg": ff,
        "install_hint": None if yt else "pip install -U yt-dlp",
    }


def build_command(args: argparse.Namespace) -> List[str]:
    yt_bin = shutil.which("yt-dlp") or "yt-dlp"
    cmd: List[str] = [yt_bin, "--no-playlist"]
    out_dir = Path(getattr(args, "out_dir", "."))
    tmpl = str(out_dir / "%(title)s [%(id)s].%(ext)s")

    if args.mode == "metadata":
        cmd += ["--dump-json", "--no-download", args.url]
        return cmd

    if args.mode == "subs":
        cmd += [
            "--skip-download",
            "--write-subs",
            "--sub-langs",
            args.langs,
            "--convert-subs",
            args.sub_format,
            "-o",
            tmpl,
        ]
        if args.auto_subs:
            cmd.append("--write-auto-subs")
        cmd.append(args.url)
        return cmd

    if args.mode == "audio":
        cmd += [
            "-x",
            "--audio-format",
            args.audio_format,
            "--audio-quality",
            "0",
            "-o",
            tmpl,
            args.url,
        ]
        return cmd

    # video or clip
    if args.max_height:
        fmt = f"bestvideo[height<={args.max_height}]+bestaudio/best[height<={args.max_height}]"
    else:
        fmt = "bestvideo+bestaudio/best"
    cmd += ["-f", fmt, "--merge-output-format", "mp4"]
    if args.h264:
        cmd += ["-S", "vcodec:h264,acodec:aac,ext:mp4:m4a"]
    if args.mode == "clip":
        cmd += ["--download-sections", f"*{args.start}-{args.end}", "--force-keyframes-at-cuts"]
    cmd += ["-o", tmpl, args.url]
    return cmd


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Safe cross-platform yt-dlp helper.")
    parser.add_argument("--doctor", action="store_true", help="Check yt-dlp and ffmpeg installation")
    sub = parser.add_subparsers(dest="mode")

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("url", help="Target media URL")
        p.add_argument("--out-dir", default=".", help="Output directory")
        p.add_argument("--dry-run", action="store_true", help="Print planned command JSON without running")

    p_vid = sub.add_parser("video", help="Download MP4 video")
    add_common(p_vid)
    p_vid.add_argument("--max-height", type=int, default=1080)
    p_vid.add_argument("--h264", action="store_true", help="Prefer edit-ready H.264/AAC streams")

    p_clip = sub.add_parser("clip", help="Download a time-range section of a video")
    add_common(p_clip)
    p_clip.add_argument("--start", required=True, help="Start timestamp (e.g. 00:05:00)")
    p_clip.add_argument("--end", required=True, help="End timestamp (e.g. 00:07:30)")
    p_clip.add_argument("--max-height", type=int, default=1080)
    p_clip.add_argument("--h264", action="store_true")

    p_aud = sub.add_parser("audio", help="Extract audio track")
    add_common(p_aud)
    p_aud.add_argument("--audio-format", choices=["wav", "mp3", "m4a", "flac"], default="wav")

    p_sub = sub.add_parser("subs", help="Download subtitles/transcripts only")
    add_common(p_sub)
    p_sub.add_argument("--langs", default="en")
    p_sub.add_argument("--auto-subs", action="store_true")
    p_sub.add_argument("--sub-format", choices=["srt", "vtt", "ass"], default="srt")

    p_meta = sub.add_parser("metadata", help="Dump video metadata JSON without downloading")
    add_common(p_meta)

    args = parser.parse_args(argv)
    if args.doctor:
        print(json.dumps(check_doctor(), indent=2))
        return 0
    if not args.mode:
        parser.error("Specify --doctor or one of: video, clip, audio, subs, metadata")
        return 2

    cmd = build_command(args)
    if args.dry_run:
        print(json.dumps({"status": "dry-run", "mode": args.mode, "command": cmd}, indent=2))
        return 0

    if not shutil.which("yt-dlp"):
        print(json.dumps({"status": "error", "message": "yt-dlp not found on PATH. Install with: pip install -U yt-dlp"}), file=sys.stderr)
        return 1

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    res = subprocess.run(cmd, check=False)
    return res.returncode


if __name__ == "__main__":
    raise SystemExit(main())
