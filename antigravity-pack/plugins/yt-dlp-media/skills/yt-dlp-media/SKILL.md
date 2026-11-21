---
name: yt-dlp-media
description: >-
  Download video, audio, time-range clips, thumbnails, metadata JSON, and native
  or auto-generated subtitles from YouTube and 1000+ sites using yt-dlp with no
  API keys. Includes edit-ready H.264/MP4 format selection, section clipping,
  subtitle-only fetching, and safe cross-platform execution via scripts/yt_dlp_helper.py.
  Use when the user asks to "download a YouTube video", "use yt-dlp", "grab audio
  from a URL", "fetch YouTube subtitles/transcript", "download a specific clip
  range", or "inspect video formats/metadata".
---

# yt-dlp Media, Audio & Subtitle Downloader (`yt-dlp-media`)

Download edit-ready video, audio tracks, specific time-range clips, metadata, and subtitles from YouTube and 1000+ supported sites using `yt-dlp` — either directly or via the safe cross-platform helper [`scripts/yt_dlp_helper.py`](./scripts/yt_dlp_helper.py) (uses `shell=False` argv execution so URLs with `&`, `?`, or parentheses never break on Windows PowerShell or bash).

## 1. Check Toolchain

```bash
python "<SKILL_DIR>/scripts/yt_dlp_helper.py" --doctor
```

- Requires `yt-dlp` (`pip install -U yt-dlp` or `winget install yt-dlp.yt-dlp` / `brew install yt-dlp`) and `ffmpeg` for merging separate video + audio streams.
- If a download fails with HTTP 403 or extractor errors, update `yt-dlp` first (`yt-dlp -U`).

## 2. Core Workflows (Always Preview With `--dry-run` When Unsure)

| Goal | Command via Helper | Raw `yt-dlp` Equivalent |
| :--- | :--- | :--- |
| **Edit-ready 1080p MP4 (H.264 + AAC)** | `python "<SKILL_DIR>/scripts/yt_dlp_helper.py" video "<URL>" --max-height 1080 --h264 --out-dir ./downloads` | `yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" -S "vcodec:h264,acodec:aac,ext:mp4:m4a" --merge-output-format mp4 -o "./downloads/%(title)s.%(ext)s" "<URL>"` |
| **Audio-only WAV for Whisper** | `python "<SKILL_DIR>/scripts/yt_dlp_helper.py" audio "<URL>" --audio-format wav --out-dir ./downloads` | `yt-dlp -x --audio-format wav --audio-quality 0 -o "./downloads/%(title)s.%(ext)s" "<URL>"` |
| **Subtitles / Transcript only (fast)** | `python "<SKILL_DIR>/scripts/yt_dlp_helper.py" subs "<URL>" --langs en --auto-subs --out-dir ./downloads` | `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs en --convert-subs srt -o "./downloads/%(title)s.%(ext)s" "<URL>"` |
| **Download only a time range** | `python "<SKILL_DIR>/scripts/yt_dlp_helper.py" clip "<URL>" --start 00:05:00 --end 00:07:30 --out-dir ./downloads` | `yt-dlp --download-sections "*00:05:00-00:07:30" --force-keyframes-at-cuts --merge-output-format mp4 "<URL>"` |
| **Inspect metadata without downloading** | `python "<SKILL_DIR>/scripts/yt_dlp_helper.py" metadata "<URL>"` | `yt-dlp --dump-json --no-download --no-playlist "<URL>"` |

## 3. Pipeline Integration & Best Practices

- **Prefer native subtitles before transcribing:** Run `subs` first; only fall back to `audio --audio-format wav` + `whisper-captions` when captions are missing or word-level precision is needed for viral pop/karaoke captions.
- **Edit-ready codec sorting (`--h264`):** YouTube often serves VP9/AV1 by default; sorting for `vcodec:h264,ext:mp4:m4a` ensures immediate compatibility with Remotion, FFmpeg lossless cuts, Premiere, and CapCut without re-encoding.
- **Section clipping (`clip`):** For multi-hour streams or walkthroughs when only specific timestamps are needed, use `--download-sections` instead of downloading multi-GB full files.
- **Respect rights & privacy:** Only download content the user owns, has permission to process, or is openly licensed; never log or persist browser cookies or session tokens.
