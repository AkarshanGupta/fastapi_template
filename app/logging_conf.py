"""
Production-safe logging configuration.
"""
import logging
import sys
from typing import Optional

from app.settings import Settings


def setup_logging(settings: Optional[Settings] = None) -> None:
    """
    Configure logging for the application.
    
    Args:
        settings: Application settings. If None, creates a new instance.
    """
    if settings is None:
        settings = Settings()
    
    # Determine log level
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    
    # In production, use JSON logging format (optional enhancement)
    if settings.is_production:
        # You can configure JSON logging here if needed
        # For now, we use structured format above
        pass
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {settings.LOG_LEVEL}")

