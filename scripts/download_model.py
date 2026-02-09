"""Download the NuExtract GGUF model to the local models/ directory.

Usage:
    python -m scripts.download_model
"""

import sys
from pathlib import Path

from huggingface_hub import hf_hub_download

# Add project root to path so we can import app.config
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from app.config import Settings


def main() -> None:
    settings = Settings()
    settings.model_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {settings.model_repo_id}/{settings.model_filename} ...")
    downloaded_path = hf_hub_download(
        repo_id=settings.model_repo_id,
        filename=settings.model_filename,
        local_dir=settings.model_dir,
    )
    print(f"Model saved to {downloaded_path}")

    expected = settings.model_path
    if expected.exists():
        print(f"Verified: {expected} ({expected.stat().st_size / 1024 / 1024:.1f} MB)")
    else:
        print(f"Warning: expected file at {expected} but not found. Check model_dir setting.")


if __name__ == "__main__":
    main()
