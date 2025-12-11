"""
Tests for health check endpoints
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_health_check(client: TestClient):
    """Test basic health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "healthy"
    assert "service" in data
    assert data["service"] == "OPAL Unified System"


@pytest.mark.unit
def test_root_endpoint(client: TestClient):
    """Test root endpoint returns API info"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "message" in data or "app_name" in data
    # Should return some info about the API


@pytest.mark.unit
def test_api_docs_available(client: TestClient):
    """Test that API documentation is accessible"""
    response = client.get("/docs")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.unit
def test_openapi_schema(client: TestClient):
    """Test OpenAPI schema is available"""
    response = client.get("/openapi.json")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data

