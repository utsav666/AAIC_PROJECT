"""All API endpoints in one place."""

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional

from app.core.config import settings
from app.core.logger import get_logger
from app.services.chat_service import handle_chat
router = APIRouter()
logger = get_logger(__name__)


# ─── RESPONSE MODELS ───

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    environment: str


class ChatRequest(BaseModel):
    """Chat endpoint request."""
    message: str
    tenant_id: str


class ChatResponse(BaseModel):
    """Chat endpoint response."""
    response: str
    tenant_id: str


class UploadResponse(BaseModel):
    """File upload response."""
    file_id: str
    presigned_url: str
    tenant_id: str


class JobStatusResponse(BaseModel):
    """Job status response."""
    job_id: str
    status: str
    result: Optional[dict] = None


# ─── HEALTH ───

@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.

    Returns:
        HealthResponse: Service status, name, and environment
    """
    logger.debug("Health check called")
    return {
        "status": "healthy",
        "service": settings.app_name,
        "environment": settings.app_env,
    }


# ─── CHAT ───

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(req: ChatRequest):
    """
    Text chat endpoint.

    Send a message and get a response from the LLM.
    Uses cache first, falls back to model if needed.
    """
    try:
        logger.info(f"Chat request | tenant={req.tenant_id} | msg_len={len(req.message)}")

        # Call the chat service
        response = await handle_chat(message=req.message, tenant_id=req.tenant_id)
        return {
            "response": response,
            "tenant_id": req.tenant_id,
        }

    except Exception as e:
        logger.exception(f"Chat error | tenant={req.tenant_id}")
        raise


# ─── FILE UPLOAD ───

@router.post("/upload", response_model=UploadResponse, tags=["Upload"])
async def upload_file_endpoint(file: UploadFile = File(...), tenant_id: str = ""):
    """
    File upload endpoint. Returns presigned URL and file_id.

    Client should:
    1. Call this endpoint to get presigned URL and file_id
    2. Upload file directly to S3 using presigned URL
    3. Call POST /jobs with file_id to start processing
    """
    try:
        logger.info(f"Upload request | tenant={tenant_id} | file={file.filename}")

        # Placeholder: will integrate S3 adapter next
        return {
            "file_id": "temp-file-id",
            "presigned_url": "https://s3.example.com/presigned-url",
            "tenant_id": tenant_id,
        }

    except Exception as e:
        logger.exception(f"Upload error | tenant={tenant_id}")
        raise


# ─── JOB STATUS ───

@router.get("/jobs/{job_id}", response_model=JobStatusResponse, tags=["Jobs"])
async def get_job_status(job_id: str):
    """
    Get status of an async job.

    Poll this endpoint to check job progress.
    """
    try:
        logger.info(f"Job status request | job_id={job_id}")

        # Placeholder: will integrate DB adapter next
        return {
            "job_id": job_id,
            "status": "queued",
            "result": None,
        }

    except Exception as e:
        logger.exception(f"Job status error | job_id={job_id}")
        raise
