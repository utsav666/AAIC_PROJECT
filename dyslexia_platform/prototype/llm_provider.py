"""
LLM Abstraction Layer
=====================
Supports: OpenAI, Azure OpenAI, Claude (direct), Claude (Merck proxy)
Switch providers by changing LLM_PROVIDER in .env
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMProvider(ABC):
    """Base class for all LLM providers."""

    @abstractmethod
    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        """Send a message and get a response string."""
        pass

    @abstractmethod
    def chat_json(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> dict:
        """Send a message and get a parsed JSON response."""
        pass


class OpenAIProvider(LLMProvider):
    """Standard OpenAI API (also works with any OpenAI-compatible endpoint)."""

    def __init__(self):
        from openai import OpenAI

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),  # None = default
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content

    def chat_json(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt + "\nRespond ONLY with valid JSON."},
                {"role": "user", "content": user_message},
            ],
        )
        return json.loads(response.choices[0].message.content)


class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI Service."""

    def __init__(self):
        from openai import AzureOpenAI

        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        )
        self.model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content

    def chat_json(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> dict:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt + "\nRespond ONLY with valid JSON."},
                {"role": "user", "content": user_message},
            ],
        )
        return json.loads(response.choices[0].message.content)


class ClaudeProvider(LLMProvider):
    """Direct Anthropic Claude API."""

    def __init__(self):
        from anthropic import Anthropic

        self.client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def chat_json(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> dict:
        raw = self.chat(
            system_prompt + "\nRespond ONLY with valid JSON. No markdown, no explanation.",
            user_message,
            temperature,
        )
        # Strip markdown code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[1:])
        if cleaned.endswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[:-1])
        return json.loads(cleaned.strip())


class ClaudeMerckProvider(LLMProvider):
    """Claude via Merck enterprise proxy."""

    def __init__(self):
        from anthropic import Anthropic

        api_key = os.getenv("MERCK_API_KEY")
        base_url = os.getenv("MERCK_BASE_URL")
        self.model = os.getenv("MERCK_MODEL", "claude-opus-4-6-v1")

        self.client = Anthropic(
            api_key="unused",
            base_url=f"{base_url}/anthropic/{self.model}",
            default_headers={"X-Merck-APIKey": api_key},
        )

    def chat(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def chat_json(self, system_prompt: str, user_message: str, temperature: float = 0.3) -> dict:
        raw = self.chat(
            system_prompt + "\nRespond ONLY with valid JSON. No markdown, no explanation.",
            user_message,
            temperature,
        )
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[1:])
        if cleaned.endswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[:-1])
        return json.loads(cleaned.strip())


# =============================================================================
# FACTORY
# =============================================================================

_PROVIDERS = {
    "openai": OpenAIProvider,
    "azure_openai": AzureOpenAIProvider,
    "claude": ClaudeProvider,
    "claude_merck": ClaudeMerckProvider,
}


def get_llm(provider: Optional[str] = None) -> LLMProvider:
    """
    Get an LLM provider instance.
    Uses LLM_PROVIDER env var if provider arg not given.
    """
    provider_name = provider or os.getenv("LLM_PROVIDER", "openai")
    if provider_name not in _PROVIDERS:
        raise ValueError(
            f"Unknown provider '{provider_name}'. Choose from: {list(_PROVIDERS.keys())}"
        )
    return _PROVIDERS[provider_name]()
