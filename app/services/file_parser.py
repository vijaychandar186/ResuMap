import io
import logging

import fitz  # pymupdf
from docx import Document
from fastapi import HTTPException, UploadFile

logger = logging.getLogger(__name__)

_ALLOWED_CONTENT_TYPES = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}


async def extract_text_from_upload(file: UploadFile) -> str:
    """Read uploaded file bytes and extract plain text."""
    content_type = file.content_type or ""
    filename = file.filename or ""

    file_type = _ALLOWED_CONTENT_TYPES.get(content_type)
    if file_type is None:
        if filename.lower().endswith(".pdf"):
            file_type = "pdf"
        elif filename.lower().endswith(".docx"):
            file_type = "docx"
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {content_type}. Upload a PDF or DOCX file.",
            )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if file_type == "pdf":
        return _extract_from_pdf(file_bytes)
    return _extract_from_docx(file_bytes)


def _extract_from_pdf(data: bytes) -> str:
    """Extract text from PDF bytes using PyMuPDF."""
    try:
        doc = fitz.open(stream=data, filetype="pdf")
        pages = [page.get_text() for page in doc]
        doc.close()
        return "\n".join(pages)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to parse PDF: {exc}") from exc


def _extract_from_docx(data: bytes) -> str:
    """Extract text from DOCX bytes using python-docx."""
    try:
        doc = Document(io.BytesIO(data))
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to parse DOCX: {exc}") from exc
