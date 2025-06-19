# 📚 GexAI — AI Audio Transcription & Diarization Pipeline

GexAI is a powerful and extensible Python pipeline that lets you transcribe audio/video files (including YouTube links) using OpenAI Whisper, and optionally perform speaker diarization using pyannote-audio.

It can be used **both in terminal** and **from Jupyter notebooks**.

---

## ✨ Features

* Transcription with [OpenAI Whisper](https://github.com/openai/whisper)
* Speaker diarization with [pyannote-audio](https://github.com/pyannote/pyannote-audio)
* Direct YouTube audio download via `yt-dlp`
* Works in CLI or Jupyter
* 📁 Exports in `.json`, `.txt`, and `.srt`

---

## Installation

```bash
# Clone the repo
$ git clone https://github.com/yourusername/gexai.git
$ cd gexai

# Create and activate virtualenv
$ python -m venv venv
$ source venv/bin/activate

# Install dependencies
$ pip install -e .
```

---

## Example usage from Python (Jupyter)

```python
from gexai.pipeline import transcribe_pipeline

# Transcribe only
directory = transcribe_pipeline("https://www.youtube.com/watch?v=sw3N0leUULg")

# Transcribe + diarize
# directory = transcribe_pipeline("https://www.youtube.com/watch?v=sw3N0leUULg", diarize=True)

print(directory)
```

This will:

* Download audio from YouTube
* Convert it to WAV
* Transcribe it using Whisper
* Save `.json`, `.txt`, `.srt` in a subfolder like: `data/transcripciones/<video-id>`
* Optionally, generate diarized versions

---

## 🖥 CLI Usage (via terminal)

This project uses Python's `-m` module execution.

```bash
# Show help
$ python -m gexai.cli --help
```

### Transcribe a YouTube video

```bash
$ python -m gexai.cli transcribe "https://www.youtube.com/watch?v=sw3N0leUULg"
```

### Transcribe + Diarize

```bash
$ python -m gexai.cli transcribe "https://www.youtube.com/watch?v=sw3N0leUULg" --diarize
```

### Diarize a local WAV file

```bash
$ python -m gexai.cli diarize path/to/audio.wav
```

### Valid CLI Combinations

```bash
# Local file only (transcription only)
$ python -m gexai.cli transcribe path/to/audio.mp3

# Local file with diarization
$ python -m gexai.cli transcribe path/to/audio.wav --diarize

# YouTube video transcription only
$ python -m gexai.cli transcribe "https://www.youtube.com/watch?v=sw3N0leUULg"

# YouTube video transcription + diarization
$ python -m gexai.cli transcribe "https://www.youtube.com/watch?v=sw3N0leUULg" --diarize

# Diarize a local WAV
$ python -m gexai.cli diarize path/to/audio.wav
```

---

## 📁 Output folder structure

```
data/
└── transcripciones/
    └── <id>/
        ├── whisper.json
        ├── texto_plano.txt
        ├── subtitulos.srt
        ├── whisper_diarized.json         # if diarize=True
        ├── texto_diarizado.txt          # if diarize=True
        └── subtitulos_diarizados.srt    # if diarize=True
```

---

## ⚙️ Configuration (Optional)

You can customize paths or Whisper model via `.env`:

```bash
cp .env.example .env
```

```env
HF_TOKEN=your_huggingface_token
GEXAI_DATA_DIR=data
WHISPER_MODEL=small
```

---

## Checklist

* [x] Works with local `.mp3`, `.mp4`, `.wav`, etc.
* [x] Works with YouTube links
* [x] CLI via `typer`
* [x] Modular design — ready to add new models
* [x] Clean and reproducible outputs

---

MIT License — © Alex Just Rodriguez





