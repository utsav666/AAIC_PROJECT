"""Provider-agnostic LLM service. Works with any OpenAI-compatible API."""

import httpx

from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import AppError
from app.services.llm_client import call_model

logger = get_logger(__name__)

TIMEOUT = 60.0
MAX_RETRIES = 2


async def call_llm(system_prompt: str, user_message: str, max_tokens: int = 1024) -> str:
    """Call LLM with retry and error handling."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"LLM call | provider={settings.llm_provider} | model={settings.llm_model} | attempt={attempt}")

            content, tokens_in, tokens_out = call_model(system_prompt, user_message, max_tokens)

            logger.info(f"LLM success | tokens_in={tokens_in} | tokens_out={tokens_out}")
            return content

        except Exception as e:
            logger.error(f"LLM error | attempt={attempt} | error={str(e)}")
            if attempt == MAX_RETRIES:
                raise AppError(f"LLM service error: {str(e)}", status_code=502)