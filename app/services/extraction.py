import json
import logging
import re

from app.core.templates import RESUME_TEMPLATE, get_template_str
from app.services.llm import LLMService
from app.services.sliding_window import sliding_window_extract

logger = logging.getLogger(__name__)


def compact_text(text: str) -> str:
    """Reduce token count by stripping empty/trivial lines."""
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 1]
    return "\n".join(lines)


def extract_json_block(text: str) -> str | None:
    """Extract first JSON object from model output."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def enforce_schema(parsed: dict, template: dict) -> dict:
    """Ensure all template keys exist in parsed output."""
    for key, value in template.items():
        if key not in parsed:
            parsed[key] = value
    return parsed


def extract_resume(text: str, llm_service: LLMService) -> tuple[dict, int]:
    """Full extraction pipeline. Returns (result_dict, chunks_processed)."""
    cleaned = compact_text(text)
    template_str = get_template_str()

    raw_json, num_chunks = sliding_window_extract(cleaned, template_str, llm_service)

    json_block = extract_json_block(raw_json)
    if not json_block:
        logger.warning("Failed to extract JSON block from model output")
        return RESUME_TEMPLATE.copy(), num_chunks

    try:
        parsed = json.loads(json_block)
    except json.JSONDecodeError:
        logger.warning("JSON parsing failed on output: %s", raw_json[:200])
        return RESUME_TEMPLATE.copy(), num_chunks

    return enforce_schema(parsed, RESUME_TEMPLATE), num_chunks
