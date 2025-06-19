# src/gexai/audio.py
"""
Conversión a WAV (16 kHz · mono · 16-bit PCM) con pydub.
Necesitas ffmpeg instalado y visible en el PATH.
"""

from pathlib import Path
from pydub import AudioSegment


def convert_to_wav(input_path: Path, output_dir: Path, overwrite: bool = False) -> Path:
    """
    Convierte cualquier archivo de audio/vídeo a WAV 16 kHz mono.

    Args:
        input_path: archivo fuente (mp3, mp4, m4a, etc.).
        output_dir: carpeta donde guardar el WAV resultante.
        overwrite: si False y el WAV ya existe, lo devuelve sin regenerar.

    Returns:
        Ruta al archivo WAV generado.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    wav_path = output_dir / f"{input_path.stem}.wav"

    if wav_path.exists() and not overwrite:
        return wav_path

    audio = AudioSegment.from_file(input_path)
    audio = (
        audio.set_frame_rate(16000)
        .set_channels(1)
        .set_sample_width(2)  # 16-bit
    )
    audio.export(wav_path, format="wav")
    return wav_path

