"""
Application configuration using Pydantic Settings.
Loads from environment variables with sensible defaults.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "ShieldAgent"
    app_version: str = "1.0.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = Field(default=True)
    api_prefix: str = "/api"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "shieldagent"
    postgres_password: str = "shieldagent_dev"
    postgres_db: str = "shieldagent"

    @computed_field
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def database_url_sync(self) -> str:
        """Construct sync PostgreSQL connection URL for Alembic."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    @computed_field
    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL."""
        if self.redis_password:
            return (
                f"redis://:{self.redis_password}@{self.redis_host}:"
                f"{self.redis_port}/{self.redis_db}"
            )
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # Security
    secret_key: str = Field(
        default="CHANGE_ME_IN_PRODUCTION_super_secret_key_12345",
        description="Secret key for JWT signing",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    # File Upload
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 50
    allowed_extensions: list[str] = Field(
        default=["pdf", "csv", "json", "txt", "md"],
        description="Allowed file extensions for upload",
    )

    # AI/LLM (Gemini)
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key",
    )
    gemini_model: str = "gemini-1.5-flash"

    # Celery
    celery_broker_url: str = ""
    celery_result_backend: str = ""

    @computed_field
    @property
    def celery_broker(self) -> str:
        """Get Celery broker URL (Redis)."""
        return self.celery_broker_url or self.redis_url

    @computed_field
    @property
    def celery_backend(self) -> str:
        """Get Celery result backend URL (Redis)."""
        return self.celery_result_backend or self.redis_url


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid re-reading environment on every call.
    """
    return Settings()


# Global settings instance
settings = get_settings()
