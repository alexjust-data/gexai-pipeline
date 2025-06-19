from __future__ import annotations

from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    """
    Global settings loaded from environment variables or .env file.
    """

    hf_token: str = Field(..., env="HF_TOKEN", description="Hugging Face token")
    data_dir: Path = Field(default=Path("data"), env="GEXAI_DATA_DIR")
    whisper_model: str = Field(default="small", env="WHISPER_MODEL")

    class Config:
        env_file = ".env"
        extra = "ignore"

# Singleton settings instance
settings = Settings()
