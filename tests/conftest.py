"""Pytest configuration and fixtures for the activities API tests."""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Arrange: Create a test client for the FastAPI app.
    
    This fixture provides a TestClient instance that can be used to make
    requests to the application endpoints during testing.
    """
    return TestClient(app)
