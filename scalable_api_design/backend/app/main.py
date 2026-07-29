"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import (
    AppError,
    app_error_handler,
    unhandled_error_handler,
)
from app.core.logger import get_logger
from app.api import routes

logger = get_logger(__name__)


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="Scalable Chat + File API with async job processing",
        docs_url="/docs",
        redoc_url=None,
    )

    # Register error handlers
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    # Register all routes
    app.include_router(routes.router)

    logger.info(f"App started | env={settings.app_env}")
    return app


app = create_app()
