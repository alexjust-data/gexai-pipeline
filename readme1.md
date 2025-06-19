# 📚 Blueprint de la aplicación *GexAI*

> Estructura inicial — pensada para crecer con nuevos algoritmos de IA y funcionar **tanto en consola como en Jupyter**.
>
> Todo el código y comandos de ejemplo están en **español** para coincidir con tu flujo de trabajo.

---

## 1. Árbol de directorios propuesto

```text
gexai/
├─ pyproject.toml          # Metadata y dependencias (Poetry / PEP‑621)
├─ README.md               # Instrucciones de uso rápido
├─ .env.example            # Variables sensibles (se copia a .env)
├─ notebooks/              # Cuadernos Jupyter exploratorios
│  ├─ 00_exploratorio.ipynb
│  └─ 01_pipeline_demo.ipynb
├─ src/
│  └─ gexai/
│     ├─ __init__.py
│     ├─ cli.py            # Entrada Typer → consola
│     ├─ config.py         # Pydantic BaseSettings
│     ├─ download.py       # YouTube y descargas generales
│     ├─ audio.py          # Conversión, cortes, silencios
│     ├─ diarization.py    # Lógica pyannote
│     ├─ transcription.py  # Lógica Whisper
│     ├─ pipeline.py       # Orquestador alto nivel
│     └─ utils.py          # Helpers comunes
└─ tests/
   └─ test_transcription.py
```

### ¿Por qué así?

* **`src/` layout** evita conflictos de imports cuando instalas en editable (`pip install -e .`).
* **Typer** da un CLI elegante y autocompletado.
* **Pydantic** centraliza configuración (tokens, paths) y puede preguntar al usuario si algo falta.
* **Notebooks** importan directamente `from gexai import ...`, garantizando que lo que pruebes en Jupyter coincide con la librería instalada.

---

## 2. `pyproject.toml` limpio y funcional (solo Poetry)

```toml
[tool.poetry]
name = "gexai"
version = "0.1.0"
description = "Pipeline for transcription, speaker diarization, and future AI tools"
authors = [ "Alex Just Rodriguez <alexjustdata@gmail.com>" ]
packages = [
  { include = "gexai", from = "src" }
]

[tool.poetry.dependencies]
python = "^3.10"
typer = { version = "^0.12", extras = ["all"] }
pydantic = "^2.7"
pydantic-settings = "^2.2"
rich = "^13.7"
tqdm = "^4.66"
openai-whisper = { git = "https://github.com/openai/whisper.git" }
pyannote-audio = "^3.3"
yt-dlp = "^2025.3"
pydub = "^0.25"
torchaudio = "2.1.0"
torch = "2.1.0"

[tool.poetry.scripts]
gexai = "gexai.cli:app"

[tool.poetry.group.dev.dependencies]
pytest = "^8.2"
black = "^24.3"
isort = "^5.13"
```

---

## 3. Configuración con Pydantic — `config.py`

```python
from __future__ import annotations
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    """Ajustes globales leídos de `.env`, variables de entorno o argumentos."""

    hf_token: str = Field(..., env="HF_TOKEN", description="Token de Hugging Face")
    data_dir: Path = Field(Path("data"), env="GEXAI_DATA_DIR")
    whisper_model: str = Field("small", env="WHISPER_MODEL")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()  # instancia única reutilizable
```

...

---

## 4. Mejoras a `pipeline.py`

El módulo `transcribe_pipeline` debe:

1. Detectar si la entrada es una URL de YouTube (`https://...`) o un archivo local (`.mp3`, `.mp4`, `.wav`, etc.).
2. Si es un enlace, descargar automáticamente el audio con `yt-dlp` y guardar en una carpeta temporal.
3. Convertir cualquier archivo de entrada a `.wav` si es necesario.
4. Ejecutar Whisper sobre el archivo `.wav` y:

   * Guardar la transcripción en `.json` (estructura completa Whisper),
   * Exportar los subtítulos `.srt`,
   * Crear un archivo `.txt` limpio solo con texto plano.
5. Mostrar mensajes claros y progresivos con `rich.print()` o `typer.echo()`:

   * Desde la detección de tipo de entrada,
   * Hasta cada paso de procesamiento,
   * Terminando con los mensajes de archivos guardados.
6. Guardar todo en una subcarpeta dentro de `data/`, nombrada con timestamp o nombre del vídeo, por ejemplo:

   ```
   data/
   ├─ transcripciones/
   │   ├─ youtube_sw3N0leUULg/
   │   │   ├─ audio.wav
   │   │   ├─ whisper.json
   │   │   ├─ subtitulos.srt
   │   │   └─ texto_plano.txt
   ```
7. Si se indica `diarize=True`, lanzar también el pipeline de diarización y guardar:

   * Transcripción etiquetada por hablante (`.json`),
   * Texto plano con nombres (por ejemplo: `SPEAKER 1: ...`),
   * Nuevos subtítulos por hablante (`.srt`).
8. Mostrar siempre la ruta **final** de cada archivo generado:

   ```
   [bold green]✔ Guardado en: data/transcripciones/youtube_sw3N0leUULg/whisper.json[/]
   [bold green]✔ Guardado en: data/transcripciones/youtube_sw3N0leUULg/subtitulos.srt[/]
   ```
