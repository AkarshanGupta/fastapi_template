"""
Reusable dependency injection patterns.
"""
from functools import lru_cache
from typing import Optional

from fastapi import Depends, Request
from app.settings import Settings


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached singleton).
    
    Returns:
        Settings instance
    """
    return Settings()


def get_request_settings(request: Request) -> Settings:
    """
    Get settings from request state (alternative pattern).
    
    Args:
        request: FastAPI request object
        
    Returns:
        Settings instance
    """
    if not hasattr(request.state, "settings"):
        request.state.settings = Settings()
    return request.state.settings


# Common dependency patterns
SettingsDep = Depends(get_settings)


