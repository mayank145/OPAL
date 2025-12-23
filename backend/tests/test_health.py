"""
Basic health check tests for the OPAL FATS API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data or "database" in data  # Check for expected fields


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "OPAL" in data["message"]


def test_docs_endpoint():
    """Test that API docs are accessible"""
    response = client.get("/docs")
    assert response.status_code == 200

