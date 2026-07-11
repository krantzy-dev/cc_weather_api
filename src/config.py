from enum import StrEnum
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="secret/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: Environment = Environment.DEVELOPMENT

    # Application server
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    reload: bool = True  # Only use in development mode

    # Logging
    log_level: LogLevel | None = None

    # Database (split so each part can be injected separately in K8s)
    postgres_user: str
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def effective_log_level(self) -> str:
        """Return the configured log level, or a sensible default per environment."""
        if self.log_level is not None:
            return self.log_level.upper()
        return "DEBUG" if self.environment is Environment.DEVELOPMENT else "INFO"

    @property
    def is_production(self) -> bool:
        return self.environment is Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance, loaded once per process."""
    return Settings()


settings = get_settings()
