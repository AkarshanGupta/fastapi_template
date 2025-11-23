"""
Tests for health check endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(test_client: TestClient):
    """
    Test that health endpoint returns status ok.
    
    Args:
        test_client: Test client fixture
    """
    response = test_client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert data["environment"] == "test"


def test_health_endpoint_structure(test_client: TestClient):
    """
    Test health endpoint response structure.
    
    Args:
        test_client: Test client fixture
    """
    response = test_client.get("/api/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all expected fields are present
    required_fields = ["status", "version", "environment"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

