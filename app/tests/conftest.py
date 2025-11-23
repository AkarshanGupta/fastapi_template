"""
Pytest configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from typing import Generator

from app.main import create_app
from app.settings import Settings


@pytest.fixture
def test_settings() -> Settings:
    """
    Create test settings with feature flags disabled by default.
    
    Returns:
        Test settings instance
    """
    return Settings(
        ENVIRONMENT="test",
        DEBUG=True,
        ENABLE_DB_POSTGRES=False,
        ENABLE_DB_MONGO=False,
        ENABLE_OCR=False,
        ENABLE_STORAGE=False,
        CORS_ORIGINS=["http://localhost:3000"],
    )


@pytest.fixture
def test_client(test_settings: Settings) -> Generator[TestClient, None, None]:
    """
    Create test client with test settings.
    
    Args:
        test_settings: Test settings fixture
        
    Yields:
        TestClient instance
    """
    app = create_app(test_settings)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_client_with_ocr(test_settings: Settings) -> Generator[TestClient, None, None]:
    """
    Create test client with OCR enabled.
    
    Args:
        test_settings: Test settings fixture
        
    Yields:
        TestClient instance with OCR enabled
    """
    test_settings.ENABLE_OCR = True
    app = create_app(test_settings)
    with TestClient(app) as client:
        yield client


