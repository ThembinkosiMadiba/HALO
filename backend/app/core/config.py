"""Application settings.

Read from environment variables (prefix HALO_) and the repository .env file.

Rules:
- Secrets are SecretStr, so they do not appear in repr(), str() or model dumps.
- The API binds to a loopback address only.
- No application code uses the database owner account (threat T19). The restricted
  halo_app account arrives with the first migration (milestone M3).
"""
from functools import lru_cache
from ipaddress import ip_address
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="HALO_",
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # "production" is the safe default: API documentation is hidden.
    environment: Literal["development", "test", "production"] = "production"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    api_host: str = "127.0.0.1"
    api_port: int = Field(default=8000, ge=1024, le=65535)

    # Application database account. Not used until milestone M3.
    db_host: str = "127.0.0.1"
    db_port: int = Field(default=5432, ge=1, le=65535)
    db_name: str = "halo"
    db_user: str | None = None
    db_password: SecretStr | None = None

    @field_validator("api_host")
    @classmethod
    def api_host_must_be_loopback(cls, value: str) -> str:
        if value == "localhost":
            return value
        try:
            is_loopback = ip_address(value).is_loopback
        except ValueError:
            is_loopback = False
        if not is_loopback:
            raise ValueError("api_host must be a loopback address (127.0.0.1, ::1 or localhost)")
        return value

    @property
    def docs_enabled(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
