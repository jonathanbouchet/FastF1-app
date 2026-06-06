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


def test_get_race_names():
    """Test getting race names for a valid year."""
    response = client.get("/years/2021/races")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2021
    assert isinstance(data["races"], list)
    assert len(data["races"]) > 0
    assert "Bahrain Grand Prix" in data["races"]


def test_get_race_names_invalid_year():
    """Test getting race names for an invalid year."""
    response = client.get("/years/1900/races")
    assert response.status_code == 404


def test_get_race_schedule():
    """Test getting schedule for a specific race."""
    response = client.get("/years/2021/races/Bahrain%20Grand%20Prix/schedule")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2021
    assert data["race_name"] == "Bahrain Grand Prix"
    assert isinstance(data["sessions"], list)
    assert len(data["sessions"]) > 0
    # Check session structure
    session = data["sessions"][0]
    assert "name" in session
    assert "date_utc" in session


def test_get_race_schedule_invalid_race():
    """Test getting schedule for a non-existent race."""
    response = client.get("/years/2021/races/Fake%20Grand%20Prix/schedule")
    assert response.status_code == 404
