#!/usr/bin/env python3
"""Local Whisper Auto-Captions CLI: backend doctor, transcription, and SRT/VTT/Remotion-JSON/ASS formatting.

Zero third-party dependencies for --doctor and --from-words formatting.
Uses faster-whisper, whisperx, or openai-whisper when transcribing audio/video.
"""

import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def detect_environment() -> Dict[str, Any]:
    backends = {}
    for mod in ("faster_whisper", "whisperx", "whisper", "mlx_whisper"):
        backends[mod] = importlib.util.find_spec(mod) is not None
    torch_spec = importlib.util.find_spec("torch")
    cuda = False
    if torch_spec is not None:
        try:
            import torch  # type: ignore
            cuda = bool(torch.cuda.is_available())
        except Exception:
            cuda = False
    preferred = next((m for m in ("faster_whisper", "whisperx", "whisper", "mlx_whisper") if backends[m]), None)
    return {
        "python": sys.version.split()[0],
        "ffmpeg": shutil.which("ffmpeg"),
        "ffprobe": shutil.which("ffprobe"),
        "backends": backends,
        "preferred_backend": preferred,
        "cuda_available": cuda,
        "install_hint": None if preferred else "pip install faster-whisper",
    }


def fmt_srt_time(ms: int) -> str:
    ms = max(0, int(round(ms)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1_000)
    return f"{h:02d}:{m:02d}:{s:02d},{milli:03d}"


def fmt_vtt_time(ms: int) -> str:
    return fmt_srt_time(ms).replace(",", ".")


def fmt_ass_time(ms: int) -> str:
    ms = max(0, int(round(ms)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1_000)
    cs = min(99, round(milli / 10))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def normalize_words(raw: Any) -> List[Dict[str, Any]]:
    items = raw["words"] if isinstance(raw, dict) and "words" in raw else raw
    if isinstance(raw, dict) and "captions" in raw and not items:
        items = raw["captions"]
    words: List[Dict[str, Any]] = []
    for item in items:
        text = str(item.get("word", item.get("text", ""))).strip()
        if not text:
            continue
        if "startMs" in item and "endMs" in item:
            start_ms = int(round(float(item["startMs"])))
            end_ms = int(round(float(item["endMs"])))
        else:
            start_ms = int(round(float(item.get("start", 0.0)) * 1000))
            end_ms = int(round(float(item.get("end", start_ms / 1000.0 + 0.15)) * 1000))
        end_ms = max(end_ms, start_ms + 60)
        words.append({
            "word": text,
            "startMs": start_ms,
            "endMs": end_ms,
            "confidence": float(item.get("confidence", item.get("probability", 1.0))),
        })
    words.sort(key=lambda w: (w["startMs"], w["endMs"]))
    return words


def group_words(words: List[Dict[str, Any]], aspect: str) -> List[Dict[str, Any]]:
    max_words = 3 if aspect == "9:16" else 7
    max_chars = 20 if aspect == "9:16" else 42
    max_gap_ms = 380 if aspect == "9:16" else 650

    groups: List[Dict[str, Any]] = []
    cur: List[Dict[str, Any]] = []
    cur_len = 0

    def flush() -> None:
        nonlocal cur, cur_len
        if not cur:
            return
        groups.append({
            "words": cur,
            "text": " ".join(w["word"] for w in cur),
            "startMs": cur[0]["startMs"],
            "endMs": cur[-1]["endMs"],
        })
        cur = []
        cur_len = 0

    for w in words:
        gap = (w["startMs"] - cur[-1]["endMs"]) if cur else 0
        next_len = cur_len + (1 if cur else 0) + len(w["word"])
        ends_sentence = bool(cur and cur[-1]["word"][-1:] in ".!?")
        if cur and (len(cur) >= max_words or next_len > max_chars or gap > max_gap_ms or ends_sentence):
            flush()
        cur.append(w)
        cur_len += (1 if len(cur) > 1 else 0) + len(w["word"])
    flush()

    # Prevent overlapping cues across adjacent groups
    for idx in range(len(groups) - 1):
        if groups[idx]["endMs"] > groups[idx + 1]["startMs"]:
            groups[idx]["endMs"] = max(groups[idx]["startMs"] + 60, groups[idx + 1]["startMs"] - 10)
    return groups


def render_srt(groups: List[Dict[str, Any]]) -> str:
    blocks = []
    for idx, g in enumerate(groups, 1):
        blocks.append(f"{idx}\n{fmt_srt_time(g['startMs'])} --> {fmt_srt_time(g['endMs'])}\n{g['text']}")
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def render_vtt(groups: List[Dict[str, Any]]) -> str:
    blocks = ["WEBVTT", ""]
    for g in groups:
        blocks.append(f"{fmt_vtt_time(g['startMs'])} --> {fmt_vtt_time(g['endMs'])}\n{g['text']}\n")
    return "\n".join(blocks)


def render_remotion_json(words: List[Dict[str, Any]]) -> str:
    payload = [
        {
            "text": (" " if idx > 0 else "") + w["word"],
            "startMs": w["startMs"],
            "endMs": w["endMs"],
            "timestampMs": (w["startMs"] + w["endMs"]) // 2,
            "confidence": w["confidence"],
        }
        for idx, w in enumerate(words)
    ]
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def render_ass(groups: List[Dict[str, Any]], aspect: str, style: str) -> str:
    play_x, play_y = (1080, 1920) if aspect == "9:16" else (1920, 1080)
    font_name = "Montserrat" if style in ("viral-pop", "karaoke") else "Inter"
    font_size = 76 if aspect == "9:16" else 54
    outline = 6 if aspect == "9:16" else 4
    margin_v = 480 if aspect == "9:16" else 70
    # ASS colors are &HAABBGGRR (yellow highlight #FFE11D -> &H001DE1FF)
    primary = "&H00FFFFFF"
    secondary = "&H001DE1FF"
    outline_col = "&H00000000"
    back_col = "&H80000000"

    header = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {play_x}",
        f"PlayResY: {play_y}",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font_name},{font_size},{primary},{secondary},{outline_col},{back_col},-1,0,0,0,100,100,1,0,1,{outline},3,2,60,60,{margin_v},1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    events: List[str] = []
    for g in groups:
        if style == "viral-pop":
            for i, active_w in enumerate(g["words"]):
                w_start = active_w["startMs"]
                w_end = g["words"][i + 1]["startMs"] if i + 1 < len(g["words"]) else g["endMs"]
                w_end = max(w_end, w_start + 50)
                parts = []
                for j, tok in enumerate(g["words"]):
                    txt = ass_escape(tok["word"].upper())
                    if j == i:
                        parts.append(r"{\c&H001DE1FF&\fscx108\fscy108}" + txt + r"{\c&H00FFFFFF&\fscx100\fscy100}")
                    else:
                        parts.append(txt)
                events.append(f"Dialogue: 0,{fmt_ass_time(w_start)},{fmt_ass_time(w_end)},Default,,0,0,0,,{' '.join(parts)}")
        elif style == "karaoke":
            parts = []
            for tok in g["words"]:
                dur_cs = max(5, round((tok["endMs"] - tok["startMs"]) / 10))
                parts.append(f"{{\\kf{dur_cs}}}{ass_escape(tok['word'])}")
            events.append(f"Dialogue: 0,{fmt_ass_time(g['startMs'])},{fmt_ass_time(g['endMs'])},Default,,0,0,0,,{' '.join(parts)}")
        else:
            txt = ass_escape(g["text"])
            events.append(f"Dialogue: 0,{fmt_ass_time(g['startMs'])},{fmt_ass_time(g['endMs'])},Default,,0,0,0,,{txt}")
    return "\n".join(header + events) + "\n"


def transcribe_media(input_path: Path, model_size: str, language: Optional[str], backend: Optional[str]) -> List[Dict[str, Any]]:
    env = detect_environment()
    chosen = backend or env["preferred_backend"]
    if not chosen:
        raise RuntimeError("No local Whisper backend installed. Install one with: pip install faster-whisper")

    words: List[Dict[str, Any]] = []
    if chosen == "faster_whisper":
        from faster_whisper import WhisperModel  # type: ignore

        device = "cuda" if env["cuda_available"] else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        segments, _info = model.transcribe(
            str(input_path),
            language=language,
            word_timestamps=True,
            vad_filter=True,
        )
        for seg in segments:
            for w in getattr(seg, "words", None) or []:
                txt = str(w.word).strip()
                if txt:
                    words.append({
                        "word": txt,
                        "startMs": int(round(w.start * 1000)),
                        "endMs": max(int(round(w.end * 1000)), int(round(w.start * 1000)) + 60),
                        "confidence": float(getattr(w, "probability", 1.0)),
                    })
    elif chosen == "whisper":
        import whisper  # type: ignore

        model = whisper.load_model(model_size)
        result = model.transcribe(str(input_path), language=language, word_timestamps=True)
        for seg in result.get("segments", []):
            for w in seg.get("words", []):
                txt = str(w.get("word", "")).strip()
                if txt:
                    s_ms = int(round(float(w["start"]) * 1000))
                    e_ms = max(int(round(float(w["end"]) * 1000)), s_ms + 60)
                    words.append({"word": txt, "startMs": s_ms, "endMs": e_ms, "confidence": float(w.get("probability", 1.0))})
    else:
        raise RuntimeError(f"Unsupported backend for direct CLI run: {chosen}. Use faster_whisper or whisper.")
    return words


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Local Whisper auto-captions & SRT/VTT/Remotion-JSON/ASS exporter.")
    parser.add_argument("input", nargs="?", help="Input video/audio file to transcribe")
    parser.add_argument("--doctor", action="store_true", help="Inspect installed Whisper backends, CUDA, and FFmpeg")
    parser.add_argument("--from-words", help="Format an existing word-timestamps JSON file without re-transcribing")
    parser.add_argument("--model", default="base", help="Whisper model size (tiny, base, small, medium, large-v3, large-v3-turbo)")
    parser.add_argument("--language", default=None, help="ISO 639-1 language code (e.g. en, es, bn) or omit for auto-detect")
    parser.add_argument("--backend", choices=["faster_whisper", "whisper"], default=None)
    parser.add_argument("--aspect", choices=["9:16", "16:9"], default="9:16")
    parser.add_argument("--style", choices=["viral-pop", "karaoke", "clean"], default="viral-pop")
    parser.add_argument("--formats", default="srt,vtt,json,ass", help="Comma-separated output formats: srt,vtt,json,ass")
    parser.add_argument("--out-dir", default=".", help="Directory for output caption files")
    args = parser.parse_args(argv)

    if args.doctor:
        print(json.dumps(detect_environment(), indent=2))
        return 0

    if args.from_words:
        src_path = Path(args.from_words)
        raw = json.loads(src_path.read_text(encoding="utf-8"))
        words = normalize_words(raw)
        stem = src_path.stem
    elif args.input:
        src_path = Path(args.input)
        if not src_path.is_file():
            print(json.dumps({"status": "error", "message": f"Input file not found: {src_path}"}), file=sys.stderr)
            return 2
        words = transcribe_media(src_path, args.model, args.language, args.backend)
        stem = src_path.stem
    else:
        parser.error("Provide an input media file, --from-words JSON, or --doctor")
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = group_words(words, args.aspect)
    wanted = [f.strip().lower() for f in args.formats.split(",") if f.strip()]
    written: Dict[str, str] = {}

    if "srt" in wanted:
        p = out_dir / f"{stem}.srt"
        p.write_text(render_srt(groups), encoding="utf-8")
        written["srt"] = str(p)
    if "vtt" in wanted:
        p = out_dir / f"{stem}.vtt"
        p.write_text(render_vtt(groups), encoding="utf-8")
        written["vtt"] = str(p)
    if "json" in wanted:
        p = out_dir / f"{stem}.captions.json"
        p.write_text(render_remotion_json(words), encoding="utf-8")
        written["json"] = str(p)
    if "ass" in wanted:
        p = out_dir / f"{stem}.ass"
        p.write_text(render_ass(groups, args.aspect, args.style), encoding="utf-8")
        written["ass"] = str(p)

    print(json.dumps({
        "status": "ok",
        "word_count": len(words),
        "cue_count": len(groups),
        "aspect": args.aspect,
        "style": args.style,
        "outputs": written,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
