"""LLM client factory. Picks the right client based on LLM_PROVIDER env var."""

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


def call_model(system_prompt: str, user_message: str, max_tokens: int = 1024) -> tuple:
    """
    Call LLM using the provider set in .env (LLM_PROVIDER).

    Returns: (content, tokens_in, tokens_out)
    
    Supported providers: claude, openai, gemini
    """
    provider = settings.llm_provider

    if provider == "claude":
        return _call_claude(system_prompt, user_message, max_tokens)
    elif provider == "openai":
        return _call_openai(system_prompt, user_message, max_tokens)
    elif provider == "gemini":
        return _call_gemini(system_prompt, user_message, max_tokens)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider}. Use: claude, openai, gemini")


def _call_claude(system_prompt: str, user_message: str, max_tokens: int) -> tuple:
    """Anthropic client via Merck proxy."""
    from anthropic import Anthropic

    client = Anthropic(
        api_key="unused",
        base_url=f"{settings.llm_base_url}/anthropic/{settings.llm_model}",
        default_headers={"X-Merck-APIKey": settings.llm_api_key},
    )

    response = client.messages.create(
        model=settings.llm_model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    return (
        response.content[0].text,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )


def _call_openai(system_prompt: str, user_message: str, max_tokens: int) -> tuple:
    """OpenAI/Azure client via Merck proxy."""
    from openai import AzureOpenAI

    client = AzureOpenAI(
        api_key=settings.llm_api_key,
        base_url=f"{settings.llm_base_url}/openai",
        default_headers={"X-Merck-APIKey": settings.llm_api_key},
    )

    response = client.chat.completions.create(
        model=settings.llm_model,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return (
        response.choices[0].message.content,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )


def _call_gemini(system_prompt: str, user_message: str, max_tokens: int) -> tuple:
    """Google Gemini client via Merck proxy."""
    import httpx

    url = f"{settings.llm_base_url}/google/{settings.llm_model}/chat/completions"

    headers = {
        "X-Merck-APIKey": settings.llm_api_key,
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.llm_model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    }

    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()

    data = response.json()
    return (
        data["choices"][0]["message"]["content"],
        data.get("usage", {}).get("prompt_tokens", 0),
        data.get("usage", {}).get("completion_tokens", 0),
    )