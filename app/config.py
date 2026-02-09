from pathlib import Path

from pydantic_settings import BaseSettings

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Model
    model_repo_id: str = "tensorblock/NuExtract-tiny-v1.5-GGUF"
    model_filename: str = "NuExtract-tiny-v1.5-Q3_K_M.gguf"
    model_dir: Path = _PROJECT_ROOT / "models"

    # LLM
    model_n_ctx: int = 8192
    model_n_threads: int = 8
    model_n_batch: int = 512

    # Inference
    max_new_tokens: int = 2048
    temperature: float = 0.0
    stop_tokens: list[str] = ["</s>", "<|im_end|>", "<|end-output|>"]

    # Sliding window
    sliding_window_overlap: int = 128

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["*"]

    # File upload
    max_upload_size_mb: int = 10

    model_config = {"env_prefix": "RESUMAP_"}

    @property
    def model_path(self) -> Path:
        return self.model_dir / self.model_filename
