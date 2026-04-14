from typing import Annotated
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # === БАЗА ДАННЫХ ===
    DATABASE_URL: Annotated[PostgresDsn, "Async SQLAlchemy DSN"]
    POSTGRES_USER: Annotated[str, "PostgreSQL user"]
    POSTGRES_PASSWORD: Annotated[str, "PostgreSQL password"]
    POSTGRES_DB: Annotated[str, "PostgreSQL database name"]

    DB_DRIVER: str = "postgresql"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_POOL_TIMEOUT: int = 30
    DB_CONNECT_TIMEOUT: int = 10
    DB_COMMAND_TIMEOUT: int = 30
    DB_STATEMENT_TIMEOUT: int = 30000
    DB_SSL_MODE: str = "prefer"

    # === БЕЗОПАСНОСТЬ ===
    APP_SECRET_KEY: str = ""
    APP_DEBUG: bool = True
    APP_ENVIRONMENT: str = "development"

    # === ПРИЛОЖЕНИЕ ===
    APP_NAME: str = "JSONPlaceholder_httpx"
    APP_TIMEZONE: str = "UTC"

    # === ВНЕШНИЕ API ===
    JSONPLACEHOLDER_API_URL: str = "https://jsonplaceholder.typicode.com"
    JSONPLACEHOLDER_TIMEOUT: int = 10

    OPENWEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    OPENWEATHER_API_KEY: str = ""
    OPENWEATHER_TIMEOUT: int = 10

    # === CORS ===
    ALLOWED_ORIGINS: str = "http://localhost:8000"

    # === pgadmin ===
    PGADMIN_DEFAULT_EMAIL: str = "admin@admin.com"
    PGADMIN_DEFAULT_PASSWORD: str = "admin"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )


settings = Settings()
