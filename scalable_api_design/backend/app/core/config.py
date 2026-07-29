"""Application configuration. Loads from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All app settings. Override via .env or environment variables."""

    # App
    app_name: str = "scalable-api"
    app_env: str = "dev"  # dev | staging | prod
    debug: bool = False

    # AWS
    aws_region: str = "us-east-1"
    s3_bucket: str = ""
    sqs_queue_url: str = ""
    llm_provider: str = "claude"  # claude | openai | gemini
    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_model: str = ""

    # Database
    database_url: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379"

    # LLM
    # llm_provider: str = "bedrock"  # bedrock | openai
    # llm_model: str = "anthropic.claude-sonnet-4-20250514-v1:0"

    # Rate limiting
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Single instance used across the app
settings = Settings()
