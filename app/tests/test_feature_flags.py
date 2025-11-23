"""
Tests for feature flag functionality.
"""
import pytest
from fastapi.testclient import TestClient


def test_ocr_endpoint_disabled(test_client: TestClient):
    """
    Test that OCR endpoint returns 404 when feature is disabled.
    
    Args:
        test_client: Test client fixture (OCR disabled by default)
    """
    # Try to access OCR endpoint
    response = test_client.get("/api/v1/ocr/status")
    
    assert response.status_code == 404
    data = response.json()
    assert "not enabled" in data["detail"].lower()


def test_ocr_endpoint_enabled(test_client_with_ocr: TestClient):
    """
    Test that OCR endpoint is accessible when feature is enabled.
    
    Args:
        test_client_with_ocr: Test client fixture with OCR enabled
    """
    response = test_client_with_ocr.get("/api/v1/ocr/status")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["enabled"] is True
    assert "provider" in data
    assert "status" in data


def test_items_endpoint_always_available(test_client: TestClient):
    """
    Test that items endpoint is always available (no feature flag).
    
    Args:
        test_client: Test client fixture
    """
    response = test_client.get("/api/v1/items")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


