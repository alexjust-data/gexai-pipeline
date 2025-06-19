# src/gexai/transcription.py

from pathlib import Path
import json
import whisper
from typing import List, Dict

def whisper_transcribe(wav_path: Path, model: str = "small") -> List[Dict]:
    """Run OpenAI Whisper on the WAV file and return segments."""
    model = whisper.load_model(model)
    result = model.transcribe(str(wav_path), verbose=False)
    return result["segments"]

# ─────── Export helpers ───────

def export_json(segments: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

def export_txt(segments: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(s["text"].strip() + "\n")

def _fmt_ts(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def export_srt(segments: List[Dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{_fmt_ts(s['start'])} --> {_fmt_ts(s['end'])}\n")
            f.write(s["text"].strip() + "\n\n")



