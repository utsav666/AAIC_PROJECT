"""Custom exceptions and global error handler."""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, status_code=400)


class RateLimitError(AppError):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, status_code=429)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Handle known application errors."""
    logger.warning(f"{exc.status_code} | {request.method} {request.url.path} | {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors. Log full trace, return safe message."""
    logger.exception(f"500 | {request.method} {request.url.path} | Unhandled error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
