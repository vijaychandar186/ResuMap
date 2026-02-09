import json
import logging

from app.services.llm import LLMService

logger = logging.getLogger(__name__)


def clean_json_text(text: str) -> str:
    """Clean JSON text as per official NuExtract implementation."""
    text = text.strip()
    text = text.replace("\\#", "#").replace("\\&", "&")
    return text


def _build_prompt(template: str, text: str, current: str | None = None) -> str:
    """Build NuExtract prompt using the model's native format.

    NuExtract uses <|input|>...<|output|> markers directly,
    without ChatML wrapping.
    """
    prompt = f"<|input|>\n### Template:\n{template}\n"
    if current is not None:
        prompt += f"### Current:\n{current}\n"
    prompt += f"### Text:\n{text}\n\n<|output|>\n"
    return prompt


def _compute_prompt_budget(llm_service: LLMService, template_str: str, max_new_tokens: int) -> int:
    """Calculate how many tokens of document text can fit in one chunk."""
    overhead_prompt = _build_prompt(template_str, text="", current=template_str)
    overhead_tokens = llm_service.count_tokens(overhead_prompt)

    n_ctx = llm_service.settings.model_n_ctx
    budget = n_ctx - overhead_tokens - max_new_tokens

    logger.info(
        "Prompt budget: n_ctx=%d - overhead=%d - max_new=%d = %d tokens for text",
        n_ctx, overhead_tokens, max_new_tokens, budget,
    )
    return budget


def split_document_by_tokens(
    text: str,
    llm_service: LLMService,
    chunk_token_budget: int,
    overlap: int = 128,
) -> list[str]:
    """Split document text into overlapping chunks based on token count."""
    token_ids = llm_service.tokenize(text)
    total_tokens = len(token_ids)

    logger.info(
        "Document length: %d tokens, chunk budget: %d, overlap: %d",
        total_tokens, chunk_token_budget, overlap,
    )

    if total_tokens <= chunk_token_budget:
        return [text]

    chunks: list[str] = []
    stride = chunk_token_budget - overlap

    for start in range(0, total_tokens, stride):
        end = min(start + chunk_token_budget, total_tokens)
        chunk_ids = token_ids[start:end]
        chunk_text = llm_service.llm.detokenize(chunk_ids).decode("utf-8", errors="replace")
        chunks.append(chunk_text)

        if end >= total_tokens:
            break

    logger.info("Split into %d chunks", len(chunks))
    return chunks


def handle_broken_output(pred: str, prev: str) -> str:
    """Handle broken output exactly as per official NuExtract implementation."""
    try:
        if all(v in ["", []] for v in json.loads(pred).values()):
            pred = prev
    except Exception:
        pred = prev
    return pred


def sliding_window_extract(
    text: str,
    template_str: str,
    llm_service: LLMService,
) -> tuple[str, int]:
    """Process document through sliding window as per official NuExtract implementation.

    Each chunk is processed with the ### Current: field carrying forward the
    accumulated result from previous chunks. Returns (json_str, num_chunks).
    """
    settings = llm_service.settings
    budget = _compute_prompt_budget(llm_service, template_str, settings.max_new_tokens)
    chunks = split_document_by_tokens(text, llm_service, budget, settings.sliding_window_overlap)

    prev = template_str

    for i, chunk in enumerate(chunks):
        logger.info("Processing chunk %d/%d ...", i + 1, len(chunks))

        # Skip ### Current: on the first chunk so the model doesn't echo the empty template
        current = clean_json_text(prev) if i > 0 else None
        prompt = _build_prompt(template_str, chunk, current=current)

        raw_output = llm_service.generate(prompt, max_tokens=settings.max_new_tokens)
        pred = clean_json_text(raw_output)
        logger.info("Raw model output for chunk %d: %s", i + 1, pred[:2000])

        pred = handle_broken_output(pred, prev)
        prev = pred

    return prev, len(chunks)
