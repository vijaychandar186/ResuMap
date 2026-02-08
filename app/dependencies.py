from fastapi import Request

from app.services.llm import LLMService


def get_llm_service(request: Request) -> LLMService:
    """Retrieve the LLM service singleton from app state."""
    return request.app.state.llm_service
