# src/gexai/pipeline.py

from .download import maybe_download_youtube
from .audio import convert_to_wav
from .transcription import whisper_transcribe, export_json, export_txt, export_srt
from .diarization import diarize_audio
from .config import settings
from rich import print
from pathlib import Path

def transcribe_pipeline(input_path: str, diarize: bool = False):
    # 1. Detecta si es URL o path local
    is_url = input_path.startswith("http")
    base_dir = settings.data_dir / "transcripciones"

    # 2. Descarga si es YouTube
    if is_url:
        print(f"[blue]🔗 Descargando desde YouTube:[/] {input_path}")
        audio_path = maybe_download_youtube(input_path, base_dir)
    else:
        audio_path = Path(input_path)

    # 3. Normaliza a WAV
    wav_path = convert_to_wav(audio_path, base_dir)
    out_dir = wav_path.parent

    # 4. Ejecuta Whisper
    print("[cyan]🔊 Transcribiendo audio con Whisper...[/]")
    segments = whisper_transcribe(wav_path)

    # 5. Guarda salidas básicas
    export_json(segments, out_dir / "whisper.json")
    export_srt(segments, out_dir / "subtitulos.srt")
    export_txt(segments, out_dir / "texto_plano.txt")

    print(f"[green]✔ Transcripción guardada en:[/] {out_dir}")

    # 6. Diarización opcional
    if diarize:
        print("[magenta]🧠 Ejecutando diarización por hablantes...[/]")
        diarized_segments = diarize_audio(wav_path, segments)

        export_json(diarized_segments, out_dir / "whisper_diarized.json")
        export_srt(diarized_segments, out_dir / "subtitulos_diarizados.srt")
        export_txt(diarized_segments, out_dir / "texto_diarizado.txt")

        print(f"[green]✔ Diarización guardada en:[/] {out_dir}")

    return out_dir
