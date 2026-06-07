from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from src.app import app, get_cache
from src.cache import CacheService


def get_mock_cache():
    """Create a mock cache service that doesn't store anything (cache misses)."""
    cache = MagicMock(spec=CacheService)
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock()
    return cache


def test_health_check():
    """Test the health check endpoint."""
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_year_availability_valid_year():
    """Test year availability for a valid F1 year."""
    with TestClient(app) as client:
        response = client.get("/years/2021/available")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2021
    assert data["has_data"] is True


def test_year_availability_invalid_year():
    """Test year availability for an invalid year."""
    with TestClient(app) as client:
        response = client.get("/years/1950/available")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 1950
    assert isinstance(data["has_data"], bool)


def test_get_race_names():
    """Test getting race names for a valid year."""
    app.dependency_overrides[get_cache] = get_mock_cache
    with TestClient(app) as client:
        response = client.get("/years/2021/races")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2021
    assert isinstance(data["races"], list)
    assert len(data["races"]) > 0
    assert "Bahrain Grand Prix" in data["races"]


def test_get_race_names_invalid_year():
    """Test getting race names for an invalid year."""
    app.dependency_overrides[get_cache] = get_mock_cache
    with TestClient(app) as client:
        response = client.get("/years/1900/races")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_race_schedule():
    """Test getting schedule for a specific race."""
    app.dependency_overrides[get_cache] = get_mock_cache
    with TestClient(app) as client:
        response = client.get("/years/2021/races/Bahrain%20Grand%20Prix/schedule")
    app.dependency_overrides.clear()
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
    app.dependency_overrides[get_cache] = get_mock_cache
    with TestClient(app) as client:
        response = client.get("/years/2021/races/Fake%20Grand%20Prix/schedule")
    app.dependency_overrides.clear()
    assert response.status_code == 404
