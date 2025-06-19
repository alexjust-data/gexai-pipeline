from pathlib import Path
from pyannote.audio import Pipeline


def diarize_audio(wav_path: Path, output_dir: Path, hf_token: str):
    """
    Runs speaker diarization on a WAV file using pyannote-audio.

    Args:
        wav_path: Path to the WAV file
        output_dir: Directory to save results
        hf_token: Hugging Face API token
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)

    diarization = pipeline(wav_path)
    rttm_path = output_dir / f"{wav_path.stem}.rttm"
    with open(rttm_path, "w") as f:
        diarization.write_rttm(f)
