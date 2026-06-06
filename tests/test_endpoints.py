from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_year_availability_valid_year():
    """Test year availability for a valid F1 year."""
    response = client.get("/years/2021/available")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2021
    assert data["has_data"] is True


def test_year_availability_invalid_year():
    """Test year availability for an invalid year."""
    response = client.get("/years/1950/available")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 1950
    assert isinstance(data["has_data"], bool)
