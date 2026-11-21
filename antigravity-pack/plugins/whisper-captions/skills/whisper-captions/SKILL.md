---
name: whisper-captions
description: >-
  Generate accurate local speech-to-text transcripts and word-timed auto captions
  using Whisper (faster-whisper, WhisperX, openai-whisper, or mlx-whisper).
  Exports SRT, WebVTT, Remotion-native captions JSON, and styled ASS karaoke/pop
  subtitles sized for vertical 9:16 (Shorts/Reels/TikTok) or 16:9 YouTube, with
  FFmpeg burn-in recipes. Use when the user asks for "whisper", "auto captions",
  "transcribe video/audio", "generate subtitles", "SRT/VTT/ASS captions",
  "karaoke captions", or "word-level timestamps".
---

# Whisper Auto Captions & Transcription (`whisper-captions`)

Produce accurate local transcripts and ready-to-burn or ready-to-render word-level captions without cloud APIs using the bundled helper script [`scripts/whisper_captions.py`](./scripts/whisper_captions.py).

## 1. Check Local Backends & Hardware First

```bash
python "<SKILL_DIR>/scripts/whisper_captions.py" --doctor
```

Backend preference order:
1. **`faster-whisper`** (CTranslate2 — 4x faster, lowest VRAM, word-level timestamps + Silero VAD).
2. **`whisperx`** (phoneme-level wav2vec2 alignment + optional pyannote speaker diarization when `HF_TOKEN` is set).
3. **`openai-whisper`** (universal fallback CLI/Python package).
4. **`mlx-whisper`** (Apple Silicon Metal acceleration on macOS).

If none is installed, tell the user the exact one-line install (`pip install faster-whisper` or `pip install openai-whisper`) rather than inventing dialogue.

## 2. Model Size Selection Guide

| Model | VRAM / RAM | Speed | Best For |
| :--- | :---: | :---: | :--- |
| `tiny` / `base` | ~1 GB | Very fast | Quick drafts, sanity checks |
| `small` | ~2 GB | Fast | Clean single-speaker clips |
| `medium` | ~5 GB | Balanced | Accents, noisy speech, multilingual |
| `large-v3` / `large-v3-turbo` | ~6–10 GB | Highest accuracy | Final production, technical terms, viral captions |

- Always pass `--language <code>` (e.g., `--language en`) when the spoken language is known to avoid misdetection and save overhead.
- Enable VAD filtering (`--vad`, on by default in `faster-whisper`) to stop Whisper hallucinating phantom words during silence or music beds.

## 3. Transcribe & Export Multiple Caption Formats

```bash
# Transcribe directly to SRT + VTT + Remotion captions JSON + viral vertical ASS karaoke
python "<SKILL_DIR>/scripts/whisper_captions.py" input.mp4 \
  --model large-v3-turbo \
  --language en \
  --aspect 9:16 \
  --style viral-pop \
  --formats srt,vtt,json,ass \
  --out-dir ./captions_out

# Or reformat an existing word-timestamps JSON into vertical ASS / SRT / Remotion JSON (zero re-transcription)
python "<SKILL_DIR>/scripts/whisper_captions.py" --from-words words.json \
  --aspect 9:16 --style viral-pop --formats srt,ass,json --out-dir ./captions_out
```

## 4. Readability & Safe-Zone Contract

- **Vertical 9:16 (1080×1920 Shorts / Reels / TikTok):**
  - **1–3 words per cue** (max `18–20` characters per line) so captions stay punchy and never wrap into walls of text.
  - Keep captions clear of the bottom ~22% platform UI chrome and top ~14% chrome (and never cover a speaker's face).
- **Horizontal 16:9 (1920×1080 YouTube / web):**
  - **Max 6–8 words per cue** (max `42` characters per line), max 2 lines.
- **ASS Color Format Rule:** Always use 8-char `&HAABBGGRR` (alpha, blue, green, red — e.g. yellow `&H001DE1FF`, white `&H00FFFFFF`, black outline `&H00000000`). Never write RGB hex into ASS styles.
- **Never fabricate or silently drop words:** Fix proper-noun spelling in the transcript JSON while preserving exact `startMs` / `endMs` timestamps.

## 5. Burn Captions Into Video (or Hand Off to Remotion / HyperFrames)

- **Hard-burn styled ASS with FFmpeg (or via `ffmpeg-skill`):**
  ```bash
  ffmpeg -i input.mp4 -vf "ass=captions_out/input.ass" -c:v libx264 -crf 18 -c:a copy captioned.mp4
  ```
  *(On Windows, escape drive colons inside FFmpeg filter graphs or run from the directory containing the `.ass` file.)*
- **Remotion (`remotion-suite` / `claude-shorts`):** Pass the generated `*.captions.json` directly to `@remotion/captions` `createTikTokStyleCaptions()`.
- **Verification:** Spot-check at least 3 spoken cues against audio timing, verify zero overlapping cues, and inspect a rendered still frame for contrast and safe-area margins.
