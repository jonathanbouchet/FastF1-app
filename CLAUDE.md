# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

### Setup
```bash
uv sync                                 # Install dependencies
```

### Run
```bash
redis-server                            # Start Redis (in another terminal)
uv run uvicorn src.app:app --reload    # Start development server (http://localhost:8000)
```

### Testing
```bash
uv run pytest                           # Run all tests
uv run pytest tests/test_endpoints.py   # Run specific test file
uv run pytest tests/test_endpoints.py::test_health_check  # Run specific test
```

## Project Overview

FastAPI backend for F1 data visualization using FastF1 as the data source. Includes Redis caching for FastF1 API calls. Uses FastAPI's lifespan for Redis connection management. The project follows PEP-8 style and uses Pydantic for validation.

**Stack:** FastAPI, Pydantic, FastF1, Redis, pytest

### Project Structure
```
src/
  app.py               # FastAPI application with all endpoints
  cache.py             # Redis caching service
  models/              # Pydantic models for validation
    __init__.py
    health.py          # HealthResponse model
    year.py            # YearAvailabilityResponse model
tests/
  test_endpoints.py    # Endpoint tests (one test per endpoint minimum)
```

### Key Dependencies
- `fastapi` — Web framework with lifespan support
- `pydantic` — Request/response validation
- `fastf1` — F1 data provider
- `redis` — Async caching layer
- `pytest`, `httpx2` — Testing (dev dependencies)

### Caching
Expensive FastF1 calls (schedule fetches, event details) are cached in Redis with a 24-hour TTL. Cache keys follow the pattern `f1:{year}:{resource}`. The cache is optional—requests work without Redis, falling back to direct FastF1 calls. Use FastAPI's lifespan feature (`@asynccontextmanager`) to manage Redis connection lifecycle.

## Development

### Adding New Endpoints
Use the `/add-endpoint` skill for guided workflow. Steps:
1. Create or update the Pydantic model in `src/models/`
2. Add endpoint to `src/app.py` (use `fastapi.status` constants for HTTP codes)
3. Add tests to `tests/test_endpoints.py` (minimum: one test per endpoint)
4. Update README.md API Endpoints section

### API Response Format
All endpoints return Pydantic models. FastAPI automatically converts these to JSON responses.

### Adding Dependencies
Edit `pyproject.toml`, add to `dependencies` or `dev` sections, then run `uv sync`.
