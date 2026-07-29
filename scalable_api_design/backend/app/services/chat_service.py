"""Chat business logic. Orchestrates the chat flow."""

from app.core.logger import get_logger
from app.services.llm_service import call_llm

logger = get_logger(__name__)

SYSTEM_PROMPT = "You are a helpful assistant. Answer clearly and concisely."


async def handle_chat(message: str, tenant_id: str) -> str:
    """
    Process a chat message.

    Flow:
    1. (Future) Check cache for repeated question
    2. Call LLM
    3. (Future) Store response in cache
    4. Return response
    """
    try:
        logger.info(f"Chat service | tenant={tenant_id} | msg_len={len(message)}")

        # TODO: check cache first (Redis)
        # TODO: route simple questions to smaller model

        response = await call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_message=message,
        )

        # TODO: cache response for future hits

        return response

    except Exception as e:
        logger.exception(f"Chat service error | tenant={tenant_id}")
        raise