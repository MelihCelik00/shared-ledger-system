from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str
    
    # Application
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "INFO"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:8000"]
    
    # API
    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "Shared Ledger System"
    API_DESCRIPTION: str = "A scalable and reusable shared ledger system"
    API_VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.
    
    Returns:
        Settings object with configuration values
    """
    return Settings() 