from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_NAME: str = "BillShield UK API"
    APP_ENV: str = "development"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./billshield_dev.db"

    FRONTEND_ORIGIN: str = "http://localhost:5173"
    CORS_ALLOW_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_MB: int = 10

    MOCK_MODE: bool = True
    ENABLE_EXTERNAL_OCR: bool = False
    ENABLE_EXTERNAL_AI: bool = False
    ENABLE_EXTERNAL_OFGEM: bool = False
    ENABLE_EXTERNAL_COUNCIL_LOOKUP: bool = False
    ENABLE_EXTERNAL_MAPS: bool = False

    LOG_LEVEL: str = "INFO"

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_UPLOAD_MB * 1024 * 1024

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.CORS_ALLOW_ORIGINS.split(",") if o.strip()]

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


settings = Settings()
