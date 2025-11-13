"""
Application configuration management using Pydantic Settings.
Supports multiple environments: dev, test, prod
"""

import os
from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Automatically loads the correct .env file based on ENVIRONMENT variable.
    """

    # Application
    APP_NAME: str = "Admin Portal API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: Literal["dev", "test", "prod"] = "dev"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "admin_portal"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 3600

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text

    # Security (for future use)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env.dev",  # Default to dev environment
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """Construct MySQL connection URL"""
        return f"mysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reading .env file multiple times.

    The correct .env file is loaded based on the ENVIRONMENT variable:
    - ENVIRONMENT=dev → loads .env.dev
    - ENVIRONMENT=test → loads .env.test
    - ENVIRONMENT=prod → loads .env.prod

    Set ENVIRONMENT variable before starting the application:
        export ENVIRONMENT=prod
        python -m uvicorn app.main:app
    """
    # Get environment from OS environment variable
    env = os.getenv("ENVIRONMENT", "dev")

    # Map environment to .env file
    env_file_map = {
        "dev": ".env.dev",
        "test": ".env.test",
        "prod": ".env.prod"
    }

    # Update model_config with correct env file
    Settings.model_config["env_file"] = env_file_map.get(env, ".env.dev")

    return Settings()


# Convenience variable
settings = get_settings()
