"""
Feature guard decorators for optional features.
"""
from functools import wraps
from typing import Callable, Any, Optional

from fastapi import HTTPException, status
from app.settings import Settings


def require_feature(feature_flag: str):
    """
    Decorator to guard endpoints that require a specific feature flag.
    
    Args:
        feature_flag: Name of the feature flag (e.g., "ENABLE_OCR")
        
    Example:
        @require_feature("ENABLE_OCR")
        async def ocr_endpoint(...):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Try to get settings from kwargs or args
            settings: Optional[Settings] = None
            
            # Check kwargs first
            if "settings" in kwargs:
                settings = kwargs["settings"]
            # Check if settings is in args (common pattern)
            else:
                for arg in args:
                    if isinstance(arg, Settings):
                        settings = arg
                        break
            
            # If not found, create new instance
            if settings is None:
                settings = Settings()
            
            # Check feature flag
            if not getattr(settings, feature_flag, False):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Feature '{feature_flag}' is not enabled"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def feature_guard(settings: Settings, feature_flag: str) -> None:
    """
    Guard function to check if a feature is enabled.
    
    Args:
        settings: Application settings
        feature_flag: Name of the feature flag
        
    Raises:
        HTTPException: If feature is not enabled
    """
    if not getattr(settings, feature_flag, False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feature '{feature_flag}' is not enabled"
        )

