"""
Application settings with feature flags using Pydantic BaseSettings.
All optional features are controlled via environment variables.
"""
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings with feature flags."""
    
    # Basic app settings
    APP_NAME: str = "FastAPI Template"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development, staging, production
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Feature flags - all optional features
    ENABLE_DB_POSTGRES: bool = False
    ENABLE_DB_MONGO: bool = False
    ENABLE_OCR: bool = False
    ENABLE_STORAGE: bool = False
    
    # PostgreSQL settings (only used if ENABLE_DB_POSTGRES=True)
    POSTGRES_HOST: Optional[str] = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = "fastapi_db"
    POSTGRES_URL: Optional[str] = None
    
    # MongoDB settings (only used if ENABLE_DB_MONGO=True)
    MONGO_HOST: Optional[str] = "localhost"
    MONGO_PORT: int = 27017
    MONGO_USER: Optional[str] = None
    MONGO_PASSWORD: Optional[str] = None
    MONGO_DB: Optional[str] = "fastapi_db"
    MONGO_URL: Optional[str] = None
    
    # OCR settings (only used if ENABLE_OCR=True)
    OCR_PROVIDER: Optional[str] = "tesseract"  # tesseract, google_vision, aws_textract
    OCR_API_KEY: Optional[str] = None
    
    # Storage settings (only used if ENABLE_STORAGE=True)
    STORAGE_TYPE: Optional[str] = "local"  # local, s3, gcs
    STORAGE_PATH: Optional[str] = "./storage"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    AWS_REGION: Optional[str] = "us-east-1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v
    
    @validator("DEBUG", always=True)
    def validate_debug_in_production(cls, v, values):
        """Ensure DEBUG is False in production."""
        if values.get("ENVIRONMENT") == "production" and v is True:
            raise ValueError("DEBUG must be False when ENVIRONMENT=production")
        return v
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


