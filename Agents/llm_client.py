"""
Centralized LLM client factory.
Reads LLM_PROVIDER from .env and returns the right ChatModel instance.

Usage:
    from llm_client import get_llm
    llm = get_llm()                    # uses LLM_PROVIDER from .env
    llm = get_llm(provider="openai")   # override provider
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_llm(provider: str = None, temperature: float = 0):
    provider = (provider or os.getenv("LLM_PROVIDER", "openai")).lower().strip()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider == "azure_openai":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            temperature=temperature,
        )

    if provider == "claude":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"),
            anthropic_api_key=os.getenv("CLAUDE_API_KEY"),
            temperature=temperature,
        )

    if provider in ("claude_merck", "corporate"):
        from langchain_anthropic import ChatAnthropic
        model = os.getenv("CORPORATE_MODEL", "claude-opus-4-6-v1")
        base = os.getenv("CORPORATE_BASE_URL")
        key = os.getenv("CORPORATE_API_KEY")
        return ChatAnthropic(
            model=model,
            api_key="unused",
            base_url=f"{base}/anthropic/{model}",
            default_headers={"X-Merck-APIKey": key},
            temperature=temperature,
        )

    raise ValueError(f"Unknown LLM_PROVIDER: '{provider}'. Use: openai, azure_openai, claude, claude_merck, corporate")


if __name__ == "__main__":
    llm = get_llm()
    print(f"Provider: {os.getenv('LLM_PROVIDER')}")
    response = llm.invoke("Say hello in one sentence.")
    print(f"Response: {response.content}")
