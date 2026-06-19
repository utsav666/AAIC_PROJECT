"""Flexible LLM provider. Supports OpenAI, Azure OpenAI, Claude, Claude Merck.
Switch by setting LLM_PROVIDER in .env"""

import os
from config import LLM_PROVIDER


def _get_openai_client():
    from openai import OpenAI
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),  # None = default
    ), os.getenv("OPENAI_MODEL", "gpt-4o")


def _get_azure_client():
    from openai import AzureOpenAI
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    ), os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")


def _get_claude_client():
    from anthropic import Anthropic
    return Anthropic(
        api_key=os.getenv("CLAUDE_API_KEY"),
    ), os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")


def _get_claude_merck_client():
    from anthropic import Anthropic
    api_key = os.getenv("MERCK_API_KEY")
    base_url = os.getenv("MERCK_BASE_URL")
    model = os.getenv("MERCK_MODEL", "claude-opus-4-6-v1")
    client = Anthropic(
        api_key="unused",
        base_url=f"{base_url}/anthropic/{model}",
        default_headers={"X-Merck-APIKey": api_key},
    )
    return client, model


def chat(system_prompt: str, user_message: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """Send a message to the configured LLM and get a response string."""

    if LLM_PROVIDER in ("openai", "azure_openai"):
        # OpenAI-compatible API
        if LLM_PROVIDER == "openai":
            client, model = _get_openai_client()
        else:
            client, model = _get_azure_client()

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content

    elif LLM_PROVIDER in ("claude", "claude_merck"):
        # Anthropic API
        if LLM_PROVIDER == "claude":
            client, model = _get_claude_client()
        else:
            client, model = _get_claude_merck_client()

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}. Use: openai, azure_openai, claude, claude_merck")
