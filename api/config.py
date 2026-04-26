"""Application settings via pydantic-settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_port: int = 8000
    log_level: str = "INFO"

    database_url: str = Field(
        default="postgresql+asyncpg://npc:changeme@localhost:5432/npcompliance"
    )
    database_url_sync: str = Field(
        default="postgresql://npc:changeme@localhost:5432/npcompliance"
    )

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    propublica_api_key: str = ""
    irs_s3_bucket: str = "irs-form-990"
    ofac_sdn_url: str = "https://www.treasury.gov/ofac/downloads/sdn.xml"


@lru_cache
def get_settings() -> Settings:
    return Settings()
