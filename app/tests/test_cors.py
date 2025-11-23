"""
Tests for CORS functionality.
"""
import pytest
from fastapi.testclient import TestClient


def test_cors_headers_present(test_client: TestClient):
    """
    Test that OPTIONS request returns CORS headers.
    
    Args:
        test_client: Test client fixture
    """
    # Make OPTIONS request
    response = test_client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }
    )
    
    # Check that CORS headers are present
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers


def test_cors_preflight_request(test_client: TestClient):
    """
    Test CORS preflight request handling.
    
    Args:
        test_client: Test client fixture
    """
    response = test_client.options(
        "/api/v1/items",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        }
    )
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers.lower()


def test_cors_actual_request(test_client: TestClient):
    """
    Test CORS headers in actual GET request.
    
    Args:
        test_client: Test client fixture
    """
    response = test_client.get(
        "/api/v1/health",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    # CORS headers should be present in actual requests too
    assert "access-control-allow-origin" in response.headers


