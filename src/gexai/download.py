# src/gexai/download.py

from yt_dlp import YoutubeDL
from pathlib import Path
import uuid

def maybe_download_youtube(url: str, output_dir: Path) -> Path:
    """Descarga el audio de un vídeo de YouTube y lo convierte a formato WAV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_name = f"{uuid.uuid4()}.%(ext)s"
    output_path = output_dir / temp_name

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Encuentra el archivo generado (.wav)
    downloaded = next(output_dir.glob("*.wav"))
    return downloaded

