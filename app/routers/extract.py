import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.dependencies import get_llm_service
from app.models import ExtractionResponse, ResumeExtraction
from app.services.extraction import extract_resume
from app.services.file_parser import extract_text_from_upload
from app.services.llm import LLMService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/parse")
async def parse_file(
    file: UploadFile = File(..., description="PDF or DOCX file"),
) -> dict:
    """Debug endpoint: extract and return raw text from an uploaded file."""
    text = await extract_text_from_upload(file)
    return {"filename": file.filename, "char_count": len(text), "text": text}


@router.post("/extract", response_model=ExtractionResponse)
async def extract_from_file(
    file: UploadFile = File(..., description="PDF or DOCX resume file"),
    llm_service: LLMService = Depends(get_llm_service),
) -> ExtractionResponse:
    """Upload a resume file (PDF or DOCX) and extract structured data."""
    text = await extract_text_from_upload(file)
    logger.info("Extracted %d chars from %s", len(text), file.filename)
    logger.info("Text preview: %s", text[:500])

    if not text.strip():
        raise HTTPException(status_code=422, detail="No text content found in file.")

    try:
        result, chunks = extract_resume(text, llm_service)
    except Exception:
        logger.exception("Extraction failed")
        return ExtractionResponse(success=False, error="Extraction failed. Please try again.")

    return ExtractionResponse(
        success=True,
        data=ResumeExtraction(**result),
        chunks_processed=chunks,
    )
