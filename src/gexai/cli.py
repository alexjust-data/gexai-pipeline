import typer
from rich import print
from .pipeline import transcribe_pipeline, diarize_pipeline
from .config import settings

import typer
from .pipeline import transcribe_pipeline, diarize_pipeline

app = typer.Typer()

@app.command()
def transcribe(input_path: str):
    """Transcribe audio/video from file or YouTube URL."""
    result = transcribe_pipeline(input_path)
    typer.echo(result)

@app.command()
def diarize(input_path: str):
    """Apply speaker diarization to file or YouTube URL."""
    result = diarize_pipeline(input_path)
    typer.echo(result)

