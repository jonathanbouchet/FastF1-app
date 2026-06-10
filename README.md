# F1 Data Visualization

A FastAPI backend + Streamlit frontend for Formula 1 data visualization powered by [FastF1](https://docs.fastf1.dev/).

## Features

### Backend
- RESTful API endpoints for F1 data
- Pydantic validation for all requests and responses
- FastF1 integration for seamless data access
- Redis caching layer for expensive FastF1 calls (24-hour TTL)
- FastAPI lifespan for automatic Redis connection management
- Comprehensive test coverage with pytest

### Frontend
- Streamlit multi-page UI
- Year-based race filtering with sidebar
- Race schedule display with UTC timestamps
- Dark/light mode following browser preferences
- Client-side caching for API responses

## Getting Started

### Prerequisites

- Python 3.13+
- uv (Python package manager)
- Redis (for caching layer)

### Installation

```bash
uv sync
```

This installs all dependencies and creates a virtual environment.

## Running

### Start Redis (required for caching)
```bash
redis-server
```

### Start the API backend (in a new terminal)
```bash
uv run uvicorn src.app:app --reload
```
API available at `http://localhost:8000`  
Interactive docs at `http://localhost:8000/docs`

### Start the Streamlit frontend (in another terminal)
```bash
uv run streamlit run streamlit_app.py
```
UI available at `http://localhost:8501`

**Note:** The API will gracefully handle Redis unavailability by bypassing the cache and fetching directly from FastF1. Streamlit will show connection errors if the API is not running.

## Testing

Run all tests:

```bash
uv run pytest
```

Run a specific test file:

```bash
uv run pytest tests/test_endpoints.py
```

Run a specific test:

```bash
uv run pytest tests/test_endpoints.py::test_health_check
```

## Backend API Endpoints

- `GET /health` — Health check endpoint
- `GET /years/{year}/available` — Check if a given year has F1 data available
- `GET /years/{year}/races` — Get all race names for a given year
- `GET /years/{year}/races/{race_name}/schedule` — Get event schedule for a race (sessions with dates)

## Frontend Pages

- **Race Names** — Browse all races for a selected year
- **Race Schedule** — View detailed session schedule for a selected race

## Caching

The API caches expensive FastF1 calls in Redis:
- Race schedules: `f1:{year}:schedule`
- Race schedules by name: `f1:{year}:{race_name}:schedule`
- Cache TTL: 24 hours

Cached endpoints automatically store and retrieve from Redis. Cache misses fall through to FastF1 without affecting response times.

## Project Structure

```
src/
  app.py             # FastAPI application with lifespan and endpoints
  cache.py           # Redis caching service
  models/            # Pydantic models for request/response validation
tests/
  test_endpoints.py  # Backend endpoint tests
streamlit_app.py     # Streamlit frontend application
```

## Best Practices

- Use `fastapi.status` constants for HTTP status codes instead of hardcoding them (e.g., `status.HTTP_404_NOT_FOUND` instead of `404`)
- Use FastAPI's lifespan feature for managing async resource lifecycles (connections, pools, etc.)
- When adding cached endpoints, inject `CacheService` via `Depends(get_cache)`
