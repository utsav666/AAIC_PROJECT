"""Structured logger for the application."""

import logging
import sys

from app.core.config import settings


def get_logger(name: str) -> logging.Logger:
    """Create a logger with consistent format."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        level = logging.DEBUG if settings.debug else logging.INFO

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        handler.setLevel(level)

        logger.setLevel(level)
        logger.addHandler(handler)

    return logger
