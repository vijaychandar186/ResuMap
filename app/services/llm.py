import logging

from llama_cpp import Llama

from app.config import Settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._llm: Llama | None = None

    def load(self) -> None:
        """Load model from local disk. Run scripts/download_model.py first."""
        model_path = self.settings.model_path
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Run 'python -m scripts.download_model' to download it."
            )

        logger.info("Loading model from %s with n_ctx=%d ...", model_path, self.settings.model_n_ctx)
        self._llm = Llama(
            model_path=str(model_path),
            n_ctx=self.settings.model_n_ctx,
            n_threads=self.settings.model_n_threads,
            n_batch=self.settings.model_n_batch,
            verbose=False,
        )
        logger.info("Model loaded successfully.")

    @property
    def llm(self) -> Llama:
        if self._llm is None:
            raise RuntimeError("LLM not loaded. Call load() first.")
        return self._llm

    def tokenize(self, text: str) -> list[int]:
        """Tokenize text using llama-cpp's built-in tokenizer."""
        return self.llm.tokenize(text.encode("utf-8"))

    def count_tokens(self, text: str) -> int:
        return len(self.tokenize(text))

    def generate(self, prompt: str, max_tokens: int | None = None) -> str:
        """Run completion and return raw text output."""
        result = self.llm(
            prompt,
            max_tokens=max_tokens or self.settings.max_new_tokens,
            temperature=self.settings.temperature,
            stop=self.settings.stop_tokens,
        )
        return result["choices"][0]["text"]
